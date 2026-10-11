# Full Refactor Workflow (Phases 0-7)

Applies when: ≥3 modules / >10 files / public contracts or schemas involved / documentation-system restructuring / product operation-logic changes / language or framework migration / the user explicitly says "big refactor". Each phase ends with **evidence artifacts + a gate**: in lightweight scenarios run on and report; in major ones (design approval, contract cutover, old-path removal) the user must green-light the next phase — "human approval = start the next phase".

Plans must be **persisted to disk** (e.g., `docs/refactor-plan.md` or wherever repo convention puts them): context degrades over long tasks, so re-read the plan file each round instead of trusting session memory. Rebuild progress from disk every round (tick off completed items in the queue file); tasks are naturally interruptible and resumable.

**Gate scope rule**: "major work" = any L3+ run on a repo with external consumers, any L4 run, or an expected blast radius >10 files. When the user has already explicitly authorized an L4 redesign, the Phase 0 task card and the Phase 3 design review are still gated (one combined approval is fine), and the Phase 4 plan gate may be merged into Phase 3's. When in doubt, present the artifact and continue non-destructive work instead of idling.

Artifacts: only the plan, the queue, and the rulebook (when fan-out is planned) are files on disk; the other artifacts (task card, recon report, final report) are reported in conversation.

## Phase 0 — Leveling and boundary

- Determine: aggression level (may be granted per block), change boundary (which modules/docs/journeys), project stage (external consumers? persisted schema? API consumers?), constraints (time/compatibility/performance).
- **Feasibility check**: after weighing cost/benefit and risk, "don't refactor / only minimal fixes / defer in stages" is a legitimate conclusion — raise it honestly.
- If the repo root has an existing plan document, read it first (it may be a previously interrupted task).
- Artifact: task card (level × boundary × acceptance standard × rollback strategy). Gate: user confirms the card (for major work).

## Phase 1 — Reconnaissance

- Generate the dependency graph with **deterministic scripts** (grep/AST tools, not memory), at both file granularity and package/module granularity — a missed package-level cycle once caused 16,000 compile errors.
- Blast radius: dependencies and dependents of the target areas, affected-file counts, risk tiers (low/medium/high).
- Test-asset inventory: which tests judge the public surface, which are implementation-coupled, where the gaps are.
- Docs involved: type-audit checklist (see docs-refactor.md). Product logic involved: journey inventory (see product-logic.md).
- Artifact: recon report (dependency graph + radius + asset inventory + gaps). Gate: none (informational), but report back if risk materially exceeds expectations.

## Phase 2 — Judges and safety net

- Test triage: public-surface tests → the final judge, carried to the end; implementation-coupled tests → rewritten as portable assertions that run against both old and new code.
- Untested areas: build characterization tests or a parity harness first (pick ~7 representative scenarios, diff old vs new output), expected values from real runs, baseline including existing bugs. Commit the baseline separately.
- **Judge validation (canary)**: confirm the judge is green on original code and turns red when you deliberately break something. An unvalidated judge is not a judge.
- Record the baseline state (including checks that already failed, to avoid misattributing them to the refactor later).
- Artifact: an executable judge-command list + a committed baseline. Gate: judge red/green validation passes.

## Phase 3 — Design and rules

- Write the **rulebook** (the migration/refactor rule set, stored in the repo — e.g., `PORTING.md` or a section of the plan doc): every decision two execution units might answer differently goes in, **decided once**. One sentence per rule + one positive and one negative example. The entire "prompting" of a million-line production port was a 576-line rulebook.
- Target design: a sketch of the new structure/contracts/journeys, with explicit acceptance standards (L4 especially must define the new standard first).
- **Pilot run**: run the full process on 2-3 representative files; the only outputs are rule revisions and design corrections — pilot code is discarded. For mechanical migrations, try double-translation comparison (one pass following the rules, one uninformed free pass; the diff exposes rule gaps) — one case caught a defect on 3 files that would have polluted 1,448.
- Artifact: rulebook + design doc. Gate: user approves the design (mandatory for major work).

## Phase 4 — Migration plan

- Pick the migration pattern (criteria in code-refactor.md's selection table): in-place incremental micro-loops / Branch-by-Abstraction / Expand-Contract / Strangler / parallel new codebase + cutover.
- **Queue on disk**: list pending units (files/callers/journeys) in a queue file; "done" means the changed file exists on disk; rebuild the remaining queue from disk each round, independent of session state.
- Plan the commit/PR sequence (batch size, order, dependencies) and rollback points (stage-level tags/branches).
- Artifact: queue file + commit-sequence plan. Gate: user approves the plan (for major work).

## Phase 5 — Execution loop

- Micro-loop: one unit at a time → edit → run the cheap judge (seconds: lint/typecheck/related tests) → commit on green, roll back and split smaller on red.
- **Judge pricing**: every judge has a price, and the price decides its place in the loop — second-level judges run every round; minute-level full builds/test suites run in batches.
- **Pattern-first**: individual failures go to a fix loop burning down the queue; **the second occurrence of an error class = the rule is guilty** → fix the rulebook → regenerate the whole affected batch; never hand-patch one file against the rules. Record every rule amendment with a one-line reason in the rulebook; in gated runs, batch-report amendments at the next gate instead of applying them silently.
- **Anti-thrash guards**: max 3 attempts on one unit before treating it as a rule problem; placeholder implementations are forbidden (a stub that cannot pass the judge is a red unit, not a done one); before creating any new helper, grep the repo for an existing one; uncertain edge cases get a `TODO(refactor):` marker, not a guess.
- **Anti-cheating**: adversarial review of test changes; no-op detection (a diff that is only reformat/moves = a fake migration); never change assertions for a green light.
- Context management: re-read the plan/queue each round; dispatch mechanical bulk changes to subagents that bring back conclusions only; run exploratory experiments in a separate worktree.
- Artifact: green commits + updated queue file. Gate: queue empty + full judge green.

## Phase 6 — Contraction and sync

- Contract: remove old paths/compat shims/dual-writes; completion requires verifying that no references and no calls remain.
- Register expiry mechanisms for feature flags and compat layers (owner + removal condition/date); no immortal switches.
- Docs sync: contract changes, command changes, and architecture changes are updated in the **same PR** as the code (docs/code separation is the source of drift).
- Product logic: publish the behavior delta log and migration guide (see product-logic.md).
- Artifact: a clean new world + an expiry task list. Gate: zero-reference verification passes.

## Phase 7 — Verification and delivery

- Adversarial review: an independent perspective (fresh session / separate subagent / another model) re-reviews key diffs and **all test changes**; resolve disagreements item by item.
- Full judge + baseline comparison; no-op detection (did this batch actually produce the intended change?).
- Behavior delta log (≥L3): item by item, `old behavior → new behavior | reason | blast radius`.
- Compact report: what changed, how it was verified, remaining risks, explicit TODOs (expiry tasks / unmigrated list). No one-off report files (unless requested or conventionally required).
- Artifact: final report + a few TODOs; offer to archive the plan/queue/rulebook (e.g., as an ADR) or delete them — they are working state, not deliverables. Gate: user accepts.

## Interruption and recovery

Interrupted at any point: the queue file and plan document are the entire state. Recovery = re-read both + reconcile against `git log`; there is no "resuming the session". When you find a plan document left from a previous run, reconcile before deciding to continue or archive it.
