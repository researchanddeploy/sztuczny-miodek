# Kanoniczna taksonomia manieryzmu AI

Plik opisuje 14 kategorii AI-manieryzmu wykrywanych przez skill `sztuczny-miodek`. Jest lustrem `ai_linter.py` — każde ID kategorii w tym dokumencie odpowiada identycznemu ID w linterze. Przy rozbieżności między dokumentem a linterem ten plik jest źródłem prawdy; linter należy zaktualizować.

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

**Wzorce techniczne (regex, Python `re.IGNORECASE | re.UNICODE`):**
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

### PL-NORMA — norma językowa w przekładzie (klasa: review)

Nie jest to manieryzm AI, tylko naruszenia normy, które przekład z angielskiego (ludzki
i maszynowy) produkuje seryjnie. Linter łapie wersje dające się opisać regexem; reszta
kategorii (łączliwość, personifikacja procesu) wymaga osądu, zob. `references/wykrywanie-bledow.md`.

| Wzorzec | Przykład błędny | Poprawka |
|---|---|---|
| stopniowanie przymiotnika absolutnego | najbardziej elementarnych reguł | elementarnych reguł |
| podwójne „się" | sprzeciwia się trzymaniu się w cieniu | odrzuca trzymanie się w cieniu |
| kalka *on its own terms* | przechwycić algorytm na jego własnych warunkach | grając według jego własnych reguł |
| uszkodzony frazeologizm | rozejść się echem | odbić się echem, rozbrzmieć |
| fałszywy przyjaciel | w minionej dekadzie | w minionym dziesięcioleciu |

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

## Warstwa konstrukcyjna

### PL-STRUKT — budowa zdania i akapitu (klasa: `strukt`, własna metryka)

Wszystko powyżej to czarna lista fraz: łapie słowa, nie konstrukcję. Ta warstwa mierzy,
jak zdanie jest zbudowane, i dlatego działa na tekstach, które nie użyły ani jednej
klisze z katalogu, a mimo to brzmią generatorowo.

Uzasadnienie z pomiaru autora: w pomiarze
między modelami sama czarna lista słów obniżyła slop o 3–40% (niestabilnie), a nadanie
modelowi systemu budowy zdania o 43–74% na każdym testowanym modelu.

| Kategoria | Próg | Co wykrywa |
|---|---|---|
| `zdanie>25w` | >25 słów | Zdanie-wielopiętrowiec. STE: 20 dla instrukcji, 25 dla opisu; polski dostaje 25, bo fleksja wydłuża |
| `akapit>6zd` | >6 zdań | Akapit bez jednego tematu |
| `strona_bierna` | każde | „zostać" + imiesłów bierny („raport został przygotowany") |
| `nominalizacja` | każde | Czasownik lekki + rzeczownik odsłowny („dokonał analizy" zamiast „przeanalizował"), „w celu przedstawienia" |
| `imieslow_seria` | ≥2 w zdaniu | Nawał imiesłowów na `-ąc`/`-wszy` („uwzględniając…, biorąc pod uwagę…") |

**Świadome ograniczenie zakresu:** strona bierna łapie wyłącznie konstrukcję z „zostać",
a nie „jest + imiesłów". W polskim „jest znany", „jest ważny" i „jest zbudowany" są
nierozróżnialne regexem, więc szerszy wzorzec produkowałby głównie fałszywe trafienia.
Ta sama pułapka wywróciła linter źródłowy eksperymentu STE, gdzie regex `is \w+ed`
liczył „is red" jako stronę bierną, a strona bierna była tam największą kategorią wyniku.

**Metryka:** `strukt/100w = naruszenia × 100 / słowa prozy`. Liczona osobno od gęstości
frazowej, bo obie skale są nieporównywalne. Proza wyłącznie: bez kodu, tabel, list,
nagłówków i cytatów.

**Kalibracja progu (2026-07-28):** prywatny korpus autora (50 plików reguł roboczych uznanych
za wzorcową polszczyznę) daje medianę 1,14 i maksimum 1,92. Tekst rozwlekły w tym samym
sensie: 14,55. Próg 4,0 leży ponad dwukrotnie nad najgorszym dobrym plikiem i daleko pod
złym. Przy zmianie zestawu reguł przelicz rozkład zamiast zgadywać.

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

### FAIL (konstrukcja)
- `strukt/100w > 4,0` — naruszenia budowy zdania na 100 słów prozy (PL-STRUKT).
- Niezależne od gęstości frazowej: tekst bez ani jednej klisze z katalogu może wpaść tu i tylko tu.

### PASS
Tylko gdy 0 blokerów, gęstość ≤ 8 i `strukt/100w` ≤ 4,0. Po korekcie każdy nierozwiązany
flag = brak PASS.

### Format wyjścia lintera

Manifest (1 linia / trafienie):
```
plik:linia:ID:KLASA:dopasowany_fragment
```

Blok podsumowania:
```
== SUMMARY ==
plik | słowa | trafienia | em-dash/akapit(max) | gęstość/500 | strukt/100w | blokery | WERDYKT
```

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
| PL-NORMA | PL | review | Norma w przekładzie: stopniowanie absolutnych, podwójne „się", „na własnych warunkach", „rozejść się echem", „dekada" |
| EN-DASH | EN | block | Em-dash ≥3/akapit w tekście angielskim |
| EN-ANTI | EN | block / review | Antyteza „not X but Y" (review), seria antytez (block) |
| EN-TRIAD | EN | review | Triada „X, Y, and Z" |
| EN-PARA | EN | review | Paralelizm „self-X and self-Y", compound-adj pairs |
| EN-CLICHE | EN | review | Signposty i klisze AI: „delve", „robust", „passionate about" itp. |
| EN-HEDGE | EN | review | Hedging: „arguably", „to some extent", „one could say" |
| EN-SUPER | EN | review | Puste superlatywy: „incredibly", „truly", „undoubtedly" |
| EN-CONCL | EN | review | Signposty zamknięcia: „in conclusion", „ultimately", „to sum up" |
| PL-STRUKT | PL | strukt | Budowa: długie zdanie/akapit, strona bierna z „zostać", nominalizacja, seria imiesłowów. Własna metryka `strukt/100w`, próg 4,0 |
