# sztuczny-miodek

Skill Claude Code do audytu polszczyzny i eradykacji manieryzmu AI (AI-tellów) w tekstach polskich i angielskich. Metodologia: pragmatyczny puryzm Jana Miodka.

## Co robi

Skill realizuje dwie misje:

1. **Wzorcowa polszczyzna (PL)** — pełny audyt tekstu polskiego wg dziesięciu priorytetów: cyrylica, kalki angielskie, fałszywi przyjaciele, anglicyzmy, sztuczne kolokacje, interpunkcja, styl i gramatyka, ortografia terminów łacińskich/greckich, manieryzm AI, typografia.
2. **Usuwanie AI-tellów (PL + EN)** — wykrywa i usuwa manieryzmy generatywne: puste signposty, triady (rule-of-three), antytezę „nie X — to Y", paralelizm, nadużycie myślnika, puste superlatywy, klisze redefinicyjne, emoji w nagłówkach. Dla raportów, syntez, listów motywacyjnych, CV i dokumentacji.

Skill działa jako **twarda bramka jakości** przed deklaracją „done". Obowiązuje semantyka **„PASS z uwagami = NIE PASS"**: każdy nierozwiązany flag blokuje werdykt PASS. Werdykt FAIL zapada przy cyrylicy w tekście PL (FAIL-HARD), markerze klasy `block` po przekroczeniu progu albo gęstości ważonej trafień powyżej 8 na 500 słów.

Zasada Miodka: poprawiaj to, co ma polski odpowiednik; zachowuj to, co przyjęło się w danej dziedzinie. Dla manieryzmu AI: zmieniaj teksturę prozy, zachowuj fakty i metryki.

## Kluczowe funkcje

**Deterministyczny linter `ai_linter.py` (Stage 1).** Pre-scan bez kosztu tokenów LLM. Generuje manifest podejrzeń w formacie `plik:linia:ID:KLASA:fragment` plus blok `== SUMMARY ==` z liczbą słów, trafień, maksymalną liczbą myślników na akapit, gęstością i werdyktem. Linter łapie szeroko (wysoki recall), świadomie dopuszcza false-positives w klasie `review`. Wyłącznie biblioteka standardowa Pythona 3, zero zależności pip.

**Osąd kontekstowy (Stage 2).** Dla każdego trafienia z manifestu: przeczytaj pełne zdanie, rozstrzygnij czy to realny manieryzm czy uzasadnienie kontekstowe, nanieś poprawkę, zweryfikuj kolokację po zamianie, wystaw werdykt. Wzorzec manifest → celowany Edit oszczędza około 60% tokenów względem czytania całych plików.

**Kanon kategorii manieryzmu (`manieryzm-ai.md`).** Źródło prawdy taksonomii. Każde ID kategorii ma odpowiednik w linterze. Kategorie PL: PL-SIGN, PL-CLICHE, PL-RHET, PL-ANTI, PL-RHYTHM, PL-HEDGE, PL-TYPO, a także PL-NORMA (naruszenia normy typowe dla przekładu z angielskiego: stopniowanie przymiotników absolutnych, podwójne „się", kalki frazeologiczne). Kategorie EN: EN-DASH, EN-ANTI, EN-TRIAD, EN-PARA, EN-CLICHE, EN-HEDGE, EN-SUPER, EN-CONCL.

**Warstwa konstrukcyjna PL-STRUKT.** Osobna metryka `strukt/100w` (próg 4,0): długie zdania i akapity, strona bierna z „zostać", nominalizacje, serie imiesłowów. Łapie tekst, który nie ma ani jednej klisze, a mimo to brzmi generatorowo.

**Tryb przekładu (`SKILL.md`).** Zasady audytu tekstu tłumaczonego: wierność treści oryginału, terminy bez odpowiednika objaśniane w przypisie „(przyp. red.)", kontrola składu PDF (sierotki, dzielenie wyrazów).

**Priorytety 1–10 (`SKILL.md`, pełny katalog w `references/wykrywanie-bledow.md`).** Ranking wykrywania błędów polszczyzny, od cyrylicy (Priorytet 1) przez sztuczne kolokacje (Priorytet 5, „najczęściej przeoczana kategoria") i interpunkcję (Priorytet 6) po typografię (Priorytet 10). Każdy priorytet ma tabelę wzorców z poprawkami i regexami skanowania.

## Instalacja

### Tryb A — bezpośredni clone (skill)

Najprostszy. Skill ląduje wprost w katalogu skilli Claude Code:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/researchanddeploy/sztuczny-miodek.git ~/.claude/skills/sztuczny-miodek
```

Claude Code wykryje skill automatycznie na podstawie `SKILL.md`. Wywołanie: `/sztuczny-miodek`.

Aktualizacja: `cd ~/.claude/skills/sztuczny-miodek && git pull`.

### Tryb B — plugin przez marketplace

Wersjonowane aktualizacje i instalacja jedną komendą:

```text
/plugin marketplace add researchanddeploy/sztuczny-miodek
/plugin install sztuczny-miodek@sztuczny-miodek
```

Wywołanie: `/sztuczny-miodek:sztuczny-miodek`. Aktualizacja: `/plugin update sztuczny-miodek@sztuczny-miodek`.

Oba tryby korzystają z tego samego `SKILL.md` w korzeniu repo. Katalog `.claude-plugin/` jest używany tylko w trybie B.

## Użycie

### W Claude Code

Skill uruchamia się przez jeden z wyzwalaczy w rozmowie:

- `sprawdź polszczyznę`
- `sztuczny miodek`
- `audyt językowy`
- `korekta tekstu`, `manieryzm AI`, `AI-tell`, `de-AI`, `usuń ślady AI`, `odAI-uj`

Claude przeprowadzi pełny protokół: pre-scan linterem, osąd kontekstowy, korektę, przebieg weryfikacyjny i werdykt PASS/FAIL.

### Linter z linii poleceń

Pre-scan można uruchomić samodzielnie:

```bash
python3 ai_linter.py --lang both ŚCIEŻKA_DO_PLIKU.md
```

Flaga `--lang` przyjmuje `pl`, `en` lub `both`. Można podać kilka ścieżek naraz.

### Interpretacja manifestu i werdyktu

Manifest to jedna linia na trafienie:

```text
raport.md:42:PL-SIGN:review:Warto podkreślić, że
```

Pola: ścieżka pliku, numer linii, ID kategorii, klasa (`review` lub `block`), dopasowany fragment. Klasa `review` wymaga osądu kontekstowego (możliwy false-positive). Klasa `block` to bloker werdyktu po przekroczeniu progu.

Blok `== SUMMARY ==` podaje werdykt na końcu:

```text
== SUMMARY ==
plik | słowa | trafienia | em-dash/akapit(max) | gęstość/500 | strukt/100w | blokery | WERDYKT
```

PASS zapada tylko przy zerze blokerów, gęstości nie większej niż 8 i `strukt/100w` nie większym niż 4,0.

## Testy

Katalog `tests/` zawiera zestaw regresyjny:

- `run_tests.sh` — uruchamia linter na plikach bazowych i porównuje wynik z oczekiwaniami.
- `GROUND_TRUTH.md` — oczekiwane werdykty i trafienia dla każdego pliku testowego (oracle).
- Pliki bazowe z manieryzmem (`baseline_pl_raport.md`, `baseline_pl_intro.md`, `baseline_en_doc.md`, `baseline_en_cover_letter.md`) oraz plik kontrolny czystego tekstu (`control_pl_clean.md`), na którym linter ma zwrócić PASS bez false-positives.
- Para `baseline_pl_strukt.md` / `control_pl_strukt.md` — ten sam sens w dwóch konstrukcjach; testuje wyłącznie warstwę PL-STRUKT.
- `baseline_pl_norma.md` — próbka przekładu; każdy z 5 wzorców PL-NORMA musi dać trafienie.

Uruchomienie:

```bash
cd tests && ./run_tests.sh
```

## Opcjonalna warstwa terminologii domenowej

Skill obsługuje opcjonalny tryb z własnym słownikiem terminów branżowych. Jeśli posiadasz taki plik, terminy w nim zdefiniowane mają pierwszeństwo nad ogólnymi regułami dla swojej dziedziny. Bez słownika skill działa w trybie ogólnym: pełny audyt polszczyzny i manieryzmu AI. Słownik domenowy jest zewnętrzny i nie wchodzi w skład repozytorium.

## Atrybucja i licencja

Kod, taksonomia AI-tellów, reguły polszczyzny i układ skilla: licencja **MIT** (zob. plik `LICENSE`).

Metodologia opiera się na pracy **Jana Miodka** (pragmatyczny puryzm, „Ojczyzna polszczyzna"). To referencja i atrybucja, nie redystrybucja chronionej treści. Licencja MIT obejmuje wyłącznie materiały tego repozytorium; nie rozciąga się na cudzą własność intelektualną, do której repo się odwołuje.
