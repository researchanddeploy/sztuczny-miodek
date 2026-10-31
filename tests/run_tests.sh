#!/usr/bin/env bash
# Regresja skilla sztuczny-miodek — warstwa manieryzmu AI (PL+EN).
# Asercje: 4 pliki baseline = FAIL (linter łapie zasiane AI-tells),
#          plik kontrolny (czysty, ludzki PL) = PASS (0 false-positives).
# Użycie: bash tests/run_tests.sh   (z katalogu skilla lub dowolnego)
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINT="$DIR/../ai_linter.py"
fail=0

assert_verdict() {
  local file="$1" want="$2" lang="$3"
  local out verdict
  out="$(python3 "$LINT" --lang "$lang" "$DIR/$file" 2>/dev/null)"
  verdict="$(printf '%s\n' "$out" | awk -F'|' '/PASS|FAIL/ {gsub(/ /,"",$NF); print $NF}' | tail -1)"
  if [[ "$verdict" == "$want"* ]]; then
    echo "OK   $file → $verdict (oczekiwano $want)"
  else
    echo "FAIL $file → '$verdict' (oczekiwano $want)"; fail=1
  fi
}

echo "== Regresja: baseline (oczekiwane FAIL) =="
assert_verdict baseline_pl_raport.md     FAIL both
assert_verdict baseline_pl_intro.md      FAIL both
assert_verdict baseline_en_cover_letter.md FAIL both
assert_verdict baseline_en_doc.md        FAIL both
echo "== Regresja: warstwa konstrukcyjna PL-STRUKT =="
# Ten sam sens, dwie konstrukcje: rozwlekła wpada, zwięzła przechodzi.
# Warstwa frazowa na obu plikach daje 0 trafień, więc werdykt zależy WYŁĄCZNIE
# od metryki strukt/100w — to jest właściwy test tej warstwy.
assert_verdict baseline_pl_strukt.md     FAIL pl
assert_verdict control_pl_strukt.md      PASS pl

echo "== Regresja: norma w przekładzie PL-NORMA =="
# Próbka <500 słów: gęstość ma podłogę mianownika (max(1, słowa/500)), więc
# sprawdzamy wykrycie, nie werdykt. Każdy z 5 wzorców musi dać trafienie.
n="$(python3 "$LINT" --lang pl "$DIR/baseline_pl_norma.md" 2>/dev/null | grep -c ':PL-NORMA:')"
if [[ "$n" -eq 5 ]]; then echo "OK   baseline_pl_norma.md → $n/5 trafień PL-NORMA"
else echo "FAIL baseline_pl_norma.md → $n/5 trafień PL-NORMA"; fail=1; fi

echo "== Regresja: kontrola (oczekiwane PASS, 0 false-positives) =="
assert_verdict control_pl_clean.md       PASS pl

if [[ $fail -eq 0 ]]; then
  echo "WSZYSTKIE TESTY PRZESZŁY."
else
  echo "REGRESJA WYKRYTA — popraw linter/taksonomię przed commitem."
fi
exit $fail
