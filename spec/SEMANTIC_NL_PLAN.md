# Semantic multilingual URI DSL profile

Candidate extension `semantic-v1`, 2026-10-01. Envelope `wellmanifest.nl-plan/v1` is owned by `wellmanifest/nl-dsl-llm`, `spec/SEMANTIC_NL_PLAN.md`. Adoption pins an independently approved revision; this candidate does not assert production rollout.

NUL-001's deterministic NL matching, ASCII normalization and PL/EN synonyms apply to the legacy compatibility profile. In semantic-v1, preserve original Unicode and use multilingual retrieval over declared, effect-filtered operation contracts, followed by a schema-constrained plan generator. Do not reject candidates using lexical subject coverage. Only exact, validated URI DSL syntax bypasses interpretation. No regex first-pass interprets natural-language negation or conversion direction.

Public contracts expose URI, description, typed input/output schemas, effects, declaration status and digest. Cache embeddings by complete public-contract digest and immutable model identity. The generator receives bounded candidate contracts and produces `ok`, `clarify` or `unsupported`; neither non-ok state compiles executable calls. Validate operation-specific arguments, effects and exact contract digest independently of generation.

A call has kind, operation, arguments and digest. A sequence contains 1–16 ordered literal calls. V1 does not support references, conditions or loops. Compile each validated call as `uri: <operation-uri> <canonical JSON arguments>`, preserving literal Unicode and metacharacters. The compiler is not a shell and does not execute. API artifacts retain expected contract digests; textual DSL must be accompanied by the validated plan when freshness binding is required.

An execution adapter must revalidate current contract/source and host policy before each call. A detached DSL string is not execution evidence or authority. Durable workflows retain ordered dependencies and digest bindings. Questions about available tasks select read-only inspection, not development.

The runtime is owned by `paxlet-com/dockuri` (`dockuri_nl` and `dockuri nl` JSON stdin/stdout). This standard owns the URI DSL profile, not a hosted model service. Existing URI names and exact DSL parsing remain compatible.

Test structural conformance separately from real-model semantics. Evaluation includes per-language operation and argument accuracy, SVG→PNG versus PNG→SVG, negation, missing arguments, unsupported requests and literal sequences. Report immutable model/runtime identity and p95 latency. Valid JSON does not prove correct intent. Granite/Qwen are benchmark candidates, not mandated or verified-quality defaults.

## Optional process exchange profile, version 1

`uri-urn-exchange-v1` adds the inert `wellmanifest.process-exchange/v1`
envelope. Its draft-2020-12 schema is embedded in `profiles/semantic-v1.json`
under `exchange.schema`. Existing semantic plans and the legacy Process URI
schema remain compatible. An adopter must explicitly pin this profile and its
complete digest; a documentation link or a schema `$id` is not deployment.

### Data identities and process bindings

Use a registered UUID URN (`urn:uuid:<lowercase UUID>`) for each request,
result and immutable data version. An URN identifies data; it does not fetch,
execute or authorize it. The resolver maps it to bytes and verifies `sha256`
and `mediaType` before use. Different content requires a new resource URN.
URN equality, SHA equality and URI syntax do not authenticate a producer.
Legacy names such as `urn:koru:ticket:338` are compatibility identifiers and
must not be used alone to identify tickets across repositories.

The operation URI must resolve to exactly one currently declared executable
binding. Query strings and fragments are excluded from this envelope: typed
arguments carry parameters. Revalidate operation-specific schemas, effects,
current `contractDigest`, source/runtime revision and host policy before each
effect. `effects` must equal the registered contract, not the model's guess.
A resource URN cannot substitute for an executable operation URI.

A request has `messageUrn == requestUrn`. Each response has a different
`messageUrn`, echoes its original `requestUrn`, operation, contract digest,
effects, context and inputs exactly, and supplies its own actual outcome.
The receiver independently compares these bindings with its persisted request;
JSON Schema cannot express this comparison. Reject duplicate resource URNs
with inconsistent digests or types, stale contract digests, wrong repositories,
wrong tickets, reused response identities and replayed responses. Resolve data
only through the configured resolver; never turn an URN into an arbitrary
filesystem path, network URL or subprocess argument.

Mutating and executing operations require explicit context: repository,
native ticket, branch, canonical worktree, owner session, plan/scope digests
and accepted base SHA. A Planfile ticket identifier and its native governance
ticket are distinct identities; their mapping must be persisted and checked.
The receiving runtime pins the exact source used by both preflight and execution.

### Admission and outcomes

Do not redefine the protected admission protocol. Use
`subactor.repository-admission-request/v1` and
`subactor.repository-admission/v1` at the declared verified HTTPS controller
binding. The exchange references their immutable request and receipt resources,
plus the lease ID, revision and fencing token. An untrusted request or result
may contain these references; it never creates a grant. The adapter must verify
the actual controller response, authority, exact workspace/context bindings,
capability, expiry and current revision/fence before every write or execution.
Do not reuse a local projection or an old receipt as current admission.
Admission for workspace writes does not grant publication or deployment.

Requests may be submitted without admission to obtain an honest `blocked`
result. A completed mutating result requires independently verified admission,
verification and completion resource references. Their presence satisfies
transport shape only; the consumer must resolve and authenticate their contents.
Read-only inspection needs no repository write grant and returns real output
resources. `clarify` and `unsupported` never cause execution.

Separate delivery of a message, termination of a worker and completion of the
requested effect. An exit code of zero or a Willman queue task marked `done`
does not make a nested blocked dispatch successful. A dispatcher reports
`blocked` when no task ran and candidates were deferred. Partial execution must
retain per-ticket outcomes and must not claim that all requested work completed.
Boards and retry policies consume the operation outcome, not only worker status.
No inferred progress, echoed input object or empty output is a completion receipt.

### Adoption acceptance

Test schema shape separately from live authority and product behavior. Cover
Unicode, cross-repository ticket collisions, reversed request/result bindings,
stale contracts, stale fencing, expired or missing admission, blocked dispatches
and false success. A real canary must traverse discovery → native allocation →
protected admission → bounded execution → product verification → independent
publication → readback, with evidence for each applicable effect. Each product
owns its adapter; this standard installs neither a controller nor a queue worker.
