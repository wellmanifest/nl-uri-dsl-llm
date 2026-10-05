# Ticket 004: Standardize Python package dependencies and metadata

- **ID**: ticket-004
- **Owner**: human:tom
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-10-05

## Goal and scope

Standardize `wellmanifest/nl-uri-dsl-llm` packaging with a canonical `pyproject.toml` aligned with sibling standards `wellmanifest/nl-dsl-llm` and `wellmanifest/nl-api-llm`:
- Package name: `wellmanifest-nl-uri-dsl-llm`
- Standard dependencies: `pydantic>=2.0.0`, `jsonschema>=4.0.0`
- Hatchling build backend with Python `>=3.11`
- Formal adoption of parent standard `wellmanifest/nl-dsl-llm@0.1.0`

## Acceptance criteria

- [x] AC-01: `pyproject.toml` created with packaging and standard adoption metadata.
- [x] AC-02: `python3 -m pytest tests/` passes.
- [x] AC-03: `./project/governance-check.sh` passes with 0 errors and 0 warnings.
