# NEVER-WIDEN -- COO HALF: two `research-fund-form` objects (method version 2) are written, one for IDVZ and one for PFOE (`HVST-cf-5`, round 92, workstream FUNDFORM-REBUILD)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-18 ~02:2xZ UTC. **Authority:** the CTO's round-91 analysis (`ledger/ROUND_ANALYSIS.round91.md` @9bdb466396, msg 7773) item 2 ("fund_form, cf-3 then cf-5, after item 1 lands: fund_form counts holding reports only and drops the two misfiled Mexico reports; built on the new silver and rebuilt under its own pair; its dossier-build hazard holds: the code lands only together with newly written fund forms"); `HVST-cf-3` (merged `04be089e13`; census re-run by the issuer: `funds=2 reports_before=139 reports_after=115 dropped_nonholding=22 dropped_misfiled=2`, IDVZ 94 to 82, PFOE 43 to 33, DIVZ 2 to 0); `HVST-cg-2` (the silver rewrite, ledger closed `8225380445`).

**A CORRECTION TO WHAT THE ISSUER WROTE ABOUT THE HAZARD (decomposition section 121, the `cf-3` design note and the `cf-3` close note said a dossier build finds NO stored fund form until this act).** Read at `lib/research/corpus/substrate.py` lines 121-159: when no stored form's `inputs` equal the current inputs, `_pick_stored` returns the lexicographically LAST stored object under the partition with `current` False; it returns "absent" only when the partition holds no object. So a dossier built after `HVST-cf-3` and before this act would NOT fail: it would SILENTLY cite the stale version-1 form (which counts candidate reports and the misfiled ones). That is the real hazard this act closes, and it is the reason no dossier is built between the two.

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`, from a worktree at commit `04be089e13` (or a later commit whose `lib/research/` tree is byte-identical to it, proven by an empty `git diff 04be089e13 <commit> -- lib/research`): (0) BEFORE, read only: build both forms IN MEMORY (`fund_form.gather_items`, `distinct_funds`, `_inputs_for_fund`, `build_document`, `_inputs_sha16`) and print, per fund, the report count, the section count, the object name and the document `content_sha256`; they must equal the measurement below; list the stored `research-fund-form` objects (expected: the version-1 objects of IDVZ, PFOE and DIVZ). (1) WRITE the two forms as SEPARATE foreground commands, PFOE (33 reports, the canary) then IDVZ (82), each a driver `cf5_run.py --fund <FUND>` built on `fund_form` that gathers, builds and calls `gold.gold_put("research-fund-form", "fund=<slug>", "<inputs_sha16>.json", payload)` for that one fund. (2) After each, READ THE OBJECT BACK and check it (Branch A below) before the next. (3) After both: `fund_form.read_latest("IDVZ")` and `read_latest("PFOE")` return the new objects; `read_latest("DIVZ")` raises `LookupError` (EXPECTED: no holding report names DIVZ, so there is no current DIVZ form; the version-1 DIVZ object stays); the substrate member `_fund_form_member` for UNH (fund of record PFOE) and CPA (IDVZ) returns the NEW object with `current` True and `method_version` "2"; and an IN-MEMORY `dossier.build` of `UNH_US_Equity` and `CPA_US_Equity` equals the stored served dossier in every field except `fund_form_ref` (which now names the new object). NOTHING is built or written beyond the two forms.

## THE MEASUREMENT (every number read by the issuer; the census is the issuer's own re-run of `cf3_census.py`, identical to the worker's)

- **After the `cf-3` rule, per fund:** IDVZ 82 reports, PFOE 33 reports, DIVZ 0 (so two funds get a form). The census totals: `reports_before=139 reports_after=115 dropped_nonholding=22 dropped_misfiled=2 absent_before=210 absent_after=232`; the 22 non-holding drops: `candidate` 14, `initiate` 2, `interest` 2, `template` 1, `none` 3.
- **The stored forms today:** version `1` objects for IDVZ, PFOE and DIVZ (counting candidate reports, the misfiled reports and three bare-token "reports"); none is changed or deleted.

## THE PROPERTY AND ITS WRITERS (printed, CLAUDE.md section 5)

The property moved is the set of `research-fund-form` gold objects that `substrate._pick_stored` resolves for a fund. **N = 1 writer:** `lib/research/corpus/fund_form.py::write` (`gold.gold_put`, called from `_run_write`; `--write` is the CLI); this act calls the same `gold_put` per fund through a driver. The rule is read: one object per distinct fund of the holding reports, named `<sha16 of method_version + sorted inputs>.json`, never overwriting. No schedule or trigger runs it (`HVST-ce-1` section (g); the issuer's `cg-2` seat read of the scheduled tasks found none for `typed.main`; the seat reads again for `fund_form`, step 0).

## WHAT THIS CHANGES IN THE WORLD (named)

- **Two gold objects are ADDED; none is changed or deleted** (`research-fund-form/fund=pfoe/<sha16>.json` and `.../fund=idvz/<sha16>.json`, method version `2`); at most 2 keys. The gold writer never overwrites; the version-1 objects stay.
- **Which form a reader gets:** for IDVZ and PFOE `_pick_stored` now finds an object whose `inputs` equal the current inputs and returns it with `current` True (before, it returned the stale version-1 object with `current` False). For DIVZ it still returns the version-1 object with `current` False (no current form exists; no security has a continuation `fund_of_record` DIVZ).
- **What changes in what is SERVED: NOTHING.** No served gateway tool reads a fund form; the stored dossiers keep citing the version-1 forms in their `fund_form_ref` until a dossier is rebuilt, which this act does not do and no schedule does. The seat proves it: UNH and CPA read served through the gateway before and after are equal.
- **Not touched:** silver, bronze, any continuation or dossier object, the gateway code and service, IAM, schedules, Terraform; the stored version-1 forms.

## BOTH BRANCHES (the half is not signed unless it covers both)

- **Branch A (the object read back equals the build):** `subject.fund` is the fund, `method_version` is `"2"`, `fields.reports` is 33 (PFOE) or 82 (IDVZ), the `inputs` list has that many entries, the recomputed `content_sha256` equals the stored one, the object name equals `_inputs_sha16(inputs)`. The next fund starts.
- **Branch B (it differs in ANY of those, or `put_performed` is false, or the build differs from the measurement before the write):** STOP before any further write; record the exact difference. A written object cannot be unwritten: the repair is a still NEWER object from a corrected run, decided by the issuer and the CTO; the seat deletes nothing.

## CONDITIONS

- **C-1.** The code is the tree at `04be089e13` (the empty `lib/research` diff proof printed in `cf5_before.out`); the funds are exactly IDVZ and PFOE; no other fund is written by hand.
- **C-2.** A change-management ledger entry is open at the start and CLOSED and COMMITTED at the end (NEVER-2; `org/critical_paths/change_management/` and the sentinel `org/critical_paths/.open_deploys/harvst-cf5-fund-form-v2-rebuild.json`), naming the bucket, the table prefix, the window and the manifest.
- **C-3.** Every put is recorded in `cf5_written.out` the moment it lands (key, VersionId, bytes, sha256, reports, UTC); the manifest IS the rollback list and is committed with the ledger close.
- **C-4.** The write principal is the one dell1's existing harvest tooling already holds; NO grant, key or policy is requested; an AccessDenied or an `IfNoneMatch` conflict is a STOP.
- **C-5 (the CTO's S44 rule).** One fund per command; EVERY command is FOREGROUND with `python -u` and its output appended to a log file; NO `nohup`, no detached or background process; after each fund read the manifest and confirm the object is present before the next; a missing key, any error or silence is a STOP; no retry loop.
- **C-6.** **NO dossier or continuation `write_one` is run by anyone from the `cf-3` merge until this ledger is closed** (the stale-citation hazard above); the in-memory `dossier.build` of step (3) writes nothing.
- **C-7.** UNH and the CONTROL: `UNH_US_Equity` and `CPA_US_Equity` are read served through the gateway BEFORE the first write and AFTER the last, with `fields` `["fund_of_record","last_stated_position"]`; every returned field entry, `content_sha256`, `source_keys` and `research_reports[]` entry is equal (the `fund_relation` key is now served on both, equal before and after).
- **C-8.** No Terminal, queue or Bloomberg use; no S3 delete by the seat; NO call of `etfs_compare_peers` on the gateway (site Z row `Z-S375`); do NOT run `fund_form --compare` (its `read_latest("DIVZ")` raises by design).
- **C-9 (site Z told first).** Before the first write the issuer asks `0.0.0_AB_MSTR~DELL1` to tell site Z the window, the table prefix and the two fund partitions, and that a site Z write to `amgt/harvest/gold/research-fund-form/` in flight is a STOP; the issuer sends GO with site Z's answer.

## ROLLBACK (stated honestly)

The act is ADD-ONLY; the pre-act state returns when the two new keys are removed, which is an S3 delete: Andrew's act, not the seat's and not pre-approved here. Removing them restores exactly the pre-act resolution (the stale version-1 form with `current` False), which is also the state before `HVST-cf-3`'s rule existed in the bucket. The manifest lists both keys and VersionIds. The 33-report PFOE canary bounds the first exposure.

## WHAT THIS DOES NOT COVER

A rebuild of any dossier or continuation (a later act, the CTO's call, so that stored dossiers cite the new forms); a DIVZ form (none exists to write); the shared classifier of gold and silver (row `D1-S49`, round 93); the `--compare` CLI's behaviour on DIVZ.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
