# System One / Jev-Compatible Typed Decision DSL and Model Profiles
## wellmanifest.system-one.nl-uri-dsl-llm / v1

- **Standard**: `wellmanifest/nl-uri-dsl-llm`
- **Specification ID**: `system-one-decision-v1`
- **Profile Status**: `normative-profile`
- **Revision**: `1.5.0`
- **Date**: `2026-10-24`
- **Applicable Domains**: `dockuri`, `heyasa`, `willmux`, `nl-dsl-llm`, `policy-dsl`, `ssot`, `nohardcode`

---

## 1. Wprowadzenie i Ramy Architektoniczne

Niniejsza specyfikacja rozszerza standard **`wellmanifest/nl-uri-dsl-llm`** o normatywny profil **System One / Jev-Compatible Typed Decision (`system-one-decision-v1`)**, który zastępuje powolną, autoregresyjną generację tekstu swobodnego przez modele LLM **jednoprzebiegowym (single-pass) podejmowaniem typowanych decyzji (`choice`, `score`, `noul`)** bezpośrednio nad katalogiem procesów **DockURI (`proc://`, `dockuri://`)** oraz kanonicznych adresów **RFC 3986 Action URI**.

Architektura integruje zasady **`wellmanifest/nohardcode`**, **`wellmanifest/ssot`**, **`wellmanifest/dsl`** oraz **`wellmanifest/policy-dsl`**, standaryzując kontrakt wywołań i odpowiedzi dla 10 rodzin otwartych modeli decyzyjnych klasy System One / Jev:

1. **Clef / Clef-flash** (`Cloudflare`, `Qwen3.8-27B` / `Qwen3.5-9B`, `Apache-2.0`) — multimodalne modele decyzyjne (`text`, `json`, `image`, `video`) ze wspólną głowicą schematu (*joint schema head*) oceniającą pytania `choice`, `score` i `noul` w jednym przebiegu (*one forward pass*), kompatybilne z Jev i System One (Workers AI oraz lokalnie z Hugging Face).
2. **GLiNER2.5-Decide** (`Fastino`, `340M DeBERTa-v3-large`, `Apache-2.0`) — kompaktowy enkoder klasyfikujący CPU/GPU z obsługą wielu głowic decyzyjnych jednocześnie oraz natywnymi więzami międzypolowymi (*cross-question constraints*), osiągający 60.2% dokładności *exact-match* w ewaluacji 17-domenowej.
3. **Laya** (`322M multilingual` / `421M EN` / `421M typed-decisions`, `Apache-2.0`) — nieautoregresyjny silnik System One z wbudowanym routerem językowym (ponad 100 języków w tym PL i EN), zwracający rozkłady prawdopodobieństwa dla `choice`, `score` i `noul` w jednym przebiegu (0.766 średniej dokładności na 9 zadaniach).
4. **Kev** (`0.8B`, `4B`, `9B`, `27B` na bazie `Qwen3.5` / `Qwen3.8`, `Apache-2.0`) — rodzina trenowalnych modeli z serwerem HTTP zgodnym z formatem żądań TypeSafe System One (0.889 średniej dokładności dla `Kev-4B`).
5. **Laya-MLX** (`Apple Silicon MLX / Core ML`, `Apache-2.0`) — niezależny runtime MLX i Core ML dla wag Laya na układach serii M (mediana latencji 7.4 ms dla modelu wielojęzycznego i 13.4 ms dla angielskiego).
6. **SemIf** (`Qwen3.5-4B` / `MiniCPM5-2B` / `Qwen3.8-27B-EXL3` + `WebGPU`, `MIT`) — bezpośredni odczyt logitów opcji z otwartych modeli językowych bez generacji tekstu, ze współdzielonym prefetchem stanu aplikacji (*state prefetch*) i kalibracją temperatury per obciążenie (56.4% dokładności w teście 17-domenowym).
7. **NanoJev** (`0.6B Qwen3-0.6B`, `MIT`) — równoległy model decyzyjny wyuczony na zadaniach sterowania i gier decyzyjnych, zwracający pełny rozkład prawdopodobieństwa dla **2 do 255 dynamicznych kandydatów akcji** dostarczanych w czasie wywołania.
8. **Bespoke Nimble** (`Bespoke-Nimble-9B` na bazie `Qwen3.5-9B`, `Apache-2.0`) — model typowanych decyzji obsługujący do 255 opcji wyboru, wartości logiczne i poziomy rubryk ocen w oknie kontekstowym 8 192 tokenów, z opublikowanym przepisem treningowym SFT + GRPO.
9. **jevlike** (`Byte Embeddings` / zamrożony `Qwen2.5-0.5B`, `MIT`) — kompaktowy skorer kandydatów oparty o *cross-attention*, w którym każda opcja kandydująca odpytuje zakodowany stan aplikacji.
10. **jevos** (`jevos-v3`, `OpenVINO 8-bit CPU` / `GGUF llama.cpp`, `Apache-2.0`) — natywna binarka CPU-first wystawiająca protokół TypeSafe Jev dla `noul`, `choice` i `score` (86.5% na wewnętrznym benchmarku Jev, ok. 500 MB RAM na CPU).

```text
┌────────────────────┐      ┌──────────────────────────┐      ┌────────────────────────────┐
│ Stan Aplikacji +   │ ───> │  System One / Jev Engine │ ───> │  Jednoprzebiegowa Decyzja  │
│ Zapytanie NL (PL)  │      │ (Clef/Laya/Kev/NanoJev)  │      │  choice + score + noul     │
└────────────────────┘      └────────────┬─────────────┘      └─────────────┬──────────────┘
                                         │                                  │
                                         ▼                                  ▼
                            ┌──────────────────────────┐      ┌────────────────────────────┐
                            │ Katalog Kandydatów URI   │      │   Więzy Policy-DSL         │
                            │ DockURI proc:// (2..255) │      │ (CrossQuestionConstraint)  │
                            └──────────────────────────┘      └─────────────┬──────────────┘
                                                                            │
                                                                            ▼
                                                              ┌────────────────────────────┐
                                                              │ Wywołanie Procesu DockURI  │
                                                              │ proc://<project>/<op>      │
                                                              └────────────────────────────┘
```

---

## 2. Normatywne Reguły Jakości (NUL-019 .. NUL-022)

### NUL-019 (Single-Pass Typed URI Decision Without Free-Form Generation)
Silniki decyzyjne tłumaczące zapytania NL i stan aplikacji na wywołania procesów DockURI (`proc://`, `dockuri://`) oraz Action URI **MUSZĄ**:
1. Formułować decyzję jako ustrukturyzowany wektor pytań typowanych (`choice`, `score`, `noul`) ocenianych w jednym przebiegu (*single forward pass*) bez autoregresyjnego generowania swobodnego tekstu:
   - `choice`: wybór kanonicznego, hierarchicznego adresu **Action URI** (`scheme://authority/path[?query]` zgodnego z gramatyką `^[a-z][a-z0-9+.-]*://[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*(?:\?[A-Za-z0-9_.,=&%+-]+)?$`, bez spacji i pustych segmentów ścieżki) spośród dynamicznego zbioru **od 2 do 255 kandydatów** wyekstrahowanych z katalogu `dockuri/proc-v1` lub rejestru `ProcessUriRegistry`,
   - `score`: dyskretna ocena ryzyka operacyjnego na skali rubrykowej `1..3` (opcje `"1"`, `"2"`, `"3"` oraz wynik całkowity `1 | 2 | 3`),
   - `noul`: binarna bramka bezpieczeństwa, autonomii i braku negacji (`true` / `false`).
2. Zwracać znormalizowany rozkład prawdopodobieństwa ($\sum P(o_i) = 1.0$) dla wszystkich dozwolonych opcji każdego pytania.

### NUL-020 (Cross-Question Policy-DSL Constraint Enforcement)
Wieloheadowe odpowiedzi modelu System One **MUSZĄ** podlegać deterministycznym więzom międzypolowym (`CrossQuestionConstraint`) zgodnym ze standardem `wellmanifest/policy-dsl`:
1. Jeżeli głowica `noul` (`execution_allowed`) zwróci wartość `false` (np. wskutek wykrycia wyraźnej negacji w poleceniu użytkownika: *"nie uruchamiaj"*, *"don't execute"* lub blokady bezpieczeństwa), więz `POLICY-NOUL-NEGATION-BLOCKS-EXECUTION` **MUSI** zablokować automatyczne wykonanie wybranego URI niezależnie od pewności głowicy `choice`.
2. Jeżeli głowica `score` (`risk_score`) przekracza próg dopuszczalny dla aktywnego trybu autonomii (`suggest` lub `confirm`), więz `POLICY-AUTONOMY-*-GATE` **MUSI** wymusić potwierdzenie użytkownika (`execution_allowed = false`, `blocked_by_constraint = true`).
3. Więzy `restrict_options` mogą zawężać zbiór dopuszczalnych kandydatów `choice` i dokonywać ponownej normalizacji rozkładu prawdopodobieństwa przed wyborem końcowego URI.

### NUL-021 (SSOT Catalog of 10 Open-Source Jev / System One Model Families)
Każda implementacja routera System One **MUSI** utrzymywać pojedyncze źródło prawdy (`wellmanifest/ssot`) opisujące wszystkie 10 rodzin modeli (`clef`, `gliner2.5-decide`, `laya`, `kev`, `laya-mlx`, `semif`, `nanojev`, `bespoke-nimble`, `jevlike`, `jevos`), zawierające co najmniej:
- identyfikator profilu (`id`) oraz rodzinę (`family`),
- licencję (`Apache-2.0` lub `MIT`), rozmiar modelu w miliardach parametrów (`params_b`) i architekturę bazową (`backbone`),
- obsługiwane typy pytań (`choice`, `score`, `noul`), modalności (`text`, `json`, `image`, `video`), języki (`pl`, `en`, `multilingual`),
- obsługiwane środowiska wykonawcze (`workers-ai`, `cuda`, `cpu`, `mlx`, `coreml`, `openvino-cpu`, `gguf-llamacpp`, `webgpu`, `http-system-one`) oraz maksymalną liczbę kandydatów (`max_candidates`, do 255).

### NUL-022 (Dynamic Telemetry and Language-Aware Model Profile Routing)
Zgodnie ze standardem `wellmanifest/nohardcode`, wybór aktywnego profilu modelu System One **NIE MOŻE** być zahardkodowany na stałe w logice biznesowej:
1. Router profilu (`select_decision_profile`) **MUSI** dobierać model dynamicznie na podstawie:
   - zmiennych środowiskowych (`HEYASA_DECISION_MODEL`, `DOCKURI_DECISION_MODEL`, `WILLMUX_DECISION_MODEL`, `NL_DSL_MODEL`),
   - modalności wejścia (`image` / `video` $\rightarrow$ `clef-flash` lub `clef`),
   - wymogu współdzielonego prefetchu stanu aplikacji (`require_state_prefetch` $\rightarrow$ `semif`),
   - telemetrii sprzętowej hosta (`Darwin + arm64` $\rightarrow$ `laya-mlx`; `CUDA GPU` $\rightarrow$ `kev` lub `clef-flash`; `CPU-only`),
   - języka zapytania oraz liczby kandydatów (`> 64` kandydatów na CPU $\rightarrow$ `nanojev`; język `pl`/`multilingual` $\rightarrow$ `laya`; język `en` $\le 128$ opcji $\rightarrow$ `gliner2.5-decide`; ultraniskie zużycie RAM na CPU $\rightarrow$ `jevos`).
2. W przypadku braku zdalnego serwera HTTP System One (`SYSTEM_ONE_ENDPOINT`), silnik **MUSI** zapewnić deterministyczny, bezgeneracyjny skorer lokalny (*zero-generation local logit/affinity scorer*) zachowujący identyczny kontrakt schematu `wellmanifest.system-one-decision/v1`.
