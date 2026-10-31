#!/usr/bin/env python3
"""
ai_linter.py — deterministyczny linter manieryzmu AI (stage-1 pre-scan, 0 tokenów LLM).
Lustro taksonomii z manieryzm-ai.md — przy zmianie synchronizuj oba pliki (te same ID).

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
from typing import List, Tuple


# ---------------------------------------------------------------------------
# KATALOG MARKERÓW
# Lustro taksonomii z manieryzm-ai.md — przy zmianie synchronizuj oba pliki (te same ID).
# Krotki: (id, lang, klasa, pattern_str, opis)
# lang: 'pl' | 'en' | 'both'
# klasa: 'block' | 'review'
# ---------------------------------------------------------------------------

MARKER_DEFS: List[Tuple[str, str, str, str, str]] = [
    # --- WARSTWA PL ---

    # PL-SIGN — puste otwarcia / signposty
    ("PL-SIGN", "pl", "review",
     r"\bwarto (?:tu )?(?:podkreśl|zauważ|zaznacz|pamięta|dodać|wspomnieć|nadmienić|zwrócić uwagę)",
     "puste otwarcie: warto podkreślić/zauważyć"),
    ("PL-SIGN", "pl", "review",
     r"\bnależy (?:tu )?(?:zauważyć|podkreślić|pamiętać|zaznaczyć|dodać|wspomnieć)\b",
     "puste otwarcie: należy zauważyć/podkreślić"),
    ("PL-SIGN", "pl", "review",
     r"\bco (?:istotne|ważne|ciekawe|znamienne|warte odnotowania),",
     "signpost: co istotne/ważne"),
    ("PL-SIGN", "pl", "review",
     r"\bw dzisiejszych czasach\b",
     "klisza temporalna: w dzisiejszych czasach"),
    ("PL-SIGN", "pl", "review",
     r"\bw (?:dobie|obliczu|erze)\b",
     "klisza temporalna: w dobie/obliczu/erze"),
    ("PL-SIGN", "pl", "review",
     r"\bw dynamicznie (?:zmieniając|rozwijając)\w* się\b",
     "klisza: w dynamicznie zmieniającym się"),
    ("PL-SIGN", "pl", "review",
     r"\bnie sposób (?:przecenić|nie\b)",
     "klisza: nie sposób przecenić"),
    ("PL-SIGN", "pl", "review",
     r"\bjak (?:powszechnie )?wiadomo\b",
     "signpost: jak (powszechnie) wiadomo"),
    ("PL-SIGN", "pl", "review",
     r"\b(?:podsumowując|reasumując|konkludując|wnioskując|na zakończenie)\b",
     "signpost zamknięcia: podsumowując/reasumując"),
    ("PL-SIGN", "pl", "review",
     r"\b(?:zanurzmy|zagłębmy|przyjrzyjmy|zastanówmy|skupmy|pochylmy) się\b",
     "meta-zaproszenie: zanurzmy/zagłębmy się"),
    ("PL-SIGN", "pl", "review",
     r"\bprzyjrzyjmy się bliżej\b",
     "meta-zaproszenie: przyjrzyjmy się bliżej"),
    ("PL-SIGN", "pl", "review",
     r"\bmam nadzieję, że (?:ten|ta|to|powyższ|niniejsz)",
     "hedging zamknięcia: mam nadzieję, że ten/ta/to"),

    # PL-CLICHE — frazy-wytrychy
    ("PL-CLICHE", "pl", "review",
     r"\bodgrywa (?:kluczow|istotn|ważn|znacząc|niebagateln)\w* rolę\b",
     "klisza: odgrywa kluczową rolę"),
    ("PL-CLICHE", "pl", "review",
     r"\b(?:kluczow|istotn|ważn)\w* rolę odgrywa\b",
     "klisza: kluczową rolę odgrywa"),
    ("PL-CLICHE", "pl", "review",
     r"\bma (?:kluczowe|istotne|ogromne|zasadnicze) znaczenie\b",
     "klisza: ma kluczowe/istotne znaczenie"),
    ("PL-CLICHE", "pl", "review",
     r"\b(?:kluczowe|istotne|ogromne) znaczenie ma\b",
     "klisza: kluczowe znaczenie ma"),
    ("PL-CLICHE", "pl", "review",
     r"\bstanowi (?:integraln\w+ część|nieodłączn\w+ element|fundament|podstawę|trzon|filar)\b",
     "klisza: stanowi integralną część/fundament"),
    ("PL-CLICHE", "pl", "review",
     r"\b(?:rewolucyjn|przełomow|innowacyjn|nowoczesn|nowatorsk|niezrównan|bezprecedensow)\w+\b",
     "superlatyw: rewolucyjny/przełomowy/innowacyjny"),
    ("PL-CLICHE", "pl", "review",
     r"\bmożliwości (?:są )?(?:praktycznie |niemal |wręcz )?(?:nieograniczone|nieskończone)\b",
     "klisza: możliwości (są) nieograniczone"),
    ("PL-CLICHE", "pl", "review",
     r"\bzmienia reguły gry\b",
     "klisza: zmienia reguły gry"),
    ("PL-CLICHE", "pl", "review",
     r"\bto dopiero (?:początek|wierzchołek)\b",
     "klisza: to dopiero początek/wierzchołek"),
    ("PL-CLICHE", "pl", "review",
     r"\bw erze (?:cyfrow|sztucznej inteligencji|AI)\w*\b",
     "klisza: w erze cyfrowej/AI"),

    # PL-RHET — figury retoryczne
    ("PL-RHET", "pl", "block",
     r"[Tt]o nie (?:jest )?.{1,40}[—–\-] to\b",
     "antyteza redefinicyjna: To nie X — to Y"),
    ("PL-RHET", "pl", "block",
     r"[Tt]o nie (?:jest )?.{1,40}\.\s+[Tt]o\b",
     "antyteza redefinicyjna: To nie X. To Y"),
    ("PL-RHET", "pl", "review",
     r"\bnie tylko\b.{1,80}?\b(?:ale|lecz)(?: również| także| i)?\b",
     "paralelizm: nie tylko… ale również"),
    ("PL-RHET", "pl", "review",
     r"\bz jednej strony\b",
     "dychotomia: z jednej strony"),
    ("PL-RHET", "pl", "review",
     r"\b(\w+), (\w+),? (?:i|oraz) (\w+)\b",
     "triada?"),
    ("PL-RHET", "pl", "review",
     r"\bod \w+(?:y|ów|i)? (?:po|aż po) \w+",
     "rozpiętość: od X po Y"),

    # PL-NORMA — naruszenia normy częste w przekładzie z ang. (nie manieryzm AI).
    # Źródło: audyt przekładu tekstu publicystycznego (2026-10-31).
    ("PL-NORMA", "pl", "review",
     r"\bnajbardziej (?:elementarn|optymaln|unikaln|idealn|doskonał"
     r"|maksymaln|minimaln|absolutn)\w*",
     "stopniowanie przymiotnika absolutnego"),
    ("PL-NORMA", "pl", "review",
     r"\bsię \w+ się\b",
     "podwójne „się” w sąsiedztwie"),
    ("PL-NORMA", "pl", "review",
     r"\bna (?:jego|jej|ich|swoich|swych|naszych|własnych) (?:własnych )?warunkach\b",
     "kalka on its own terms: według własnych reguł?"),
    ("PL-NORMA", "pl", "review",
     r"\brozesz\w* się echem|\brozejść się echem",
     "frazeologizm: odbić się echem / rozbrzmieć"),
    ("PL-NORMA", "pl", "review",
     r"\b(?:minion|ostatni|poprzedni)\w* dekad",
     "fałszywy przyjaciel: dekada → dziesięciolecie"),

    # PL-ANTI — antyteza przeciwstawna NIEreferencyjna (bez myślnika, bez "to ... to")
    # generatorowe domknięcie retoryczne: "X, a nie Y" / inwersja "Y, nie X".
    # Każde z osobna bywa poprawne w swobodnej mowie → klasa review (high recall);
    # nagromadzenie ≥3 w pliku eskaluje do block (patrz "PL-ANTI seria" niżej).
    # Symetryczne do EN-ANTI. Bliźniak redefinicyjnej PL-RHET, której brakowało wariantu bez myślnika.
    ("PL-ANTI", "pl", "review",
     r",\s+a nie\b",
     "antyteza: X, a nie Y"),
    ("PL-ANTI", "pl", "review",
     r",\s+nie\s+\w+(?:\s+\w+)?(?=[.!?;\n]|$)",
     "antyteza inwersyjna: ..., nie Y (domknięcie)"),

    # PL-HEDGE — hedging / nadmierna grzeczność
    ("PL-HEDGE", "pl", "review",
     r"\b(?:mogłoby|mógłby|można by|dałoby się)\b.{0,30}\b(?:potencjalnie|ewentualnie|w pewnym sensie)\b",
     "podwójny hedge: mogłoby… potencjalnie"),
    ("PL-HEDGE", "pl", "review",
     r"\bpotencjalnie\b",
     "hedge: potencjalnie"),
    ("PL-HEDGE", "pl", "review",
     r"\bwydaje się, że\b",
     "hedge: wydaje się, że"),
    ("PL-HEDGE", "pl", "review",
     r"\bzdaje się, że\b",
     "hedge: zdaje się, że"),
    ("PL-HEDGE", "pl", "review",
     r"\bwarto byłoby rozważyć\b",
     "hedge: warto byłoby rozważyć"),
    ("PL-HEDGE", "pl", "review",
     r"\bw pewnym sensie\b",
     "hedge: w pewnym sensie"),

    # PL-TYPO — typografia / struktura AI
    # (nagłówki-klisze jako review; em-dash i emoji-w-nagłówku obsługiwane osobną logiką)
    # bold-overload liczony osobno per akapit (detect_bold_overload) — bez wpisu katalogowego,
    # by uniknąć fałszywych trafień na wierszach zaczynających się od **etykieta:**
    ("PL-TYPO", "pl", "review",
     r"(?m)^#{1,6}\s*(?:Kluczowe wnioski|Najważniejsze (?:punkty|wnioski|informacje)|Co dalej\??|Podsumowanie|Wnioski końcowe)\b",
     "nagłówek-klisza: Kluczowe wnioski / Podsumowanie"),

    # --- WARSTWA EN ---

    # EN-ANTI — antithesis
    ("EN-ANTI", "en", "review",
     r"\bnot (?:just|only|merely|simply)\b.{1,80}?\b(?:but|it'?s|it is)\b",
     "antythesis: not only/just… but"),
    ("EN-ANTI", "en", "review",
     r"\bit'?s not\b.{1,40}[—–\-]\s*it'?s\b",
     "antythesis: it's not X — it's Y"),
    ("EN-ANTI", "en", "review",
     r"\bnot \w+, but \w+\b",
     "antythesis: not X, but Y"),

    # EN-TRIAD — rule-of-three
    ("EN-TRIAD", "en", "review",
     r"\b(\w+), (\w+),? and (\w+)\b",
     "triad?"),

    # EN-PARA — balanced parallelism
    ("EN-PARA", "en", "review",
     r"\bself-\w+ and self-\w+\b",
     "parallelism: self-X and self-Y"),
    ("EN-PARA", "en", "review",
     r"\b(\w+)-(\w+) and (\w+)-(\w+)\b",
     "parallelism: X-Y and A-B"),

    # EN-CLICHE — signposty / klisze
    ("EN-CLICHE", "en", "review",
     r"\b(?:it'?s worth noting|worth noting that|in today'?s (?:fast-paced|ever-changing) world"
     r"|ever-evolving (?:landscape|world)|delve into|delv(?:e|ing)|tapestry|a testament to"
     r"|testament to|navigate the complexities|first-class|seamless(?:ly)?|robust"
     r"|leverag(?:e|ing)|spearhead(?:ed|ing)?|i am (?:confident|excited|thrilled|passionate)"
     r"(?: that| to| about)?|passionate about|at the end of the day|the through-line"
     r"|game-?changer|cutting-edge|best-in-class|state-of-the-art"
     r"|unlock(?:ing)?(?: the)? potential)\b",
     "EN klisza/signpost"),

    # EN-HEDGE
    ("EN-HEDGE", "en", "review",
     r"\b(?:arguably|it could be argued|to some extent|one could say|it may well be)\b",
     "hedge EN"),

    # EN-SUPER — puste superlatywy
    ("EN-SUPER", "en", "review",
     r"\b(?:incredibly|extremely|truly|remarkably|highly|exceptionally|undoubtedly|absolutely|deeply)\b",
     "superlatyw EN"),

    # EN-CONCL — signposty zamknięcia
    ("EN-CONCL", "en", "review",
     r"\b(?:in conclusion|overall|ultimately|all in all|in summary|to sum up|in essence|when all is said)\b",
     "signpost zamknięcia EN"),
]


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


# ---------------------------------------------------------------------------
# WARSTWA KONSTRUKCYJNA — PL-STRUKT
# Katalog markerów wyżej to czarna lista fraz: łapie slowa, nie budowę zdania.
# Ta warstwa mierzy konstrukcję i jest liczona OSOBNO (własna metryka strukt/100w),
# bo skala naruszeń budowy jest inna niż skala trafień frazowych.
# Podstawa: ASD-STE100 + /rules/ai-tells.md (system pisania bije czarną listę).
# ---------------------------------------------------------------------------

MAX_ZDANIE_SLOW = 25      # STE: 20 dla instrukcji, 25 dla opisu; polski dłuższy fleksyjnie
MAX_ZDAN_AKAPIT = 6
PROG_STRUKT_100W = 4.0    # ponytail: kalibrowane na tests/, nie z teorii — przestrój, gdy szumi

_CODE_RE = re.compile(r"```.*?```", re.S)
_INLINE_CODE_RE = re.compile(r"`[^`]*`")
_SKROT_RE = re.compile(r"\b(?:np|itd|itp|tj|tzw|m\.in|ok|ul|r|w|nr|str|proc|dr|prof|godz)\.", re.I | re.U)

# Strona bierna analityczna: "zostać" + imiesłów bierny. Wysoka precyzja — po formie
# "został" praktycznie zawsze stoi imiesłów. Świadomie NIE łapiemy "jest + -ny",
# bo tam mieszają się orzeczniki przymiotnikowe ("jest ważny") i powstaje szum.
BIERNA_RE = re.compile(r"\bzosta\w{1,4}\s+(?:\w+\s+)?\w{4,}(?:ny|na|ne|ni|ty|ta|te|ci)\b", re.I | re.U)

# Nominalizacja: czasownik lekki + rzeczownik odsłowny zamiast jednego czasownika.
NOMINALIZACJA_RE = re.compile(
    r"\b(?:dokona\w*|dokonyw\w*|przeprowadz\w*|realizuj\w*|realizowa\w*|ulega\w*|podlega\w*|następuje|następują)"
    r"\s+(?:\w+\s+)?(?:\w{4,}(?:nia|nie|niu|cji|cja|cję|ości|anie|ania|eniu)"
    r"|analiz\w*|ocen[aęy]\w*|weryfikacj\w*|przegląd\w*|korekt\w*|pomiar\w*|wybor\w*)\b",
    re.I | re.U,
)
W_CELU_RE = re.compile(r"\bw celu\s+(?:\w+\s+)?\w{4,}(?:nia|enia|ania|cji)\b", re.I | re.U)

# Imiesłowy przysłówkowe: pojedynczy jest poprawny, nagromadzenie w jednym zdaniu
# to typowy generatorowy zawijas.
IMIESLOW_RE = re.compile(r"\b\w{4,}(?:ąc|ąwszy|wszy)\b", re.U)


def _strip_code(text: str) -> str:
    """Usuwa bloki i wstawki kodu — składnia nie podlega ocenie stylu."""
    return _INLINE_CODE_RE.sub(" ", _CODE_RE.sub(" ", text))


def _split_sentences_pl(text: str) -> List[str]:
    """Dzieli prozę na zdania, chroniąc skróty typu 'np.', 'm.in.', 'r.'."""
    masked = _SKROT_RE.sub(lambda m: m.group(0).replace(".", "\x00"), text)
    out = []
    for part in re.split(r"(?<=[.!?…])\s+", masked):
        s = part.replace("\x00", ".").strip()
        if s:
            out.append(s)
    return out


def _slowa(s: str) -> int:
    return len(re.findall(r"\w+", s, re.U))


def scan_structure(text: str) -> Tuple[List[Tuple[int, str, str]], int]:
    """
    Warstwa konstrukcyjna. Zwraca (lista (line, kategoria, fragment), liczba_słów_prozy).
    Liczona na samej prozie: bez kodu, tabel, list, nagłówków i cytatów.
    """
    text = _strip_code(text)
    hits: List[Tuple[int, str, str]] = []
    slowa_prozy = 0

    for offset, para in split_paragraphs(text):
        proza = _prose_only(para)
        if not proza.strip():
            continue
        zdania = _split_sentences_pl(proza)
        slowa_prozy += sum(_slowa(z) for z in zdania)
        linia_akapitu = get_line_number(text, offset)

        if len(zdania) > MAX_ZDAN_AKAPIT:
            hits.append((linia_akapitu, "akapit>6zd",
                         truncate_fragment(f"akapit ×{len(zdania)} zdań: {proza[:40]}")))

        for z in zdania:
            n = _slowa(z)
            linia = get_line_number(text, offset + proza.find(z)) if proza.find(z) >= 0 else linia_akapitu
            if n > MAX_ZDANIE_SLOW:
                hits.append((linia, f"zdanie>{MAX_ZDANIE_SLOW}w",
                             truncate_fragment(f"{n} słów: {z}")))
            for m in BIERNA_RE.finditer(z):
                hits.append((linia, "strona_bierna", truncate_fragment(m.group(0))))
            for rx in (NOMINALIZACJA_RE, W_CELU_RE):
                for m in rx.finditer(z):
                    hits.append((linia, "nominalizacja", truncate_fragment(m.group(0))))
            imieslowy = IMIESLOW_RE.findall(z)
            if len(imieslowy) >= 2:
                hits.append((linia, "imieslow_seria",
                             truncate_fragment(f"×{len(imieslowy)}: {', '.join(imieslowy[:3])}")))

    return hits, slowa_prozy


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
    strukt: int = 0
    strukt_per100w: float = 0.0


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

    # --- Specjalna logika em-dash (block po progu ≥3) ---
    # Dla EN: EN-DASH, dla PL/both: PL-TYPO
    eff_lang = lang_filter if lang_filter != "both" else "pl"  # domyślnie PL dla both
    # Sprawdź rozszerzenie lub treść — jeśli plik nie ma słów PL, traktuj jako EN
    # Uproszczenie: opieramy się na lang_filter
    for (dl, dmid, dfrag) in detect_emdash_overuse(text, eff_lang):
        hits.append(Hit(filepath, dl, dmid, "block", dfrag))
        blockers += 1

    # --- Emoji w nagłówkach (block) ---
    for (el, efrag) in detect_emoji_in_headings(text):
        hits.append(Hit(filepath, el, "PL-TYPO", "block", efrag))
        blockers += 1

    # --- Bold-overload (review, nie bloker) ---
    for (bl, bmid, bfrag) in detect_bold_overload(text, eff_lang):
        hits.append(Hit(filepath, bl, bmid, "review", bfrag))
        # review — nie dodaje do blockers

    # --- SVO rhythm (review) ---
    for (sl, sfrag) in detect_svo_rhythm(text):
        hits.append(Hit(filepath, sl, "PL-RHYTHM", "review", sfrag))

    # --- Nawał łączników-otwarć (block jeśli ≥3) ---
    connector_hits = detect_connector_overload(text)
    for (cl, cfrag) in connector_hits:
        hits.append(Hit(filepath, cl, "PL-RHYTHM", "block", cfrag))
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

    # --- Gęstość (tylko warstwa frazowa) ---
    total_hits = len(hits)
    density = total_hits / max(1, words / 500)

    # --- Warstwa konstrukcyjna: własny licznik, poza `density` ---
    struct_hits, slowa_prozy = scan_structure(text)
    for (sl, kat, sfrag) in struct_hits:
        hits.append(Hit(filepath, sl, "PL-STRUKT", "strukt", f"{kat}: {sfrag}"))
    strukt_per100w = len(struct_hits) * 100.0 / max(1, slowa_prozy)

    # --- Werdykt ---
    cyrillic_found = any(h.mid == "PL-SIGN" and "CYRYLICA" in h.match_fragment for h in hits)
    if cyrillic_found:
        verdict = "FAIL-HARD"
    elif blockers > 0 or density > 8 or strukt_per100w > PROG_STRUKT_100W:
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
        strukt=len(struct_hits),
        strukt_per100w=round(strukt_per100w, 2),
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
    lines.append("plik | słowa | trafienia | em-dash/akapit(max) | gęstość/500 | strukt/100w | blokery | WERDYKT")
    for s in summaries:
        lines.append(
            f"{s.file} | {s.words} | {s.hits} | {s.emdash_max} | {s.density} | "
            f"{s.strukt_per100w} | {s.blockers} | {s.verdict}"
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
                "strukt": s.strukt,
                "strukt_per100w": s.strukt_per100w,
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
