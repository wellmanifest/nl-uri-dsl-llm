# Ticket 005: Financial transactions and invoice taxonomy DSL profile

- **ID**: ticket-005
- **Owner**: agent:antigravity
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-10-05

## Goal and scope

Establish and standardize the Financial Transactions, Invoice Taxonomy, and Evidence Envelope DSL within `wellmanifest/nl-uri-dsl-llm`. Formulate normative rules NUL-010..013 enforcing capitalized DSL tokens (eliminating LLM hallucinations and ensuring deterministic microscale evaluation), RFC 3986 URI/URN addressing for financial evidence, auto-splitting of payment gateway fees, and demarcation of internal transfers from taxable income/expense. Provide canonical JSON schemas (`wellmanifest.faktury.dossier/v1` and `wellmanifest.faktury.source/v1`) and comprehensive conformance tests.

## Acceptance criteria

- [x] AC-01: Create `spec/FINANCIAL_TRANSACTIONS_TAXONOMY_DSL.md` with normative rules NUL-010..013, channel taxonomies, and capitalized DSL dictionaries.
- [x] AC-02: Create `schemas/financial-dossier.schema.json` validating the 5-node dossier structure and capitalized status tokens.
- [x] AC-03: Create `schemas/financial-source.schema.json` validating channel manifest contracts (`bank-*`, `paypal-*`, `stripe-*`, `allegro-*`, `ksef-*`, `www-*`).
- [x] AC-04: Implement pytest test suite `tests/test_financial_dsl.py` verifying schema validation, URI resolving, and token constraints.
- [x] AC-05: Update `README.md`, `CHANGELOG.md`, and `.governance/manifest.json`.
- [x] AC-06: Pass repository preflight and governance checks (`GOV-PASS`).
