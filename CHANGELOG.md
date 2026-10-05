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
