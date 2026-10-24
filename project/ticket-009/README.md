# Ticket 009: Standardize System One Jev-compatible typed decision DSL and model profiles

- **ID**: ticket-009
- **Owner**: agent:antigravity
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-24

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: User explicitly requested implementation of System One / Jev-compatible typed decisions (`choice`, `score`, `noul`) over DockURI URI processes conforming to `wellmanifest/nohardcode`, `wellmanifest/ssot`, `wellmanifest/dsl`, `wellmanifest/policy-dsl`, and `wellmanifest/nl-*`, covering the 10 open-source Jev / System One model families (`Clef`/`Clef-flash`, `GLiNER2.5-Decide`, `Laya`, `Kev`, `Laya-MLX`, `SemIf`, `NanoJev`, `Bespoke Nimble`, `jevlike`, `jevos`).

1. **Normative Specification (`spec/SYSTEM_ONE_DECISION_DSL.md`)**:
   - Define `system-one-decision-v1` (`wellmanifest.system-one.nl-uri-dsl-llm / v1`) and quality rules `NUL-019` (`Single-Pass Typed URI Decision Without Free-Form Generation`), `NUL-020` (`Cross-Question Policy-DSL Constraint Enforcement`), `NUL-021` (`SSOT Catalog of 10 Open-Source Jev / System One Model Families`), and `NUL-022` (`Dynamic Telemetry and Language-Aware Model Profile Routing`).
2. **Machine-Verifiable JSON Schema (`schemas/system-one-decision.schema.json`)**:
   - Define `wellmanifest.system-one-decision/v1` validating request/response envelopes (`state`, `questions` of kind `choice`, `score`, `noul`, `probabilities`, `cross_constraints`, `selected_uri`, `model_profile_id`).
3. **Conformance Tests (`tests/test_system_one_decision_dsl.py`)**:
   - Validate the normative specification, rules `NUL-019..022`, all 10 model families, and positive/negative instances against `schemas/system-one-decision.schema.json`.

## Acceptance criteria

- [x] AC-01: `spec/SYSTEM_ONE_DECISION_DSL.md` and `README.md` document rules `NUL-019..022` and the 10 open-source Jev / System One model families.
- [x] AC-02: `schemas/system-one-decision.schema.json` validates `wellmanifest.system-one-decision/v1` envelopes (`choice` 2..255 URI options, `score`, `noul`, cross-question constraints).
- [x] AC-03: `tests/test_system_one_decision_dsl.py`, `./project/governance-check.sh`, and `wellman check` pass.

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.
