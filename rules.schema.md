# Schemat `rules.json` — katalog markerów manieryzmu AI

`rules.json` to dane reguł lintera wydzielone z kodu (Epik A — „Reguła jako dane").
Plik jest tablicą JSON obiektów. Parsowalny wyłącznie biblioteką standardową Pythona
(moduł `json`) — bez żadnej zależności z pip (ZERO-DEP).

## Format pliku

Tablica `[ {...}, {...}, ... ]` reguł. **Kolejność wpisów ma znaczenie** dla detekcji
i musi być zachowana 1:1 względem historycznego `MARKER_DEFS`. **Duplikaty `id` są
normalne** — jeden identyfikator (np. `PL-SIGN`) grupuje wiele wariantów wzorca; przy
zliczaniu i raportowaniu liczy się każdy wpis z osobna.

## Pola reguły

Pola **obowiązkowe** (odpowiadają pięciu polom dawnej krotki `MARKER_DEFS`):

| Pole      | Typ    | Dozwolone wartości       | Opis |
|-----------|--------|--------------------------|------|
| `id`      | string | np. `PL-SIGN`, `EN-TRIAD` | Identyfikator kategorii markera. Lustro kategorii z `manieryzm-ai.md`. Może się powtarzać między wpisami. |
| `lang`    | string | `pl` \| `en` \| `both`    | Warstwa językowa. Filtr `--lang` wybiera wpisy, gdzie `lang` pasuje lub jest `both`. |
| `klasa`   | string | `block` \| `review`       | Waga markera: `block` = werdykt FAIL (blokuje), `review` = do przeglądu (nie blokuje sam z siebie). |
| `pattern` | string | dowolny regex Pythona     | Wzorzec wyrażenia regularnego. Kompilowany z flagami `re.IGNORECASE | re.UNICODE`. Escaping zapisany w składni JSON (np. `\\b` to `\b` regexa). Pole `pattern` może zawierać inline flagi modułu `re` (np. `(?m)`, `(?s)`) jako część składni wzorca — `(?m)` jest realnie używany w regule PL-TYPO. |
| `opis`    | string | dowolny tekst             | Krótki, ludzki opis tego, co marker wykrywa. |

Pola **opcjonalne** (przewidziane na przyszłą rozbudowę — A5 i rozszerzanie katalogu;
brak pola = brak wartości; linter A2 traktuje je jako opcjonalne i ich nieobecność nie zmienia zachowania):

| Pole         | Typ            | Opis |
|--------------|----------------|------|
| `prog`       | number         | Próg detekcji dla reguł nie-regexowych / proceduralnych (np. minimalna liczba wystąpień, by eskalować). |
| `przyklady`  | array<string>  | Lista przykładowych fragmentów, które reguła ma łapać (do testów i dokumentacji). |
| `doc`        | string         | Dłuższy tekst do generowanego katalogu w `manieryzm-ai.md` (A3). |

## Zasady spójności (gate review)

1. **Liczba wpisów** w `rules.json` musi się zgadzać z liczbą wpisów `MARKER_DEFS` (dopóki ten ostatni istnieje — do A2).
2. **Patterny 1:1** — każdy `pattern` jest dokładną kopią wzorca źródłowego; żaden znak escapingu nie może zostać zgubiony.
3. **Każdy `pattern` musi się kompilować** przez `re.compile(pattern, re.IGNORECASE | re.UNICODE)`.
4. Zbiór `id` w `rules.json`, w linterze i w `manieryzm-ai.md` musi być spójny (test wprowadzany w A4).

## Generowanie / weryfikacja

`rules.json` powstał skryptem `tools/gen_rules_json.py`, który importuje `MARKER_DEFS`
z `ai_linter.py` i serializuje je 1:1 (dzięki temu escaping nie jest przepisywany ręcznie).

```bash
python3 tools/gen_rules_json.py          # (re)generacja pliku
python3 tools/gen_rules_json.py --check  # tylko weryfikacja (liczba wpisów + kompilacja regexów)
```
