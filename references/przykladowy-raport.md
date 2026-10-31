# Przykładowy raport audytu

Wyniesione z `SKILL.md` (sekcja 9) w ramach progressive disclosure.

## 9. Przykładowy Raport Audytu

```
## Plik: Bentov+Pribram+Bohm — Zintegrowany model.md

### Cyrylica
- Linia 264: "Память jako rezonans"
  → Zmienić na: "Pamięć jako rezonans"
  Uzasadnienie: rosyjskie „Память" zamiast polskiego „Pamięć"

### Sztuczne Kolokacje
- Linia 331: "dostarczyli rusztowania pojęciowego"
  → Zmienić na: "dostarczyli szkieletu pojęciowego"
  Uzasadnienie: „rusztowanie pojęciowe" nie funkcjonuje w polszczyźnie
- Linia 15: "linie myślenia, które zbiegają na tym samym wniosku"
  → Zmienić na: "linie myślenia, które prowadzą do tego samego wniosku"
  Uzasadnienie: „zbiegać na wniosku" — nienaturalna kolokacja

### Hybrydy Angielsko-Polskie
- Linia 288: "Pribram mierzył to EEG i lesionami."
  → Zmienić na: "Pribram mierzył to EEG i lezjami."
  Uzasadnienie: ang. lesion + pol. -ami = hybryda; zaadaptowana forma: lezja

### Interpunkcja
- Linia 107: "stwierdzał że mają"
  → Zmienić na: "stwierdzał, że mają"
- Linia 160: "to co mierzalne"
  → Zmienić na: "to, co mierzalne"
- Linia 329: "raport żeby odpowiedzieć"
  → Zmienić na: "raport, żeby odpowiedzieć"

### Styl i Gramatyka
- Linia 174: "przepływu informacji-energii cyklicznie między"
  → Zmienić na: "cyklicznego przepływu informacji-energii między"
  Uzasadnienie: zawieszony przysłówek (kalka ang. szyku)
- Linia 107: "niewielkie ablacje ... niewielki wpływ"
  → Zmienić na: "drobne ablacje ... niewielki wpływ"
  Uzasadnienie: powtórzenie leksykalne w jednym zdaniu

### Podsumowanie
Liczba błędów: 25 | Krytycznych: 1 (cyrylica) | Kolokacje: 3 | Interpunkcja: 14 | Drobnych: 7
```

---

## 10. Checklist Audytu

- [ ] **Faza 0 — pre-scan linterem** (`python3 ai_linter.py --lang both …` → manifest)
- [ ] Skanowanie cyrylicy (regex `[А-Яа-яЁё]`)
- [ ] Skanowanie kalek angielskich (lista 29 słów kluczowych)
- [ ] Skanowanie fałszywych przyjaciół (13 wzorców)
- [ ] Skanowanie anglicyzmów z polskim odpowiednikiem
- [ ] Skanowanie hybryd angielsko-polskich (ang. rdzeń + pol. deklinacja)
- [ ] **Skanowanie interpunkcji** (przecinki przed który/że/żeby/gdy, „to, co")
- [ ] **Weryfikacja kolokacji** (każda zamiana anglicyzmu → sprawdź naturalność frazy)
- [ ] **Manieryzm AI — warstwa PL** (PL-SIGN signposty, PL-CLICHE wytrychy, PL-RHET triady/paralelizm/antyteza redefinicyjna, PL-ANTI antyteza przeciwstawna „X, a nie Y", PL-RHYTHM rytm, PL-HEDGE, PL-TYPO myślniki/emoji) — wg `manieryzm-ai.md`
- [ ] **Manieryzm AI — warstwa EN** (EN-DASH, EN-ANTI, EN-TRIAD, EN-PARA, EN-CLICHE, EN-HEDGE, EN-SUPER, EN-CONCL) dla tekstów angielskich
- [ ] Analiza gramatyki (strona bierna, imiesłowy, nominalizacje, zawieszony przysłówek, powtórzenia)
- [ ] Sprawdzenie aspektu czasowników (dokonany vs niedokonany)
- [ ] **Ortografia terminów łacińskich/greckich** (sprawdź samogłoski)
- [ ] **Typografia** (cudzysłowy angielskie → polskie)
- [ ] **[Tryb Chase]** Weryfikacja terminów z RADA_JEZYKOWA.md
- [ ] Raportowanie z numerami linii i uzasadnieniami
- [ ] Automatyczna korekta (edycja plików)
- [ ] **PRZEBIEG WERYFIKACYJNY** — ponowne skanowanie po korekcie (interpunkcja, kolokacje, hybrydy, ortografia, cudzysłowy, powtórzenia)
- [ ] Weryfikacja końcowa: `grep -rP "[А-Яа-яЁё]"` powinien dać 0 trafień
- [ ] **Werdykt bramki PASS/FAIL** (sekcja 5.1) — „PASS z uwagami = NIE PASS"; re-run lintera, 0 blokerów
- [ ] Podsumowanie dla użytkownika (liczba poprawek na plik, podział na kategorie)

---

## 11. Referencje

- **Jan Miodek**, "Ojczyzna polszczyzna" — metodologia puryzmu pragmatycznego
- **`manieryzm-ai.md`** — kanoniczna taksonomia manieryzmu AI (14 kategorii PL+EN), źródło prawdy
- **`ai_linter.py`** — deterministyczny pre-scan (Stage 1), operacyjne lustro taksonomii
- **RADA_JEZYKOWA.md** — źródło terminologii Chase Hughes Framework (tryb Chase)
- **Słownik Języka Polskiego PWN** — weryfikacja form ogólnopolskich
- **Wielki Słownik Poprawnej Polszczyzny PWN (WSPP)** — rozstrzyganie wątpliwości poprawnościowych
- **Sesja audytowa Bentov/Pribram/Bohm (2026-03-29)** — empiryczna walidacja protokołu: 14+11 usterek w 2 przebiegach, 7 kategorii błędów nie pokrytych przez wersję 1.0
