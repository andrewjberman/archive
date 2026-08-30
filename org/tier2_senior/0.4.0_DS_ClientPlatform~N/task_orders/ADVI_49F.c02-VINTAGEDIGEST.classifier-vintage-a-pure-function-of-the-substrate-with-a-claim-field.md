# TO ADVI_49F.c02-VINTAGEDIGEST — `_classifier_vintage` becomes a PURE FUNCTION of the loaded classifier substrate (canon-json-v1), with a sibling claim field so a pre-fix random value and a deterministic one are told apart BY THE ROW (cell C02-g-13)

<task_order id="ADVI_49F.c02-VINTAGEDIGEST" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~N</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T14:2xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md -- <owned_cells>C02-g-13</owned_cells></decomp_ref>
<proof_of_spec>
  <expected_criteria>V-1,V-2,V-3,V-4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~N/deliverables/ADVI_49F.c02-VINTAGEDIGEST.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json V-1,V-2,V-3,V-4 ; checker vintage printed, rc read UNPIPED -->
</proof_of_spec>
<status>pending -- GO on delivery of this face. C02-g-10 holds at A7-4 (UNCOMPUTABLE until Monday's 12:45Z fire, filed correctly at 87882) and owes nothing before that fire, so this cell starts now rather than idling the seat ~22 h on a timed read. V-1 is RULED (CTO 87534) -- the code implements exactly that form. Nothing served moves until V-4's named fire; the deploy under this face is sequenced so that Monday's 12:45Z fire is NOT the first exercise of TWO unrelated changes at once unless the seat says so and the before/after separates them (A7-4's read is on `_ingested_at`/`source_pipeline`; V-4's is on `_classifier_vintage` + the claim field -- different columns, separable; the seat states which fire carries V-4).</status>
<priority>P2 -- a served field on 2 tables x 540 dates that changes on EVERY run regardless of content, so a re-run and a real classifier change read identically: a value not carrying its claim, DISCRIMINATION-dead by construction (DS~N 87514, CVO 87528 reproduced 4-for-4). The consumer's real substrate identity meanwhile is the manifest's content_hash.</priority>
<authority>CTO 87534 (V-1 the canonical form + the sibling claim field; the arms; the loader limit); CTO 87522 (the pure-function convention line for every digest field; the digest-field census); CVO 87528 (the channel item; REC (a)+(b), (b) as its own cell); DS~N 87514 (the mechanism at source with the PYTHONHASHSEED control). Rule 13: a DS-lane gold script. D2 drive-pair scope. Not to 4.0.0_SA_CRO.</authority>
</task_order>

## READ THIS FIRST -- the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md`, cell `C02-g-13`** -- V-1's ruled form verbatim, V-2's arms with the failing baseline FIRST, V-3's limit, V-4's serve, and the loader limit. **This face does not restate it.** Where the two differ, the cell governs.

## The one-paragraph version

a07:264-265 digests `str(sorted(ticker_map[t].items()))` where `name_aliases` is a DynamoDB string SET; `str()` of a set is iteration-order dependent under CPython's per-process hash randomisation, so the SAME bytes against the SAME substrate yield a different `_classifier_vintage` on every run (3 runs, 3 vintages, `content_hash` identical; 3 processes differ at the default seed and agree at `PYTHONHASHSEED=0`). Replace the digest with the gate's canonical form (sha256 over canonical JSON of the LOADED substrate: `sort_keys` at every depth, sets → sorted lists, Decimal → str, any other type REFUSED, nothing through `str()`), add the sibling field `_classifier_vintage_form = "canon-json-v1"` on the rows and in the manifest, prove determinism and discrimination in both directions with the failing baseline run first, census every other digest field in a0*..c0* against the same test, and serve it before a named fire.

## Acceptance criteria -- V-1 through V-4, verbatim from cell `C02-g-13`

<criterion id="V-1" cell_refs="C02-g-13"/> **THE CANONICAL FORM as RULED (87534):** `json.dumps(ticker_map, sort_keys=True, separators=(",",":"), ensure_ascii=False, default=canon)` with `canon(set|frozenset) -> sorted(list(x))`, `canon(Decimal) -> str(x)`, `canon(anything else) -> raise TypeError`; sha256 of the UTF-8 bytes, hex; the sibling `_classifier_vintage_form = "canon-json-v1"` on the same rows and in the manifest; nothing in the input passes through `str()`, `repr()` or default container iteration. Commit-gate clean; `safe-commit -F`.
<criterion id="V-2" cell_refs="C02-g-13"/> **THE ARMS:** (i) DETERMINISM -- three processes at the default seed over the same loaded substrate -> ONE value; **the failing baseline (the current code, 3 values) run FIRST**; the mutation restoring `str(set)` fails it; AMENDED 14:4xZ (gate 87997): the seeds are NAMED (distinct fixed PYTHONHASHSEED values -- seed-independence is the property; a default-seed disagreement can pass by luck); the baseline over a FROZEN substrate; the legacy-form arm committed as a standing failing baseline. BUILT @1befd43cef and already SERVED (e0bde0a5... at the 14:42Z window); the cell governs. (ii) DISCRIMINATION both directions -- one alias ADDED in a scratch copy -> a DIFFERENT value; one alias REORDERED (same set, different insertion order) -> the SAME value; (iii) `content_hash` unchanged by the fix; (iv) THE DIGEST-FIELD CENSUS -- every field in a0*..c0* whose name or producer marks it a hash/digest/vintage run through arm (i), denominator = fields found, corpus named; `content_hash` expected to pass; any other failing is a FINDING routed to the issuer, not fixed here.
<criterion id="V-3" cell_refs="C02-g-13"/> **THE LIMIT, on the cell:** the 1,080 stored partitions keep their random vintages, distinguished BY THE CLAIM FIELD (`_classifier_vintage_form` ABSENT vs `canon-json-v1`), never by value or deploy date; a re-stamp of history is its own never-widen act and whether it is cut at all is the issuer's question at this cell's close. The loader limit stated: the form is over the LOADED substrate; an order-dependent loader would still move the digest and arm (i) catches it as the loader's, named separately.
<criterion id="V-4" cell_refs="C02-g-13"/> **THE SERVE:** deployed under the index-blob identity (22a; ledger opened/closed on the running-artifact read) before a NAMED 12:45Z fire; two consecutive fires with an unchanged substrate carry the SAME `_classifier_vintage` and `_classifier_vintage_form = "canon-json-v1"`, read from the S3 objects on both tables. Proof positional V-1..V-4, checker vintage printed, rc unpiped; graded by `3.0.0_SA_CVO`.

## Do NOT

- ⛔ **Do not touch a06, a00, or a07's provenance lines** (C02-g-8's, C02-g-10's) -- one field, one cell.
- ⛔ **Do not re-derive history** -- the claim field is the boundary, not a backfill.
- ⛔ **Do not fire a dated production run**; the serve is read on the scheduled fire the seat names.
- ⛔ **Do not `cp` from the worktree** for the deploy digest -- the index blob is the identity (22a; nine CRLF worktrees in this directory today).
- ⛔ Nothing to `4.0.0_SA_CRO`.

## Reporting

V-1 + V-2 as one message (the baseline's three values, the arm outputs, the census denominator) to the issuer + CTO; V-3 on the cell; V-4 on the fire read to issuer + CTO + CVO; the proof at the close. Surprise channel: one line to `3.0.0_SA_CVO` cc issuer.
