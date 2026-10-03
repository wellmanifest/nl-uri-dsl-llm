# wellmanifest/nl-uri-dsl-llm

**Standard architektury trójwarstwowej: Natural Language (NL) → Action URI / Resource URN (DSL) → LLM Code Generation → Taskand Capsule Execution.**

HOME: `wellmanifest`  
STATUS: `standard-v1.0`  
POWIĄZANE STANDARDY: [`wellmanifest/nl-dsl-llm`](../nl-dsl-llm), [`wellmanifest/uriprocess`](../uriprocess), [`wellmanifest/taskand`](../taskand), [`wellmanifest/dsl`](../dsl)

---

## 1. Wprowadzenie i Cel Standardu

Standard `nl-uri-dsl-llm` definiuje deterministyczny, odporny na halucynacje łańcuch przetwarzania poleceń w języku naturalnym (NL) na operacje systemowe, kod i zadania orkiestrowane przez silniki autonomii (np. Koru, Paxlet, Tellmesh, Subactor) za pośrednictwem środowiska wykonawczego `taskand`.

```text
┌─────────────────┐       ┌──────────────────────┐       ┌────────────────────────┐
│  Mowa / Tekst   │ ────> │   Natywny Dispatch   │ ────> │   Process URI / URN    │
│  (NL: PL / EN)  │       │ (Levenshtein/Regex)  │       │ (RFC 3986 Action URI)  │
└─────────────────┘       └──────────────────────┘       └───────────┬────────────┘
                                                             │ Fallback
                                                             ▼
                                                 ┌────────────────────────┐
                                                 │      LLM + GBNF        │
                                                 │ (Grammar-Constrained)  │
                                                 └───────────┬────────────┘
                                                             │
                                                             ▼
                                                 ┌────────────────────────┐
                                                 │   Taskand / Sandbox    │
                                                 │   Capsule Execution    │
                                                 │  (Docker / CDP / CLI)  │
                                                 └────────────────────────┘
```

---

## 2. Warstwy Architektury

### 2.1. Warstwa Wejścia: Natural Language (NL)
- Obsługa języka polskiego i angielskiego.
- Normalizacja tekstu z usunięciem znaków diakrytycznych (`ą, ć, ę, ł, ń, ó, ś, ź, ż` → ASCII).
- Odporność na literówki poprzez ograniczoną metrykę odległości edycyjnej (Levenshtein Distance <= 2).

### 2.2. Warstwa Kanoniczna: Action URI oraz Resource URN (DSL)
Zamiast swobodnego formatu YAML/JSON podatnego na błędy składniowe, każda akcja i zasób są jednoznacznie adresowane:
1. **Action URI**:
   ```
   scheme://domain/action[?query_params]
   ```
   *Przykłady*:
   - `koru://loop/stop`
   - `koru://queue/task/claim?ticket_id=338`
   - `sandbox://run?image=python:3.11-slim`
   - `browser://navigate?url=https://example.com`

2. **Resource URN**:
   ```
   urn:domain:resource_type:resource_id
   ```
   *Przykłady*:
   - `urn:koru:ticket:338`
   - `urn:taskand:capsule:7cb3ea7c`

3. **Format hybrydowy zapisu strumieniowego**:
   ```text
   uri: scheme://domain/action {"param": "value"}
   ```

### 2.3. Warstwa Tłumaczenia LLM z Gramatyką GBNF
W przypadku poleceń złożonych, wykraczających poza lokalny słownik regułowy:
- Rejestr akcji (`ProcessUriRegistry`) dynamicznie generuje gramatykę GGML BNF (**GBNF**).
- Model LLM (lokalny w llama.cpp/Ollama lub zdalny) generuje tokeny **wyłącznie** pod dyktando gramatyki, uniemożliwiając halucynowanie nieistniejących endpointów czy błędnych struktur JSON.

### 2.4. Warstwa Wykonawcza: Taskand Capsule & Sandbox Runner
Wygenerowany i zwalidowany Process URI trafia do kapsuły wykonawczej standardu `wellmanifest/taskand`:
- **Docker Sandbox Runner**: Izolacja kontenerowa z ograniczeniami zasobów (`--memory=512m`, `--cpus=1.0`, `--network=none`).
- **CDP Browser Controller**: Sterowanie przeglądarką Chromium poprzez JSON-RPC DevTools Protocol.
- **Fail-Closed Contract**: Kod wyjścia `0` = sukces, `1` = błąd wykonania, `2` = naruszenie kontraktu.

---

## 3. Normatywna Polityka Jakości (Reguły NUL-001..006)

- **`NUL-001 (Deterministic First)`**: System musi najpierw podjąć próbę deterministycznego sparsowania intencji lokalnie (Levenshtein/Regex); zapytanie do LLM jest dozwolone wyłącznie jako fallback.
- **`NUL-002 (RFC 3986 Conformance)`**: Każde legalne polecenie DSL musi być poprawnym Action URI lub Resource URN zgodnie z RFC 3986.
- **`NUL-003 (Grammar Constraint)`**: Każde zapytanie do LLM kompilujące NL na Process URI musi być obwarowane wygenerowaną gramatyką GBNF lub schematem JSON.
- **`NUL-004 (Parameter Schema Validation)`**: Przed przekazaniem do wykonawcy parametry URI muszą przejść walidację JSON-Schema zarejestrowaną w `ProcessUriRegistry`.
- **`NUL-005 (Sandbox Isolation)`**: Operacje zewnętrzne (`sandbox://`, `pypi://`) muszą być domyślnie izolowane procesowo lub kontenerowo (`--network=none` lub dedykowany worktree v5).
- **`NUL-006 (Closed-Loop Receipt)`**: Każde wykonanie musi wyemitować raport ze statusem i artefaktami powiązanymi z identyfikatorem biletu / zasobu URN.

## Optional semantic profile

[Semantic multilingual URI DSL](spec/SEMANTIC_NL_PLAN.md) replaces NL word rules within the explicitly selected `semantic-v1` profile. [Machine profile](profiles/semantic-v1.json) adopts the shared validated plan envelope; legacy exact DSL and PL/EN behavior remain compatible. This is a candidate extension until independent protected publication and pinned adoption.

Version 1.1 adds the optional [typed URI/URN exchange profile](spec/SEMANTIC_NL_PLAN.md#optional-process-exchange-profile-version-1).
Its JSON Schema is embedded under `exchange.schema` in the machine profile.
It binds data UUID URNs and digests to a process URI, request/result correlation,
governed workspace context and truthful outcomes. Admission remains an actual
protected-controller decision; the schema and identifiers grant no authority.
Runtime adoption and an observed execution canary are required separately.
