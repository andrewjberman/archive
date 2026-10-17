# NEVER-WIDEN -- COO HALF: the gold continuation and dossier objects of 17 securities are rebuilt so no candidate reads as a fund of record and no description paragraph reads as a position (`HVST-cf-4`, round 91, workstream CS61-REBUILD)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-17 ~21:4xZ UTC. **Authority:** the CTO's round-90 analysis (`ledger/ROUND_ANALYSIS.round90.md` @307764abfe, msg 7721) item 2 ("the forward rebuild of the affected names writes NEWER objects under its own never-widen pair; no delete. Proof: MNST served with no PFOE fund_of_record, UNH unchanged, and a control") and msg 7735 (the holding classification ratified; the four JP names join); `HVST-cf-1` (merged `934ecb88c5`); `HVST-cf-2` (merged `80d0701876`).

**THIS HALF CORRECTS A CLAIM THE ISSUER SERVED.** Round 90's rebuild (`HVST-ce-4`) wrote `fund_of_record` `PFOE`/`IDVZ` for nine names from lines that say only `CANDIDATE FOR ...` (the issuer read those lines as stated positions). This act writes NEWER objects that withdraw that claim, and does the same for four names that serve a company-description paragraph as a position and four older names served the same way before round 90.

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`, from a worktree at commit `80d0701876` (or a later commit whose `lib/research/` tree is byte-identical to it, proven by an empty `git diff 80d0701876 <commit> -- lib/research`): for each security in `deliverables/2.0.0_SA_COO_W1/round91/cf4_securities.txt` (17 names, sha256 `221a63c311c9d0f13baeff2a346169b62f27cec7d32c33270ba1b2e1ac58ee48`): (1) BUILD without writing (`continuation.build(security_key)`) and print `fund_of_record` and `last_stated_position`; (2) WRITE `continuation.write_one(security_key)`, then (3) `dossier.build(security_key)` in memory and print, then (4) `dossier.write_one(security_key)`; (5) read the result on the served gateway tool. Canary first: `MNST_US_Equity` then `8306_JP_Equity`, read served, then the other 15, each as a separate FOREGROUND command with unbuffered output.

## THE PROPERTY AND ITS WRITERS (printed, CLAUDE.md section 5)

The property moved is the served `fund_of_record` and `last_stated_position` of a security. **N = 2 writers:** `lib/research/corpus/continuation.py::write_one` (the derivation `_resolve_fund_and_position` after `HVST-cf-2`) and `lib/research/corpus/dossier.py::write_one` (copies both fields from the stored continuation, `dossier.py` lines 1490-1502). Both rules are read. No schedule or trigger runs them (`HVST-ce-1`, section (g)).

## WHAT THIS CHANGES IN THE WORLD (named)

- **Gold objects are ADDED; none is changed or deleted.** For each of the 17 securities two NEW objects (`research-continuation/security_key=<KEY>/<sha16>.json`, method `amgt-corpus-continuation/5`, and `research_dossier/security_key=<KEY>/as_of=<as_of>.<sha16>.json`) in `opal-data-harvest`; at most 34 keys. The gold writer never overwrites; the old objects stay; the gateway serves the newest, so the NEW objects become what `harvest_get_research` returns for these 17 at once.
- **What changes in what is served, per the `HVST-cf-2` census (`cf2_census.out`, 94 of 94, the same fetched extractions, both rules run, baseline pinned at the round-90 commit `dca8722353`):** (a) 13 securities (`8035_JP`, `ADBE`, `BZLFY`, `CDNS`, `CELH`, `CLX`, `CNR`, `HEI`, `ML_FP`, `MNST`, `MSCI`, `SNPS`, `ST_SP`) go from `fund_of_record` a fund token to ABSENT; their `last_stated_position` text is unchanged and gains `"stance"` (`candidate`, or `template` for `ML_FP`) with `"fund"` null and `"candidate_fund"` the token; (b) 4 securities (`8306_JP`, `8316_JP`, `8766_JP`, `9433_JP`) go from a `COMPANY DESCRIPTION:` paragraph as `last_stated_position` to ABSENT. **No holding line's value changes** (`HOLDING_CHANGED=0`); `BABA`, `SHOP_CN`, `WALMEX*_MM` (no fund token) are not touched.
- **The CTO ratified the classification** (msg 7735): `potential add in`, `increase position in`, `maintain or consider increasing` are holdings; `initiate`, `candidate for`, `interesting exposure for` and the bracketed template are not; the default for an unknown phrase is NOT a holding.
- **Not touched:** the gateway code and service (no restart), any other security, silver, bronze, the corpus-wide `fund_form` object (`HVST-cf-3` and `-5` stay held behind this act), schedules, IAM, Terraform.

## BOTH BRANCHES (the half is not signed unless it covers both)

- **For each name, branch A (the build equals the census line):** the built `fund_of_record` is absent and the position's `stance` and first 60 characters equal `stance_after` and `position_after` of its `CHANGED` line of `cf2_census.out` (for the four JP names: `last_stated_position` absent). The pair is written.
- **Branch B (the build differs from its census line in ANY of those):** STOP before that name's write, write nothing for it, record it, continue with the other names only after the issuer's word.
- **Either way, a holding line is never changed:** if a build for a name in the list shows a `fund_of_record` that is a fund token, STOP (it would contradict the census).

## CONDITIONS

- **C-1.** The code is the tree at `80d0701876` (empty `lib/research` diff proof printed in `cf4_before.out`); the list is the file with the printed sha256; no name is added.
- **C-2.** A change-management ledger entry is open at the start and CLOSED and COMMITTED at the end (NEVER-2; `org/critical_paths/change_management/` and the sentinel `org/critical_paths/.open_deploys/harvst-cf4-gold-rebuild-20261017.json`), naming the bucket and the object families, the window and the manifest.
- **C-3.** Every write is recorded in `cf4_written.out` the moment it lands (key, VersionId, bytes, sha256, UTC); the manifest IS the rollback list and is committed with the ledger close.
- **C-4.** The write principal is the one dell1's existing harvest tooling already holds; NO grant, key or policy is requested; an AccessDenied is a STOP.
- **C-5 (the CTO's rule for long write runs, row `D1-S44`).** Serial, one security at a time, `continuation` before `dossier`; EVERY name is a separate FOREGROUND command with `python -u` and its output appended to a log file; NO `nohup`, no detached or background process; after each name read the manifest and confirm BOTH keys of that name are present before starting the next; a missing key, a gap, any error (`GoldImmutableError`, AccessDenied, a throttle) or silence is a STOP with the exact text; no retry loop.
- **C-6.** The canary (`MNST_US_Equity`, then `8306_JP_Equity`) is read SERVED before the other 15 are written: `harvest_get_research` as an Opal principal with `as_of` and `source_keys` printed: MNST `fund_of_record` absent, `last_stated_position` text `CANDIDATE FOR PFOE` with `stance` `candidate`; `8306_JP_Equity` `last_stated_position` absent.
- **C-7.** UNH and the CONTROL: `UNH_US_Equity` (fund `PFOE`, `Maintain positions in PFOE and DIVZ`, `line_only` true) and `CPA_US_Equity` (fund `IDVZ`, the 1-2% position) are read served BEFORE the first write and AFTER the last; both equal. UNH's continuation is NOT rebuilt (it is outside the list); an in-memory `continuation.build("UNH_US_Equity")` from the pinned tree must print the same fund and position (proof the rule leaves a holding unchanged).
- **C-8.** After all 17: served reads of three more names of the list (the first, a middle and the last of the sorted file other than the canaries) and the 4 JP names' `last_stated_position`; each equals its census line.
- **C-9.** No Terminal, queue or Bloomberg use; no S3 delete by the seat; NO call of `etfs_compare_peers` on the gateway (site Z row `Z-S375`).
- **C-10 (site Z told first).** Before the first write the issuer asks `0.0.0_AB_MSTR~DELL1` to tell site Z the window and the 17 names (hash above) and that a site Z rebuild in flight on any of them is a STOP; the issuer sends GO with site Z's answer.

## ROLLBACK (stated honestly)

The act is ADD-ONLY; the pre-act state returns when the new keys are removed, which is an S3 delete: Andrew's act, not the seat's and not pre-approved here. The seats' own correction of a wrong value is a fixed rebuild that writes a still newer object. The manifest lists every new key (and VersionId). The two-name canary bounds the exposure.

## WHAT THIS DOES NOT COVER

A rebuild of any other security (the census says no other value changes); the corpus-wide `fund_form` object (still counts the two Mexico reports, `D1-W158-S2`); the `line_only` text cut at a line break; a gateway release.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
