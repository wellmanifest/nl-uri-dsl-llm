# Wellmanifest Specification: Conversational Process Isolation and Bidirectional State URL Synchronization

- **Standard**: `wellmanifest/nl-uri-dsl-llm`
- **Profile**: `conversational-process-isolation-v1`
- **Status**: `Standard Specification`
- **Revision**: `1.2.0`
- **Date**: `2026-10-04`

---

## 1. Executive Summary & Problem Statement

Modern conversational agents and developer interfaces combine natural language (NL) dialogue with shell and command-line execution (`!command`, `$cmd`, CLI tools, container processes). In naive implementations, executing processes write raw terminal output (`stdout`, `stderr`, ANSI escape sequences, interactive curses, ASCII progress bars) directly into the conversational chat stream.

This creates critical systemic failures:
1. **Context Window Degradation & Token Waste**: Large process outputs consume LLM context windows, push out important instructions, and drive up API token costs.
2. **Loss of Dialogue Coherence**: Mixed streams make human and agent conversational turns unreadable.
3. **Loss of State & Deep Linking**: Refreshing or sharing a session loses window layouts, focused views, active tabs, and input states unless deterministically serialized to standard URL query parameters.
4. **Lack of Programmatic Introspection**: Autonomous coding agents cannot reliably inspect running and completed processes when process state is unstructured DOM text.

The **Conversational Process Isolation & State URL Synchronization Standard** resolves these issues by strictly separating conversational messaging from process execution, enforcing canonical URI/URN addressing, and mandating bidirectional URL state persistence.

---

## 2. Core Architectural Contracts

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Conversational Chat Stream                             │
│  - Natural language user & agent dialogue                                   │
│  - Strict conversational purity (NO raw stdout/stderr, NO ANSI escapes)    │
│  - Concise execution receipts:                                              │
│      URN: urn:<domain>:proc:<id>                                            │
│      URI: process://<host>/<bin>?<params>                                   │
│      Status: exit_code, timing, link to [Terminal ↗]                        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ References (URN & URI)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 Dedicated Process / Terminal Artifact View                  │
│  - Isolated terminal screen (.pal-term-screen)                              │
│  - Process switcher pills (active & historical processes)                   │
│  - Exit code badges, execution duration, timestamp                         │
│  - Interactive CLI input for chained operations                             │
│  - Copy controls (output buffer, URI, URN)                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ▲
                                       │ Bidirectional Sync
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 Bidirectional URL State Synchronization                     │
│  - location.search (history.replaceState with 150ms debounce)               │
│  - Parameters: layout, order, panes, focus, dialog, tab, q, user, act       │
│  - Deterministic boot restoration: exact state recreated on reload          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Rule CPI-001 (Conversational Stream Purity)
The conversational dialogue log (`chat`) is reserved exclusively for:
- User natural language prompts and commands.
- Assistant/agent natural language responses.
- System operational notices.
- Concise, structured execution notifications.

Under no circumstances may raw process output, multiline terminal logs, or interactive CLI streams be appended directly to the conversational chat log.

### 2.2 Rule CPI-002 (Canonical Process Addressing via RFC 3986 URI and URN)
Every initiated process execution MUST be assigned:
1. **Process URI** (Execution Action URI):
   ```text
   process://<host>/<path>[?<query-params>]
   ```
   *Example*: `process://host/bin/sh?cmd=ls` or `process://192.168.1.10/usr/bin/uptime`
2. **Resource URN** (Persistent Execution Identity):
   ```text
   urn:<domain>:proc:<process-id>
   ```
   *Example*: `urn:willmux:proc:1` or `urn:paxlet:proc:7c9e`

The execution notification in the conversational stream must display both the URN and a clickable reference to the process view.

### 2.3 Rule CPI-003 (Dedicated Process / Terminal Artifact Presentation)
Process execution output MUST be routed to a dedicated **Process / Terminal Artifact View** (e.g. `Terminal` tab in the artifact palette):
- **Output Screen**: Renders raw or formatted stdout/stderr, ANSI colors, and termination status.
- **Process Header**: Displays active Process URN, Process URI, exit code (`0` for success, non-zero for failure), execution latency (`ms`), and start timestamp.
- **Process Switcher**: Enables switching between active and historical background executions without mixing their streams.
- **Interactive CLI**: Allows issuing subsequent or interactive commands within the same execution context.
- **Action Toolbar**: Dedicated copy buttons for copying terminal output, copying URN/URI, and clearing the buffer.

### 2.4 Rule CPI-004 (Bidirectional State URL Synchronization)
Every adopting interactive UI MUST synchronize the full operational state to RFC 3986 URL query parameters in real time via `history.replaceState` (debounced, typically 100–200ms).

The canonical URL query parameters include:
| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `layout` | string | Normalized layout mode | `cols`, `rows`, `grid`, `zoom` |
| `order` | string | Comma-separated pane identifiers | `A,B,C,D` |
| `panes` | string | Pane view bindings (`<id>:<view>`) | `A:shell,B:logs,C:apps` |
| `focus` | string | Currently focused pane identifier | `B` |
| `dialog` | string | Currently active modal or palette | `chat`, `classic` |
| `tab` | string | Active artifact tab in palette | `term`, `windows`, `commands` |
| `q` / `user`| string | Active search/input query | `!uptime` |
| `targetPane`| string | Targeted pane for execution | `A` |
| `targetEnv` | string | Targeted execution node/mesh | `mesh`, `local` |
| `act` | string | Last user or agent interaction event | `exec:!ls`, `tab:term` |
| `lastClick`| string | Human-readable trace of clicked element | `pane:B:rec`, `tab:Okna` |

### 2.5 Rule CPI-005 (Deterministic State Restoration on Boot)
When a client navigates to an URL containing state parameters, the application MUST deterministically reconstruct that exact visual and operational state:
1. Rebuild pane layout, window ordering, and view bindings.
2. Set focus on the designated pane.
3. Open the designated dialog or palette if specified.
4. Select the active artifact tab.
5. Populate the query input field if specified.
6. Verify that no state degradation or layout desynchronization occurs.

### 2.6 Rule CPI-006 (Structured Introspection Snapshot Schema)
Adopting systems MUST provide a structured JSON introspection export conforming to `wellmanifest.conversational-process-snapshot/v1`. This enables automated tools and AI subagents to extract the full state without DOM scraping:
```json
{
  "schema": "wellmanifest.conversational-process-snapshot/v1",
  "exportedAt": "2026-10-04T18:00:00Z",
  "url": "http://127.0.0.1:7070/?layout=cols&focus=B&dialog=chat&tab=term&q=!uptime",
  "state": {
    "layout": "cols",
    "focus": "B",
    "dialog": "chat",
    "activeTab": "term",
    "query": "!uptime"
  },
  "chat": {
    "messageCount": 2,
    "messages": [
      { "role": "user", "text": "!uptime", "timestamp": "2026-10-04T17:59:58Z" },
      { "role": "system", "text": "Uruchomiono proces na host: uptime · urn:willmux:proc:1", "urn": "urn:willmux:proc:1" }
    ]
  },
  "processes": {
    "activeProcessId": 1,
    "items": [
      {
        "id": 1,
        "urn": "urn:willmux:proc:1",
        "uri": "process://host/usr/bin/uptime",
        "command": "uptime",
        "host": "host",
        "status": "completed",
        "exitCode": 0,
        "output": " 18:00:00 up 10 days, 2 users, load average: 0.15, 0.22, 0.18\n",
        "startedAt": "2026-10-04T17:59:58Z"
      }
    ]
  }
}
```

### 2.7 Rule CPI-007 (Window Media & Artifact Recording Standard)
Adopting interfaces MUST provide standardized recording controls (Play / Stop toggle on pane headers and window tools menus):
- Enables selective screen and audio recording for a single window or all windows.
- Encodes video in standard format (`video/webm;codecs=vp9,opus`).
- Saves recording as an immutable media artifact identified by `urn:<domain>:media:<uuid>`.

---

## 3. Conformance Checkpoints

- **`[CONF-CPI-01] Chat Log Purity`**: Assert that shell commands do not dump stdout/stderr directly into conversational log nodes.
- **`[CONF-CPI-02] Process URN & URI Resolution`**: Assert every execution generates valid RFC 3986 URI and URN.
- **`[CONF-CPI-03] Dedicated Terminal Tab Visibility`**: Assert terminal view is mounted with isolated screen and interactive CLI.
- **`[CONF-CPI-04] Full State URL Reflection`**: Assert URL parameters update dynamically upon user/agent interaction.
- **`[CONF-CPI-05] Deterministic URL State Boot`**: Assert loading an URL with state parameters reproduces the exact layout, focus, dialog, and tab.
- **`[CONF-CPI-06] Schema-Valid Introspection Export`**: Assert export payload validates against `wellmanifest.conversational-process-snapshot/v1`.
