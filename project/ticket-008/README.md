# Ticket 008: Standardize MCP process gateway and fleet batch execution profiles

- **ID**: ticket-008
- **Owner**: agent:antigravity
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-10-11

## Goal and scope

Standardize Model Context Protocol (MCP) process routing, fleet-wide batch execution, and LLM cost attribution in `wellmanifest/nl-uri-dsl-llm`:
1. **MCP Process Gateway**:
   - Standardize JSON-RPC 2.0 tool binding to RFC 3986 Action URIs (`NUL-015`).
   - Enforce schema constraints (`inputSchema`) as anti-hallucination barriers.
   - Enforce conversational stream isolation returning structured URN receipts.
2. **Fleet Batch Execution**:
   - Standardize multi-repository fleet execution with mandatory `--dry-run` (`NUL-016`).
   - Define machine-verifiable receipt schema `wellmanifest.fleet-execution-receipt/v1`.
3. **Fleet Dependency Health**:
   - Define impact classification (`major`, `minor`, `patch`) and offline TTL caching (`NUL-017`).
4. **LLM Cost Attribution**:
   - Mandate application identity (`OPENROUTER_APP_NAME`, `OPENROUTER_APP_URL`) and HTTP header bindings (`NUL-018`).
5. **Artifacts & Verification**:
   - `spec/MCP_FLEET_EXECUTION_DSL.md`
   - `schemas/mcp-process-gateway.schema.json`
   - `schemas/fleet-execution-receipt.schema.json`
   - `tests/test_mcp_fleet_dsl.py`

## Acceptance criteria

- [x] AC-01: Specification `spec/MCP_FLEET_EXECUTION_DSL.md` defines MCP routing, fleet batch execution, semver bump impact classification, and LLM application identity rules NUL-015..NUL-018.
- [x] AC-02: JSON schemas `schemas/mcp-process-gateway.schema.json` and `schemas/fleet-execution-receipt.schema.json` validate against Draft 2020-12 meta-schema.
- [x] AC-03: Conformance test suite `tests/test_mcp_fleet_dsl.py` passes with 0 failures.
- [x] AC-04: Full test suite passes and `./project/governance-check.sh` succeeds with 0 errors and 0 warnings (`GOV-PASS`).

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.
