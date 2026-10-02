# Semantic multilingual URI DSL profile

Candidate extension `semantic-v1`, 2026-10-01. Envelope `wellmanifest.nl-plan/v1` is owned by `wellmanifest/nl-dsl-llm`, `spec/SEMANTIC_NL_PLAN.md`. Adoption pins an independently approved revision; this candidate does not assert production rollout.

NUL-001's deterministic NL matching, ASCII normalization and PL/EN synonyms apply to the legacy compatibility profile. In semantic-v1, preserve original Unicode and use multilingual retrieval over declared, effect-filtered operation contracts, followed by a schema-constrained plan generator. Do not reject candidates using lexical subject coverage. Only exact, validated URI DSL syntax bypasses interpretation. No regex first-pass interprets natural-language negation or conversion direction.

Public contracts expose URI, description, typed input/output schemas, effects, declaration status and digest. Cache embeddings by complete public-contract digest and immutable model identity. The generator receives bounded candidate contracts and produces `ok`, `clarify` or `unsupported`; neither non-ok state compiles executable calls. Validate operation-specific arguments, effects and exact contract digest independently of generation.

A call has kind, operation, arguments and digest. A sequence contains 1–16 ordered literal calls. V1 does not support references, conditions or loops. Compile each validated call as `uri: <operation-uri> <canonical JSON arguments>`, preserving literal Unicode and metacharacters. The compiler is not a shell and does not execute. API artifacts retain expected contract digests; textual DSL must be accompanied by the validated plan when freshness binding is required.

An execution adapter must revalidate current contract/source and host policy before each call. A detached DSL string is not execution evidence or authority. Durable workflows retain ordered dependencies and digest bindings. Questions about available tasks select read-only inspection, not development.

The runtime is owned by `paxlet-com/dockuri` (`dockuri_nl` and `dockuri nl` JSON stdin/stdout). This standard owns the URI DSL profile, not a hosted model service. Existing URI names and exact DSL parsing remain compatible.

Test structural conformance separately from real-model semantics. Evaluation includes per-language operation and argument accuracy, SVG→PNG versus PNG→SVG, negation, missing arguments, unsupported requests and literal sequences. Report immutable model/runtime identity and p95 latency. Valid JSON does not prove correct intent. Granite/Qwen are benchmark candidates, not mandated or verified-quality defaults.
