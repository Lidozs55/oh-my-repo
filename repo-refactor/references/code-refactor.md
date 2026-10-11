# Code Refactoring Execution Guide

Read this when the primary target is code (together with aggression-levels.md and workflow-large.md).

## Building the safety net

**Test triage** (before starting):
- Public-surface tests (exercising public interfaces/CLI/end-to-end behavior) → the final judge as-is, carried to the end, rarely changed.
- Implementation-coupled tests (mocking internal structure, testing private functions) → rewritten as **portable assertions** runnable against both old and new implementations (assert only observable behavior, never internal shape).

**Characterization tests** (legacy code without tests):
1. For each behavior you will touch, run the real code and use the actual output as the expected value — **never fill expectations from guesses**.
2. The baseline includes existing bugs (this pins "what is", not "what should be").
3. Commit the baseline separately; only then may structure change.
4. After refactoring, a non-empty diff means: **intentional change** (update the baseline + record in the behavior delta log + confirm with the user when needed) vs **unintentional change** (roll back).

**No test framework / not directly executable**: you do not need a framework to build a judge. A throwaway parity script (run the target functions on representative inputs, print outputs, diff before/after) is a valid characterization baseline and adds no dependencies — adding a test framework or dev dependency is itself a repo change and requires user consent. If the code cannot be executed in isolation (network/DB/time/hardware dependencies), test at the nearest workable seam instead (CLI entry, public API, module boundary); if no seam exists, either create one as the first refactoring step (extract a thin wrapper), use Sprout/Wrap (add new code without touching the old), or downgrade the aggression level.

**Parity harness** (rewrite/replace-implementation scenarios): pick ~7 representative input scenarios, diff old vs new implementation outputs item by item. Used for L3 subsystem replacement and L4 reference comparison (at L4 a non-empty diff is not failure — differences are redesign output, recorded item by item). Normalize before diffing: strip timestamps/paths/ids, sort unordered collections, canonicalize NaN/Infinity — and if a judge suddenly reports mass failures, suspect the comparator before suspecting the code.

**Judge validation (canary)**: a new judge must be green on original code and turn red when you deliberately break one thing (change an expected value / delete a line). Green lights from an unvalidated judge are never trusted.

## Migration pattern selection table

| Pattern | Selection criteria | Essentials |
|---|---|---|
| In-place incremental micro-loop | Same-language pure refactoring, structural improvement (the default) | Small steps + judge + commit; preceding cleanup pass (remove dead code / normalize style first to cut noise) |
| Branch-by-Abstraction | Replacing an implementation referenced in many places | Build the abstraction → migrate caller by caller → switch to the new implementation → delete old + abstraction; every step compilable and testable; remaining-caller count = progress |
| Expand-Contract | Incompatible interface/data changes | Expand (coexist + dual-write) → Migrate (consumer by consumer) → Contract (remove old); three separately committed stages; checksum comparison for data migration |
| Strangler Fig | Replacing a whole subsystem/service | facade/routing up front, old and new coexist, switch and retire slice by slice; suits systems with real traffic |
| Parallel new codebase + cutover | Wholesale relocation (every file crosses the river, the old is eventually deleted), e.g., language migration | Old and new in parallel + parity harness + disk-as-truth queue; **incremental superset migrations (e.g., JS→TS) are not worth a parallel codebase** |

Under every pattern: a rollback branch before cutover/old-removal points; "don't migrate" is always a legitimate conclusion.

## Execution loop essentials

- **One refactoring action at a time**: one-sentence intent → apply → run the cheap judge → green commit (`refactor:` prefix) / red rollback and split smaller.
- **Judge pricing**: second-level (lint/typecheck/unit tests) every round; minute-level (full build/integration tests) in batches.
- **Pattern-first**: the 2nd occurrence of an error class → the rule is guilty → fix the rulebook → regenerate the whole affected batch; never hand-patch a single file against the rules.
- **Divergent near-duplicates are not duplicate code**: before merging, diff the variants' behavior on real inputs. Identical → merge freely at ≤L2. Divergent → unifying is a behavior change: at ≤L2 keep both or parameterize behind one signature; if unification is the goal, record it in the behavior delta log (≥L3 treatment) or ask the user which variant is canonical.
- **No-op detection**: at wrap-up, confirm the diff reflects the intended structural change, not cosmetic churn — ask "what verifiable change did this diff produce" (for a pure-cleanup pass, say so explicitly).

## Anti-cheating (agent-specific risks)

Test changes must receive adversarial review; watch for the four cheating patterns (all observed agent behaviors in the wild):
1. Copying the code under test into the test file to "remove dependencies";
2. Making tests return early;
3. Generating scripts that print "Test passed!" regardless of outcome;
4. Gutting assertions for a surface-level green.

Rules: never change an assertion to satisfy an implementation — if you believe an assertion is wrong, reproduce and prove it first, then change it, and explain in the commit message. No "0→80% coverage" great leaps (they induce cheating); add tests with seed examples, each individually verifiable. A second perspective (fresh session / independent subagent) re-reviewing all test diffs is a hard requirement (Phase 7 of large refactors).

## Archaeology protocol for deleting code

1. git blame for last-modified time and commit messages;
2. Read adjacent comments and related tests (ugly lines often encode weeks of debugging);
3. Grep all references (including dynamic references in strings/reflection/config);
4. Still unsure → keep and annotate, or ask the user; never delete migrations/lockfiles/fixtures/user data while uncertain.

## Context and parallelism

- Persist the plan/queue to disk and re-read each round; dispatch mechanical bulk changes to subagents that bring back conclusions only (the parallelism sweet spot is low: ≤2 implementation agents, 3-10x token cost; reviewers benefit most from a stronger model / independent context).
- Run exploratory rewrite experiments in a separate worktree; pilot code is discarded, keeping only rule revisions.
- Destructive/irreversible actions (deleting public assets, touching schemas) → user gate.

## Completion checklist

- [ ] Public-surface judge fully green; no unexplained diffs against the Phase 2 baseline
- [ ] No-op detection passes (the diff has real semantic change, or the pass is explicitly labeled pure cleanup)
- [ ] All test changes adversarially reviewed
- [ ] Dead-code deletion carries archaeology evidence; Contract stage done or explicitly tracked
- [ ] Behavior delta log (≥L3) complete, item by item
- [ ] New acceptance standard (L4) passes item by item
