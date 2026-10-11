# PART 2c -- can a firm free-name a comparison model, and does the composition's writer enforce its schema (2026-10-11 ~20:5xZ)

Seat: 2.0.0_SA_COO~T2 (cell TR-cn-23). Asked by 1.0.0_SA_CTO~DELL2 msg 5761 ("One more read, code only, because it is what DOES leave
today"). Code read only, in `infra/aws/lambda/investor-reporting/`; no table, model or client record was read.

## 1. Answers

| question | answer |
|---|---|
| Can a firm free-name a model in the catalogue? | **NO, by the code read.** A comparison name is one of two things, and a firm types neither |
| Could a comparison name carry a client's name? | Not through the catalogue. Only if a seat commits one, or the classification table holds one |
| Does the composition's writer enforce its schema? | **YES.** The closed schema is validated at submission and again at worker replay; a non-conforming document is refused |

## 2. Where a comparison name comes from (`_scope/maintained_sources.py`, lines 596-632)

For each key the advisor PICKED, the server looks it up; it never takes a name from the browser.

| source | what it is | who authors the name | how many |
|---|---|---|---|
| the packaged catalogue: `ycharts/generate/templates.json` `comparison_catalog.entries` | a committed config file, deployed with the function | a seat. The loader REFUSES the file unless `maintainer` reads `2.0.0_SA_COO~Y` and the version reads `irpt-ycharts-comparison-candidate.20260927.v2` | 4 entries today: Opal Long-Term, Opal Short-Term, Opal Intermediate-Term, Opal Ultra Long-Term. `permitted_firm_ids` is empty on all four |
| the classification table: DynamoDB `etf-classifications` (`_classified_etf`, lines 545-558) | a ticker's `name` attribute; the key must match `[A-Z][A-Z0-9.]{0,9}` | whoever writes that table: MDPF_SECCLASS (the code names `2.0.0_SA_COO~M` as source owner) | read live on 2026-10-01 by its author: 2,309 ticker rows, 317 named (the module's own note; not re-read here) |
| anything else | REFUSED: `comparison key unknown or ambiguous` | -- | -- |

A firm has no route to add an entry: the catalogue is a file in this repo, and a firm principal "never carries a firm catalogue"
(`_scope/tests/test_resolve.py:191`, `test_global.py:137`, by their test names; the tests were not run here). So the names that reach
Moonshot today are Opal's four model names, or an ETF's fund name for a ticker the advisor picked.

## 3. The composition's writer enforces the closed schema

`ycharts/generate/composition_admission.py` `CompositionAdmission.validate` runs a JSON Schema Draft 2020-12 validator built from the
checked-in `RequestComposition.schema.json`, then the cross-field bindings, and raises `SubmissionRefused("CLOSED_COMPOSITION_REQUIRED")`
on any failure. It is constructed or called at 6 product sites in 5 files (tests excluded):

- submission: `custody_submission.py:62`, `prospect_submission.py:42`, `submission_service.py:93` and `:132`;
- worker replay: `frozen_worker.py:51`;
- the resident's install: `resident_installed.py:396`, which also refuses to install if the schema file is missing (`:158`).

So a stored composition cannot carry a top-level `commentary_basis`: the schema's top level is closed (5 properties,
`additionalProperties: false`) and admission refuses anything else. That strengthens PART 2b: producing the three free-text members
would need a schema change first, which is a contract change under a pair, not a quiet code edit.

**A limit of that guarantee.** The schema's `resolved` block declares no properties and no `additionalProperties` rule (read from the
schema file), so `resolved` is OPEN at the schema level; what it may hold is fixed by `validate_bindings` and the composer, not by the
schema. `commentary_basis` is read from the top level, so this does not reopen it, but a future reader that took a member from
`resolved` would not have the schema's protection.

## 4. Not measured

- Who can write the `etf-classifications` table, and what its 317 names are. A name there is sent verbatim when its ticker is picked.
  The table is MDPF_SECCLASS's; the read of its writers (IAM) and of its name values is that project's.
- That the deployed functions run this code (this is a read of the repo at box/dell2 HEAD, not of deployed bytes).
- The two tests named in section 2 were read by name, not run.

## 5. What it means for the call

With PART 2 and PART 2b: the request content reaching Moonshot today is the variant (1, 2 or 3) and comparison names drawn from four
Opal model names and ETF fund names. No member typed by an advisor or a client reaches it. The one open edge is the names held in
`etf-classifications`.
