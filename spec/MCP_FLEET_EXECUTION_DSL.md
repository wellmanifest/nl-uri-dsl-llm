# MCP Process Gateway, Fleet Batch Execution, and LLM Cost Attribution Profile
## wellmanifest.mcp-fleet.nl-uri-dsl-llm / v1

- **Standard**: `wellmanifest/nl-uri-dsl-llm`
- **Specification ID**: `mcp-fleet-dsl-v1`
- **Profile Status**: `normative-profile`
- **Revision**: `1.4.0`
- **Date**: `2026-10-11`
- **Applicable Domains**: `mcp`, `fleet`, `multi-gitter`, `diagit`, `search`, `openrouter`, `governance`

---

## 1. Wprowadzenie i Ramy Architektoniczne

Niniejsza specyfikacja rozszerza standard **`wellmanifest/nl-uri-dsl-llm`** o normatywny most do protokołu **Model Context Protocol (MCP)**, zunifikowane zarządzanie hurtowym wykonywaniem poleceń na flocie repozytoriów (**Fleet Batch Execution**) oraz bezwzględny ład tożsamości i atrybucji kosztów modeli LLM (**LLM Cost Attribution & Identity Mandate**).

W nowoczesnych środowiskach agentowych (Antigravity, Claude Desktop, Cursor, Koru, Willman, Paxlet) LLM nie wykonuje bezpośrednich poleceń powłoki w sposób nieograniczony. Protokół MCP stanowi ustandaryzowaną warstwę narzędziową JSON-RPC 2.0, w której schematy wejściowe (`inputSchema`) pełnią rolę wiążących barier ant-halucynacyjnych, a wywołania `tools/call` przekładane są deterministycznie na kanoniczne adresy RFC 3986 Action URI.

Jednocześnie operacje hurtowe obejmujące setki repozytoriów (np. masowe aktualizacje zależności przez `multi-gitter` czy skanowanie bezpieczeństwa przez `subactor-search`) wymagają bezwzględnej izolacji strumienia dialogu (NUL-007), obowiązkowej weryfikacji przedwykonawczej (`--dry-run`) oraz znormalizowanych kwitów odbiorczych URN.

```text
┌─────────────────┐       ┌──────────────────────┐       ┌────────────────────────┐
│  Mowa / Tekst   │ ────> │      MCP Gateway     │ ────> │   Process URI / URN    │
│  (NL: PL / EN)  │       │ (JSON-RPC tools/call)│       │ (RFC 3986 Action URI)  │
└─────────────────┘       └──────────┬───────────┘       └───────────┬────────────┘
                                     │                               │
                                     ▼                               ▼
                          ┌──────────────────────┐       ┌────────────────────────┐
                          │  inputSchema / GBNF  │       │   Fleet Batch Runner   │
                          │ (Anti-Hallucination) │       │ (Multi-Gitter/Diagit)  │
                          └──────────────────────┘       └───────────┬────────────┘
                                                                     │
                                                                     ▼
                                                         ┌────────────────────────┐
                                                         │ Fleet Execution Receipt│
                                                         │ (URN + JSON Envelope)  │
                                                         └────────────────────────┘
```

---

## 2. Normatywne Reguły Jakości (NUL-015 .. NUL-018)

### NUL-015 (Model Context Protocol Process Gateway Conformance)
Wszelkie interfejsy narzędziowe wystawiane dla autonomicznych agentów AI za pośrednictwem protokołu Model Context Protocol (MCP) **MUSZĄ**:
1. Eksponować schematy wejściowe w formacie JSON Schema Draft-2020-12 lub Draft-07, ograniczając przestrzeń argumentów wyłącznie do typowanych parametrów akcji.
2. Odwzorowywać wywołania narzędzi (`tools/call`) na kanoniczne RFC 3986 Action URI (`search://...`, `diagit://...`, `fleet://...`).
3. Ściśle przestrzegać reguły czystości strumienia konwersacyjnego (NUL-007): odpowiedź narzędzia MCP zwraca zwięzłe podsumowanie oraz unikalny identyfikator URN kwitu (`urn:<domain>:<subdomain>:<id>`). Surowe wyjście procesowe (stdout/stderr) trafia wyłącznie do dedykowanych logów artefaktowych i nie może zalewać okna dialogowego agenta.
4. Obsługiwać transport stdio (jedna ramka JSON-RPC na linię UTF-8) lub Server-Sent Events (SSE).

### NUL-016 (Fleet Multi-Repository Batch Dry-Run and Execution Receipt Mandate)
Operacje hurtowe modyfikujące wiele repozytoriów w danej organizacji lub w całej flocie:
1. **Obowiązkowy tryb symulacji (`--dry-run`)**: Każde narzędzie wykonawcze floty (`diagit multi-gitter`, `fleet://exec`) musi bezwzględnie wspierać flagę `--dry-run`, pozwalającą na pełną weryfikację wpływu operacji bez modyfikacji plików i tworzenia commitów.
2. **Kwit wykonawczy zgodny ze schematem**: Każde wykonanie zbiorcze MUSI wyemitować ustrukturyzowany kwit zgodny ze schematem `wellmanifest.fleet-execution-receipt/v1` (i implementacją `diagit.fleet_execution/v1`), zawierający: `root`, `total_repositories`, `modified_repositories`, `failed_repositories`, `dry_run`, `script` oraz listę wyników per-repozytorium z kodami wyjścia i gałęziami roboczymi.
3. **Higiena gałęzi i worktree**: Wszelkie zmiany mutujące kod floty muszą być izolowane w dedykowanych gałęziach lub katalogach roboczych (`.worktrees/ticket-NNN--...`).

### NUL-017 (Fleet Dependency Health & Impact Classification Mandate)
Narzędzia audytu i analizy zależności we flocie projektów (`search://fleet/dependencies/outdated`):
1. **Klasyfikacja wpływu semantycznego**: Każda wykryta przestarzała zależność musi być jednoznacznie skategoryzowana:
   - `major`: potencjalnie przełamująca zmiana semantyczna (breaking change, zmiana API),
   - `minor`: wstecznie kompatybilne nowe funkcjonalności,
   - `patch`: wstecznie kompatybilne poprawki błędów i bezpieczeństwa.
2. **Odporność i praca offline**: Skanery zależności floty muszą implementować lokalną pamięć podręczną (TTL cache) metadanych pakietów oraz flagę `--offline`, umożliwiając audyt środowisk bez dostępu do sieci.

### NUL-018 (LLM Cost Attribution and Application Identity Mandate)
Wszelkie procesy, usługi i agenci komunikujący się z zewnętrznymi dostawcami i pośrednikami modeli LLM (np. OpenRouter):
1. **Obowiązkowa tożsamość aplikacji**: Aplikacja **MUSI** deklarować tożsamość poprzez zmienne środowiskowe `OPENROUTER_APP_NAME` (z automatycznym fallbackiem do nazwy katalogu repozytorium w przypadku braku) oraz `OPENROUTER_APP_URL` lub `OPENROUTER_SITE_URL`.
2. **Wiązanie nagłówków HTTP**: W każdym wychodzącym żądaniu HTTP do API dostawcy model musi zbindować nagłówki `HTTP-Referer` (z adresem aplikacji) oraz `X-OpenRouter-Title` (z nazwą aplikacji).
3. **Fail-Closed w audycie ładu**: Brak deklaracji w plikach `.env` / `.env.example` lub brak nagłówków w kodzie klienta LLM skutkuje błędem audytu ładu (`DIAGIT-LLM-001` / `OPENROUTER_APP_IDENTITY_MISSING`) i uniemożliwia zaliczenie bramki weryfikacyjnej.

---

## 3. Przykłady Mapowania i Adresacji

### 3.1. Skanowanie zależności floty przez MCP
- **Natural Language (NL)**: *"Przeskanuj przestarzałe pakiety PyPI w projektach semcod/*"*
- **Action URI**: `search://fleet/dependencies/outdated?project=semcod/*&ecosystem=pypi&format=toon`
- **MCP Tool**: `check_outdated_dependencies`
- **Resource URN**: `urn:subactor:search:outdated:20261011T130421Z`

### 3.2. Hurtowa operacja Multi-Gitter przez MCP / Diagit
- **Natural Language (NL)**: *"Uruchom symulację dodania pliku licencji Apache-2.0 we wszystkich repozytoriach semcod"*
- **Action URI**: `diagit://fleet/multi-gitter/local-run?root=~/github&org=semcod&dry_run=true`
- **MCP Tool**: `diagit_multi_gitter_local_run`
- **Execution Receipt**: `urn:diagit:fleet:batch:7a8b9c0d` zgodny ze schematem `wellmanifest.fleet-execution-receipt/v1`.
