# Ticket 002: Typed URI / URN exchange

- **ID**: ticket-002
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-10-03

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: the user requested investigation and implementation of URI process and URN data exchange for Willman/Koru. Deliver an inert, versioned exchange contract and real schema conformance tests in this standard. Runtime rollout and admission policy changes remain separate product work.

## Acceptance criteria

- [x] AC-01: Resource identity, correlation and live digest checks are specified; 42 schema conformance cases pass.
- [x] AC-02: Negative shape cases reject missing bindings, malformed cursors, ambiguous authority fields and false success. Native governance passes. Live authority and stale-cursor rejection remain runtime obligations.
- [ ] AC-03: Publish through protected independent exact-head review and distinguish standard publication from runtime adoption.
