# Ticket 006: Mandate universal URN identifiers for all financial artifacts transactions and messages

- **ID**: ticket-006
- **Owner**: agent:antigravity
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-10-05

## Goal and scope

Mandate and standardize universal RFC 8141 URN identifiers across all financial entities, including transaction envelopes (`urn:fin:dossier:...`), documents/invoices (`urn:fin:doc:invoice:...`), banking/wallet transactions (`urn:fin:txn:...`), emails/messages (`urn:fin:email:...`), and source channels (`urn:fin:source:...`). Formulate normative rule NUL-014 (Universal URN Identifier Mandate), update schemas with mandatory URN properties, and verify complete test suite.

## Acceptance criteria

- [x] AC-01: Add normative rule NUL-014 and canonical URN taxonomy to `spec/FINANCIAL_TRANSACTIONS_TAXONOMY_DSL.md`.
- [x] AC-02: Update `schemas/financial-dossier.schema.json` with mandatory URNs on dossier cases, source nodes, document nodes, transaction nodes, and confirmation nodes.
- [x] AC-03: Update `schemas/financial-source.schema.json` with mandatory `SOURCE_URN` and `FILE_URN`.
- [x] AC-04: Add test cases to `tests/test_financial_dsl.py` verifying URN syntax and schema conformance.
- [x] AC-05: Update `README.md`, `CHANGELOG.md`, `VERSION` (1.3.1), and `project/TICKETS.md`.
- [x] AC-06: Pass repository governance checks (`GOV-PASS`).
