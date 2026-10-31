# Wykrywanie błędów — pełny katalog wzorców

Wyniesione z `SKILL.md` (sekcja 3) w ramach progressive disclosure.

## 3. Wykrywanie Błędów — Ranking Priorytetów

### Priorytet 1: Cyrylica [A-Яa-яЁё]

**Regex:** `[А-Яа-яЁё]`

- Oznacza błąd adiustacji (rosyjskie znaki zamiast łacińskich w polskim tekście)
- Zawsze poprawiać — to nigdy nie jest celowe
- Typowe przypadki: `а` (cyrylica) zamiast `a` (łaciński), `о` zamiast `o`, `с` zamiast `c`
- Uwaga: mogą się pojawić całe słowa cyrylicą wklejone ze źródeł (np. `Память` zamiast `Pamięć`)

---

### Priorytet 2: Kalki Angielskie

| Błąd | Poprawna forma | Kontekst |
|---|---|---|
| detektujesz / detektować | **wykrywasz / wykrywać** | audyt, analiza |
| ekstraktować / ekstraktujesz | **wydobywać, pozyskiwać** | dane, informacja |
| implementować (poza IT) | **wdrażać, realizować, zastosować** | procesy, strategie |
| raportować (relacja) | **meldować, sprawozdawać** | komunikacja |
| raport (w znaczeniu rapport) | **więź, relacja, powiązanie** | interpersonalne |
| wizualny | **wzrokowy** (percepcja) | zmysły |
| audytywny / audialny | **słuchowy** | zmysły |
| manifestować | **przejawiać, wyrażać, objawiać** | cechy, objawy |
| konfrontować | **stawiać czoła, mierzyć się z** | wyzwania |
| triggerować | **wyzwalać, uruchamiać** | mechanizmy |
| compliance (ogólnie) | **zgodność, uległość** | wymogi |
| baseline (ogólnie) | **punkt odniesienia, stan początkowy** | pomiary |
| engage (z osobą) | **zaangażować, włączyć** | ludzie |
| feedback | **opinia, informacja zwrotna** | komunikacja |
| validować | **potwierdzać, weryfikować** | testy |
| konsystentny / konsystentnie | **spójny / spójnie** | opis, dane, zachowanie |
| rezonować (z kimś) | **współbrzmieć, trafiać do** | komunikacja, odbiorca |
| adresować (problem) | **zająć się, odnieść się do** | problemy, kwestie |
| dedykowany (= przeznaczony) | **przeznaczony, wydzielony** | zasoby, narzędzia |
| focusować się | **skupiać się, koncentrować się** | uwaga, zadanie |
| targetować | **celować w, kierować do** | osoby, grupy |
| priorytetyzować | **ustalać priorytety** | zadania, cele |
| eskalować (ogólnie) | **nasilać się, zaostrzać się** | sytuacje, konflikty |
| proaktywny | **aktywny, zapobiegawczy** | działanie |
| ewaluować | **oceniać, szacować** | wyniki, skuteczność |
| generować (poza IT) | **wytwarzać, powodować** | emocje, reakcje |
| finalizować | **kończyć, doprowadzać do końca** | procesy |
| aplikacja (= zastosowanie) | **zastosowanie** | poza IT |
| dla opisania / dla wyjaśnienia | **do opisu / do wyjaśnienia** | kalka z ang. *for describing* |
| cerebrospinalny | **mózgowo-rdzeniowy** | kalka z ang. *cerebrospinal*; pol. termin medyczny: PMR |
| kardiowasku­larny | **sercowo-naczyniowy** | kalka z ang. *cardiovascular* |
| muskuloskeletalny | **mięśniowo-szkieletowy** | kalka z ang. *musculoskeletal* |
| transceiver | **nadajnik-odbiornik** | pol. termin radiotechniczny |
| na jego własnych warunkach | **według jego własnych reguł** | kalka z ang. *on its own terms* |
| mirroring / lustrzenie | **odzwierciedlanie** | „lustrzenie" nie istnieje w SJP |
| insurgencja | **insurekcja, powstanie, rebelia** | kalka z ang. *insurgency*; „insurekcja" ma polską tradycję |
| post (w tekście ogólnym) | **wpis** | media społecznościowe |
| hashtag | **hasztag** | pisownia przyswojona, notowana przez PWN |
| feed | **tablica, kanał aktualności** | media społecznościowe |
| zgrywalizowany / gamifikowany | **przypominający grę** | poza tekstem specjalistycznym |

---

### Priorytet 3: Fałszywi Przyjaciele

| Błąd | Znaczenie angielskie | Poprawny polski |
|---|---|---|
| sensitivny | wrażliwy (sensitive) | **wrażliwy, czuły** |
| efektywnie (= effectively) | skutecznie | **skutecznie** (gdy chodzi o efekt, nie wydajność) |
| kooptować | przejąć (co-opt) | **przejąć, przeciągnąć na swoją stronę** |
| aktualnie (= actually) | w rzeczywistości | **właściwie, w rzeczywistości** |
| ewentualnie (= eventually) | w końcu, ostatecznie | **ostatecznie, w końcu** |
| sympatyczny (= sympathetic) | współczujący | **współczujący, pełen zrozumienia** |
| intencja (= intention, luźno) | zamiar | **zamiar, cel** (gdy nie jest termin prawniczy) |
| transparentny | przejrzysty (transparent) | **przejrzysty, jawny** |
| kompetentny (o rzeczy) | odpowiedni (competent) | **odpowiedni, właściwy** |
| agresywny (pozytywnie) | zdecydowany (aggressive) | **zdecydowany, intensywny** |
| dekada (= decade) | dziesięciolecie | **dziesięciolecie** (jeśli nie w kontekście muzycznym) |
| definitywnie (= definitely) | zdecydowanie | **zdecydowanie, bez wątpienia** |

**Uwaga**: Fałszywi przyjaciele wymagają analizy kontekstu. Samo wystąpienie słowa to jeszcze nie błąd — np. "aktualnie" w znaczeniu "obecnie" jest poprawne.

---

### Priorytet 4: Anglicyzmy z Polskim Odpowiednikiem

| Anglicyzm | Polski odpowiednik |
|---|---|
| pattern | **wzór, schemat, motyw** |
| mindset | **mentalność, nastawienie** |
| skillset | **zestaw umiejętności, kompetencje** |
| leverage (czasownik) | **wykorzystywać, operować** |
| insight | **spostrzeżenie, wgląd** |
| feedback loop | **pętla informacji zwrotnej** |
| framework (nie jako nazwa własna) | **ramy, struktura** |
| approach (w tekście mieszanym) | **podejście** |
| scaffolding (nie w IT) | **szkielet pojęciowy, ramy** |

**Wyjątek**: Jeśli anglicyzm jest nazwą własną (np. "Chase Hughes Framework"), zachowaj go.

#### Podtyp: Hybrydy angielsko-polskie

Angielski rdzeń z polską deklinacją/koniugacją. Nie są to zaadaptowane pożyczki — to formy ad hoc, które nie trafiły do słowników.

| Hybryda | Poprawna forma | Uzasadnienie |
|---|---|---|
| lesionami | **lezjami** | ang. *lesion* → pol. *lezja* (zaadaptowane); „lesion" + pol. -ami = hybryda |
| scrollować | **przewijać** | ang. *scroll* + pol. -ować |
| pushować | **wypychać, przesyłać** | ang. *push* + pol. -ować (poza git) |
| fetchować | **pobierać** | ang. *fetch* + pol. -ować (poza IT) |

**Test**: Czy słowo z polską końcówką istnieje w SJP/WSPP? Jeśli nie — szukaj zaadaptowanej formy lub polskiego odpowiednika.

---

### Priorytet 5: Sztuczne Kolokacje i Związki Frazeologiczne

**KLUCZOWA KATEGORIA** — najczęściej przeoczana, bo oba słowa z osobna są poprawne.

Zamiana anglicyzmu na polski odpowiednik NIE wystarczy. Trzeba sprawdzić, czy powstała kolokacja faktycznie funkcjonuje w polszczyźnie.

| Sztuczna kolokacja | Naturalny związek frazeologiczny | Źródło błędu |
|---|---|---|
| rusztowanie pojęciowe | **szkielet pojęciowy, ramy pojęciowe** | kalka z ang. *conceptual scaffolding* |
| zbiegać na wniosku | **prowadzić do wniosku** | „zbiegać się" wymaga „w punkcie", nie „na wniosku" |
| adresować problem | **zająć się problemem, odnieść się do problemu** | kalka z ang. *address a problem* |
| budować rapport | **budować więź** | *rapport* nie jest polskim słowem |
| przywileje sięgające ponad granicami | **wykraczające poza granice** | zły przyimek i przypadek |
| rozejść się echem | **odbić się (szerokim) echem, rozbrzmieć** | skażony frazeologizm |
| wyważyć błony | **przebić błony** | wyważa się drzwi, nie błony |
| uderzenie sądowe | **atak na drodze sądowej** | kalka z ang. *judicial attack* |
| zarażać lawiną informacji | **zarażać entuzjazmem, który niesie lawina** | zarażać można stanem, nie masą |
| hasztagi do wypromowania, frazy do wypromowania | **hasztagi do wylansowania, frazy do wypromowania** | powtórzenie w jednym wyliczeniu |
| odzwierciedlanie toczy spór | **odzwierciedlanie to spór** | personifikacja procesu: zjawisko nie wykonuje czynności osobowej |

**Procedura weryfikacji kolokacji:**
1. Po zamianie anglicyzmu na polski odpowiednik — przeczytaj pełne zdanie na głos
2. Zadaj pytanie: „Czy ktokolwiek naturalnie by tak powiedział?"
3. Jeśli wątpliwość — szukaj ustalonego związku frazeologicznego
4. Typowe pułapki:
   - Czasownik + przyimek: „zbiegać **na**" zamiast „prowadzić **do**"
   - Rzeczownik + przymiotnik: „rusztowanie **pojęciowe**" zamiast „szkielet **pojęciowy**"
   - Czasownik + rzeczownik: „budować **rapport**" zamiast „budować **więź**"

---

### Priorytet 6: Interpunkcja

Najczęstsza kategoria błędów ilościowo (często 50%+ wszystkich poprawek w pliku).

#### Obowiązkowy przecinek PRZED:

| Spójnik/zaimek | Przykład błędny | Poprawka |
|---|---|---|
| **który/która/które** | `odkrycie które doprowadziło` | `odkrycie, które doprowadziło` |
| **że** | `stwierdzał że mają` | `stwierdzał, że mają` |
| **żeby/aby** | `raport żeby odpowiedzieć` | `raport, żeby odpowiedzieć` |
| **gdy/kiedy** | `nie spodziewałem się gdy` | `nie spodziewałem się, gdy` |
| **co** (zaimek względny po „to") | `to co mierzalne` | `to, co mierzalne` |
| **do czego / o czym** (zaimek wzgl.) | `tam do czego mamy dostęp` | `tam, do czego mamy dostęp` |

#### Obowiązkowy przecinek w wyliczeniach z zaprzeczeniem:

| Przykład błędny | Poprawka |
|---|---|
| `transceiver nie źródło` | `transceiver, nie źródło` |
| `w celach praktycznych nie eksploracyjnych` | `w celach praktycznych, nie eksploracyjnych` |

**Regex skanowania** (główne wzorce):
```
\w+ któr[yaeąegomuychim]\b    → sprawdź czy jest przecinek przed
\w+ że \b                      → sprawdź czy jest przecinek przed
\w+ żeby \b                    → sprawdź czy jest przecinek przed
\w+ gdy \b                     → sprawdź czy jest przecinek przed
 to co \b                      → sprawdź czy jest przecinek między
```

---

### Priorytet 7: Błędy Stylu i Gramatyki

**Imiesłowy przymiotnikowe czynne tworzone od kalek:**
- Błędnie: "Osoba detektująca błąd"
- Poprawnie: "Osoba wykrywająca błąd"

**Strona bierna tam, gdzie naturalna jest czynna:**
- Błędnie: "Błąd jest detektowany przez audytora"
- Poprawnie: "Audytor wykrywa błąd"

**Zbędne nominalizacje:**
- Błędnie: "Przeprowadzanie procesu analizy"
- Poprawnie: "Analiza"

**Błędny szyk zdania (kalka SVO):**
- Błędnie: "Osoba wykonuje ruch. Osoba wykazuje stres. Osoba zmienia temat."
- Poprawnie: "Wykonuje ruch, wykazuje stres, zmienia temat." (naturalny szyk polski)

**Zawieszony przysłówek (kalka szyku angielskiego):**
W angielskim przysłówek często stoi po dopełnieniu. W polskim — przed rzeczownikiem, który modyfikuje.
- Błędnie: "przepływu informacji-energii **cyklicznie** między domenami"
- Poprawnie: "**cyklicznego** przepływu informacji-energii między domenami"
- Błędnie: "model świadomości **holistycznie** obejmujący całość"
- Poprawnie: "**holistyczny** model świadomości obejmujący całość"
- **Test**: Czy przysłówek modyfikuje czasownik, czy w rzeczywistości opisuje rzeczownik? Jeśli rzeczownik — zamień na przymiotnik i przenieś przed rzeczownik.

**Powtórzenia leksykalne w jednym zdaniu:**
- Błędnie: "**niewielkie** ablacje kory i stwierdzał, że mają **niewielki** wpływ"
- Poprawnie: "**drobne** ablacje kory i stwierdzał, że mają niewielki wpływ"
- **Reguła**: Jeśli to samo słowo (lub rdzeń) pojawia się 2× w jednym zdaniu i nie jest celowym powtórzeniem retorycznym — zamień jedno na synonim.
- Przykład z przekładu: „pokazywać swoje poglądy **polityczne** za pomocą **politycznych** banerów" → „za pomocą banerów".

**Podwójne „się" w sąsiedztwie** (linter: PL-NORMA):
- Błędnie: „Ruch sprzeciwia **się** trzymaniu **się** w cieniu"
- Poprawnie: „Ruch odrzuca trzymanie się w cieniu"

**Stopniowanie przymiotników absolutnych** (linter: PL-NORMA):
- Błędnie: „najbardziej elementarne reguły", „najbardziej optymalny", „bardziej unikalny"
- Poprawnie: „elementarne reguły", „optymalny", „unikalny"

**Dwuznaczna koordynacja po zdaniu względnym:**
- Błędnie: „trzeba wyszkolić użytkowników, którzy będą działać wspólnie, **i przechwycić** dynamikę" (kto przechwytuje?)
- Poprawnie: „trzeba wyszkolić użytkowników, którzy wspólnie wkroczą do gry i **przechwycą** dynamikę"
- **Test**: Czy bezokolicznik po przecinku i „i" da się jednoznacznie przypisać do podmiotu zdania nadrzędnego? Jeśli nie, przebuduj.

**Odmiana obcych imion i nazwisk:**
- Błędnie: „myśliciela **Antonio** Gramsciego" (nazwisko odmienione, imię nie)
- Poprawnie: „myśliciela **Antonia** Gramsciego". Włoskie imiona na *-o* odmieniamy jak „Henio": Antonio, Antonia, Antoniowi (Poradnia Językowa PWN, sjp.pwn.pl, hasło „Antonio", 2026-01-02).
- Forma nieodmieniona bywa odbierana jako „poprawniejsza", bo brzmi bliżej oryginału. To nadkorekta. Gdy autor lub zleceniodawca prosi o formę nieodmienioną, pokaż źródło normy i zostaw decyzję jemu; nie zgaduj w żadną stronę.

**Pusta zapowiedź w przekładzie:**
- Oryginał „Several aspects should be highlighted" nie usprawiedliwia „Warto podkreślić kilka aspektów". Przełóż treściowo: „Kilka spraw zasługuje tu na podkreślenie" albo od razu wylicz.

---

### Priorytet 8: Ortografia terminów łacińskich i greckich

Terminy naukowe zaadaptowane z łaciny/greki mają ustalone formy polskie. Błędy często dotyczą samogłosek.

| Błędna forma | Poprawna forma | Etymologia |
|---|---|---|
| homonkulus | **homunkulus** | łac. *homunculus* (drugie „u", nie „o") |
| encelafografia | **encefalografia** | gr. *enkephalos* |
| hipotalamus | **podwzgórze** (lub *hypothalamus* w kontekście ang.) | gr. *hypo* + *thalamos* |

**Procedura**: Przy terminach łacińskich/greckich — sprawdź pisownię w SJP/WSPP. Częsty błąd: zamiana samogłosek (*u↔o*, *e↔a*) przez analogię do angielskiej wymowy.

---

### Priorytet 9: Manieryzm AI (warstwa rozszerzona — PL+EN)

**Pełny kanon: `manieryzm-ai.md`.** Ta sekcja to skrót operacyjny; pełna taksonomia 14 kategorii
(z regexami, przykładami, poprawkami i progami) żyje w pliku referencyjnym
`~/.claude/skills/sztuczny-miodek/manieryzm-ai.md`. Deterministyczny pre-scan robi
`ai_linter.py` (patrz „Protokół dwuetapowy"). Przy audycie tekstu wczytaj `manieryzm-ai.md`.

Kategorie kanonu (te same ID w dok i linterze):

| ID | Język | Co łapie |
|---|---|---|
| PL-SIGN | PL | puste otwarcia/signposty („Warto podkreślić", „W dzisiejszych czasach", „Zanurzmy się") |
| PL-CLICHE | PL | frazy-wytrychy („odgrywa kluczową rolę", „rewolucyjny", „stanowi integralną część") |
| PL-RHET | PL | antyteza redefinicyjna „to nie X — to Y", paralelizm „nie tylko… ale również", triady, „z jednej… z drugiej strony" |
| PL-ANTI | PL | antyteza przeciwstawna bez myślnika: „X, a nie Y" / inwersja „Y, nie X" (generatorowe domknięcie); seria ≥3 = block |
| PL-RHYTHM | PL | monotonny szyk SVO, nawał łączników-otwarć („Ponadto/Co więcej/Dodatkowo") |
| PL-HEDGE | PL | hedging („mogłoby potencjalnie", „warto byłoby rozważyć") |
| PL-TYPO | PL | nadużycie myślnika, emoji w nagłówkach, bold-overload, nagłówki-klisze |
| EN-DASH | EN | em-dash overuse |
| EN-ANTI | EN | „not X, but Y" / „it's not X — it's Y" |
| EN-TRIAD | EN | rule-of-three („fast, reliable, and scalable") |
| EN-PARA | EN | balanced parallelism („self-documenting and self-checking") |
| EN-CLICHE | EN | „delve into", „testament to", „leverage", „seamless", „first-class", „I am excited to" |
| EN-HEDGE | EN | „arguably", „to some extent" |
| EN-SUPER | EN | puste superlatywy („incredibly", „truly", „remarkably") |
| EN-CONCL | EN | signposty zamknięcia („In conclusion", „Overall", „Ultimately") |

Skrót wzorców PL (artefakty maszynowe, które nie brzmią naturalnie po polsku):

| Wzorzec | Przykład błędny | Poprawna forma |
|---|---|---|
| Nadmierne hedgowanie | "Mogłoby to potencjalnie wskazywać..." | "To wskazuje na..." |
| Nienaturalna formalność | "Niniejszy dokument ma na celu..." | "Ten dokument opisuje..." |
| Powtarzalny szyk SVO | "Osoba wykonuje ruch. Osoba wykazuje stres." | "Wykonuje ruch. Wykazuje stres." |
| Nadużycie strony biernej | "Jest to obserwowane przez badacza" | "Badacz to obserwuje" |
| Zbędne wzmacniacze | "Bardzo istotne i niezwykle ważne" | "Kluczowe" |
| Nadmierne nominalizacje | "Przeprowadzanie procesu analizy danych" | "Analiza danych" |
| Błędny aspekt czasownika | "Wykrywać anomalię" (jednorazowo) | "Wykryć anomalię" |
| Złe przyimki (kalki) | "bazować na czymś" | "opierać się na czymś" |
| Sztuczne łączniki zdań | "Co więcej, dodatkowo, ponadto" (jeden po drugim) | Usuń nadmiarowe, zostaw jeden |
| Nadmierna grzeczność | "Warto byłoby rozważyć możliwość..." | "Rozważ..." |
| **Kalka redefinicyjna "to nie X — to Y"** | "Dziennik to nie refleksja — to kalibracja. Pomiar to nie ocena — to odczyt." (>3× na plik) | Zachowaj max 1-2 na plik. Reszta: zdanie twierdzące ("Dziennik kalibruje."), "=" ("Pomiar = odczyt stanu"), lub przeformułuj konstrukcję. |

**Kalka redefinicyjna** — szczegóły:
- Wzorzec: `[Rzeczownik] to nie [X] — to [Y]` lub `To nie jest [X]. To [Y].`
- Dlaczego to artefakt: AI nadużywa tej figury retorycznej jako "sztucznej epifanii" — czytelnik ma poczuć wgląd. Gdy jest 3+ razy na plik, efekt zanika i tekst brzmi jak manifest.
- **Regex detekcji:** `[Tt]o nie .{1,40}[—–-] to |[Tt]o nie .{1,40}\. [Tt]o `
- **Próg ilościowy:** max 1-2 na plik. Powyżej = popraw nadmiarowe.
- **Próg kontekstowy (ważniejszy):** nawet 1 wystąpienie wymaga poprawki, gdy kalka współwystępuje z innymi markerami AI (hedgowanie, sztuczny cytat, nienaturalna retoryka). Przykład: `„to nie jest magia — to jest fizyka, których jeszcze nie rozumiemy w pełni"` — kalka redefinicyjna + hedgowanie + pseudo-cytat = potrójny marker, popraw niezależnie od progu ilościowego.
- **Alternatywy:** zdanie twierdzące, konstrukcja z "=", metafora, pytanie retoryczne.

**Test praktyczny**: Przeczytaj fragment na głos. Jeśli brzmi jak tłumaczenie maszynowe albo jak podręcznik biurokracji — wymaga poprawki.

---

### Priorytet 10: Typografia

| Błąd | Poprawka | Kontekst |
|---|---|---|
| "cytat" (ang. cudzysłów) | **„cytat"** (pol. cudzysłów) | w tekście polskim |
| 'cytat' (ang. pojedynczy) | **'cytat'** lub **«cytat»** | zagnieżdżone cytaty |

**Wyjątek**: W blokach kodu, w angielskich cytatach i w polach technicznych — zachowaj oryginalne znaki.

#### Skład (PDF, druk) — dwie usterki, których nie widać w Markdownie

| Błąd | Poprawka | Kontrola |
|---|---|---|
| Sierotka: jednoliterowy spójnik lub przyimek (a, i, o, u, w, z) na końcu wiersza | Twarda spacja U+00A0 po takim wyrazie, wstawiana przed składem | `pdftotext plik.pdf - \| grep -cE ' (i\|w\|z\|a\|o\|u)$'` → 0 |
| Automatyczne dzielenie wyrazów rozcina złożenia w złym miejscu („po-pkulturę"); słowniki dzielenia (pyphen w WeasyPrint, CSS `hyphens:auto`) nie znają polskich złożeń | Przy wyrównaniu do lewej wyłącz dzielenie (`hyphens: manual`). Przy justowaniu przejrzyj każde przeniesienie | `pdftotext plik.pdf - \| grep -E '[a-ząćęłńóśźż][-‐]$'` → przejrzyj każde trafienie |

---

