# Kanoniczna taksonomia manieryzmu AI

Plik opisuje 14 kategorii AI-manieryzmu wykrywanych przez skill `sztuczny-miodek`. Jest lustrem `ai_linter.py` — każde ID kategorii w tym dokumencie odpowiada identycznemu ID w linterze. Przy rozbieżności między dokumentem a linterem ten plik jest źródłem prawdy; linter należy zaktualizować.

Sekcje opisowe (przykłady, kolumny „Dlaczego/Poprawka/Próg", bramka PASS/FAIL) są pisane ręcznie. Natomiast sekcja **„Katalog reguł (auto-generowany z rules.json)"** powstaje automatycznie z pliku reguł `rules.json` (jedno źródło prawdy wzorców regex) przez `tools/gen_doc_catalog.py` — nie edytuj jej ręcznie. Po każdej zmianie `rules.json` uruchom generator, a CI pilnuje zgodności (`gen_doc_catalog.py --check`).

---

## Warstwa PL

Dotyczy tekstów polskich: raportów, syntez, dokumentów produktowych, CV, korespondencji.

### PL-SIGN — puste otwarcia / signposty (klasa: review)

Frazy, które nie wnoszą treści — jedynie sygnalizują, że AI „przechodzi do clue". Typowe na początku zdania lub akapitu.

| Wzorzec (ludzki opis) | Przykład (błędny) | Dlaczego to AI-tell | Poprawka | Próg/uwaga |
|---|---|---|---|---|
| „Warto podkreślić / zauważyć / zaznaczyć…" | „Warto podkreślić, że projekt zakończył się sukcesem." | Pusty wstępniak — nic nie dodaje do treści. | „Projekt zakończył się sukcesem." | review; dowolne wystąpienie flaguj |
| „Należy zauważyć / podkreślić…" | „Należy zauważyć, że dane są niekompletne." | Jw. — nadmiarowy sygnał meta. | „Dane są niekompletne." | review |
| „Co istotne / ważne / ciekawe," | „Co istotne, model osiąga 94% precyzji." | Wartościowanie przed faktem zamiast faktu samego. | „Model osiąga 94% precyzji." | review |
| „W dzisiejszych czasach / w dobie / w erze / w obliczu…" | „W dzisiejszych czasach AI rewolucjonizuje przemysł." | Ogólnikowe zakotwiczenie temporalne bez substancji. | Usuń i zacznij od konkretnej tezy. | review |
| „W dynamicznie zmieniającej / rozwijającej się…" | „W dynamicznie zmieniającym się środowisku biznesowym…" | Frazeologiczny autopilot. | Usuń albo podaj konkretny kontekst. | review |
| „Nie sposób przecenić…" | „Nie sposób przecenić znaczenia tej decyzji." | Hiperboliczny wstępniak — ocena zamiast argumentu. | Podaj konkretny dowód znaczenia. | review |
| „Jak powszechnie wiadomo…" | „Jak powszechnie wiadomo, JavaScript dominuje frontend." | AI maskuje twierdzenie jako aksjomat. | Usuń i podaj źródło lub po prostu stwierdź fakt. | review |
| Wyrazy otwarcia podsumowania: „Podsumowując / reasumując / konkludując…" | „Podsumowując, projekt spełnił założenia." | Sygnały przejścia niepotrzebne w zwięzłym tekście. | Usuń lub przejdź do treści bez wstępniaka. | review |
| Zaproszenia do zagłębiania: „Zanurzmy się / przyjrzyjmy się bliżej…" | „Przyjrzyjmy się bliżej temu zagadnieniu." | AI-tell: naśladowanie stylu edukacyjnego wideo. | Usuń; zacznij od meritum. | review |
| „Mam nadzieję, że ten / ta / to…" | „Mam nadzieję, że ta analiza okaże się pomocna." | Kurtuazyjna formułka AI na końcu odpowiedzi. | Usuń całkowicie. | review |

**Wzorce techniczne (regex, Python `re.IGNORECASE | re.UNICODE`):** _(lista poglądowa, może być niekompletna — źródło prawdy regexów: sekcja „Katalog reguł" niżej, auto-generowana z `rules.json`)_
`\bwarto (?:tu )?(?:podkreśl|zauważ|zaznacz|pamięta|dodać|wspomnieć|nadmienić|zwrócić uwagę)` · `\bnależy (?:tu )?(?:zauważyć|podkreślić|pamiętać|zaznaczyć|dodać|wspomnieć)\b` · `\bco (?:istotne|ważne|ciekawe|znamienne|warte odnotowania),` · `\bw dzisiejszych czasach\b` · `\bw (?:dobie|obliczu|erze)\b` · `\bw dynamicznie (?:zmieniając|rozwijając)\w* się\b` · `\bnie sposób (?:przecenić|nie\b)` · `\bjak (?:powszechnie )?wiadomo\b` · `\b(?:podsumowując|reasumując|konkludując|wnioskując|na zakończenie)\b` · `\b(?:zanurzmy|zagłębmy|przyjrzyjmy|zastanówmy|skupmy|pochylmy) się\b` · `\bprzyjrzyjmy się bliżej\b` · `\bmam nadzieję, że (?:ten|ta|to|powyższ|niniejsz)`

---

### PL-CLICHE — frazy-wytrychy (klasa: review)

Okleiny o wysokiej częstotliwości w prozie AI; zwłaszcza sugerujące wagę lub wyjątkowość bez pokrycia.

| Wzorzec | Przykład (błędny) | Dlaczego to AI-tell | Poprawka | Próg/uwaga |
|---|---|---|---|---|
| „odgrywa kluczową / istotną / ważną rolę" | „Komunikacja odgrywa kluczową rolę w projekcie." | Puste stwierdzenie wagi zamiast wyjaśnienia mechanizmu. | „Komunikacja decyduje o tym, czy…" | review |
| „ma kluczowe / istotne / ogromne znaczenie" | „Bezpieczeństwo ma kluczowe znaczenie." | Jw. | „Bez tego mechanizmu…" | review |
| „stanowi integralną część / nieodłączny element / fundament / filar" | „Testowanie stanowi integralny element procesu." | Metaforyczne wypełniacze bez informacji. | „Testowanie wchodzi w skład…" | review |
| Superlatywy: rewolucyjny / przełomowy / innowacyjny / niezrównany / bezprecedensowy | „To przełomowe rozwiązanie zmienia branżę." | AI domyślnie stosuje najwyższy stopień. | Konkretna cecha lub metryka. | review; jeśli brak mierzalnej podstawy = flag |
| „możliwości są (praktycznie) nieograniczone" | „Możliwości tego modelu są nieograniczone." | Hiperboła bez pokrycia. | Podaj zakres / benchmark. | review |
| „zmienia reguły gry" | „To narzędzie zmienia reguły gry w logistyce." | Klisza marketingowa. | Opisz konkretną zmianę. | review |
| „to dopiero początek / wierzchołek" | „To tylko wierzchołek góry lodowej." | Sensacjonalistyczne zakończenie. | Wskaż co jest poniżej, albo usuń. | review |
| „w erze cyfrowej / sztucznej inteligencji / AI" | „W erze AI każda firma musi…" | Zakotwiczenie bez treści. | Usuń lub podaj rok / kontekst. | review |

**Wzorce techniczne:** `\bodgrywa (?:kluczow|istotn|ważn|znacząc|niebagateln)\w* rolę\b` · `\bma (?:kluczowe|istotne|ogromne|zasadnicze) znaczenie\b` · `\bstanowi (?:integraln\w+ część|nieodłączn\w+ element|fundament|podstawę|trzon|filar)\b` · `\b(?:rewolucyjn|przełomow|innowacyjn|nowoczesn|nowatorsk|niezrównan|bezprecedensow)\w+\b` · `\bmożliwości (?:są )?(?:praktycznie |niemal |wręcz )?(?:nieograniczone|nieskończone)\b` · `\bzmienia reguły gry\b` · `\bto dopiero (?:początek|wierzchołek)\b` · `\bw erze (?:cyfrow|sztucznej inteligencji|AI)\w*\b`

---

### PL-RHET — figury retoryczne (klasa: block dla antyteza redefinicyjna; reszta review)

| Figura | Przykład (błędny) | Dlaczego to AI-tell | Poprawka | Próg/klasa |
|---|---|---|---|---|
| Antyteza redefinicyjna: „To nie X — to Y" | „To nie narzędzie — to partner w pracy." | Dramatyzacja przez zaprzeczenie-i-redefinicję. Przy ≥1 innym markerze w akapicie = bloker. | Zdanie twierdzące: „Narzędzie pełni rolę partnera przez…" | **block** gdy z innym markerem; review solo; max 1–2/plik |
| Nie tylko… ale (również/także) | „Raport nie tylko opisuje dane, ale również je interpretuje." | Paralelizm AI sugerujący dwa równorzędne argumenty. | „Raport opisuje i interpretuje dane." | review |
| „Z jednej strony… z drugiej strony" | „Z jednej strony dane, z drugiej strony etyka." | Sztuczna dialektyka bez rozstrzygnięcia. | Wybierz dominującą tezę lub podaj wniosek. | review (raportuj parę) |
| Triada: „X, Y i Z" | „Efektywność, innowacyjność i rentowność." | Grupy trzech jako AI-sygnatura. Może być uzasadnione — stąd review. | Jeśli nie wszystkie 3 są równie nośne, zredukuj do 2. | review (FP możliwy) |
| „Od X po Y" | „Od start-upów po korporacje." | Span-klisza. | Podaj konkretny zakres lub usuń. | review |

**Wzorce techniczne:** `[Tt]o nie (?:jest )?.{1,40}[—–-] to\b` · `[Tt]o nie (?:jest )?.{1,40}\.\s+[Tt]o\b` · `\bnie tylko\b.{1,80}?\b(?:ale|lecz)(?: również| także| i)?\b` · `\bz jednej strony\b` · `\b(\w+), (\w+),? (?:i|oraz) (\w+)\b` · `\bod \w+(?:y|ów|i)? (?:po|aż po) \w+`

---

### PL-ANTI — antyteza przeciwstawna NIEreferencyjna (klasa: review; block przy serii ≥3)

Bliźniak PL-RHET, którego brakowało: ta sama figura przeciwstawienia, ale **bez myślnika i bez „to … to"**. Najczęściej przeoczana, bo każde zdanie z osobna brzmi naturalnie w mowie. Maniera ujawnia się dopiero w nagromadzeniu — gdy niemal każdy akapit domyka się rytmem „robię X, a nie Y". Symetryczna do EN-ANTI.

| Figura | Przykład (błędny) | Dlaczego to AI-tell | Poprawka | Próg/klasa |
|---|---|---|---|---|
| „X, a nie Y" | „To opis mojego dnia, a nie ogłoszenie." | Domknięcie przez kontrast — generator lubi przeciwstawić, żeby brzmieć dobitnie. | Zdanie twierdzące: „To opis mojego dnia." | review; block w serii ≥3/plik |
| Inwersja „Y, nie X" | „To zasada operacyjna, nie hasło." | Ta sama figura odwrócona; sufiksowe „nie X" jako pseudo-pointa. | „Tę zasadę stosuję na co dzień." | review; block w serii ≥3/plik |

**Uwaga na granicę z interpunkcją:** wyliczenie z zaprzeczeniem („transceiver, nie źródło") bywa *poprawne* i jest osobną kwestią (przecinek). PL-ANTI celuje w *retoryczne* domknięcie, nie w listę. Dlatego klasa `review` — osąd w Stage 2 rozstrzyga, a dopiero ≥3 wystąpienia w pliku eskalują do `block`.

**Wzorce techniczne:** `,\s+a nie\b` · `,\s+nie\s+\w+(?:\s+\w+)?(?=[.!?;\n]|$)`

---

### PL-RHYTHM — rytm / składnia (klasa: review; bloker po progu)

| Problem | Przykład (błędny) | Dlaczego to AI-tell | Poprawka | Próg/klasa |
|---|---|---|---|---|
| Nawał łączników na początku zdań: „Ponadto / Co więcej / Dodatkowo / Jednocześnie…" | „Projekt zakończył się. Ponadto osiągnął ROI. Co więcej, zespół docenił wyniki." | AI nawleka zdania jak korale — każde zaczyna od łącznika. | Zostaw jeden łącznik; krótkie zdanie dosadne. | **block** jeśli ≥3 w pliku lub 2 pod rząd |
| Powtarzalny szyk SVO (trzy zdania zaczynające się tym samym tokenem) | „Mózg przetwarza sygnały. Mózg filtruje szum. Mózg buduje model." | Monotoniczna repetycja tokenu otwierającego. | Zmień szyk lub połącz zdania. | review (logika, nie regex) |

**Łączniki wykrywane:** `Ponadto`, `Co więcej`, `Dodatkowo`, `Jednocześnie`, `Następnie`, `Warto dodać`, `Mało tego` — na początku zdania (po `^` lub `. `).

---

### PL-HEDGE — hedging / nadmierna ostrożność (klasa: review)

| Wzorzec | Przykład (błędny) | Dlaczego to AI-tell | Poprawka |
|---|---|---|---|
| „Mogłoby to potencjalnie…" | „Mogłoby to potencjalnie wskazywać na problem." | Podwójne zabezpieczenie się: tryb warunkowy + „potencjalnie". | „To wskazuje na problem." |
| „potencjalnie" (solo) | „Takie podejście potencjalnie zwiększa wydajność." | Strach przed kategorycznym twierdzeniem. | „Takie podejście zwiększa wydajność o X%." |
| „wydaje się, że / zdaje się, że" | „Wydaje się, że dane są poprawne." | Pseudo-skromność zamiast weryfikacji. | Sprawdź i stwierdź; jeśli niepewność jest realna — opisz jej źródło. |
| „warto byłoby rozważyć" | „Warto byłoby rozważyć zmianę architektury." | Miękka rekomendacja zamiast decyzji. | „Zmień architekturę, bo…" |
| „w pewnym sensie" | „To jest w pewnym sensie rozwiązanie." | Relatywizacja bez uzasadnienia. | Usuń lub wyjaśnij sens. |

**Wzorce techniczne:** `\b(?:mogłoby|mógłby|można by|dałoby się)\b.{0,30}\b(?:potencjalnie|ewentualnie|w pewnym sensie)\b` · `\bpotencjalnie\b` · `\bwydaje się, że\b` · `\bzdaje się, że\b` · `\bwarto byłoby rozważyć\b` · `\bw pewnym sensie\b`

---

### PL-TYPO — typografia / struktura AI (klasa: block po progu dla em-dash i emoji w nagłówku)

| Problem | Przykład (błędny) | Dlaczego to AI-tell | Poprawka | Próg/klasa |
|---|---|---|---|---|
| Emoji w nagłówku | `## 🚀 Kluczowe wnioski` | AI dekoruje strukturę dokumentu emoji. | Usuń emoji z nagłówków. | **block** — dowolne emoji w linii `##` |
| Nadużycie em-dasha (—) lub spacjowanego en-dasha ( – ) | „Cel — optymalizacja — jest jasny — i mierzalny." | ≥3 myślniki w akapicie to sygnatura AI-listy-udającej-zdanie. | Przecinki, kropki lub restrukturyzacja zdania. | **block** jeśli ≥3/akapit; review przy 1–2 |
| Bold-overload (≥4 pogrubień w akapicie) | „**Cel**, **zakres**, **budżet** i **termin** są kluczowe." | AI bold-uje każde słowo klucz. | Zostaw pogrubienie dla max 1 elementu w akapicie. | review jeśli ≥4/akapit |
| Nagłówki-klisze | `## Kluczowe wnioski`, `## Co dalej?`, `## Wnioski końcowe` | Szablonowe tytuły sekcji bez informacji. | Nagłówek = treść: `## Decyzje do podjęcia w Q3` | review |

**Wzorce nagłówków-klisz:** `^#{1,6}\s*(?:Kluczowe wnioski|Najważniejsze (?:punkty|wnioski|informacje)|Co dalej\??|Podsumowanie|Wnioski końcowe)\b`

---

## Warstwa EN (proza angielska — CV/CL/docs)

Dotyczy angielskich tekstów kandydackich i dokumentów profesjonalnych. Kolumny „Dlaczego" i „Poprawka" po polsku — dla operatora PL.

### EN-DASH — em-dash overuse (klasa: block po progu)

| Wzorzec | Przykład (błędny) | Dlaczego to AI-tell | Poprawka | Próg |
|---|---|---|---|---|
| ≥3 em-dash (—) lub spacjowanych en-dash ( – ) w akapicie | "I led the team — designed the roadmap — and shipped — on time." | Jw. jak PL-TYPO: AI unika interpunkcji przez nawlekanie myślników. | Przecinki, zdania podrzędne lub podział na zdania. | **block** jeśli ≥3/akapit |

---

### EN-ANTI — antithesis patterns (klasa: review; block przy serii)

| Wzorzec | Przykład (błędny) | Dlaczego to AI-tell | Poprawka | Klasa |
|---|---|---|---|---|
| „not just/only/merely/simply… but" | "Not just a developer — but a builder of systems." | Dramatyzacja przez zaprzeczenie. | "I build systems, not write isolated code." | review; **block** przy serii (not X, but Y; not Z, but W) |
| „It's not X — it's Y" | "It's not a job — it's a mission." | Klisza redefinicyjna. | Zdanie twierdzące z konkretną treścią. | review |
| „not X, but Y" (krótka forma) | "Not reactive, but proactive." | Jw. | "Proactive approach: I anticipate…" | review |

**Wzorce techniczne:** `\bnot (?:just|only|merely|simply)\b.{1,80}?\b(?:but|it'?s|it is)\b` · `\bit'?s not\b.{1,40}[—–-]\s*it'?s\b` · `\bnot \w+, but \w+\b`

---

### EN-TRIAD — rule of three (klasa: review)

| Wzorzec | Przykład (błędny) | Dlaczego to AI-tell | Poprawka |
|---|---|---|---|
| „X, Y, and Z" | "Efficient, reliable, and scalable." | Triada jako domyślny rytm AI. Może być uzasadniona — review. | Jeśli nie wszystkie 3 elementy są równie nośne, skróć do 2. |

**Wzorzec techniczny:** `\b(\w+), (\w+),? and (\w+)\b`

---

### EN-PARA — balanced parallelism (klasa: review)

| Wzorzec | Przykład (błędny) | Dlaczego to AI-tell | Poprawka |
|---|---|---|---|
| „self-X and self-Y" | "self-motivated and self-driven" | Redundantny paralelizm z prefiksem „self-". | Wybierz jeden i dodaj dowód. |
| Pary przymiotników złożonych (X-Y and Z-W) | "data-driven and results-oriented" | Podwójny compound-adjective jako sygnatura AI-CV. | Podaj konkretny wynik zamiast etykietki. |

**Wzorce techniczne:** `\bself-\w+ and self-\w+\b` · `\b(\w+)-(\w+) and (\w+)-(\w+)\b`

---

### EN-CLICHE — signposty / klisze (klasa: review)

Jeden pattern obejmuje wszystkie warianty (IGNORECASE):

`it's worth noting` · `worth noting that` · `in today's fast-paced world` · `ever-evolving landscape` · `delve into` · `delving` · `tapestry` · `a testament to` · `navigate the complexities` · `seamlessly` · `robust` · `leveraging` · `spearheading` · `I am confident/excited/thrilled/passionate` · `passionate about` · `at the end of the day` · `game-changer` · `cutting-edge` · `best-in-class` · `state-of-the-art` · `unlock the potential`

| Przykład (błędny) | Dlaczego to AI-tell | Poprawka |
|---|---|---|
| "I am passionate about building scalable systems." | „Passionate about" to klisza CV nr 1. | "I built 3 distributed systems in 18 months." |
| "Let's delve into the architecture." | „Delve" to sygnatura AI-tutorialu. | "The architecture consists of…" |
| "A robust, seamless solution." | Dwa AI-przymiotniki pod rząd. | Podaj benchmark: "Handles 10k rps with p99 < 50ms." |

**Wzorzec techniczny:** regex alternacja z flag IGNORECASE — pełna lista w sekcji wyżej.

---

### EN-HEDGE — hedging (klasa: review)

| Wzorzec | Przykład (błędny) | Dlaczego to AI-tell | Poprawka |
|---|---|---|---|
| „arguably" | "This is arguably the best approach." | Mięknie twierdzenie bez powodu. | "This approach reduces latency by 40% vs. X." |
| „it could be argued" | "It could be argued that the model overfits." | Jw. | "The model overfits: train 98%, val 71%." |
| „to some extent / one could say" | "To some extent this improves UX." | Relatywizacja. | Podaj mierzalny efekt lub usuń zastrzeżenie. |

**Wzorce techniczne:** `\b(?:arguably|it could be argued|to some extent|one could say|it may well be)\b`

---

### EN-SUPER — puste superlatywy (klasa: review)

| Wzorzec | Przykład (błędny) | Dlaczego to AI-tell | Poprawka |
|---|---|---|---|
| incredibly / extremely / truly / remarkably / highly / exceptionally / undoubtedly / absolutely / deeply | "I am incredibly passionate and truly dedicated." | Intensyfikatory bez substancji — AI podnosi ton zamiast treści. | Usuń; jeśli intensywność ważna, podaj fakt. |

**Wzorzec techniczny:** `\b(?:incredibly|extremely|truly|remarkably|highly|exceptionally|undoubtedly|absolutely|deeply)\b`

---

### EN-CONCL — signposty zamknięcia (klasa: review)

| Wzorzec | Przykład (błędny) | Dlaczego to AI-tell | Poprawka |
|---|---|---|---|
| in conclusion / overall / ultimately / all in all / in summary / to sum up / in essence / when all is said | "In conclusion, I believe I am the right candidate." | AI sygnalizuje koniec zamiast kończyć. | Usuń; ostatnie zdanie niech będzie treścią, nie meta-komentarzem. |

**Wzorzec techniczny:** `\b(?:in conclusion|overall|ultimately|all in all|in summary|to sum up|in essence|when all is said)\b`

---

## Bramka PASS/FAIL

Semantyka: **„PASS z uwagami = NIE PASS"**. Każdy nierozwiązany flag po korekcie blokuje PASS.

### FAIL-HARD
- Cyrylica w tekście PL: dowolny znak `[А-Яа-яЁё]`. Bezwarunkowy bloker, niezależnie od kontekstu.

### FAIL (blokery warunkowe)

| Bloker | Warunek |
|---|---|
| PL-TYPO / EN-DASH em-dash | akapit z ≥3 myślnikami (—  lub  – ) |
| PL-TYPO emoji w nagłówku | dowolne emoji w linii `##…` |
| PL-RHET antyteza redefinicyjna | współwystępuje z ≥1 innym markerem w tym samym akapicie |
| PL-ANTI seria antytez | ≥3 trafień „X, a nie Y" / „Y, nie X" w pliku (maniera rozsiana po akapitach) |
| EN-ANTI seria antytez | pattern „not X, but Y; not Z, but W" (≥2 w bliskim sąsiedztwie) |
| PL-RHYTHM łączniki-otwarcia | ≥3 w pliku lub ≥2 pod rząd |

### FAIL (gęstość)
- Gęstość ważona > progu: `trafienia / max(1, słowa/500) > 8`.
- Obliczenie: `słowa = len(re.findall(r"\w+", text))`.

### PASS
Tylko gdy 0 blokerów i gęstość ≤ 8. Po korekcie każdy nierozwiązany flag = brak PASS.

### Format wyjścia lintera

Manifest (1 linia / trafienie):
```
plik:linia:ID:KLASA:dopasowany_fragment
```

Blok podsumowania:
```
== SUMMARY ==
plik | słowa | trafienia | em-dash/akapit(max) | gęstość/500 | blokery | WERDYKT
```

---

## Detektory proceduralne (kontrakt)

Reguły wykrywania dzielą się na dwa rozłączne rodzaje — to świadomy, czysty podział (Epik A, A5):

1. **Reguły deklaratywne** — czyste wzorce regex. Mieszkają w `rules.json` (jedno źródło prawdy), ładowane do `MARKER_DEFS` i kompilowane przez `compile_markers()`. Wykrywane jedną wspólną pętlą `finditer`. To one są przedmiotem auto-katalogu niżej.

2. **Reguły proceduralne** — wymagają progów i logiki, których nie da się wyrazić pojedynczym regexem (liczenie myślników na akapit, monotoniczny szyk SVO, nawał łączników-otwarć, emoji w nagłówku, bold-overload). Pozostają funkcjami `detect_*` w `ai_linter.py` i **z założenia NIE trafiają do `rules.json`** ani do auto-katalogu.

**Dlaczego rozdział:** wzorzec regex jest danymi (konfiguracją), a detektor proceduralny jest kodem (algorytmem z progiem). Trzymanie ich osobno pozwala edytować katalog regexów bez dotykania kodu i odwrotnie.

### Rejestr i wołanie po identyfikatorze

Detektory proceduralne są wołane **po identyfikatorze** przez rejestr `DETECTOR_REGISTRY` w `ai_linter.py` — lista par `(detector_id, adapter)` w ustalonej kolejności wykonania. `scan_file` iteruje po rejestrze (nie zna już poszczególnych funkcji `detect_*` z nazwy), a pojedynczy detektor można uruchomić funkcją `run_procedural_detector(detector_id, text, eff_lang)`.

| `detector_id` | Funkcja `detect_*` | ID markera | Klasa | Próg |
|---|---|---|---|---|
| `emdash-overuse` | `detect_emdash_overuse` | `PL-TYPO` (PL/both) / `EN-DASH` (en) | block | ≥3 myślniki w akapicie |
| `emoji-in-heading` | `detect_emoji_in_headings` | `PL-TYPO` | block | dowolne emoji w linii nagłówka |
| `bold-overload` | `detect_bold_overload` | `PL-TYPO` | review | ≥4 pogrubienia w akapicie |
| `svo-rhythm` | `detect_svo_rhythm` | `PL-RHYTHM` | review | 3 zdania z tym samym tokenem otwierającym |
| `connector-overload` | `detect_connector_overload` | `PL-RHYTHM` | block | ≥3 łączniki-otwarcia w pliku |

**Kolejność w rejestrze ma znaczenie** (wyznacza porządek dodawania trafień przed sortowaniem po linii) — nie zmieniaj jej bez powodu.

### Kontrakt adaptera

```
adapter(text: str, eff_lang: str) -> List[Tuple[int, str, str, str]]
```

Zwraca listę krotek `(line, mid, klasa, fragment)`:
- `line` — numer linii 1-based (`int`),
- `mid` — identyfikator markera (`'PL-TYPO'` | `'EN-DASH'` | `'PL-RHYTHM'` | …),
- `klasa` — `'block'` | `'review'` (`block` liczy się do blokerów i może dać werdykt FAIL),
- `fragment` — krótki opis trafienia (`str`).

Adapter jest cienkim wrapperem nad funkcją `detect_*` — progi i logika żyją w `detect_*`, nie w adapterze. Nieznany `detector_id` w `run_procedural_detector` → `KeyError` (świadoma, głośna awaria, by literówka identyfikatora się nie prześliznęła).

---

## Katalog reguł (auto-generowany z rules.json)

> **Źródło prawdy regexów.** Poniższy katalog (sekcja ujęta w znaczniki „RULES:START" / „RULES:END") jest JEDYNYM miarodajnym źródłem wzorców regex — generowany automatycznie z `rules.json` przez `tools/gen_doc_catalog.py`. Listy „Wzorce techniczne" przy poszczególnych kategoriach wyżej mają charakter wyłącznie opisowy i mogą być NIEKOMPLETNE względem `rules.json` (do czasu pełnej konsolidacji). W razie rozbieżności rozstrzyga ten katalog.

<!-- RULES:START -->
Sekcja wygenerowana automatycznie z `rules.json` przez `tools/gen_doc_catalog.py` — nie edytuj ręcznie. Liczba reguł regexowych: 47 w 13 kategoriach.

### PL-SIGN — PL — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| puste otwarcie: warto podkreślić/zauważyć | `\bwarto (?:tu )?(?:podkreśl\|zauważ\|zaznacz\|pamięta\|dodać\|wspomnieć\|nadmienić\|zwrócić uwagę)` |
| puste otwarcie: należy zauważyć/podkreślić | `\bnależy (?:tu )?(?:zauważyć\|podkreślić\|pamiętać\|zaznaczyć\|dodać\|wspomnieć)\b` |
| signpost: co istotne/ważne | `\bco (?:istotne\|ważne\|ciekawe\|znamienne\|warte odnotowania),` |
| klisza temporalna: w dzisiejszych czasach | `\bw dzisiejszych czasach\b` |
| klisza temporalna: w dobie/obliczu/erze | `\bw (?:dobie\|obliczu\|erze)\b` |
| klisza: w dynamicznie zmieniającym się | `\bw dynamicznie (?:zmieniając\|rozwijając)\w* się\b` |
| klisza: nie sposób przecenić | `\bnie sposób (?:przecenić\|nie\b)` |
| signpost: jak (powszechnie) wiadomo | `\bjak (?:powszechnie )?wiadomo\b` |
| signpost zamknięcia: podsumowując/reasumując | `\b(?:podsumowując\|reasumując\|konkludując\|wnioskując\|na zakończenie)\b` |
| meta-zaproszenie: zanurzmy/zagłębmy się | `\b(?:zanurzmy\|zagłębmy\|przyjrzyjmy\|zastanówmy\|skupmy\|pochylmy) się\b` |
| meta-zaproszenie: przyjrzyjmy się bliżej | `\bprzyjrzyjmy się bliżej\b` |
| hedging zamknięcia: mam nadzieję, że ten/ta/to | `\bmam nadzieję, że (?:ten\|ta\|to\|powyższ\|niniejsz)` |

### PL-CLICHE — PL — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| klisza: odgrywa kluczową rolę | `\bodgrywa (?:kluczow\|istotn\|ważn\|znacząc\|niebagateln)\w* rolę\b` |
| klisza: kluczową rolę odgrywa | `\b(?:kluczow\|istotn\|ważn)\w* rolę odgrywa\b` |
| klisza: ma kluczowe/istotne znaczenie | `\bma (?:kluczowe\|istotne\|ogromne\|zasadnicze) znaczenie\b` |
| klisza: kluczowe znaczenie ma | `\b(?:kluczowe\|istotne\|ogromne) znaczenie ma\b` |
| klisza: stanowi integralną część/fundament | `\bstanowi (?:integraln\w+ część\|nieodłączn\w+ element\|fundament\|podstawę\|trzon\|filar)\b` |
| superlatyw: rewolucyjny/przełomowy/innowacyjny | `\b(?:rewolucyjn\|przełomow\|innowacyjn\|nowoczesn\|nowatorsk\|niezrównan\|bezprecedensow)\w+\b` |
| klisza: możliwości (są) nieograniczone | `\bmożliwości (?:są )?(?:praktycznie \|niemal \|wręcz )?(?:nieograniczone\|nieskończone)\b` |
| klisza: zmienia reguły gry | `\bzmienia reguły gry\b` |
| klisza: to dopiero początek/wierzchołek | `\bto dopiero (?:początek\|wierzchołek)\b` |
| klisza: w erze cyfrowej/AI | `\bw erze (?:cyfrow\|sztucznej inteligencji\|AI)\w*\b` |

### PL-RHET — PL — klasa: block / review

| Opis | Wzorzec (regex) |
|---|---|
| antyteza redefinicyjna: To nie X — to Y | `[Tt]o nie (?:jest )?.{1,40}[—–\-] to\b` |
| antyteza redefinicyjna: To nie X. To Y | `[Tt]o nie (?:jest )?.{1,40}\.\s+[Tt]o\b` |
| paralelizm: nie tylko… ale również | `\bnie tylko\b.{1,80}?\b(?:ale\|lecz)(?: również\| także\| i)?\b` |
| dychotomia: z jednej strony | `\bz jednej strony\b` |
| triada? | `\b(\w+), (\w+),? (?:i\|oraz) (\w+)\b` |
| rozpiętość: od X po Y | `\bod \w+(?:y\|ów\|i)? (?:po\|aż po) \w+` |

### PL-ANTI — PL — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| antyteza: X, a nie Y | `,\s+a nie\b` |
| antyteza inwersyjna: ..., nie Y (domknięcie) | `,\s+nie\s+\w+(?:\s+\w+)?(?=[.!?;\n]\|$)` |

### PL-HEDGE — PL — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| podwójny hedge: mogłoby… potencjalnie | `\b(?:mogłoby\|mógłby\|można by\|dałoby się)\b.{0,30}\b(?:potencjalnie\|ewentualnie\|w pewnym sensie)\b` |
| hedge: potencjalnie | `\bpotencjalnie\b` |
| hedge: wydaje się, że | `\bwydaje się, że\b` |
| hedge: zdaje się, że | `\bzdaje się, że\b` |
| hedge: warto byłoby rozważyć | `\bwarto byłoby rozważyć\b` |
| hedge: w pewnym sensie | `\bw pewnym sensie\b` |

### PL-TYPO — PL — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| nagłówek-klisza: Kluczowe wnioski / Podsumowanie | `(?m)^#{1,6}\s*(?:Kluczowe wnioski\|Najważniejsze (?:punkty\|wnioski\|informacje)\|Co dalej\??\|Podsumowanie\|Wnioski końcowe)\b` |

### EN-ANTI — EN — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| antythesis: not only/just… but | `\bnot (?:just\|only\|merely\|simply)\b.{1,80}?\b(?:but\|it'?s\|it is)\b` |
| antythesis: it's not X — it's Y | `\bit'?s not\b.{1,40}[—–\-]\s*it'?s\b` |
| antythesis: not X, but Y | `\bnot \w+, but \w+\b` |

### EN-TRIAD — EN — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| triad? | `\b(\w+), (\w+),? and (\w+)\b` |

### EN-PARA — EN — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| parallelism: self-X and self-Y | `\bself-\w+ and self-\w+\b` |
| parallelism: X-Y and A-B | `\b(\w+)-(\w+) and (\w+)-(\w+)\b` |

### EN-CLICHE — EN — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| EN klisza/signpost | `\b(?:it'?s worth noting\|worth noting that\|in today'?s (?:fast-paced\|ever-changing) world\|ever-evolving (?:landscape\|world)\|delve into\|delv(?:e\|ing)\|tapestry\|a testament to\|testament to\|navigate the complexities\|first-class\|seamless(?:ly)?\|robust\|leverag(?:e\|ing)\|spearhead(?:ed\|ing)?\|i am (?:confident\|excited\|thrilled\|passionate)(?: that\| to\| about)?\|passionate about\|at the end of the day\|the through-line\|game-?changer\|cutting-edge\|best-in-class\|state-of-the-art\|unlock(?:ing)?(?: the)? potential)\b` |

### EN-HEDGE — EN — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| hedge EN | `\b(?:arguably\|it could be argued\|to some extent\|one could say\|it may well be)\b` |

### EN-SUPER — EN — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| superlatyw EN | `\b(?:incredibly\|extremely\|truly\|remarkably\|highly\|exceptionally\|undoubtedly\|absolutely\|deeply)\b` |

### EN-CONCL — EN — klasa: review

| Opis | Wzorzec (regex) |
|---|---|
| signpost zamknięcia EN | `\b(?:in conclusion\|overall\|ultimately\|all in all\|in summary\|to sum up\|in essence\|when all is said)\b` |
<!-- RULES:END -->

---

## Indeks markerów (ściąga)

| ID | Język | Klasa | Opis jednolinijkowy |
|---|---|---|---|
| PL-SIGN | PL | review | Puste otwarcia i signposty („warto podkreślić", „zanurzmy się") |
| PL-CLICHE | PL | review | Frazy-wytrychy i superlatywy („kluczową rolę", „przełomowy") |
| PL-RHET | PL | block / review | Antyteza redefinicyjna (block), triady, paralelizm (review) |
| PL-ANTI | PL | block / review | Antyteza przeciwstawna „X, a nie Y" / „Y, nie X" (review), seria ≥3 (block) |
| PL-RHYTHM | PL | block / review | Nawał łączników (block ≥3), monotoniczny szyk SVO (review) |
| PL-HEDGE | PL | review | Hedging: tryb warunkowy + „potencjalnie", „wydaje się że" |
| PL-TYPO | PL | block / review | Em-dash ≥3/akapit (block), emoji w nagłówku (block), bold-overload (review) |
| EN-DASH | EN | block | Em-dash ≥3/akapit w tekście angielskim |
| EN-ANTI | EN | block / review | Antyteza „not X but Y" (review), seria antytez (block) |
| EN-TRIAD | EN | review | Triada „X, Y, and Z" |
| EN-PARA | EN | review | Paralelizm „self-X and self-Y", compound-adj pairs |
| EN-CLICHE | EN | review | Signposty i klisze AI: „delve", „robust", „passionate about" itp. |
| EN-HEDGE | EN | review | Hedging: „arguably", „to some extent", „one could say" |
| EN-SUPER | EN | review | Puste superlatywy: „incredibly", „truly", „undoubtedly" |
| EN-CONCL | EN | review | Signposty zamknięcia: „in conclusion", „ultimately", „to sum up" |
