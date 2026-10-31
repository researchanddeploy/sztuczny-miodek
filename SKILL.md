---
name: sztuczny-miodek
version: 1.1.0
description: Use when auditing language quality or stripping AI mannerisms (AI-tells) from Polish or English text, and as a hard quality gate before declaring work "done" — flags signpost openers, rule-of-three triads, "not X but Y" antithesis, balanced parallelism, em-dash overuse, empty superlatives, redefinition clichés, heading emoji, plus Polish Cyrillic, calques, false friends, anglicisms, phantom collocations, and punctuation (Jan Miodek pragmatic purism). Covers reports, syntheses, cover letters, CVs, docs. Triggers on "sprawdź polszczyznę", "korekta tekstu", "audyt językowy", "sztuczny miodek", "manieryzm AI", "AI-tell", "de-AI", "stealth", "brzmi jak AI", "usuń ślady AI", "kalki AI", "odAI-uj".
---

# Sztuczny Miodek — Audyt Polszczyzny

## 1. Przegląd

**Co**: Audyt i korekta polszczyzny oraz eradykacja manieryzmu AI w tekstach PL i EN. Dwie misje: (1) wzorcowa polszczyzna wg Miodka; (2) usunięcie AI-tellów (manieryzmów generatywnych) z każdego tekstu dla człowieka: raportów, syntez, listów motywacyjnych, CV, dokumentacji.

**Zakres**: Teksty PL (pełen audyt Priorytety 1–10 + warstwa manieryzmu AI) oraz teksty EN (warstwa anty-AI-tell: nadużycie myślnika, „not X but Y", triady, klisze, superlatywy). Dla dokumentów Chase Hughes Framework — dodatkowa warstwa terminologiczna (RADA_JEZYKOWA.md). Pozostałe — audyt ogólny bez warstwy Chase'a.

**Rola bramki**: Skill jest twardą bramką jakości przed „done". Semantyka „PASS z uwagami = NIE PASS" — każdy nierozwiązany flag blokuje werdykt PASS.

**Pełna taksonomia manieryzmu AI**: plik referencyjny `manieryzm-ai.md` (kanon 14 kategorii PL+EN). Deterministyczny pre-scan: `ai_linter.py` (Priorytet 0 protokołu).

**Metodologia**: Pragmatyczny puryzm Jana Miodka — poprawiaj to, co ma polski odpowiednik; zachowaj to, co przyjęło się w domenie. Dla manieryzmu AI: zmieniaj teksturę prozy, zachowuj fakty.

**Wyzwalacze**: `sprawdź polszczyznę`, `korekta tekstu`, `audyt językowy`, `sztuczny miodek`.

---

## 2. Hierarchia Źródeł

Kolejność rozstrzygania konfliktów:

### Tryb Chase Hughes (pliki w `Chase Hughes Framework/`)
1. **RADA_JEZYKOWA.md** — nadrzędne źródło terminologii Chase'a (model SAAIPS, 20 sygnatur, modalności sensoryczne, błędy niedopuszczalne). Gdy RADA definiuje termin, jej wersja obowiązuje bezwzględnie.
2. **SKILL.md** (ten dokument) — nadrzędne źródło dla procesu audytu, wzorców detekcji, ogólnych reguł polszczyzny, kategorii błędów.
3. **W razie sprzeczności** — RADA_JEZYKOWA.md wygrywa dla terminów domenowych Chase'a. SKILL.md wygrywa dla ogólnych reguł językowych.
4. **Praktyczna zasada**: Przed audytem wczytaj RADA_JEZYKOWA.md jako referencję terminologiczną.

### Tryb ogólny (wszystkie inne pliki)
1. **SKILL.md** (ten dokument) — jedyne źródło reguł.
2. Nie wczytuj RADA_JEZYKOWA.md — nie dotyczy.
3. Terminy domenowe pliku (np. naukowe, filozoficzne) zachowuj w formie przyjętej w danej dziedzinie.

---

## 3. Wykrywanie Błędów — Ranking Priorytetów

Pełny katalog wzorców z przykładami i kontrprzykładami:
`references/wykrywanie-bledow.md` — wczytaj go przy każdym audycie.
Ranking (1 = najpoważniejsze):

1. Cyrylica `[A-Яa-яЁё]`
2. Kalki angielskie
3. Fałszywi przyjaciele
4. Anglicyzmy z polskim odpowiednikiem (w tym hybrydy angielsko-polskie)
5. Sztuczne kolokacje i związki frazeologiczne
6. Interpunkcja
7. Błędy stylu i gramatyki
8. Ortografia terminów łacińskich i greckich
9. Manieryzm AI (warstwa rozszerzona PL+EN — kanon w `manieryzm-ai.md`)
10. Typografia

## 4. Zasady Miodka — Praktyczne Decyzje

### Zasada 1: Czy istnieje polski odpowiednik?
- **Tak** — zmień na polski
- **Nie** — zachowaj anglicyzm (ewentualnie z wyjaśnieniem w nawiasie)

### Zasada 2: Czy jest to termin domenowy ustanowiony?
- W Chase'ie: **"rapport"** (= więź), **"elicytacja"** — ZACHOWAJ w formie ustalonej przez RADĘ JĘZYKOWĄ
- W Chase'ie: **"detektować sprzeczność"** — ZMIEŃ na "wykrywać sprzeczność"
- W naukach ścisłych: terminy łacińskie/greckie zaadaptowane — sprawdź pisownię w SJP

### Zasada 3: Test Naturalności
Przeczytaj fragment na głos. Czy to brzmi jak polska mowa, czy jak tłumaczenie z Google?
- Jeśli "jak tłumaczenie" — popraw

### Zasada 4: Minimalność Ingerencji
Nie rób zmian "dla lepszego stylu", jeśli tekst jest poprawny gramatycznie i merytorycznie. Audyt to nie redakcja literacka.

### Zasada 5: Weryfikacja kolokacji
Po każdej zamianie anglicyzmu na polski odpowiednik — sprawdź, czy powstały związek frazeologiczny faktycznie istnieje w naturalnej polszczyźnie. Dwa poprawne słowa mogą tworzyć sztuczną kolokację (np. „rusztowanie pojęciowe" — oba słowa OK, ale nikt tak nie mówi; poprawnie: „szkielet pojęciowy").

---

## 5. Bramka PASS/FAIL, Protokół Dwuetapowy i Racjonalizacje

### 5.1. Bramka PASS/FAIL

Skill kończy audyt jawnym werdyktem. Reguła nadrzędna: **„PASS z uwagami = NIE PASS".**

Werdykt **FAIL**, gdy zachodzi którykolwiek warunek:
- **FAIL-HARD**: jakakolwiek cyrylica `[А-Яа-яЁё]` w tekście PL.
- Marker klasy `block` po przekroczeniu progu: akapit z em-dash ≥3; emoji w linii nagłówka;
  antyteza redefinicyjna PL współwystępująca z ≥1 innym markerem w tym samym akapicie; seria
  antytez EN; **seria PL-ANTI ≥3 w pliku** (antyteza „X, a nie Y" / „Y, nie X" rozsiana po akapitach);
  ≥3 łączniki-otwarcia w pliku (PL-RHYTHM).
- Gęstość ważona > progu: trafienia / (słowa / 500) > **8**.
- **Konstrukcja: `strukt/100w` > 4,0** (PL-STRUKT — długie zdania i akapity, strona bierna
  z „zostać", nominalizacja, seria imiesłowów). Miara niezależna od gęstości frazowej:
  tekst może nie mieć ani jednej klisze z katalogu i wpaść wyłącznie tutaj.
- Po korekcie został choć jeden nierozwiązany flag.

Werdykt **PASS** tylko przy zerze blokerów, gęstości ≤ próg i `strukt/100w` ≤ 4,0.
Blok werdyktu na końcu raportu:

```
== WERDYKT: PASS | FAIL ==
Blokery: [lista ID + linia] lub „brak"
Gęstość/500: X (próg 8)
Strukt/100w: Y (próg 4,0)
```

Dwie miary są rozdzielone celowo, bo mierzą różne rzeczy: gęstość łapie **słownictwo**
(czarną listę fraz), `strukt` łapie **budowę zdania**. Pomiar między modelami pokazał, że
sama czarna lista jest najsłabszym narzędziem przeciw slopowi, a system reguł budowy —
najmocniejszym (pomiar autora skilla, opisany w `manieryzm-ai.md`, warstwa konstrukcyjna).
Wniosek dla korekty: przy `strukt` powyżej progu przepisz zdania, nie podmieniaj słów.

### 5.2. Protokół dwuetapowy (linter → osąd)

Zgodny z regułą dwustopniowości: deterministyczny pre-scan, potem osąd kontekstowy.

**Stage 1 — `ai_linter.py` (0 tokenów LLM).** Pre-scan generuje manifest:
```bash
python3 ~/.claude/skills/sztuczny-miodek/ai_linter.py --lang both ŚCIEŻKA…
# wyjście: plik:linia:ID:KLASA:fragment  +  blok == SUMMARY == (z kolumną strukt/100w)
```
Manifest = mapa podejrzeń. Linter łapie szeroko (wysoki recall), świadomie dopuszcza
false-positives w klasie `review` — to zadanie Stage 2, nie powód, by mu nie ufać.

**Stage 2 — osąd.** Dla każdego trafienia z manifestu:
1. Przeczytaj pełne zdanie (nie wyrywaj z kontekstu).
2. Rozstrzygnij: realny manieryzm czy uzasadniony kontekstem (klasa `review`).
3. Nanieś poprawkę — zmień teksturę prozy, zachowaj fakt/metrykę.
4. Zweryfikuj kolokację po zamianie (Zasada 5).
5. Wystaw werdykt wg 5.1.

Wzorzec oszczędza ~60% tokenów względem czytania całych plików (manifest → celowany Edit).

### 5.3. Tabela racjonalizacji — kontry na wymówki

Manieryzm AI przetrwa audyt tylko wtedy, gdy audytor da sobie wmówić, że to nie manieryzm.
Zasada-fundament: **łamanie litery reguł jest łamaniem ich ducha.**

| Wymówka | Rzeczywistość |
|---|---|
| „Ten myślnik jest stylistyczny" | Policz. ≥2 wtrącenia myślnikiem na akapit = maniera. Przecinek lub kropka. |
| „Ta triada jest celowa" | Tylko gdy wszystkie 3 człony to fakty nośne. Inaczej tnij do 2. |
| „Antyteza dodaje mocy" | Max 1 redefinicyjna na plik. Powtórzony wzór „to nie X — to Y" = manifest, nie myśl. |
| „Brzmi profesjonalnie" | „Profesjonalnie" to często właśnie etykieta AI-tellu. Konkret bije ton. |
| „Tekst jest wygenerowany, ale poprawny" | Poprawność gramatyczna ≠ brak manieryzmu. To dwie różne osie. |
| „To drobiazg, zostawię" | Reguła bramki: PASS z uwagami = NIE PASS. Drobiazg też blokuje. |
| „Signpost porządkuje wywód" | „Warto zauważyć / Podsumowując" nie niesie treści. Zacznij od rzeczy. |
| „Superlatyw oddaje skalę" | „Niezwykle/incredibly" nie mierzy. Podaj liczbę albo wytnij. |
| „To tylko jedno wystąpienie" | Marker klasy block przy współwystąpieniu blokuje niezależnie od progu ilościowego. |

### 5.4. Red Flags — STOP i popraw

Te myśli w trakcie audytu znaczą, że właśnie racjonalizujesz manieryzm:
- „Zostawię ten akapit, bo zmiana go spłaszczy."
- „Autor pewnie chciał tak brzmieć."
- „To zbyt subtelne, żeby czytelnik wyłapał."
- „Wszystkie trzy człony triady pasują." (sprawdź: czy każdy to fakt?)
- „PASS, ale z drobnymi uwagami."

Każda z nich oznacza: wróć do manifestu, popraw flag, nie wystawiaj PASS przedwcześnie.

---

## 6. Protokół Audytu

### Faza 0: Pre-scan linterem (Stage 1, 0 tokenów LLM)

Przed audytem manualnym uruchom `ai_linter.py` (sekcja 5.2) — manifest kieruje uwagę
celowanie zamiast czytania na ślepo. Jeśli linter niedostępny, przejdź wprost do Fazy 1.

### Faza 1: Skanowanie — przebieg pierwszy (każdy plik osobno)

```
1. Regex cyrylicy: [А-Яа-яЁё]
   → Zapisz linie z cyrylicą

2. Słowa kluczowe (przeszukaj z kontekstem):
   - "detekt" → sprawdź kontekst
   - "ekstrak" → sprawdź kontekst
   - "implemen" → sprawdź kontekst (poza IT?)
   - "raport" → sprawdź kontekst (więź czy dokument?)
   - "wizuali" → sprawdź kontekst (zmysł?)
   - "audyt" → sprawdź (słuchowy?)
   - "manifest" → sprawdź kontekst
   - "konfront" → sprawdź kontekst
   - "trigger" → sprawdź kontekst
   - "compliance" → sprawdź kontekst
   - "baseline" → sprawdź kontekst
   - "konsystent" → sprawdź kontekst
   - "rezonow" → sprawdź kontekst
   - "adresow" → sprawdź kontekst (problem?)
   - "dedykow" → sprawdź kontekst
   - "fokus" / "focus" → sprawdź kontekst
   - "target" → sprawdź kontekst
   - "priorytety" → sprawdź formę
   - "eskalow" → sprawdź kontekst
   - "ewaluow" → sprawdź kontekst
   - "finaliz" → sprawdź kontekst
   - "aplikacj" → sprawdź kontekst (IT vs zastosowanie)
   - "scaffolding" → zamień na szkielet/ramy

3. Interpunkcja (regex):
   - \w+ któr[yaeąegomuychim]\b → sprawdź przecinek przed "który"
   - \w+ że \b → sprawdź przecinek przed "że"
   - \w+ żeby \b → sprawdź przecinek przed "żeby"
   - \w+ gdy \b → sprawdź przecinek przed "gdy"
   - " to co " → sprawdź przecinek między "to" i "co"
   - "\w+ do czego" → sprawdź przecinek przed "do czego"

4. Artefakty AI:
   - Szukaj "niniejszy", "ponadto", "co więcej" (nadmiarowe)
   - Szukaj powtarzalnego szyku podmiot-orzeczenie-dopełnienie
   - Szukaj hedgowania: "potencjalnie", "mogłoby", "ewentualnie"
   - Szukaj zbędnych wzmacniaczy: "bardzo", "niezwykle", "wyjątkowo"
   - Szukaj kalki redefinicyjnej: "to nie X — to Y" (>2× na plik)

5. Gramatyka:
   - Szukaj imiesłowów: -ący, -ujący — czy pochodzą od kalek?
   - Sprawdź stronę bierną — czy jest naturalna?
   - Sprawdź aspekt czasowników — dokonany vs niedokonany
   - Szukaj nominalizacji — czy można uprościć?
   - Szukaj zawieszonych przysłówków (ang. szyk)
   - Szukaj powtórzeń leksykalnych w jednym zdaniu

6. Fałszywi przyjaciele:
   - "aktualnie" → sprawdź znaczenie (obecnie vs w rzeczywistości)
   - "ewentualnie" → sprawdź znaczenie (opcjonalnie vs w końcu)
   - "sympatyczn" → sprawdź kontekst
   - "transparentn" → sprawdź kontekst
   - "definitywn" → sprawdź kontekst
   - "dekad" → sprawdź kontekst (dziesięciolecie?)

7. Hybrydy angielsko-polskie:
   - Szukaj angielskich rdzeni z polskimi końcówkami: -ować, -ami, -ów
   - Jeśli forma nie istnieje w SJP — zamień na zaadaptowaną pożyczkę lub polski odpowiednik

8. Ortografia terminów łacińskich/greckich:
   - Szukaj terminów naukowych i sprawdź pisownię (częste: zamiana u↔o, e↔a)

9. Typografia:
   - Szukaj angielskich cudzysłowów "..." w polskim tekście (poza blokami kodu)
```

### Faza 2: Analiza Kontekstu

Dla każdego znalezionego potencjalnego błędu:
1. Przeczytaj pełne zdanie (nie wyrywaj z kontekstu)
2. **[Tryb Chase]** Sprawdź w RADA_JEZYKOWA.md, czy termin jest zdefiniowany
3. Oceń, czy to naprawdę błąd (czasem anglicyzm jest celowy lub termin jest domenowy)
4. Jeśli błąd — zaproponuj konkretną poprawkę z uzasadnieniem
5. **Przy zamianach anglicyzmów — weryfikuj kolokację** (Zasada 5)

### Faza 3: Raport

Format dla każdego pliku:

```
## Plik: NAZWA.md

### Cyrylica
- Linia X: `[cytat]` → Zmienić na: `[poprawka]`

### Kalki Angielskie
- Linia Y: `[cytat]` → Zmienić na: `[poprawka]`

### Fałszywi Przyjaciele
- Linia Z: `[cytat]` → Zmienić na: `[poprawka]`

### Anglicyzmy / Hybrydy
- Linia W: `[cytat]` → Zmienić na: `[poprawka]`

### Sztuczne Kolokacje
- Linia S: `[cytat]` → Zmienić na: `[poprawka]`

### Interpunkcja
- Linia I: `[cytat]` → Zmienić na: `[poprawka]`

### Styl i Gramatyka
- Linia V: `[cytat]` → Zmienić na: `[poprawka]`

### Artefakty AI
- Linia U: `[cytat]` → Zmienić na: `[poprawka]`

### Podsumowanie
Liczba błędów: X | Krytycznych: Y | Drobnych: Z
```

Jeśli plik jest czysty — napisz: "Brak błędów."

### Faza 4: Automatyczna Korekta

Edycja każdego pliku z naniesionymi poprawkami.

### Faza 5: Przebieg weryfikacyjny (OBOWIĄZKOWY)

Jednoprzebiegowy audyt regularnie pomija ~40% usterek (empirycznie: 14 znalezione w przebiegu 1., dodatkowe 11 w przebiegu 2.). Dlatego po korekcie:

1. Wczytaj plik ponownie (pełny odczyt)
2. Skanuj pod kątem kategorii **najczęściej pomijanych w przebiegu 1.**:
   - **Interpunkcja** — przejdź grep po `\w+ któr`, `\w+ że `, `\w+ żeby `, ` to co `
   - **Kolokacje** — przeczytaj każdą zmienioną frazę w kontekście zdania
   - **Hybrydy** — szukaj ang. rdzeni z pol. końcówkami
   - **Ortografia terminów naukowych** — sprawdź samogłoski
   - **Cudzysłowy** — szukaj `"..."` w tekście polskim
   - **Powtórzenia** — szukaj zdań z 2× tym samym rdzeniem
3. Raportuj dodatkowe znaleziska jako "Runda 2"
4. Weryfikacja końcowa: `grep -rP "[А-Яа-яЁё]"` powinien dać 0 trafień

---

## 7. Wyjątki i Przypadki Szczególne

### Cytaty i Fragmenty Angielskie
Jeśli fragment jest cytatem z angielskiego źródła — zachowaj z wyjaśnieniem w komentarzu.

### Nazwy Własne
Nie poprawiać: nazwisk, miejsc, tytułów publikacji, nazw modeli (np. "Six-Minute X-Ray" jako tytuł).

### Terminy Techniczne (IT)
- "API", "machine learning", "JSON", "YAML" — zachować
- Ale "trigger" w znaczeniu ogólnym — zmienić na "wyzwalacz"

### Terminy Naukowe w Blokach Kodu
Angielskie terminy w blokach kodu (```) z polskim objaśnieniem obok — zachować. Przykład: `SURFACE STRUCTURE — zlokalizowane obwody neuronowe` — OK, bo to oryginalna terminologia autora umieszczona w schemacie.

### Terminy Zdefiniowane w RADA_JEZYKOWA.md (tylko tryb Chase)
20 sygnatur Chase'a, model SAAIPS, modalności sensoryczne — zawsze stosuj wersję z RADY. Nie zmieniaj samodzielnie terminów, które RADA ustaliła.

### Polskie Słowa Rzadkie
Jeśli poprawka używa słowa rzadkiego, dodaj wyjaśnienie:
- "Elicytacja (ang. *elicitation* — wydobywanie informacji)"

---

### Tryb przekładu (tekst tłumaczony z obcego języka)

Audyt przekładu ma dwa ograniczenia, których nie ma audyt tekstu autorskiego:

1. **Wierność treści.** Poprawiaj język, nie przekaz. Wyliczenia, antytezy i triady autora
   oryginału zostają, nawet gdy linter oznacza je jako `review`. Usuwasz manierę przekładu,
   nie styl autora.
2. **Termin bez odpowiednika.** Nie zostawiaj gołego anglicyzmu. Wprowadź go z objaśnieniem
   w przypisie zakończonym „(przyp. red.)": co znaczy, skąd pochodzi, czemu nie ma polskiej
   formy. Przykład: „Przynęta na gniew (ang. ragebait): treść celowo skrojona tak, by wywołać
   oburzenie… (przyp. red.)". Przypis podaje tylko fakty pewne; czego nie da się potwierdzić,
   nie objaśniaj.

Dodatkowo:
- Kalkę terminu autora zastąp polskim słowem o tej samej tradycji, jeśli istnieje
  (*insurgency* → „insurekcja", *mirroring* → „odzwierciedlanie").
- Pustej zapowiedzi oryginału („should be highlighted") nie przenoś dosłownie.
- Gdy przekład idzie do składu (PDF), sprawdź sierotki i dzielenie wyrazów
  (`references/wykrywanie-bledow.md`, Priorytet 10).
- Gdy zleceniodawca prosi o formę niezgodną z normą (np. nieodmienione imię obce),
  sprawdź normę w poradni (`tvly search` po sjp.pwn.pl), pokaż źródło i daj mu wybór.

## 8. Szybka Ściąga — Najczęstsze Błędy

| # | Błąd | Poprawka | Kategoria |
|---|---|---|---|
| 1 | brak przecinka przed „który/że/żeby" | **dodaj przecinek** | Interpunkcja |
| 2 | rusztowanie pojęciowe | **szkielet pojęciowy** | Sztuczna kolokacja |
| 3 | raport (= więź) | **więź, relacja** | Fałszywy przyjaciel |
| 4 | detektować | **wykrywać** | Kalka angielska |
| 5 | lesionami / scrollować | **lezjami / przewijać** | Hybryda ang.-pol. |
| 6 | dekady | **dziesięciolecia** | Fałszywy przyjaciel |
| 7 | konsystentny | **spójny** | Kalka angielska |
| 8 | "Niniejszy dokument..." | **"Ten dokument..."** | Artefakt AI |
| 9 | bazować na | **opierać się na** | Zły przyimek / kalka |
| 10 | dla opisania | **do opisu** | Kalka składniowa |
| 11 | homonkulus | **homunkulus** | Ortografia łac./gr. |
| 12 | "cytat" | **„cytat"** | Typografia |
| 13 | „Warto podkreślić, że / Podsumowując" | **zacznij od rzeczy** | Manieryzm AI (PL-SIGN) |
| 14 | „odgrywa kluczową rolę / rewolucyjny" | **konkret lub metryka** | Manieryzm AI (PL-CLICHE) |
| 15 | triada „szybko, sprawnie i skutecznie" | **2 człony, jeśli nie wszystkie nośne** | Manieryzm AI (PL/EN-TRIAD) |
| 16 | myślnik w każdym zdaniu | **przecinek/kropka** | Manieryzm AI (PL-TYPO / EN-DASH) |
| 17 | „not just X — it's Y" / „it's not X, it's Y" | **state the positive directly** | Manieryzm AI (EN-ANTI) |
| 18 | „delve into / leverage / seamless / I am excited to" | **plain verb, cut filler** | Manieryzm AI (EN-CLICHE) |
| 19 | najbardziej elementarny / sprzeciwia się trzymaniu się | **elementarny / odrzuca trzymanie się** | Norma (PL-NORMA) |
| 20 | na jego własnych warunkach (*on its own terms*) | **według jego własnych reguł** | Kalka (PL-NORMA) |
| 21 | myśliciela Antonio Gramsciego | **Antonia Gramsciego** | Odmiana imion obcych |
| 22 | goły anglicyzm w przekładzie (ragebait) | **polski opis + przypis „(przyp. red.)"** | Tryb przekładu |
| 23 | sierotka „i/w/z" na końcu wiersza; „po-pkulturę" | **twarda spacja; wyłączone dzielenie** | Skład PDF |

---

## 9. Przykładowy Raport Audytu

Wzorcowy raport z komentarzem: `references/przykladowy-raport.md`.
