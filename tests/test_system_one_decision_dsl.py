import json
from pathlib import Path
import jsonschema
import pytest

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"
SPEC_DIR = Path(__file__).resolve().parent.parent / "spec"

TEN_JEV_FAMILIES = (
    "clef",
    "gliner2.5-decide",
    "laya",
    "kev",
    "laya-mlx",
    "semif",
    "nanojev",
    "bespoke-nimble",
    "jevlike",
    "jevos",
)


def test_system_one_decision_spec_exists_and_declares_rules_and_models():
    spec_path = SPEC_DIR / "SYSTEM_ONE_DECISION_DSL.md"
    assert spec_path.exists()
    content = spec_path.read_text(encoding="utf-8")
    for rule_id in ("NUL-019", "NUL-020", "NUL-021", "NUL-022"):
        assert rule_id in content
    for family in TEN_JEV_FAMILIES:
        assert family in content.lower()
    assert "choice" in content
    assert "score" in content
    assert "noul" in content
    assert "proc://" in content


def test_system_one_decision_schema_validates_envelope_and_constraints():
    schema_path = SCHEMA_DIR / "system-one-decision.schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    valid_decision = {
        "schema": "wellmanifest.system-one-decision/v1",
        "model_profile_id": "laya",
        "family": "laya",
        "wire_format": "system-one",
        "state": {
            "query": "uruchom testy jednostkowe projektu heyasa",
            "autonomy_mode": "auto",
            "modality": "text",
        },
        "questions": [
            {
                "id": "uri_choice",
                "type": "choice",
                "question": "Select the canonical DockURI / Action URI.",
                "options": [
                    "proc://heyasa/test",
                    "proc://heyasa/lint",
                    "proc://willmux/start",
                ],
            },
            {
                "id": "risk_score",
                "type": "score",
                "question": "Score operational risk level from 1 to 3.",
                "options": ["1", "2", "3"],
            },
            {
                "id": "execution_allowed",
                "type": "noul",
                "question": "Is immediate execution safe and free of negation?",
                "options": ["true", "false"],
            },
        ],
        "answers": {
            "uri_choice": "proc://heyasa/test",
            "risk_score": 1.15,
            "execution_allowed": True,
        },
        "probabilities": {
            "uri_choice": {
                "proc://heyasa/test": 0.91,
                "proc://heyasa/lint": 0.06,
                "proc://willmux/start": 0.03,
            },
            "risk_score": {"1": 0.87, "2": 0.11, "3": 0.02},
            "execution_allowed": {"true": 0.95, "false": 0.05},
        },
        "selected_uri": "proc://heyasa/test",
        "selected_action_id": "dockuri.heyasa.test",
        "confidence": 0.91,
        "risk_score": 1.15,
        "execution_allowed": True,
        "blocked_by_constraint": False,
        "applied_constraints": [],
        "latency_ms": 4.2,
        "transport": "local-zero-gen",
    }

    jsonschema.validate(instance=valid_decision, schema=schema)

    # Validate all 10 model families are accepted by the schema enum
    for family in TEN_JEV_FAMILIES:
        candidate = dict(valid_decision, family=family, model_profile_id=family)
        jsonschema.validate(instance=candidate, schema=schema)

    # Reject unknown model family
    invalid_family = dict(valid_decision, family="unknown-model")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_family, schema=schema)

    # Reject non-RFC-3986 selected_uri
    invalid_uri = dict(valid_decision, selected_uri="not_a_valid_uri")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_uri, schema=schema)

    # Reject empty probability distribution (NUL-019)
    empty_probs = dict(
        valid_decision,
        probabilities={
            "uri_choice": {},
            "risk_score": {"1": 0.87, "2": 0.11, "3": 0.02},
            "execution_allowed": {"true": 0.95, "false": 0.05},
        },
    )
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=empty_probs, schema=schema)

    # Reject incomplete execution_allowed distribution missing 'false'
    incomplete_noul = dict(
        valid_decision,
        probabilities={
            "uri_choice": valid_decision["probabilities"]["uri_choice"],
            "risk_score": {"1": 0.87, "2": 0.11, "3": 0.02},
            "execution_allowed": {"true": 1.0},
        },
    )
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=incomplete_noul, schema=schema)

    # Reject invalid question options for score and noul conditional schemas
    invalid_noul_options = dict(
        valid_decision,
        questions=[
            valid_decision["questions"][0],
            valid_decision["questions"][1],
            {
                "id": "execution_allowed",
                "type": "noul",
                "question": "Is immediate execution safe?",
                "options": ["yes", "no", "maybe"],
            },
        ],
    )
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_noul_options, schema=schema)

    invalid_score_options = dict(
        valid_decision,
        questions=[
            valid_decision["questions"][0],
            {
                "id": "risk_score",
                "type": "score",
                "question": "Score risk level.",
                "options": ["low", "high"],
            },
            valid_decision["questions"][2],
        ],
    )
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_score_options, schema=schema)
