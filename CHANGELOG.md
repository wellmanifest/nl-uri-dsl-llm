# 1.5.0 — 2026-10-24

- Add the System One / Jev-Compatible Typed Decision DSL and Model Profiles specification (`spec/SYSTEM_ONE_DECISION_DSL.md`, `system-one-decision-v1`).
- Add normative rules `NUL-019` (Single-Pass Typed URI Decision Without Free-Form Generation), `NUL-020` (Cross-Question Policy-DSL Constraint Enforcement), `NUL-021` (SSOT Catalog of 10 Open-Source Jev / System One Model Families), and `NUL-022` (Dynamic Telemetry and Language-Aware Model Profile Routing).
- Add machine-verifiable JSON Schema `schemas/system-one-decision.schema.json` (`wellmanifest.system-one-decision/v1`).
- Add automated conformance and validation tests (`tests/test_system_one_decision_dsl.py`).

# 1.4.0 — 2026-10-11

- Add the MCP Process Gateway, Fleet Batch Execution, and LLM Cost Attribution profile (`spec/MCP_FLEET_EXECUTION_DSL.md`, `mcp-fleet-dsl-v1`).
- Add normative rules `NUL-015` (Model Context Protocol Process Gateway Conformance), `NUL-016` (Fleet Multi-Repository Batch Dry-Run and Execution Receipt Mandate), `NUL-017` (Fleet Dependency Health & Impact Classification Mandate), and `NUL-018` (LLM Cost Attribution and Application Identity Mandate).
- Add machine-verifiable JSON Schemas `schemas/mcp-process-gateway.schema.json` (`wellmanifest.mcp-process-gateway/v1`) and `schemas/fleet-execution-receipt.schema.json` (`wellmanifest.fleet-execution-receipt/v1`).
- Add automated conformance and validation tests (`tests/test_mcp_fleet_dsl.py`).

# 1.3.1 — 2026-10-05

- Add normative rule `NUL-014` (Universal URN Identifier Mandate for Financial Entities) to `spec/FINANCIAL_TRANSACTIONS_TAXONOMY_DSL.md`.
- Enforce mandatory RFC 8141 URN properties (`CASE_URN`, `SOURCE_URN`, `DOCUMENT_URN`, `TRANSACTION_URN`, `CONFIRMATION_URN`, `FILE_URN`) across `schemas/financial-dossier.schema.json` and `schemas/financial-source.schema.json`.
- Add automated URN syntax and schema conformance tests (`tests/test_financial_dsl.py`).

# 1.3.0 — 2026-10-05

- Add the Financial Transactions and Invoice Taxonomy DSL profile (`spec/FINANCIAL_TRANSACTIONS_TAXONOMY_DSL.md`).
- Add normative rules `NUL-010` (Financial DSL Capitalize Token Determinism), `NUL-011` (Dossier Evidence Envelope RFC 3986 Addressing), `NUL-012` (Internal Transfer vs Tax Event Demarcation), and `NUL-013` (Payment Gateway Fee Auto-Splitting).
- Add machine-verifiable JSON Schemas `schemas/financial-dossier.schema.json` (`wellmanifest.faktury.dossier/v1`) and `schemas/financial-source.schema.json` (`wellmanifest.faktury.source/v1`).
- Add automated conformance tests (`tests/test_financial_dsl.py`).

# 1.2.0 — 2026-10-04

- Add the Conversational Process Isolation and Bidirectional State URL Synchronization standard (`spec/CONVERSATIONAL_PROCESS_ISOLATION.md`).
- Add normative rules `NUL-007` (Conversational Stream & Process Isolation), `NUL-008` (Bidirectional Interactive State URL Synchronization), and `NUL-009` (Conversational & Process State Introspection Snapshot).
- Add machine-verifiable JSON Schema `schemas/conversational-process-snapshot.schema.json` (`wellmanifest.conversational-process-snapshot/v1`).
- Add automated conformance tests (`tests/test_conversational_process_isolation.py`).

# 1.1.0 — 2026-10-03

- Add the optional typed URI/URN process-exchange profile, request/result correlation, scoped data bindings and truthful execution outcomes.
- Add schema conformance cases; publication of the standard does not deploy or authorize a runtime.

# Changelog

## Unreleased

- Add the semantic-v1 multilingual, Unicode-preserving URI DSL profile.
- Adopt published immutable governance, native fenced ticket recovery and real conformance CI.

## 1.0.0

- Existing legacy URI DSL standard.
