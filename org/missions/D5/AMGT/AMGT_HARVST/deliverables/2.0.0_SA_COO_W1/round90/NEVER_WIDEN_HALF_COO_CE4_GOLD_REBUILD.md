# NEVER-WIDEN -- COO HALF: the gold continuation and dossier objects of 31 securities are rebuilt (`HVST-ce-4`, round 90, workstream S43-REBUILD)

**Signer:** `2.0.0_SA_COO~W1`, drafted 2026-10-17 ~17:0xZ UTC. **Authority:** the CTO's round-89 analysis (`ledger/ROUND_ANALYSIS.round89.md` @fa28a5790e, msg 7642) items 1 and 3; `HVST-ce-1` (`CAUSE=rule_miss`, merged `0dfc96bdd1`); `HVST-ce-2` (the pdf line rule as a fallback, continuation method `/4`, merged `344ea6a5fc`); `HVST-ce-6` (the corpus library drops the two misfiled KMB reports, merged `87b542aed4`).

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`, from a worktree at commit `344ea6a5fc` (or a later commit whose `lib/research/` tree is byte-identical to it, proven by an empty `git diff 344ea6a5fc <commit> -- lib/research`): for each security in `deliverables/2.0.0_SA_COO_W1/round90/ce4_securities.txt` (31 names, sha256 `7881772da6e204818fd50a02050cc7456b7de5a6d0912b6d663817f12930c67b`), (1) BUILD without writing (`continuation.build(security_key)` and the dossier's build) and print the `fund_of_record` and `last_stated_position` it would write, (2) WRITE `continuation.write_one(security_key)` and then `dossier.write_one(security_key)`, (3) read the result on the served gateway tool. Canary first: `UNH_US_Equity` and `KMB_US_Equity`, read served, then the other 29.

## THE PROPERTY AND ITS WRITERS (printed, CLAUDE.md section 5)

The property moved is the served `fund_of_record` and `last_stated_position` of a security (and, for KMB only, the other fields its dossier derived from the two misfiled reports). **N = 2 writers:** `lib/research/corpus/continuation.py::write_one` (the derivation `_resolve_fund_and_position`, after `HVST-ce-2` and `HVST-ce-6`) and `lib/research/corpus/dossier.py::write_one` (which copies both fields from the stored continuation object, `dossier.py` lines 1490-1502). Both rules are read. No other writer of those objects was found by `HVST-ce-1` (`ce1_measure.out` section (g)); no schedule or trigger runs them.

## WHAT THIS CHANGES IN THE WORLD (named)

- **Gold objects are ADDED, none is changed or deleted.** For each of the 31 securities two NEW objects are written under the harvest bucket `opal-data-harvest`: `amgt/harvest/gold/research-continuation/security_key=<KEY>/<sha16>.json` and `amgt/harvest/gold/research_dossier/security_key=<KEY>/as_of=<as_of>.<sha16>.json`. The gold writer never overwrites (an existing name with other bytes raises `GoldImmutableError`); the old objects stay. The gateway serves the newest (`harvest_research.py`: continuation by greatest LastModified, dossier by greatest as_of stamp then LastModified), so the NEW objects become what every caller of `harvest_get_research` sees for these 31 securities, at once.
- **What changes in what is served, per the census (`ce2_census.out` of `HVST-ce-2`, 94 of 94 securities, both rules run on the same fetched extractions):** 30 securities go from `fund_of_record` and `last_stated_position` ABSENT to a value (the UNH class: `UNH_US_Equity` to fund `PFOE`, `Maintain positions in PFOE and DIVZ`). The 30 are exactly the names in `ce4_securities.txt` except `KMB_US_Equity`. **No existing value changes** (`VALUE_TO_VALUE=0`; `CPA_US`, `JD_US`, `MER_PM`, `ML_FP` read as before). A position value read from a pdf line carries `"line_only": true`.
- **KMB (the thirty-first):** its dossier is rebuilt from the reports that remain after the two Mexico reports are excluded. The census did not include the exclusion, so KMB's built values are NOT predicted here: see BOTH BRANCHES.
- **Not touched:** the gateway code and service (no restart), any other security, silver, bronze, the corpus-wide `fund_form` and `sector_template` objects, any schedule, IAM, Terraform.

## BOTH BRANCHES (the half is not signed unless it covers both)

- **KMB branch X (the build gives `fund_of_record` and `last_stated_position` ABSENT):** the dossier is written with them absent and the served read shows them absent with their reasons; this is a correct outcome (no remaining KMB report states a position).
- **KMB branch Y (the build gives a value from a remaining report):** the value is written; the served read shows it with its citation; also correct.
- **Either branch is valid ONLY IF the built KMB continuation and dossier JSON contain neither `fbd50086c4065785` nor `1a3b56044db679a5` anywhere** (scan the whole built document, print the two counts, both must be 0); otherwise STOP before the write and tell the issuer.
- **For each of the other 30 (branch A, the census outcome):** the built `fund_of_record` is the fund token the census names and `last_stated_position` is the census text, with `line_only` true where the supplying report was read by the line rule. **Branch B (the built value differs from the census line):** STOP before that security's write, write nothing for it, record it, and continue with the others only after the issuer says so.

## CONDITIONS

- **C-1.** The code is the tree at `344ea6a5fc` (empty `lib/research` diff proof printed in `ce4_before.out`); the list is the file with the printed sha256; no name is added.
- **C-2.** A change-management ledger entry is open at the start and closed at the end (NEVER-2; `org/critical_paths/change_management/` and the sentinel `org/critical_paths/.open_deploys/harvst-ce4-gold-rebuild-20261017.json`). It names the harvest bucket and the two object families, and holds the manifest of every key written.
- **C-3.** Every write is recorded in `ce4_written.out` the moment it lands: key, VersionId if the bucket returns one, bytes, sha256, UTC time. This manifest IS the rollback list.
- **C-4.** The write principal is the one dell1's existing harvest tooling already holds. NO grant, key or policy is requested or created; an AccessDenied on the first put is a STOP with the exact error, and the issuer reads it.
- **C-5.** Serial, one security at a time, `continuation.write_one` before `dossier.write_one` (the dossier build reads the stored continuation). No parallel run, no retry loop: a `GoldImmutableError` or any error is a STOP.
- **C-6.** The canary (`UNH_US_Equity`, `KMB_US_Equity`) is read SERVED before the other 29 are written: `harvest_get_research` as an Opal principal, response `as_of` and `source_keys` printed (a cache is not a read). UNH shows fund `PFOE` and the position text with `line_only` true; KMB shows no string carrying either Mexico id and `misfiled_fields_excluded` as the gateway computes it.
- **C-7.** After all 31: served reads of three of the other 29 (the first, a middle and the last of the sorted list) and of the CONTROL `CPA_US_Equity`, which is not rebuilt: its `fund_of_record` and `last_stated_position` equal the values read BEFORE the first write (read and print them first).
- **C-8.** No Terminal, queue or Bloomberg use; no S3 delete by the seat.

## ROLLBACK (stated honestly)

The old objects are untouched, so the served state before the act returns when the NEW objects are removed. Removing an S3 object is an S3 delete: it needs Andrew's confirmation under the agent-autonomy rule, and it is not the seat's act. The manifest `ce4_written.out` lists every new key (and VersionId where versioned). A rollback of one security is: Andrew-confirmed deletion of that security's two new keys. Until then a wrong value is correctable the other way, by a fixed rebuild writing a still newer object (the gateway serves the newest). The act is therefore ADD-ONLY and its first stage is the two-name canary.

## WHAT THIS DOES NOT COVER

A rebuild of any other security (the census says no other value changes; a name added later is a new pair); the corpus-wide `fund_form` object (it still counts the two Mexico reports, `D1-W158-S2`); a gateway release; the `line_only` text being cut at a line break (the value says so).

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at these bytes.
