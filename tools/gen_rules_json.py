#!/usr/bin/env python3
"""
gen_rules_json.py — jednorazowy generator rules.json z zaszytego MARKER_DEFS (Epik A, A1).

Importuje MARKER_DEFS bezpośrednio z ai_linter, dzięki czemu regex patterny trafiają do
rules.json bez ręcznego przepisywania — escaping zachowany 1:1. Zachowuje kolejność wpisów
(ma znaczenie dla detekcji) oraz wszystkie duplikaty ID (to normalne — jeden ID = wiele wariantów).

Po A2 linter będzie czytał rules.json zamiast MARKER_DEFS; ten skrypt zostaje jako narzędzie
pomocnicze (np. do regeneracji baseline, gdyby ktoś chciał zacząć od kodu).

Użycie:
    python3 tools/gen_rules_json.py            # zapisuje rules.json w katalogu repo
    python3 tools/gen_rules_json.py --check    # tylko weryfikacja, bez zapisu
"""

import json
import os
import re
import sys

# Import z katalogu nadrzędnego (repo root)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

import ai_linter  # noqa: E402

RULES_PATH = os.path.join(REPO_ROOT, "rules.json")

# Pola opcjonalne przewidziane na przyszłość (A5 + rozbudowa katalogu).
# Generator NIE wypełnia ich teraz — schema je dopuszcza, linter (A2) traktuje jako opcjonalne.
OPTIONAL_FIELDS = ("prog", "przyklady", "doc")


def build_rules():
    """Buduje listę reguł (dict) z MARKER_DEFS, zachowując kolejność i duplikaty ID."""
    rules = []
    for mid, lang, klasa, pattern, opis in ai_linter.MARKER_DEFS:
        rules.append({
            "id": mid,
            "lang": lang,
            "klasa": klasa,
            "pattern": pattern,
            "opis": opis,
        })
    return rules


def verify(rules):
    """Sanity-check: liczba wpisów oraz kompilacja każdego regexa."""
    assert len(rules) == len(ai_linter.MARKER_DEFS), (
        f"Niezgodna liczba wpisów: rules={len(rules)} vs "
        f"MARKER_DEFS={len(ai_linter.MARKER_DEFS)}"
    )
    flags = re.IGNORECASE | re.UNICODE
    for i, r in enumerate(rules):
        # struktura
        for field in ("id", "lang", "klasa", "pattern", "opis"):
            assert field in r, f"Wpis #{i} bez pola '{field}'"
        assert r["lang"] in ("pl", "en", "both"), f"Wpis #{i} zły lang: {r['lang']}"
        assert r["klasa"] in ("block", "review"), f"Wpis #{i} zła klasa: {r['klasa']}"
        # regex się kompiluje (te same flagi co linter)
        re.compile(r["pattern"], flags)
    # patterny 1:1 względem MARKER_DEFS
    for r, src in zip(rules, ai_linter.MARKER_DEFS):
        assert r["pattern"] == src[3], f"Pattern rozjechany dla {r['id']}"
    print(f"OK   {len(rules)} wpisów, wszystkie regexy się kompilują, patterny 1:1.")


def main():
    check_only = "--check" in sys.argv[1:]
    rules = build_rules()
    verify(rules)
    if check_only:
        return
    with open(RULES_PATH, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Zapisano: {RULES_PATH}")


if __name__ == "__main__":
    main()
