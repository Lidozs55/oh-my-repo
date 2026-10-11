# Documentation Refactoring Guide

Read this when the primary target is docs (README, docs/, ADRs, wikis, API references, tutorials). The industry has no existing practice for docs refactoring (current skills cover code only); the safety nets below are original designs.

## Core principles

1. **One fact, one canonical owner**: every durable fact is authoritatively recorded in exactly one place; everything else links or gives a one-line summary. Duplicated facts are the source of drift — update one place, miss three others.
2. **One type per page (Diátaxis)**: tutorial (follow along) / how-to (solve a task) / reference (look up facts) / explanation (understand why). A page mixing types → split it. To classify a page, ask what the reader does with it.
3. **Docs and code in the same PR**: update docs alongside contract/command/architecture changes; separation is where drift begins.
4. **Dead docs: delete or seal**: when Google shut down a wiki, 90% of documents went unvisited for months — unowned docs are liabilities, not assets. But deletion follows repo-steward's safety classification (migrations/legal/release metadata are protected).
5. **Prefer less**: the default goal is "the smallest coherent doc set", not "a more complete doc system". Before creating a new doc, ask: which existing canonical doc should own this fact?

## Workflow

1. **Inventory**: list every doc → for each, record path, type (one of the four / mixed / none), facts carried, owner (which code/decision), freshness (how far it drifted from code).
2. **Type audit**: mark mixed-type and untyped docs → decide split/merge/delete/rewrite.
3. **Duplicate-fact mapping**: where does the same fact appear → pick (or create) the single canonical owner; the rest become links or get deleted.
4. **Design the new structure**: organize by type (e.g., docs/tutorial, docs/how-to, docs/reference, docs/explain) or by repo convention; produce an old→new path mapping table.
5. **Migrate**: use `git mv` to preserve history; commit content reorganization separately from location moves; run link checks after each move.
6. **Drift repair**: execute command-type content item by item to verify (scriptable parts get spot checks); compile/run code samples; align version numbers, paths, and parameter names with code.
7. **Acceptance** (the safety net): no broken links (including spot-checked external ones); command spot checks pass; no orphan pages (nothing links in); no duplicated canonical facts; every page has a type and an owner; README and docs/ index reach core content in ≤2 hops.

## What the levels mean for docs

- **L1**: fix typos, unify terminology, normalize formatting — zero content change.
- **L2**: reorganize directories, merge duplicates, delete dead docs — **the fact set is unchanged** (every fact remains findable, and easier to find).
- **L3**: documentation-architecture redesign (rebuild the type system, re-partition audiences) + contract-doc updates coupled to code changes — produce an old→new mapping table; for deleted/merged docs, state "where the content went".
- **L4**: start over (e.g., moving from a wiki-style knowledge base to docs-as-code) — define the new audience and journeys first (who, coming to do what, expecting to find it how fast), accept by journey; archive old docs rather than silently vaporizing them (keep one accessible version).

## Anti-patterns

- Generating one-off SUMMARY/ANALYSIS/report documents nobody asked for (repo-steward's output policy applies here too).
- Building hollow directory trees and index pages to "look systematic".
- Rewriting entire pages just to unify tone or format (the docs equivalent of a no-op refactor).
- Writing tutorials as reference manuals (type mismatch is the most common quality problem).
- Typical AI-generated doc noise: paragraphs that paraphrase the code, "In this document, we will..." boilerplate, information-free section headers — prioritize deleting these during rewrites.
