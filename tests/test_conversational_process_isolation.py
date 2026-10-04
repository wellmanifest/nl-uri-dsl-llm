"""Conformance test suite for Conversational Process Isolation and State URL Synchronization.

Standard: wellmanifest/nl-uri-dsl-llm
Profile: conversational-process-isolation-v1
"""

import json
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse
import pytest
from jsonschema import Draft202012Validator


SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "conversational-process-snapshot.schema.json"


@pytest.fixture(scope="module")
def schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def validator(schema):
    return Draft202012Validator(schema)


def test_valid_conversational_process_snapshot(validator):
    sample = {
        "schema": "wellmanifest.conversational-process-snapshot/v1",
        "exportedAt": "2026-10-04T18:00:00Z",
        "url": "http://127.0.0.1:7070/?layout=cols&focus=B&dialog=chat&tab=term&q=!uptime",
        "state": {
            "layout": "cols",
            "order": "A,B,C",
            "panes": "A:shell,B:logs,C:apps",
            "focus": "B",
            "dialog": "chat",
            "activeTab": "term",
            "query": "!uptime",
            "targetPane": "B",
            "targetEnv": "mesh",
            "act": "exec:!uptime",
            "lastClick": "tab:Terminal",
        },
        "chat": {
            "messageCount": 2,
            "messages": [
                {
                    "role": "user",
                    "text": "!uptime",
                    "timestamp": "2026-10-04T17:59:58Z",
                },
                {
                    "role": "system",
                    "text": "Uruchomiono proces na host: uptime · urn:willmux:proc:1",
                    "timestamp": "2026-10-04T17:59:58Z",
                    "urn": "urn:willmux:proc:1",
                    "uri": "process://host/usr/bin/uptime",
                },
            ],
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
                    "startedAt": "2026-10-04T17:59:58Z",
                }
            ],
        },
    }

    errors = list(validator.iter_errors(sample))
    assert not errors, f"Validation errors: {[e.message for e in errors]}"


def test_invalid_snapshot_missing_processes(validator):
    bad_sample = {
        "schema": "wellmanifest.conversational-process-snapshot/v1",
        "exportedAt": "2026-10-04T18:00:00Z",
        "state": {},
        "chat": {"messageCount": 0, "messages": []},
    }
    errors = list(validator.iter_errors(bad_sample))
    assert any("processes" in e.message for e in errors)


def test_invalid_process_uri_scheme(validator):
    bad_sample = {
        "schema": "wellmanifest.conversational-process-snapshot/v1",
        "exportedAt": "2026-10-04T18:00:00Z",
        "state": {},
        "chat": {"messageCount": 0, "messages": []},
        "processes": {
            "activeProcessId": 1,
            "items": [
                {
                    "id": 1,
                    "urn": "urn:willmux:proc:1",
                    "uri": "http://not-a-process-uri/bin/ls",  # Must be process://
                    "command": "ls",
                    "status": "completed",
                }
            ],
        },
    }
    errors = list(validator.iter_errors(bad_sample))
    assert len(errors) > 0


def test_invalid_process_urn_format(validator):
    bad_sample = {
        "schema": "wellmanifest.conversational-process-snapshot/v1",
        "exportedAt": "2026-10-04T18:00:00Z",
        "state": {},
        "chat": {"messageCount": 0, "messages": []},
        "processes": {
            "activeProcessId": 1,
            "items": [
                {
                    "id": 1,
                    "urn": "invalid-urn-not-proc",  # Must match urn:<domain>:proc:<id>
                    "uri": "process://host/bin/ls",
                    "command": "ls",
                    "status": "completed",
                }
            ],
        },
    }
    errors = list(validator.iter_errors(bad_sample))
    assert len(errors) > 0


def test_bidirectional_url_state_serialization():
    original_state = {
        "layout": "cols",
        "order": "A,B,C",
        "panes": "A:shell,B:logs,C:apps",
        "focus": "B",
        "dialog": "chat",
        "tab": "term",
        "q": "!uptime",
        "targetPane": "B",
        "targetEnv": "mesh",
        "act": "exec:!uptime",
    }

    query_string = urlencode(original_state)
    full_url = f"http://127.0.0.1:7070/?{query_string}"

    parsed = urlparse(full_url)
    reconstructed = {k: v[0] for k, v in parse_qs(parsed.query).items()}

    assert reconstructed["layout"] == original_state["layout"]
    assert reconstructed["order"] == original_state["order"]
    assert reconstructed["panes"] == original_state["panes"]
    assert reconstructed["focus"] == original_state["focus"]
    assert reconstructed["dialog"] == original_state["dialog"]
    assert reconstructed["tab"] == original_state["tab"]
    assert reconstructed["q"] == original_state["q"]
    assert reconstructed["targetPane"] == original_state["targetPane"]
    assert reconstructed["targetEnv"] == original_state["targetEnv"]
    assert reconstructed["act"] == original_state["act"]


def test_conversational_stream_purity_assertion():
    """Verify chat message does not accept unisolated raw stdout streams."""
    def is_chat_pure(message_text: str) -> bool:
        # A pure chat message must not contain multiline command dumps or terminal escape headers
        lines = message_text.strip().splitlines()
        if len(lines) > 10 and not any(k in lines[0] for k in ["Uruchomiono proces", "Zakończono proces"]):
            return False
        if "\x1b[" in message_text:
            return False
        return True

    # Pure notification: PASS
    assert is_chat_pure("Uruchomiono proces na host: ls · urn:willmux:proc:1")
    # Natural conversation: PASS
    assert is_chat_pure("Tryb: Równoważenie")
    # Raw multiline command dump: REJECT
    raw_dump = "\n".join([f"file_{i}.txt" for i in range(50)])
    assert not is_chat_pure(raw_dump)
    # Raw ANSI terminal output: REJECT
    assert not is_chat_pure("\x1b[32mPASS\x1b[0m test_all")
