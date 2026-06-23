#!/usr/bin/env python3
"""
check_id_consistency.py — test spójności identyfikatorów markerów (Epik A, A4 / KAN-183).

Pilnuje, by zbiór identyfikatorów (ID) markerów był zgodny między TRZEMA źródłami:
  1. rules.json                — reguły DEKLARATYWNE (regexy),
  2. ai_linter.py              — skompilowane markery (compile_markers) + detektory PROCEDURALNE,
  3. manieryzm-ai.md           — dokument-kanon (auto-katalog + „Indeks markerów").

Model spójności (świadomy, bo źródła nie są płaskie — patrz rozdział z A5):
  A) ZBIÓR DEKLARATYWNY musi być IDENTYCZNY w trzech miejscach:
       rules.json  ==  compile_markers(linter)  ==  auto-katalog w manieryzm-ai.md
       (auto-katalog generowany jest z rules.json, więc to też wykrywa nieodświeżony dokument).
  B) PEŁNY KATALOG ID (deklaratywne ∪ proceduralne) musi się zgadzać z „Indeksem markerów":
       (deklaratywne ∪ ai_linter.PROCEDURAL_MARKER_IDS)  ==  Indeks markerów w manieryzm-ai.md
       ID proceduralne (PL-RHYTHM, EN-DASH, PL-TYPO) NIE są w rules.json — to celowe (A5).
  C) UDOKUMENTOWANE proceduralne == FAKTYCZNIE EMITOWANE przez DETECTOR_REGISTRY (na próbkach):
       ai_linter.PROCEDURAL_MARKER_IDS  ==  {mid emitowane przez detektory}
       (chroni przed rozjazdem ręcznie deklarowanej stałej z rzeczywistą emisją detektorów).
  D) ASERCJA KIERUNKOWA (sedno A4/A5): każdy ID, jaki linter MOŻE wyemitować (deklaratywny +
       proceduralny), należy do (ID rules.json ∪ udokumentowane proceduralne) — nic spoza katalogu.

ZERO-DEP (stdlib: json, re). Exit 0 = spójne; exit 1 = rozjazd (z czytelnym raportem różnic).

Użycie:
    python3 tools/check_id_consistency.py
"""

import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(REPO_ROOT, "rules.json")
DOC_PATH = os.path.join(REPO_ROOT, "manieryzm-ai.md")

# Import lintera (REPO_ROOT na ścieżce) — źródło compile_markers i PROCEDURAL_MARKER_IDS.
sys.path.insert(0, REPO_ROOT)
import ai_linter  # noqa: E402

# Wzorzec ID markera — TYLKO realne prefiksy taksonomii: PL- / EN-.
# Celowo zawężony (nie [A-Z]{2,}-[A-Z]+), by parsowanie dokumentu nie złapało przypadkiem
# tokenów typu FAIL-HARD, AI-CV, EN-DASH-podobnych obcych ciągów, gdy dokument ewoluuje.
# Jeśli kiedyś dojdzie nowy prefiks językowy (np. DE-), dopisz go tutaj świadomie.
ID_RE = r"(?:PL|EN)-[A-Z]+"


def ids_from_rules() -> set:
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return {r["id"] for r in json.load(f)}


def ids_from_linter_declarative() -> set:
    return {m[0] for m in ai_linter.compile_markers("both")}


def _read_doc() -> str:
    with open(DOC_PATH, "r", encoding="utf-8") as f:
        return f.read()


def ids_from_catalog(doc: str) -> set:
    """ID z auto-katalogu (nagłówki '### XX-YY —' między znacznikami RULES:START/END)."""
    m = re.search(r"<!-- RULES:START -->(.*?)<!-- RULES:END -->", doc, re.DOTALL)
    if not m:
        print("[ERROR] manieryzm-ai.md: brak sekcji auto-katalogu (znaczniki RULES:START/END).",
              file=sys.stderr)
        sys.exit(1)
    return set(re.findall(r"^### (" + ID_RE + r") —", m.group(1), re.MULTILINE))


def ids_from_index(doc: str) -> set:
    """ID z sekcji 'Indeks markerów (ściąga)' (pierwsza kolumna tabeli)."""
    m = re.search(r"## Indeks markerów.*", doc, re.DOTALL)
    if not m:
        print("[ERROR] manieryzm-ai.md: brak sekcji 'Indeks markerów'.", file=sys.stderr)
        sys.exit(1)
    return set(re.findall(r"^\| (" + ID_RE + r") \|", m.group(0), re.MULTILINE))


# Próbki tekstu wyzwalające KAŻDY detektor proceduralny — pozwalają sprawdzić, jakie mid
# faktycznie emituje DETECTOR_REGISTRY, i porównać z udokumentowanym PROCEDURAL_MARKER_IDS.
_PROC_SAMPLES = {
    "emdash-overuse": "Cel — to — jest — jasny — i mierzalny.",
    "emoji-in-heading": "## 🚀 Nagłówek z emoji",
    "bold-overload": "**alfa** **beta** **gamma** **delta** w jednym akapicie.",
    "svo-rhythm": "Mózg przetwarza sygnały. Mózg filtruje szum. Mózg buduje model.",
    "connector-overload": "Projekt ruszył. Ponadto rośnie. Co więcej skaluje. Dodatkowo zarabia.",
}


def emitted_procedural_ids() -> set:
    """Zbiór mid faktycznie emitowanych przez detektory z DETECTOR_REGISTRY (na próbkach).

    Każdy detektor odpalamy dla 'pl' i 'en' (em-dash daje różne ID zależnie od języka).
    To weryfikuje kierunkowo: 'każdy ID, który linter może wyemitować proceduralnie' — czyli
    czy udokumentowany PROCEDURAL_MARKER_IDS nie rozjechał się z faktyczną emisją.
    """
    emitted = set()
    for detector_id, _adapter in ai_linter.DETECTOR_REGISTRY:
        sample = _PROC_SAMPLES.get(detector_id)
        if sample is None:
            print(f"[ERROR] Brak próbki testowej dla detektora {detector_id!r} — "
                  f"dodaj wpis w _PROC_SAMPLES.", file=sys.stderr)
            sys.exit(1)
        for lang in ("pl", "en"):
            for (_line, mid, _klasa, _frag) in ai_linter.run_procedural_detector(detector_id, sample, lang):
                emitted.add(mid)
    return emitted


def _report(label_a: str, a: set, label_b: str, b: set) -> bool:
    """Zwraca True gdy zbiory równe; inaczej drukuje różnice i zwraca False."""
    if a == b:
        return True
    only_a = sorted(a - b)
    only_b = sorted(b - a)
    print(f"[ERROR] Rozjazd ID: {label_a} vs {label_b}", file=sys.stderr)
    if only_a:
        print(f"        tylko w {label_a}: {only_a}", file=sys.stderr)
    if only_b:
        print(f"        tylko w {label_b}: {only_b}", file=sys.stderr)
    return False


def main():
    doc = _read_doc()

    decl_rules = ids_from_rules()
    decl_linter = ids_from_linter_declarative()
    decl_catalog = ids_from_catalog(doc)

    proc = set(ai_linter.PROCEDURAL_MARKER_IDS)
    full_linter = decl_linter | proc
    index_doc = ids_from_index(doc)
    emitted_proc = emitted_procedural_ids()

    ok = True
    # A) zbiór deklaratywny: rules == linter == auto-katalog
    ok &= _report("rules.json", decl_rules, "linter(compile_markers)", decl_linter)
    ok &= _report("rules.json", decl_rules, "auto-katalog (manieryzm-ai.md)", decl_catalog)
    # B) pełny katalog: linter(deklaratywne ∪ proceduralne) == Indeks markerów
    ok &= _report("linter pełny (decl ∪ proceduralne)", full_linter,
                  "Indeks markerów (manieryzm-ai.md)", index_doc)
    # C) udokumentowane proceduralne == faktycznie emitowane przez DETECTOR_REGISTRY
    ok &= _report("PROCEDURAL_MARKER_IDS (udokumentowane)", proc,
                  "emitowane przez DETECTOR_REGISTRY", emitted_proc)

    # D) asercja kierunkowa (sedno kontraktu A5/A4): KAŻDY ID, jaki linter może wyemitować
    #    (deklaratywny z compile_markers + proceduralny z rejestru), należy do
    #    (ID rules.json ∪ udokumentowane proceduralne). Nic „spoza katalogu" się nie prześliźnie.
    emittable = decl_linter | emitted_proc
    allowed = decl_rules | proc
    stray = sorted(emittable - allowed)
    if stray:
        print(f"[ERROR] Linter może wyemitować ID spoza katalogu (rules.json ∪ proceduralne): {stray}",
              file=sys.stderr)
        ok = False

    if not ok:
        print("[ERROR] Spójność ID NARUSZONA. Zsynchronizuj rules.json / linter / manieryzm-ai.md "
              "(po zmianie rules.json: python3 tools/gen_doc_catalog.py).", file=sys.stderr)
        sys.exit(1)

    print(f"OK   spójność ID: deklaratywne={len(decl_rules)} (rules==linter==katalog), "
          f"pełny katalog={len(full_linter)} (linter==Indeks), "
          f"proceduralne udokumentowane==emitowane ({sorted(proc)}). "
          f"Każdy emitowalny ID mieści się w katalogu.")


if __name__ == "__main__":
    main()
