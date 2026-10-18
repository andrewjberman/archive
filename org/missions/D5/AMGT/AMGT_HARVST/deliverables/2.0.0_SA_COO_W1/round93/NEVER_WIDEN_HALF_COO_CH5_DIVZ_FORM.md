# NEVER-WIDEN -- COO HALF: one `research-fund-form` object (method version 2) is written for DIVZ, with 0 reports and an absent reason (`HVST-ch-5`, round 93, workstream DIVZ-WRITE)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-18 ~04:1xZ UTC. **Authority:** the CTO's `cf-5` half (`ledger/NEVER_WIDEN_CF5_FUND_FORM_V2_CTO_HALF.md` @78b98db60d, condition 2: DIVZ "resolves to a version-2 form with 0 reports and an absent reason"), his D1-S52 ruling (@162d5a6934, item 2: "with DIVZ") and his round-92 analysis item 1; `HVST-ch-4` (merged `2e0dc6af2e`; census re-run by the issuer: `FORM DIVZ reports=0 object=a181f84957dbb8b7.json content_sha256=34524f75 stored=absent`, IDVZ and PFOE `stored=equal`).

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`, from a worktree at commit `2e0dc6af2e` (or a later commit whose `lib/research/` tree is byte-identical to it, proven by an empty `git diff 2e0dc6af2e <commit> -- lib/research`): (0) BEFORE, read only: build the DIVZ form IN MEMORY (`fund_form.gather_items`, `build_document`, `_inputs_sha16`) and print it; it must equal the measurement below; list the stored `research-fund-form` objects (expected 11: IDVZ x5 and PFOE x5 of which one each is version 2, DIVZ x1 version 1). (1) WRITE the ONE object with a driver `ch5_run.py` built on `fund_form` that calls `gold.gold_put("research-fund-form", "fund=divz", "a181f84957dbb8b7.json", payload)` for the DIVZ document only (never `fund_form --write`, which attempts all three funds). (2) READ THE OBJECT BACK and check it (Branch A). (3) AFTER: `fund_form.read_latest("DIVZ")` returns the new object; `substrate._pick_stored("research-fund-form", "fund=divz", fund_form.current_inputs("DIVZ"), fund_form.METHOD_VERSION, client)` returns it with `current` True; `fund_form --compare` (read only) runs to completion over the three funds (it raised on DIVZ before). NOTHING else is built or written.

## THE MEASUREMENT (read by the issuer)

- **The DIVZ form the changed code builds:** object `a181f84957dbb8b7.json`, `content_sha256` `34524f75...`, `fields.reports` 0, `skeleton` empty, `by_class` empty, `fields.absent` `no report whose silver row states fund_relation == holding names DIVZ`, `inputs` `[]`, `method_version` `"2"`. IDVZ (`65a5baab3afd06f0.json`, 82 reports) and PFOE (`57cee6de8b2cd85e.json`, 33 reports) are byte-equal to the stored version-2 objects, so this act does not touch them.
- **The stored forms today:** 11 objects (the 9 version-1 forms and the 2 version-2 forms written by `HVST-cf-5`); DIVZ has one version-1 object (`e19a2eb0a66b84a2.json`, 2 reports counting candidate and misfiled reports).

## THE PROPERTY AND ITS WRITERS (printed, CLAUDE.md section 5)

The property moved is the set of `research-fund-form` objects that `substrate._pick_stored` and `fund_form.read_latest` resolve for DIVZ. **N = 1 writer:** `lib/research/corpus/fund_form.py` (`gold.gold_put`; `write()` and this act's driver both end in it). The rule is read: an object named `<sha16 of method_version + sorted inputs>.json`, never overwriting. No schedule runs it (the issuer's `cf-5` read; the seat reads again, step 0).

## WHAT THIS CHANGES IN THE WORLD (named)

- **One gold object is ADDED; none is changed or deleted** (`research-fund-form/fund=divz/a181f84957dbb8b7.json`). The gold writer never overwrites; the version-1 DIVZ object stays.
- **Which form a reader gets for DIVZ:** before, `_pick_stored` returned the stale version-1 object with `current` False (the fallback by key order of `substrate.py` line 158, the second fallback `HVST-ch-1` names); after, it returns the new object with `current` True, and `read_latest("DIVZ")` no longer raises.
- **What changes in what is SERVED: NOTHING.** No served gateway tool reads a fund form, and no security's gold `fund_of_record` is DIVZ today (DIVZ is named only by two `CLX` candidate reports), so no dossier or continuation reads this form. The seat proves it: the gateway read of `UNH_US_Equity` before and after is equal.
- **Not touched:** silver, bronze, any continuation or dossier, the gateway, IAM, schedules, Terraform, the IDVZ and PFOE forms.

## BOTH BRANCHES (the half is not signed unless it covers both)

- **Branch A (the object read back equals the build):** `subject.fund` is `DIVZ`, `method_version` `"2"`, `fields.reports` 0, `fields.absent` as above, `inputs` `[]`, the recomputed `content_sha256` equals the stored one, the object name equals `_inputs_sha16([])`.
- **Branch B (it differs in ANY of those, or `put_performed` is false, or the in-memory build before the write differs from the measurement):** STOP; before the write, write nothing; after the write, nothing else is started. A written object cannot be unwritten: the repair is a still NEWER object from a corrected run, decided by the issuer and the CTO; the seat deletes nothing.

## CONDITIONS

- **C-1.** The code is the tree at `2e0dc6af2e` (empty `lib/research` diff proof printed in `ch5_before.out`); only the DIVZ object is written.
- **C-2.** A change-management ledger entry is open at the start and CLOSED and COMMITTED at the end (NEVER-2; `org/critical_paths/change_management/` and the sentinel `org/critical_paths/.open_deploys/harvst-ch5-divz-form-v2.json`), with the window and the manifest.
- **C-3.** The put is recorded in `ch5_written.out` the moment it lands (key, VersionId, bytes, sha256, UTC); the manifest IS the rollback list and is committed with the ledger close.
- **C-4.** The write principal is the one dell1's harvest tooling already holds; NO grant, key or policy is requested; an AccessDenied or an `IfNoneMatch` conflict is a STOP.
- **C-5 (the S44 rule).** FOREGROUND, `python -u`, output appended to a log file; no `nohup`, no detached process, no retry loop; a missing object, an error or silence is a STOP with the exact text.
- **C-6.** **C-6 of the `cf-5` pair (no dossier or continuation `write_one`) stays in force for every name with no `/5` continuation until `HVST-ch-1` and `HVST-ch-2` are merged and their censuses read 0 differing (the CTO's ruling @162d5a6934).** This act lifts ONLY the DIVZ-form part of it (a build that reads DIVZ's form resolves the new object once this ledger is closed).
- **C-7.** UNH control: `UNH_US_Equity` read through the gateway BEFORE and AFTER with `fields` `["fund_of_record","last_stated_position"]`; every returned field entry, `content_sha256`, `source_keys` and `research_reports[]` entry equal.
- **C-8.** No Terminal, queue or Bloomberg use; no S3 delete by the seat; NO call of `etfs_compare_peers` on the gateway (site Z row `Z-S375`).
- **C-9 (site Z told first).** Before the write the issuer asks `0.0.0_AB_MSTR~DELL1` to tell site Z the window, the table prefix and the one object, and that a site Z write to `amgt/harvest/gold/research-fund-form/` in flight is a STOP; the issuer sends GO with site Z's answer.

## ROLLBACK (stated honestly)

The act is ADD-ONLY; the pre-act state returns when the one new key is removed, which is an S3 delete: Andrew's act, not the seat's and not pre-approved here. Removing it restores exactly the pre-act resolution (the stale version-1 DIVZ form, `current` False). The manifest lists the key and VersionId.

## WHAT THIS DOES NOT COVER

The picker fix and the shared classifier (`HVST-ch-1`, `-2`); the `/5` rebuild (`HVST-ch-7`); a rebuild of any dossier or continuation; the second key-order fallback of `substrate.py` line 158 (a row of `ch-1`).

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
