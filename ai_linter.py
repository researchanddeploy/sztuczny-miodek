#!/usr/bin/env python3
"""
ai_linter.py — deterministyczny linter manieryzmu AI (stage-1 pre-scan, 0 tokenów LLM).
Katalog markerów ładowany z pliku danych rules.json (Epik A: „Reguła jako dane"; schemat: rules.schema.md).
Lustro taksonomii z manieryzm-ai.md — przy zmianie synchronizuj rules.json i dokument (te same ID).

Dwa rozłączne rodzaje reguł (czysty rozdział, A5):
  - DEKLARATYWNE — czyste regexy z rules.json (→ MARKER_DEFS → compile_markers, jedna pętla finditer).
  - PROCEDURALNE — progi/logika niewyrażalne regexem; funkcje detect_* wołane PO IDENTYFIKATORZE
    przez DETECTOR_REGISTRY / run_procedural_detector. ID proceduralne: PL-RHYTHM, PL-TYPO, EN-DASH.
    Z założenia NIE wchodzą do rules.json (regex = dane, detektor = kod z progiem).
    Kontrakt: patrz DETECTOR_REGISTRY niżej oraz sekcja „Detektory proceduralne (kontrakt)" w manieryzm-ai.md.

Użycie:
    python3 ai_linter.py [--lang {pl,en,both}] [--format {manifest,json}] ścieżka [...]
"""

import re
import sys
import os
import json
import argparse
import glob
from dataclasses import dataclass
from typing import Callable, List, Tuple


# ---------------------------------------------------------------------------
# KATALOG MARKERÓW — ładowany z pliku danych rules.json (Epik A: „Reguła jako dane").
#
# Reguły mieszkają w rules.json (jedno źródło prawdy, parsowalne stdlib — modułem json,
# ZERO zależności z pip). Linter wczytuje je przy starcie do MARKER_DEFS w identycznym
# formacie jak dawniej zaszyty literał: lista 5-krotek (id, lang, klasa, pattern_str, opis).
# Dzięki temu reszta kodu (compile_markers, scan_file) oraz narzędzie tools/gen_rules_json.py
# działają bez zmian, a zachowanie lintera pozostaje identyczne.
#
# Schemat pliku: rules.schema.md. Kolejność wpisów i duplikaty ID mają znaczenie i są
# zachowywane 1:1. Pola opcjonalne (prog, przyklady, doc) są w tej warstwie ignorowane —
# A2 nie zmienia detekcji.
#
# Lustro taksonomii z manieryzm-ai.md — przy zmianie synchronizuj rules.json i dokument.
# lang: 'pl' | 'en' | 'both'; klasa: 'block' | 'review'.
# ---------------------------------------------------------------------------

# Ścieżka do pliku reguł — względem lokalizacji ai_linter.py (a NIE bieżącego katalogu),
# żeby linter działał wywoływany z dowolnego miejsca (tak robią testy: python3 .../ai_linter.py).
RULES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules.json")


def load_marker_defs(path: str = RULES_PATH) -> List[Tuple[str, str, str, str, str]]:
    """Wczytuje katalog markerów z rules.json do listy 5-krotek (id, lang, klasa, pattern, opis).

    Zachowuje kolejność wpisów i duplikaty ID 1:1. Pola opcjonalne (prog/przyklady/doc) są
    pomijane — ta warstwa odwzorowuje wyłącznie dawny literał MARKER_DEFS.

    Kończy z czytelnym błędem (exit 2) gdy: brak pliku, niepoprawny JSON, korzeń JSON nie
    jest listą reguł, lub wpis nie ma wymaganego pola (linter bez poprawnych reguł nie ma sensu).
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Brak pliku reguł: {path}", file=sys.stderr)
        sys.exit(2)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[ERROR] Nie można wczytać reguł z {path}: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(raw, list):
        print(f"[ERROR] rules.json: oczekiwano tablicy reguł, otrzymano {type(raw).__name__}",
              file=sys.stderr)
        sys.exit(2)

    defs: List[Tuple[str, str, str, str, str]] = []
    for i, r in enumerate(raw):
        try:
            defs.append((r["id"], r["lang"], r["klasa"], r["pattern"], r["opis"]))
        except KeyError as e:
            # e.args[0] = nazwa brakującego klucza (bez apostrofów surowego str(KeyError))
            print(f"[ERROR] rules.json: wpis #{i} — brakujące wymagane pole: {e.args[0]}",
                  file=sys.stderr)
            sys.exit(2)
        except TypeError:
            # wpis nie jest obiektem (np. liczba / string zamiast słownika reguły)
            print(f"[ERROR] rules.json: wpis #{i} nie jest obiektem reguły (otrzymano "
                  f"{type(r).__name__})", file=sys.stderr)
            sys.exit(2)
    return defs


MARKER_DEFS: List[Tuple[str, str, str, str, str]] = load_marker_defs()


# ---------------------------------------------------------------------------
# EMOJI: zakresy ze specyfikacji
# ---------------------------------------------------------------------------
EMOJI_RANGES = [
    (0x1F000, 0x1FAFF),
    (0x2600,  0x27BF),
    (0x2190,  0x21FF),
    (0x2B00,  0x2BFF),
    (0xFE0F,  0xFE0F),
]

# Regex cyrylicy
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]", re.UNICODE)

# Regex em-dash i spacjowanego en-dash
DASH_RE = re.compile(r"—| – ")

# Nagłówek Markdown
HEADING_RE = re.compile(r"^#{1,6}\s", re.MULTILINE)

# Nawał łączników na początku zdań
CONNECTOR_RE = re.compile(
    r"(?:^|(?<=[.!?])\s+)(?:Ponadto|Co więcej|Dodatkowo|Jednocześnie|Następnie|Warto dodać|Mało tego)\b",
    re.IGNORECASE | re.UNICODE | re.MULTILINE
)

# Bold
BOLD_RE = re.compile(r"\*\*[^*]+\*\*")


def has_emoji(s: str) -> bool:
    """Zwraca True jeśli napis zawiera emoji z zakresów ze specyfikacji."""
    for ch in s:
        cp = ord(ch)
        for lo, hi in EMOJI_RANGES:
            if lo <= cp <= hi:
                return True
    return False


def compile_markers(lang_filter: str):
    """Kompiluje katalog markerów do listy (id, lang, klasa, compiled_re, opis)."""
    compiled = []
    flags = re.IGNORECASE | re.UNICODE
    for mid, mlang, mclass, pattern, desc in MARKER_DEFS:
        if lang_filter == "both" or mlang == lang_filter or mlang == "both":
            try:
                compiled.append((mid, mlang, mclass, re.compile(pattern, flags), desc))
            except re.error as e:
                print(f"[WARN] Błąd kompilacji regexa {mid}: {e}", file=sys.stderr)
    return compiled


@dataclass
class Hit:
    file: str
    line: int
    mid: str
    klasa: str
    match_fragment: str


@dataclass
class FileSummary:
    file: str
    words: int
    hits: int
    emdash_max: int
    density: float
    blockers: int
    verdict: str


def truncate_fragment(s: str, maxlen: int = 60) -> str:
    """Przytnij fragment do maxlen znaków, usuń znaki nowej linii."""
    s = s.replace("\n", " ").replace("\r", " ").strip()
    if len(s) > maxlen:
        s = s[:maxlen - 1] + "…"
    return s


def get_line_number(text: str, pos: int) -> int:
    """Zwraca numer linii (1-based) dla pozycji w tekście."""
    return text.count("\n", 0, pos) + 1


def split_paragraphs(text: str) -> List[Tuple[int, str]]:
    """Zwraca listę (offset_start, paragraph_text)."""
    paras = re.split(r"\n\s*\n", text)
    result = []
    offset = 0
    for p in paras:
        result.append((offset, p))
        offset += len(p) + 2  # przybliżony offset (dwie nowe linie)
    return result


def detect_svo_rhythm(text: str) -> List[Tuple[int, str]]:
    """
    Wykrywa powtarzalny SVO: 3 kolejne zdania zaczynające się tym samym tokenem
    (min 3 znaki, case-insensitive).
    Zwraca listę (line_number, fragment).
    """
    sentences = re.split(r"[.!?]+", text)
    hits = []
    # Zbierz pierwsze tokeny zdań z ich pozycjami
    tokens = []
    pos = 0
    for sent in sentences:
        stripped = sent.strip()
        if stripped:
            words = re.findall(r"\w+", stripped)
            if words and len(words[0]) >= 3:
                tokens.append((words[0].lower(), pos, stripped[:60]))
        pos += len(sent) + 1  # +1 za separator

    # Szukaj 3 z rzędu z tym samym tokenem
    i = 0
    while i < len(tokens) - 2:
        t0, p0, s0 = tokens[i]
        t1, p1, s1 = tokens[i + 1]
        t2, p2, s2 = tokens[i + 2]
        if t0 == t1 == t2:
            line = get_line_number(text, p0)
            fragment = f"{t0}×3: {s0[:40]}"
            hits.append((line, fragment))
            i += 3  # przesuń za wykryty blok
        else:
            i += 1
    return hits


def detect_connector_overload(text: str) -> List[Tuple[int, str]]:
    """
    Nawał łączników-otwarć: ≥3 w pliku → block (PL-RHYTHM).
    Zwraca listę (line, fragment) wszystkich trafień jeśli łącznie ≥3.
    """
    matches = list(CONNECTOR_RE.finditer(text))
    if len(matches) >= 3:
        result = []
        for m in matches:
            line = get_line_number(text, m.start())
            result.append((line, truncate_fragment(m.group(0))))
        return result
    return []


_NON_PROSE_RE = re.compile(r"^\s*(?:#{1,6}\s|[-*+]\s|\d+\.\s|>|\[[ x]\])")


def _prose_only(para: str) -> str:
    """Zostawia tylko wiersze prozy. Wyklucza tabele (`|`), listy (`-`/`*`/`1.`),
    nagłówki (`#`), cytaty (`>`) i checklisty. Bold i myślnik w tych strukturach to
    formatowanie, nie manieryzm prozy — a myślnik-etykieta w nagłówku jest dozwolony."""
    return "\n".join(
        ln for ln in para.split("\n")
        if "|" not in ln and not _NON_PROSE_RE.match(ln)
    )


def detect_emdash_overuse(text: str, lang: str) -> List[Tuple[int, str, str]]:
    """
    Em-dash overuse: akapit z ≥3 myślnikami → BLOCK.
    Zwraca listę (line, mid, fragment) gdzie mid = EN-DASH lub PL-TYPO.
    """
    mid = "EN-DASH" if lang == "en" else "PL-TYPO"
    hits = []
    paras = split_paragraphs(text)
    for offset, para in paras:
        dashes = DASH_RE.findall(_prose_only(para))
        if len(dashes) >= 3:
            line = get_line_number(text, offset)
            fragment = truncate_fragment(f"em-dash ×{len(dashes)}: {para[:40]}")
            hits.append((line, mid, fragment))
    return hits


def detect_emoji_in_headings(text: str) -> List[Tuple[int, str]]:
    """
    Emoji w nagłówku Markdown → BLOCK (PL-TYPO).
    Zwraca listę (line, fragment).
    """
    hits = []
    for m in HEADING_RE.finditer(text):
        # Pobierz całą linię nagłówka
        line_start = m.start()
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        heading_text = text[line_start:line_end]
        if has_emoji(heading_text):
            line = get_line_number(text, line_start)
            hits.append((line, truncate_fragment(heading_text)))
    return hits


def detect_bold_overload(text: str, lang: str) -> List[Tuple[int, str, str]]:
    """
    Bold-overload: ≥4 boldów w akapicie → review (PL-TYPO).
    """
    mid = "PL-TYPO"
    hits = []
    paras = split_paragraphs(text)
    for offset, para in paras:
        bolds = BOLD_RE.findall(_prose_only(para))
        if len(bolds) >= 4:
            line = get_line_number(text, offset)
            fragment = truncate_fragment(f"bold ×{len(bolds)}: {para[:40]}")
            hits.append((line, mid, fragment))
    return hits


# ---------------------------------------------------------------------------
# REJESTR DETEKTORÓW PROCEDURALNYCH (Epik A: „Reguła jako dane", A5)
#
# Czysty rozdział dwóch rodzajów reguł:
#   1. Reguły DEKLARATYWNE — czyste wzorce regex, mieszkają w rules.json, ładowane do
#      MARKER_DEFS i kompilowane przez compile_markers(). Wykrywane jedną pętlą po `finditer`.
#   2. Reguły PROCEDURALNE — wymagają progów i logiki niewyrażalnej regexem (liczenie myślników
#      na akapit, monotoniczny szyk SVO, nawał łączników, emoji w nagłówku, bold-overload).
#      Pozostają funkcjami `detect_*` w kodzie i są wołane PO IDENTYFIKATORZE przez ten rejestr.
#
# KONTRAKT ADAPTERA PROCEDURALNEGO:
#   adapter(text: str, eff_lang: str) -> List[Tuple[int, str, str, str]]
#   Zwraca listę krotek (line, mid, klasa, fragment):
#     - line     : numer linii 1-based (int),
#     - mid       : identyfikator markera ('PL-TYPO' | 'EN-DASH' | 'PL-RHYTHM' | ...),
#     - klasa    : 'block' | 'review'  (block → liczy się do blockers i może dać werdykt FAIL),
#     - fragment : krótki opis trafienia (str).
#   Adapter jest cienkim wrapperem nad funkcją detect_* (progi/logika żyją w detect_*, nie tutaj).
#
# DETECTOR_REGISTRY: lista (detector_id, adapter) w KOLEJNOŚCI wykonania. Kolejność ma znaczenie —
# wyznacza porządek dodawania trafień do listy hits (przed końcowym sortowaniem po linii), więc
# zmiana kolejności mogłaby zmienić wyjście przy remisie linii. NIE zmieniaj bez powodu.
# Wołanie „po identyfikatorze": detektor wybierany jest przez swój detector_id w rejestrze,
# a nie przez rozsiane po scan_file magic-stringi.
# ---------------------------------------------------------------------------

def _proc_emdash(text: str, eff_lang: str) -> List[Tuple[int, str, str, str]]:
    """Em-dash overuse (≥3/akapit → block). mid zależny od języka: PL-TYPO / EN-DASH."""
    return [(line, mid, "block", frag) for (line, mid, frag) in detect_emdash_overuse(text, eff_lang)]


def _proc_emoji_heading(text: str, eff_lang: str) -> List[Tuple[int, str, str, str]]:
    """Emoji w nagłówku Markdown → block (PL-TYPO)."""
    return [(line, "PL-TYPO", "block", frag) for (line, frag) in detect_emoji_in_headings(text)]


def _proc_bold(text: str, eff_lang: str) -> List[Tuple[int, str, str, str]]:
    """Bold-overload (≥4/akapit → review, PL-TYPO)."""
    return [(line, mid, "review", frag) for (line, mid, frag) in detect_bold_overload(text, eff_lang)]


def _proc_svo(text: str, eff_lang: str) -> List[Tuple[int, str, str, str]]:
    """Monotoniczny szyk SVO (3 zdania z tym samym tokenem → review, PL-RHYTHM)."""
    return [(line, "PL-RHYTHM", "review", frag) for (line, frag) in detect_svo_rhythm(text)]


def _proc_connector(text: str, eff_lang: str) -> List[Tuple[int, str, str, str]]:
    """Nawał łączników-otwarć (≥3 w pliku → block, PL-RHYTHM)."""
    return [(line, "PL-RHYTHM", "block", frag) for (line, frag) in detect_connector_overload(text)]


# Kolejność jak w historycznym scan_file: emdash → emoji → bold → svo → connector.
DETECTOR_REGISTRY: List[Tuple[str, Callable[[str, str], List[Tuple[int, str, str, str]]]]] = [
    ("emdash-overuse", _proc_emdash),
    ("emoji-in-heading", _proc_emoji_heading),
    ("bold-overload", _proc_bold),
    ("svo-rhythm", _proc_svo),
    ("connector-overload", _proc_connector),
]

# Zbiór ID markerów emitowanych przez detektory PROCEDURALNE (nie z rules.json).
# Jawnie deklarowany, by test spójności (A4) nie musiał odpalać detektorów na próbkach.
# PL-TYPO występuje też wśród deklaratywnych (em-dash/emoji/bold to PL-TYPO); PL-RHYTHM i
# EN-DASH są wyłącznie proceduralne. Pełny katalog ID = deklaratywne ∪ PROCEDURAL_MARKER_IDS.
PROCEDURAL_MARKER_IDS = frozenset({"PL-TYPO", "EN-DASH", "PL-RHYTHM"})


def run_procedural_detector(detector_id: str, text: str, eff_lang: str) -> List[Tuple[int, str, str, str]]:
    """Uruchamia pojedynczy detektor proceduralny PO IDENTYFIKATORZE (detector_id z rejestru).

    Zwraca listę krotek (line, mid, klasa, fragment) zgodnie z kontraktem adaptera.
    Nieznany detector_id → KeyError (świadoma, głośna awaria — literówka w id nie ma się prześliznąć).
    """
    for did, adapter in DETECTOR_REGISTRY:
        if did == detector_id:
            return adapter(text, eff_lang)
    raise KeyError(f"Nieznany detektor proceduralny: {detector_id!r}")


def scan_file(filepath: str, compiled_markers, lang_filter: str) -> Tuple[List[Hit], FileSummary]:
    """Skanuje jeden plik. Zwraca (hits, summary)."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as e:
        print(f"[ERROR] Nie można otworzyć {filepath}: {e}", file=sys.stderr)
        return [], FileSummary(filepath, 0, 0, 0, 0.0, 0, "ERROR")

    hits: List[Hit] = []
    blockers = 0

    # --- Wykrycie cyrylicy → FAIL-HARD ---
    cyrillic_match = CYRILLIC_RE.search(text)
    if cyrillic_match:
        line = get_line_number(text, cyrillic_match.start())
        hits.append(Hit(filepath, line, "PL-SIGN", "block",
                        f"CYRYLICA: {truncate_fragment(cyrillic_match.group(0))}"))
        blockers += 1

    # --- Metryki ---
    words = len(re.findall(r"\w+", text))

    # Em-dash max na akapit (do metryki summary)
    paras = split_paragraphs(text)
    emdash_max = 0
    for _, para in paras:
        cnt = len(DASH_RE.findall(para))
        if cnt > emdash_max:
            emdash_max = cnt

    # --- Detektory PROCEDURALNE (wołane po identyfikatorze z DETECTOR_REGISTRY) ---
    # Em-dash: dla EN → ID EN-DASH; dla PL/both → ID PL-TYPO. Próg/logika żyją w funkcjach detect_*;
    # tutaj tylko iterujemy rejestr w ustalonej kolejności i mapujemy klasę → blockers.
    eff_lang = lang_filter if lang_filter != "both" else "pl"  # domyślnie PL dla both
    for detector_id, _adapter in DETECTOR_REGISTRY:
        for (pline, pmid, pklasa, pfrag) in run_procedural_detector(detector_id, text, eff_lang):
            hits.append(Hit(filepath, pline, pmid, pklasa, pfrag))
            if pklasa == "block":
                blockers += 1

    # --- Antyteza redefinicyjna PL (block przy współwystąpieniu z innym markerem w akapicie) ---
    # Zbierz trafienia antytezy redefinicyjnej
    redef_patterns = [m for m in compiled_markers if m[0] == "PL-RHET" and m[2] == "block"]

    # --- Główna pętla regex po liniach ---
    # Dla PL-RHET block: tymczasowo jako review, potem sprawdzimy współwystąpienie
    for mid, mlang, mclass, cre, desc in compiled_markers:
        # Pomiń markery block PL-RHET (obsługiwane osobno)
        if mid == "PL-RHET" and mclass == "block":
            continue
        for m in cre.finditer(text):
            line = get_line_number(text, m.start())
            fragment = truncate_fragment(m.group(0))
            # Dla PL-RHET review i reszty — normalne trafienie
            hits.append(Hit(filepath, line, mid, mclass, fragment))
            if mclass == "block":
                blockers += 1

    # Antyteza redefinicyjna PL: sprawdź współwystąpienie z innymi markerami w tym samym akapicie
    if redef_patterns:
        for pi, (offset, para) in enumerate(paras):
            # Czy jest antyteza redefinicyjna w akapicie?
            redef_found = []
            for mid, mlang, mclass, cre, desc in redef_patterns:
                for m in cre.finditer(para):
                    line = get_line_number(text, offset + m.start())
                    fragment = truncate_fragment(m.group(0))
                    redef_found.append((line, mid, mclass, fragment))

            if redef_found:
                # Sprawdź czy w tym samym akapicie jest jakikolwiek inny marker
                other_in_para = 0
                for mid2, mlang2, mclass2, cre2, desc2 in compiled_markers:
                    if mid2 == "PL-RHET" and mclass2 == "block":
                        continue
                    if cre2.search(para):
                        other_in_para += 1

                klasa_redef = "block" if other_in_para >= 1 else "review"
                for (line, mid, _, fragment) in redef_found:
                    hits.append(Hit(filepath, line, mid, klasa_redef, fragment))
                    if klasa_redef == "block":
                        blockers += 1

    # --- EN-ANTI seria: block jeśli ≥2 trafień antytezy EN w pliku ---
    en_anti_count = sum(1 for h in hits if h.mid == "EN-ANTI")
    if en_anti_count >= 2:
        for h in hits:
            if h.mid == "EN-ANTI" and h.klasa == "review":
                h.klasa = "block"
                blockers += 1

    # --- PL-ANTI seria: block jeśli ≥3 trafień w pliku (rozproszona maniera antytezy) ---
    # Próg 3 (nie 2 jak EN), bo ", nie"/"a nie" częstsze naturalnie w polszczyźnie.
    # Łapie przypadek, gdy pojedyncze antytezy są OK, ale ich nawał po akapitach brzmi generatorowo.
    pl_anti_count = sum(1 for h in hits if h.mid == "PL-ANTI")
    if pl_anti_count >= 3:
        for h in hits:
            if h.mid == "PL-ANTI" and h.klasa == "review":
                h.klasa = "block"
                blockers += 1

    # --- Gęstość ---
    total_hits = len(hits)
    density = total_hits / max(1, words / 500)

    # --- Werdykt ---
    cyrillic_found = any(h.mid == "PL-SIGN" and "CYRYLICA" in h.match_fragment for h in hits)
    if cyrillic_found:
        verdict = "FAIL-HARD"
    elif blockers > 0 or density > 8:
        verdict = "FAIL"
    else:
        verdict = "PASS"

    summary = FileSummary(
        file=filepath,
        words=words,
        hits=total_hits,
        emdash_max=emdash_max,
        density=round(density, 2),
        blockers=blockers,
        verdict=verdict,
    )

    # Posortuj trafienia po linii
    hits.sort(key=lambda h: h.line)
    return hits, summary


def collect_files(paths: List[str]) -> List[str]:
    """Zbiera pliki .md i .txt z podanych ścieżek, obsługuje glob i katalogi."""
    result = []
    for p in paths:
        # Glob
        expanded = glob.glob(p, recursive=True)
        if expanded:
            for ep in expanded:
                if os.path.isdir(ep):
                    for root, _, files in os.walk(ep):
                        for fn in files:
                            if fn.endswith((".md", ".txt")):
                                result.append(os.path.join(root, fn))
                elif os.path.isfile(ep):
                    result.append(ep)
        elif os.path.isdir(p):
            for root, _, files in os.walk(p):
                for fn in files:
                    if fn.endswith((".md", ".txt")):
                        result.append(os.path.join(root, fn))
        elif os.path.isfile(p):
            result.append(p)
        else:
            print(f"[WARN] Nie znaleziono: {p}", file=sys.stderr)
    # Deduplikacja z zachowaniem kolejności
    seen = set()
    unique = []
    for f in result:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def format_manifest(all_hits: List[Hit], summaries: List[FileSummary]) -> str:
    """Formatuje wyjście manifest."""
    lines = []
    for h in all_hits:
        lines.append(f"{h.file}:{h.line}:{h.mid}:{h.klasa}:{h.match_fragment}")

    lines.append("")
    lines.append("== SUMMARY ==")
    lines.append("plik | słowa | trafienia | em-dash/akapit(max) | gęstość/500 | blokery | WERDYKT")
    for s in summaries:
        lines.append(
            f"{s.file} | {s.words} | {s.hits} | {s.emdash_max} | {s.density} | {s.blockers} | {s.verdict}"
        )
    return "\n".join(lines)


def format_json(all_hits: List[Hit], summaries: List[FileSummary]) -> str:
    """Formatuje wyjście JSON."""
    output = {
        "hits": [
            {"file": h.file, "line": h.line, "id": h.mid, "klasa": h.klasa, "match": h.match_fragment}
            for h in all_hits
        ],
        "summary": [
            {
                "file": s.file,
                "words": s.words,
                "hits": s.hits,
                "emdash_max": s.emdash_max,
                "density": s.density,
                "blockers": s.blockers,
                "verdict": s.verdict,
            }
            for s in summaries
        ],
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="ai_linter.py — deterministyczny linter manieryzmu AI (0 tokenów LLM).",
        epilog="Kod wyjścia: 1 jeśli którykolwiek plik = FAIL/FAIL-HARD, 0 jeśli wszystkie PASS.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        metavar="ścieżka",
        help="Plik(i), wzorzec glob lub katalog (rekursywnie *.md i *.txt).",
    )
    parser.add_argument(
        "--lang",
        choices=["pl", "en", "both"],
        default="both",
        help="Filtruj katalog markerów wg języka (domyślnie: both).",
    )
    parser.add_argument(
        "--format",
        choices=["manifest", "json"],
        default="manifest",
        help="Format wyjścia (domyślnie: manifest).",
    )
    args = parser.parse_args()

    files = collect_files(args.paths)
    if not files:
        print("[ERROR] Brak plików do analizy.", file=sys.stderr)
        sys.exit(1)

    compiled = compile_markers(args.lang)

    all_hits: List[Hit] = []
    summaries: List[FileSummary] = []

    for filepath in files:
        hits, summary = scan_file(filepath, compiled, args.lang)
        all_hits.extend(hits)
        summaries.append(summary)

    if args.format == "json":
        print(format_json(all_hits, summaries))
    else:
        print(format_manifest(all_hits, summaries))

    # Kod wyjścia: 1 jeśli którykolwiek plik = FAIL/FAIL-HARD
    if any(s.verdict in ("FAIL", "FAIL-HARD") for s in summaries):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
