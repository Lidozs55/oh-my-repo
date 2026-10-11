# Product Operation Logic Refactoring Guide

Read this when the primary target is user-perceivable operational behavior: CLI interaction flows, UI journeys, API usage experience, configuration and onboarding experience, error and recovery paths. Also read this when defining the new acceptance standard at L4.

What makes product-logic refactoring special: its "behavior" is the product itself, so the safety net is not tests but **journeys**. Like docs refactoring, this domain has no established industry practice for agents; the journey-based safety net below is an original design.

## Core method: the journey trio

### 1. Journey inventory
Enumerate every path a user takes to accomplish a task: signup/initialization, core workflows, error recovery, upgrade/migration... Sources: code entry points (route tables/command registration), existing how-to docs, real complaints in issues/tickets. For each journey, record: entry → step sequence → exits (success/failure shapes).

### 2. Current-behavior snapshot (the equivalent of characterization tests for code)
For every journey you will touch, **record** current behavior live instead of describing it from memory:
- Web UI: walk it with browser-use; screenshots + step records;
- CLI: script-record real sessions (command sequences + output);
- API: representative request/response samples.
The snapshot serves two purposes: (a) the regression baseline at ≤L3; (b) at any level, the "evidence of the status quo" — the new design must account for every old journey, item by item.

### 3. Behavior-change table (mandatory at ≥L3)
One line per controlled behavior change: `old behavior (with snapshot evidence) → new behavior | reason | blast radius (which users/which journey)`. At L4 the log also records deletions and their rationale ("which journeys/steps were removed, and why").

## L4: operationalizing product-quality-first

"Product quality first" must be translated into verifiable new acceptance standards; every core journey answers at least:

- **Completion**: can the task be done in N steps? (give a target N)
- **Recoverability**: after a mid-flow failure, where can the user resume? Is data lost?
- **Comprehensibility**: do error messages say "what broke + what to do"?
- **Discoverability**: can a new user guess the next step without docs? (smoke-verify with browser-use)
- **Consistency**: do similar operations behave the same across entry points?

These standards are **defined before code is written** (Phase 3, design) and checked at the very end (Phase 7).

## Migration strategy (by project stage)

- **dev-stage (no external consumers)**: switch directly + changelog + one-line migration note. Dropping compatibility entirely is the recommended move (SemVer 0.x semantics allow it); the only requirement is no silent breakage — changes must be traceable.
- **Has users**: breaking changes are a process, not an event — an old→new mapping table + a migration guide (write a codemod/migration script when automatable); dual-entry transitions or gradual rollout for high-risk journeys (feature flags, with registered expiry); deprecation warnings first (keep ≥2 minor versions before removal, the PEP 387 convention).
- **Data operations**: any operation that destroys user data (changing storage formats, dropping fields) gets an unconditional user gate, with a rollback path (backup/export).

## Coupling with code and doc changes

- Interaction-flow changes → update in the same PR: CLI help text and completions, UI copy, error messages, related how-to docs, sample code. Interaction changed but docs didn't is the most common drift.
- The behavior delta log is the raw material for the migration guide: once the table is written, the guide is mostly formatting.
- Config-format changes are persisted contracts: follow Expand-Contract in code-refactor.md.

## Acceptance checklist

- [ ] Full journey coverage: every old journey has an explicit disposition in the new world (kept/simplified/merged/deleted, deletions justified)
- [ ] Snapshot comparison (≤L3): affected journeys re-recorded and verified; every difference appears in the behavior delta log
- [ ] New acceptance standards (L4) pass item by item, with evidence (screenshots/session recordings used for verification; no need to keep them on file)
- [ ] Migration guide/changelog exists and matches the behavior delta log
- [ ] Error paths are not an afterthought: verify at least one failure scenario per core journey
