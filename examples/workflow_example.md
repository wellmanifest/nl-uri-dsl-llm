# Przykłady generowania i wykonania w architekturze NL-URI-DSL-LLM

## 1. Wejście Natural Language (NL)
Użytkownik wprowadza polecenie mową lub tekstem w czacie:
> *"Uruchom testy w kontenerze Pythona z limitem 512MB RAM i zrób zrzut ekranu strony raportu."*

## 2. Tłumaczenie LLM z użyciem gramatyki GBNF
Rejestr `ProcessUriRegistry` generuje gramatykę GBNF ograniczającą wyjście:

```gbnf
root ::= action_line ( "\n" action_line )*
action_line ::= uri ( " " json_payload )?
uri ::= "browser://navigate" | "browser://screenshot" | "sandbox://run"
json_payload ::= "{" [^}\n]* "}"
```

Model LLM generuje zwięzły strumień URI DSL:
```text
uri: sandbox://run {"image": "python:3.11-slim", "cmd": "pytest tests/ -q"}
uri: browser://navigate {"url": "http://localhost:8000/report"}
uri: browser://screenshot {"output": "reports/run-result.png"}
```

## 3. Wykonanie przez Taskand Capsule / Runner
1. `sandbox://run`: `DockerSandboxRunner` montuje katalog `/workspace` i uruchamia proces z flagami `--memory=512m --cpus=1.0 --network=none`.
2. `browser://navigate`: `CdpBrowserController` wysyła ramkę JSON-RPC `{"id": 1, "method": "Page.navigate", "params": {"url": "http://localhost:8000/report"}}`.
3. `browser://screenshot`: `CdpBrowserController` wysyła ramkę `Page.captureScreenshot` i zapisuje plik wynikowy w katalogu artefaktów.
