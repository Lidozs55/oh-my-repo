# Aggression Level Execution Detail

Leveling happens in step one of SKILL.md; this file holds each level's allowed/forbidden lists, safety nets, acceptance, and commit discipline. Principle: **higher aggression means more freedom but stricter acceptance** — delegation is not abdication.

**Defining the public surface** (needed at ≥L2): the public surface is everything a consumer *outside the boundary you are allowed to change* can observe. In practice: for a published library, its exported API; for an application, its entrypoints and their I/O (CLI arguments/output/exit codes, config files, persisted schemas, network APIs, machine-readable logs); for an internal module, its direct importers are the consumers — grep the import/require sites to enumerate them. When the boundary is ambiguous, treat the wider surface as public.

---

## L1 Conservative (strict Fowler refactoring)

**Essence**: behavior-preserving structural improvement. Refactoring by definition means "adjusting structure without changing observable behavior" — at this level a bug is also behavior, and fixing it is a violation.

**Allowed**: extract/inline functions and variables, move code, rename, deduplicate, simplify conditionals and control flow, eliminate magic numbers, replace conditionals with polymorphism, and other Fowler moves; semantics-preserving performance optimization (with benchmark evidence).

**Forbidden**: any observable behavior change; changing output, return values, logs, or error-message text; bug fixes (record bugs separately and handle them in their own change); changing the semantics of any interface, public or internal (signatures may change, semantics may not).

**Safety net**: full test suite green relative to the recorded baseline (pre-existing failures are recorded, not fixed, at this level). In a repo without tests, first write characterization tests pinning current behavior: for every function you will touch, use real execution results as expected values (never fill them in from guesses), include existing bugs in the baseline, and commit the baseline separately before starting.

**Acceptance**: full judge green relative to baseline + (on critical paths) an empty before/after output diff.

**Commit discipline**: one `refactor:` commit per atomic move, with the message naming the technique used.

**User prompt signals**: "keep it safe" / "don't change behavior" / "pure refactor" / "safe refactor".

---

## L2 Standard (internal cleanup and local improvement)

**Essence**: public contracts frozen, internals free. Internal boundaries may be redrawn as long as the public surface stays identical.

**Allowed**: everything in L1 + redrawing internal APIs, merging/splitting files and modules, deleting dead code (after archaeology), replacing internal implementations, removing pressure-free internal abstractions, paying down small-scale tech debt.

**Forbidden**: changes to public API signatures or semantics, CLI arguments, config formats, persisted schemas, machine-readable parts of logs, external error codes.

**Safety net**: two judge layers — public-surface tests (the final judge, carried to the end) + implementation-coupled tests (rewritten as portable assertions that run against both old and new implementations). Where the public surface lacks tests, first add characterization tests covering public behavior.

**Acceptance**: public-surface judge green + no public-surface entries in the change list + no-op detection passes.

**Commit discipline**: one commit per internal-boundary migration step; dead-code deletion in its own commit with archaeology evidence in the message (e.g., "last touched 2023-x, no callers, grep-verified").

**User prompt signals**: "tidy this up" / "clean up the tech debt" / "do whatever you like internally, just don't touch the interface".

---

## L3 Bold (boundary redesign)

**Essence**: contracts may change, but change is a controlled process. Product/module boundaries are redrawn and public contracts updated.

**Allowed**: everything in L2 + public-contract changes (via the Expand-Contract pattern — Expand → Migrate → Contract, three separately-committed stages), module reorganization, replacing subsystems with Strangler / Branch-by-Abstraction, data-format migration.

**Process skeleton**:
1. Expand: new and old contracts coexist (new path + compat shim / dual-write).
2. Migrate: migrate caller by caller (treat the grepped caller list as the implicit contract; migrate and verify one at a time; "remaining caller count" is the progress metric). Every step stays compilable and testable.
3. Contract: remove the old path; completion requires verifying that no references and no calls remain.

**Forbidden**: skipping Contract (either finish it or list it as an owner-assigned explicit TODO — compatibility layers are debt with interest; the Knight Capital incident was caused by a stale flag); unrecorded behavior changes; one-shot big-bang cutover (unless the user approves).

**Safety net**: L2's two judge layers + contract tests (representative cases for both old and new callers) + dual-write verification for data-migration scenarios.

**Acceptance**: new-contract judge green + complete behavior delta log (each entry: `old behavior → new behavior | reason | blast radius`) + a migration guide exists (old→new mapping table, plus a codemod when automatable) + Contract done or explicitly tracked.

**Commit discipline**: the three stages commit separately; behavior changes and structural migrations in separate commits for reviewability.

**User prompt signals**: "redesign the interface" / "this module boundary is wrong" / "contracts can change but keep it smooth".

---

## L4 Free (product-quality-first redesign)

**Essence**: old behavior and contracts **are not the goal**; the new product quality standard is. Local or even global redesign and re-orchestration are allowed.

**Preconditions** (all required):
1. dev-stage (no external consumers + no persisted-schema burden + no API consumers — with all three absent, compatibility can be dropped wholesale), or the user explicitly authorizes "go wild / ignore compatibility".
2. **The new acceptance standard is defined**: product quality must be operationalized — every core journey has a verifiable standard (step count, recoverability, error-message comprehensibility, latency...). Otherwise "quality first" degrades into "I feel it's better".
3. A bakeoff/pilot is done: first run a discardable pilot scaled to the blast radius (for small scopes an adversarial design review alone suffices), whose only outputs are rule revisions and design corrections — pilot code is thrown away. For redesign-type migrations, use adversarial design-document review instead of double-translation comparison.

**Allowed**: globally redesigning architecture, data flow, or interaction; removing old paths without compat; rewriting instead of going incremental; re-orchestrating how modules coordinate; retiring entire subsystems; behavior diverging from the old version arbitrarily.

**Still forbidden**:
- Treating "I feel it's better" as acceptance — everything is judged against precondition 2's new standard.
- Making features vanish without a trace — even when dropping compatibility entirely, leave a changelog and a one-line migration note (future you and your teammates are also users; SemVer 0.x allows breakage, but not silent breakage).
- Irreversible actions without a gate: deleting data, breaking schemas, or removing assets with external consumers still requires user approval. A gate means "human approval = start the next phase", not asking at every step.

**Safety net**: build judges oriented to the **new** contracts (write acceptance tests for the new journeys first); the old code serves as a reference implementation (parity comparison may inspire, but a non-empty diff no longer counts as failure — differences are the redesign's output, recorded item by item in the behavior delta log).

**Acceptance**: every item of the new acceptance standard passes + a complete behavior delta log (old→new mapping, including "what was deleted and why") + changelog/migration guide + adversarial review (an independent perspective re-reviews design decisions and test changes).

**Commit discipline**: staged large commits + per-stage tags/branches for whole-stage rollback; each stage boundary is a safe stopping point.

**User prompt signals**: "go wild" / "redesign it as your own product" / "don't care how the old version did it" / "start over from scratch".

---

## Self-check while leveling

- What users call "refactoring" is often really L3/L4 redesign — align on the level before starting; avoid doing L4 work under an L1 label.
- Conversely, an "incidental small change" on a released product is often a contract change in disguise — the moment a public-surface entry appears in the change list, upgrade the process or shrink the change.
- One task can have per-block leveling: "core modules L1, peripheral tools L4" — write each block's level into the task card.
