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


def validate_system_one_decision_envelope(instance: dict, schema: dict) -> None:
    """Enforce JSON Schema and NUL-019 cross-field consistency + probability normalization (sum == 1.0)."""
    jsonschema.validate(instance=instance, schema=schema)
    probs = instance["probabilities"]
    questions_by_id = {q["id"]: q for q in instance["questions"]}
    for q in instance["questions"]:
        qid = q["id"]
        if qid not in probs:
            raise ValueError(f"Missing probability distribution for question '{qid}'")
        dist = probs[qid]
        expected_options = set(q["options"])
        actual_options = set(dist.keys())
        if actual_options != expected_options:
            raise ValueError(f"Probability keys {actual_options} do not match allowed options {expected_options} for '{qid}'")
        total = sum(float(v) for v in dist.values())
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"Probabilities for '{qid}' do not sum to 1.0 (got {total})")

    answers = instance["answers"]
    choice_options = set(questions_by_id["uri_choice"]["options"])
    if answers["uri_choice"] not in choice_options:
        raise ValueError("answers.uri_choice is not in questions[0].options")
    if instance["selected_uri"] != answers["uri_choice"]:
        raise ValueError("selected_uri must equal answers.uri_choice")
    if instance["risk_score"] != answers["risk_score"]:
        raise ValueError("risk_score must equal answers.risk_score")
    if instance["execution_allowed"] != answers["execution_allowed"]:
        raise ValueError("execution_allowed must equal answers.execution_allowed")


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
            "risk_score": 1,
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
        "risk_score": 1,
        "execution_allowed": True,
        "blocked_by_constraint": False,
        "applied_constraints": [],
        "latency_ms": 4.2,
        "transport": "local-zero-gen",
    }

    validate_system_one_decision_envelope(valid_decision, schema)

    # Validate all 10 model families are accepted by the schema enum
    for family in TEN_JEV_FAMILIES:
        candidate = dict(valid_decision, family=family, model_profile_id=family)
        validate_system_one_decision_envelope(candidate, schema)

    # Reject unknown model family
    invalid_family = dict(valid_decision, family="unknown-model")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_family, schema=schema)

    # Accept hierarchical RFC 3986 Action URIs with ports, percent-encoding, queries, and fragments
    complex_uri = "https://example.com:8443/a%20b?x=1&y=2#section"
    complex_decision = dict(
        valid_decision,
        questions=[
            {
                "id": "uri_choice",
                "type": "choice",
                "question": "Select the canonical DockURI / Action URI.",
                "options": [complex_uri, "proc://heyasa/lint"],
            },
            valid_decision["questions"][1],
            valid_decision["questions"][2],
        ],
        answers={**valid_decision["answers"], "uri_choice": complex_uri},
        probabilities={
            **valid_decision["probabilities"],
            "uri_choice": {complex_uri: 0.9, "proc://heyasa/lint": 0.1},
        },
        selected_uri=complex_uri,
    )
    validate_system_one_decision_envelope(complex_decision, schema)

    # Reject contradictory selected_uri != answers.uri_choice or not in questions[0].options
    with pytest.raises(ValueError, match="selected_uri must equal answers.uri_choice"):
        validate_system_one_decision_envelope(
            dict(valid_decision, selected_uri="proc://heyasa/lint"),
            schema,
        )
    with pytest.raises(ValueError, match="not in questions\\[0\\]\\.options"):
        validate_system_one_decision_envelope(
            dict(
                valid_decision,
                answers={**valid_decision["answers"], "uri_choice": "proc://other/unlisted"},
                selected_uri="proc://other/unlisted",
            ),
            schema,
        )

    # Reject non-RFC-3986 or malformed Action URIs (spaces, missing authority)
    for bad_uri in (
        "not_a_valid_uri",
        "proc://heyasa/test with spaces",
        "proc:///missing-authority",
        "://missing-scheme",
    ):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=dict(valid_decision, selected_uri=bad_uri), schema=schema)

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

    # Reject invalid question options or wrong question IDs for tuple prefixItems
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

    # Reject non-discrete risk_score values and undeclared risk_score probability keys
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=dict(valid_decision, risk_score=1.5), schema=schema)

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(
            instance=dict(
                valid_decision,
                probabilities={
                    **valid_decision["probabilities"],
                    "risk_score": {"1": 0.7, "2": 0.2, "3": 0.05, "4": 0.05},
                },
            ),
            schema=schema,
        )

    # Reject under-normalized and over-normalized distributions across each question head (NUL-019)
    for head_key, bad_dist in (
        ("uri_choice", {"proc://heyasa/test": 0.50, "proc://heyasa/lint": 0.10, "proc://willmux/start": 0.10}),
        ("uri_choice", {"proc://heyasa/test": 0.80, "proc://heyasa/lint": 0.30, "proc://willmux/start": 0.20}),
        ("risk_score", {"1": 0.40, "2": 0.20, "3": 0.10}),
        ("risk_score", {"1": 0.80, "2": 0.30, "3": 0.20}),
        ("execution_allowed", {"true": 0.40, "false": 0.20}),
        ("execution_allowed", {"true": 0.80, "false": 0.50}),
    ):
        bad_instance = dict(
            valid_decision,
            probabilities={
                **valid_decision["probabilities"],
                head_key: bad_dist,
            },
        )
        with pytest.raises(ValueError, match="do not sum to 1.0"):
            validate_system_one_decision_envelope(bad_instance, schema)
