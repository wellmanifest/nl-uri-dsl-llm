# Ticket 003: Conversational process isolation and state URL sync standard

- **ID**: ticket-003
- **Owner**: agent:antigravity
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-10-04

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: The user requested investigating where these proven architectural patterns are standardized in wellmanifest/* and extending wellmanifest/nl-* standards with the concrete patterns tested in practice (e.g. in willmux).
Codify:
1. Conversational Stream Purity and Process Isolation (`NUL-007`): Chat retains dialogue and structured execution receipts with process URI (`process://`) and resource URN (`urn:<domain>:proc:<id>`), while raw stdout/stderr, interactive terminals, and process buffers are isolated in dedicated Process/Terminal views.
2. Bidirectional URL State Synchronization (`NUL-008`): Interactive surfaces synchronize 100% of workspace/view/focus/palette/tab/query states to URL query params, guaranteeing deterministic restoration on reload or deep-link navigation.
3. Structured Snapshot Introspection Schema (`NUL-009`): Machine-verifiable schema (`wellmanifest.conversational-process-snapshot/v1`) for complete conversational history, active processes, and state introspection.

## Acceptance criteria

- [x] AC-01: Standard specification `spec/CONVERSATIONAL_PROCESS_ISOLATION.md` and machine-verifiable schema `schemas/conversational-process-snapshot.schema.json` are authored; conformance tests pass.
- [x] AC-02: Native governance check (`./project/governance-check.sh`) and worktree policies pass without errors.
