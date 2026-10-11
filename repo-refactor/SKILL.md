---
name: repo-refactor
description: Deep refactoring, rewriting, and optimization of everything inside a repository - code structure, legacy systems, tech debt, large migrations, documentation overhauls, and product interaction/operation logic. Use whenever the user asks to refactor, rewrite, clean up, or overhaul the codebase or any part of it, mentions tech debt, code rot, legacy code, migration, modernization, architecture adjustment, documentation restructuring, or interaction/operation-flow redesign, or when a planned change is too large or too risky for one edit - even if the word "refactor" never appears. Provides graded aggression levels (behavior-preserving to product-quality-first redesign) and a gated phase workflow for large refactors. For behavior-preserving hygiene passes (redundancy removal, drift repair, AI-output cleanup) prefer repo-steward; this skill is for "get better" redesign, rewrite, and migration work.
---

# Repo Refactor

Refactoring is among the task types where agents fail most often, and the root cause is the harness, not the model. This skill does not teach "how to edit code" — it forces every refactor to first establish the five harness components — **rules (rulebook), judge, queue, gate, rollback** — and then grants freedom by aggression level. Lower aggression means more constraints; higher aggression means more freedom, but also stricter acceptance standards.

## Step one, always: pick the aggression level

| Level | Name | One-line definition | Observable behavior | Contracts |
|---|---|---|---|---|
| L1 | Conservative | Strict Fowler refactoring: behavior-preserving structural improvement | Zero change (bugs included) | Frozen |
| L2 | Standard | Internal cleanup and local improvement | Public surface unchanged | Public contracts frozen, internals free |
| L3 | Bold | Boundary redesign | Controlled change, recorded item by item | Changeable via Expand-Contract |
| L4 | Free | Product-quality-first redesign | Any change; old behavior is not the goal | Can be abandoned wholesale |

Leveling rules:

1. If the user states the level explicitly ("keep it safe" / "go wild" / "ignore compatibility" / "redesign it as your own product") → follow it.
2. Otherwise determine **project stage** first: no external consumers + no persisted-schema burden + no API consumers = dev-stage (0.x / unreleased / internal tool) → default L2-L3, and you may suggest dropping compatibility entirely; released with users → start at L1-L2. In a monorepo, determine stage per package/component; code shared across components is governed by the strictest applicable stage.
3. Big-bang global redesign (L4) is always an **explicit choice requiring user sign-off**, never the default — weird old code carries implicit knowledge, and rewrites have real costs. Likewise, **"don't refactor / make only the minimal fix" is a legitimate conclusion** — raise it honestly after the level assessment.
4. If unsure and the choice would materially change behavior, compatibility, or scope, ask (with your recommendation).
5. For docs or product-logic targets the level meanings differ — read the levels section of the matching reference (docs-refactor.md / product-logic.md) *before* deciding, not after.

For each level's allowed/forbidden lists, safety-net requirements, acceptance standards, and commit discipline: read `references/aggression-levels.md` before making any change.

## Step two: pick the scale

**Lightweight path** (single module, expected ≤ ~5 files, no public contracts touched, the user wants a quick cleanup) → use the micro-loop below directly.

**Full workflow** (any one condition triggers it): spans ≥3 modules or >10 expected files; touches public APIs / CLI / config formats / persisted schemas; documentation-system-level restructuring; product operation-logic changes; legacy modernization or language/framework migration; the user explicitly says "big refactor". → Read `references/workflow-large.md` and execute Phases 0-7.

Anything in between (2 modules, 6-10 files, no contracts) is your call — default to the full workflow when unsure, or ask. Thresholds are estimates, not laws: start lightweight when in doubt, and escalate to the full workflow the moment recon reveals a blast radius beyond the lightweight criteria (a contract gets touched, the radius grows, the baseline cannot be established). Downgrading mid-run is not a thing — finish or explicitly abort.

## Lightweight path: the micro-loop

```
0. Git check: the working tree must be clean (or get the user's confirmation about existing
   changes first); confirm you are on a branch. Not a git repo? That is a risk multiplier: ask
   to `git init` (or take a file-copy snapshot) before starting, or proceed only at ≤L2 with
   smaller steps and an explicit warning that per-step rollback is unavailable.
1. Blast radius: which files will this touch? What depends on them? Report the affected-file
   count and risk tier (low = single leaf module, no contract; medium = multi-module or shared
   helpers; high = any contract/schema/journey touched).
2. Judge in place: find the repo's existing test/lint/build commands, run them once, record the
   baseline (including pre-existing failures). Never touch code without a judge — write
   characterization tests pinning current behavior first (see references/code-refactor.md).
3. Micro-loop (one refactoring action at a time):
   a. State this step's intent in one sentence (extract X / inline Y / move Z)
   b. Apply the change
   c. Run the judge
   d. Green → atomic commit (message prefixed "refactor:"); red → git-roll back this step,
      split the action smaller, retry
4. After all steps, run one broad verification pass (full tests or a wider build) and report
   against the step-2 baseline.
```

## Three-domain routing (each domain has a different safety net)

| Change target | Safety net | Detailed guidance |
|---|---|---|
| Code | Tests / lint / build / parity diff | `references/code-refactor.md` |
| Docs | Type audit + canonical owner + link/command spot checks | `references/docs-refactor.md` |
| Product operation logic (CLI interaction flows, UI journeys, API usage experience) | Journey inventory + current-behavior snapshot + behavior delta log | `references/product-logic.md` |

For mixed changes (e.g., an L4 redesign touching code + interaction + docs), pick the reference matching the primary target; for the other two, at least read their safety-net sections.

## Red lines (effective at every level, ahead of all process)

1. **Judge before blade**, and the judge must be validated: it passes on the original code or fails only in ways recorded as pre-existing in the baseline, and a check that passes at baseline turns red when you deliberately break what it covers. "Green" always means green *relative to the recorded baseline* — no new failures — never "all tests passing" when the baseline itself was red. Never modify an existing test to reach green; pre-existing failures are recorded, not fixed, at ≤L2. An unvalidated judge is not a judge.
2. **Atomic commit on green, immediate rollback on red.** Git checkpoints are the only insurance; knowing the working tree can always be reset is where courage comes from.
3. **Never mix refactoring with feature work** (strictly enforced at ≤L2; at L3/L4, behavior changes and structural migration are also committed separately for reviewability).
4. **Archaeology before deleting code you don't understand**: git blame, adjacent comments, related tests. An ugly line may encode weeks of debugging.
5. **Test changes must get adversarial review**: never change an assertion to satisfy an implementation — if the assertion is truly wrong, prove it first, then change it. Watch for the four cheating patterns: copying the code under test into the test, early-returning tests, scripts that print success regardless of outcome, and gutted assertions.
6. **User gate for irreversible/destructive actions**: deleting public assets, touching persisted schemas, deleting data, removing interfaces that have external consumers.
7. **Contraction must be explicit**: the Contract step (removing old paths/contracts) is either completed (with a verified no-references check) or listed as an explicit TODO. Skipping contraction is worse than not refactoring — every leftover compatibility layer or flag is debt with interest.

## Completion standard

- ≤L1: full judge green relative to baseline; L2: public-surface judge green relative to baseline (green = no new failures vs the recorded baseline) + no-op detection (the diff reflects the intended structural change, not cosmetic churn).
- ≥L3: additionally produce a **behavior delta log** — one line per controlled behavior change: `old behavior → new behavior | reason | blast radius`. L4 must also define and pass a **new acceptance standard** (how product quality is measured — see references/product-logic.md).
- Report compactly: what changed, how it was verified, remaining risks, explicit TODOs. Do not generate one-off report files like REFACTOR_REPORT.md (unless the user asks or repo convention requires one).

## Division of labor with other skills

- repo-steward: hygiene cleanup, redundancy removal, drift prevention (behavior-preserving "get clean"). This skill: "get better" — redesign, rewrite, migrate. The two can be used in sequence. Tie-breaker: if the work only deletes or merges redundant artifacts in place, repo-steward suffices; the moment you restructure across callers (extract, move, rename, re-boundary), it is a refactor — use this skill.
- browser-use (control-browser / web-gui-tester): for "current behavior snapshots" of product operation logic — use them to record existing flows live.

## Reference files

| File | When to read |
|---|---|
| `references/aggression-levels.md` | After leveling, before touching anything — execution detail per level |
| `references/workflow-large.md` | When the full workflow triggers — Phases 0-7 |
| `references/code-refactor.md` | When the primary target is code |
| `references/docs-refactor.md` | When the primary target is docs |
| `references/product-logic.md` | When the primary target is product operation logic/interaction, or when defining the new acceptance standard at L4 |
