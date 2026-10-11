import json
from pathlib import Path
import jsonschema
import pytest

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"
SPEC_DIR = Path(__file__).resolve().parent.parent / "spec"


def test_mcp_fleet_spec_exists_and_declares_rules():
    spec_path = SPEC_DIR / "MCP_FLEET_EXECUTION_DSL.md"
    assert spec_path.exists()
    content = spec_path.read_text(encoding="utf-8")
    assert "NUL-015" in content
    assert "NUL-016" in content
    assert "NUL-017" in content
    assert "NUL-018" in content
    assert "Model Context Protocol" in content
    assert "tools/call" in content
    assert "dry_run" in content
    assert "diagit.fleet_execution/v1" in content
    assert "OPENROUTER_APP_NAME" in content
    assert "OPENROUTER_APP_URL" in content


def test_fleet_execution_receipt_schema_valid():
    schema_path = SCHEMA_DIR / "fleet-execution-receipt.schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    valid_receipt = {
        "schema": "diagit.fleet_execution/v1",
        "root": "/home/tom/github",
        "total_repositories": 2,
        "modified_repositories": 1,
        "failed_repositories": 0,
        "dry_run": True,
        "script": "if [ ! -f LICENSE ]; then echo 'MISSING'; fi",
        "run_id": "run-01928374",
        "results": [
            {
                "repository": "semcod/fixplesk",
                "path": "/home/tom/github/semcod/fixplesk",
                "exit_code": 0,
                "modified": False,
                "committed": False,
                "branch": None,
                "stdout": "",
                "stderr": "",
            },
            {
                "repository": "semcod/search",
                "path": "/home/tom/github/semcod/search",
                "exit_code": 0,
                "modified": True,
                "committed": False,
                "branch": "chore/add-license",
                "stdout": "MISSING\n",
                "stderr": "",
            },
        ],
    }

    # Should validate cleanly
    jsonschema.validate(instance=valid_receipt, schema=schema)

    # Invalid: missing root
    invalid_receipt = dict(valid_receipt)
    del invalid_receipt["root"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_receipt, schema=schema)

    # Invalid: wrong schema name
    invalid_schema = dict(valid_receipt, schema="invalid.schema/v0")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_schema, schema=schema)


def test_mcp_process_gateway_schema_valid():
    schema_path = SCHEMA_DIR / "mcp-process-gateway.schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    valid_envelope = {
        "schema": "wellmanifest.mcp-process-gateway/v1",
        "mcp_method": "tools/call",
        "tool_name": "check_outdated_dependencies",
        "process_uri": "search://fleet/dependencies/outdated?project=semcod/*&format=toon",
        "arguments": {
            "project": "semcod/*",
            "ecosystem": "all",
            "format": "toon",
        },
        "receipt": {
            "urn": "urn:subactor:search:outdated:20261011T130421Z",
            "status": "succeeded",
            "summary": "Scanned 74 projects in 1538ms; found 1269 outdated packages.",
            "artifact_uris": ["reports/outdated-20261011.toon"],
            "duration_ms": 1538,
        },
        "cost_attribution": {
            "app_name": "subactor-search",
            "app_url": "https://github.com/semcod/search",
            "model": "deepseek/deepseek-flash",
        },
    }

    # Should validate cleanly
    jsonschema.validate(instance=valid_envelope, schema=schema)

    # Invalid: missing cost_attribution app_name
    invalid_envelope = json.loads(json.dumps(valid_envelope))
    del invalid_envelope["cost_attribution"]["app_name"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_envelope, schema=schema)

    # Invalid: non-URN pattern
    invalid_urn = json.loads(json.dumps(valid_envelope))
    invalid_urn["receipt"]["urn"] = "not-a-valid-urn"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_urn, schema=schema)
