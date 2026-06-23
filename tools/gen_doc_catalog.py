#!/usr/bin/env python3
"""
gen_doc_catalog.py — generator katalogu reguł w manieryzm-ai.md z rules.json (Epik A, A3).

Dokument manieryzm-ai.md jest kanonem opisowym: zawiera ręcznie pisane przykłady, kolumny
„Dlaczego/Poprawka/Próg" oraz bramkę PASS/FAIL — tego NIE da się (ani nie chcemy) odtworzyć
z samych reguł. Driftem, który tu likwidujemy, są listy „Wzorce techniczne" (regexy) rozsiane
po sekcjach i przepisywane ręcznie — rozjeżdżały się z faktyczną zawartością lintera.

Rozwiązanie: jedna AUTO-GENEROWANA sekcja katalogu, wstrzykiwana między znaczniki
  <!-- RULES:START --> ... <!-- RULES:END -->
Sekcja powstaje WYŁĄCZNIE z rules.json (jedno źródło prawdy reguł regexowych), więc nigdy się
nie rozjedzie. Reszta dokumentu pozostaje nietknięta. Skrypt jest bezpieczny do wielokrotnego
uruchomienia (zawsze ten sam wynik, podmienia treść między znacznikami — nie dokleja duplikatów).

Reguły grupowane są po ID w kolejności PIERWSZEGO wystąpienia w rules.json (ta sama kolejność
co w linterze). Każdy wariant wzorca to jeden wiersz (opis + regex). Język i klasa brane z reguł.

Kategorie obsługiwane proceduralnie (PL-RHYTHM, EN-DASH oraz progi em-dash/emoji/bold) NIE mają
wpisów regexowych w rules.json — z założenia nie pojawią się w tym katalogu; ich opis żyje w
ręcznych sekcjach dokumentu. To świadome (patrz A5: detektory proceduralne).

Użycie:
    python3 tools/gen_doc_catalog.py            # wstrzykuje/odświeża sekcję w manieryzm-ai.md
    python3 tools/gen_doc_catalog.py --check     # exit 1 jeśli dokument jest nieaktualny (CI/A4)
"""

import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(REPO_ROOT, "rules.json")
DOC_PATH = os.path.join(REPO_ROOT, "manieryzm-ai.md")

BEGIN_MARK = "<!-- RULES:START -->"
END_MARK = "<!-- RULES:END -->"

LANG_LABEL = {"pl": "PL", "en": "EN", "both": "PL+EN"}


def load_rules(path: str = RULES_PATH):
    """Wczytuje rules.json jako listę dictów (zachowuje kolejność i duplikaty ID)."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _md_escape_cell(text: str) -> str:
    """Eskejpuje znaki łamiące komórkę tabeli Markdown (pipe), regex w backtickach."""
    return text.replace("|", "\\|")


def build_catalog(rules) -> str:
    """Buduje treść sekcji katalogu (między znacznikami) z listy reguł.

    Grupuje po ID w kolejności pierwszego wystąpienia. Dla każdej grupy: nagłówek z ID,
    językiem i klasą(-ami), oraz tabela wariantów (opis + wzorzec regex w backtickach).
    """
    # Kolejność ID wg pierwszego wystąpienia
    order = []
    groups = {}
    for r in rules:
        rid = r["id"]
        if rid not in groups:
            groups[rid] = []
            order.append(rid)
        groups[rid].append(r)

    out = []
    out.append("Sekcja wygenerowana automatycznie z `rules.json` przez "
               "`tools/gen_doc_catalog.py` — nie edytuj ręcznie. "
               f"Liczba reguł regexowych: {len(rules)} w {len(order)} kategoriach.")
    out.append("")

    for rid in order:
        variants = groups[rid]
        langs = sorted({v["lang"] for v in variants})
        klasy = sorted({v["klasa"] for v in variants})
        lang_str = " / ".join(LANG_LABEL.get(l, l) for l in langs)
        klasa_str = " / ".join(klasy)
        out.append(f"### {rid} — {lang_str} — klasa: {klasa_str}")
        out.append("")
        out.append("| Opis | Wzorzec (regex) |")
        out.append("|---|---|")
        for v in variants:
            opis = _md_escape_cell(v["opis"])
            pattern = _md_escape_cell(v["pattern"])
            out.append(f"| {opis} | `{pattern}` |")
        out.append("")

    # Bez końcowej pustej linii nadmiarowej
    return "\n".join(out).rstrip() + "\n"


def render_section(rules) -> str:
    """Zwraca pełny blok ze znacznikami BEGIN/END i katalogiem w środku."""
    return f"{BEGIN_MARK}\n{build_catalog(rules)}{END_MARK}"


def inject(doc: str, section: str) -> str:
    """Podmienia zawartość między znacznikami BEGIN/END.

    Wymaga DOKŁADNIE jednego BEGIN_MARK i jednego END_MARK we właściwej kolejności.
    Gdyby znacznik pojawił się dodatkowo gdzie indziej (np. literalnie w prozie/disclaimerze),
    generator ODMAWIA (exit 2) zamiast cicho uszkodzić dokument, podmieniając zły fragment.
    """
    n_begin = doc.count(BEGIN_MARK)
    n_end = doc.count(END_MARK)
    if n_begin == 0 or n_end == 0:
        print(f"[ERROR] Brak znaczników {BEGIN_MARK} ... {END_MARK} w {DOC_PATH}",
              file=sys.stderr)
        sys.exit(2)
    if n_begin != 1 or n_end != 1:
        print(f"[ERROR] {DOC_PATH}: oczekiwano DOKŁADNIE jednej pary znaczników, znaleziono "
              f"{n_begin}× {BEGIN_MARK} i {n_end}× {END_MARK}. Usuń literalne wystąpienia "
              f"znaczników z prozy (np. ujmij nazwy w cudzysłów: „RULES:START\").",
              file=sys.stderr)
        sys.exit(2)
    if doc.index(BEGIN_MARK) > doc.index(END_MARK):
        print(f"[ERROR] {DOC_PATH}: znacznik {END_MARK} występuje przed {BEGIN_MARK}.",
              file=sys.stderr)
        sys.exit(2)

    pattern = re.compile(
        re.escape(BEGIN_MARK) + r".*?" + re.escape(END_MARK),
        re.DOTALL,
    )
    return pattern.sub(lambda _m: section, doc, count=1)


def main():
    check_only = "--check" in sys.argv[1:]
    rules = load_rules()
    section = render_section(rules)

    with open(DOC_PATH, "r", encoding="utf-8") as f:
        doc = f.read()

    new_doc = inject(doc, section)

    if check_only:
        if new_doc != doc:
            print("[ERROR] manieryzm-ai.md jest NIEAKTUALNY względem rules.json — "
                  "uruchom: python3 tools/gen_doc_catalog.py", file=sys.stderr)
            sys.exit(1)
        print("OK   manieryzm-ai.md zgodny z rules.json (katalog aktualny).")
        return

    if new_doc == doc:
        print("OK   manieryzm-ai.md już aktualny — bez zmian.")
        return

    with open(DOC_PATH, "w", encoding="utf-8") as f:
        f.write(new_doc)
    print(f"Zaktualizowano katalog w: {DOC_PATH}")


if __name__ == "__main__":
    main()
