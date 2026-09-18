# C6 -- the onboarding checklist's first real run

**Cell:** `CN-o-5` (the PRD's C6), LGIC_CANON round 4 slot `~1`. **Worker:** `0.9.0_WK_LGIC_CANON~1`, issued by
`2.0.0_SA_COO~G`. **Subject:** the `LGIC_LGCTFM` practice wave `20260918T011619Z-8db9eb1` under
`workflows/legacy_transform/blackdiamond-49financial/`, `contract.json` hash
`33204e29839de89af81fb293317cce3ccdf2266d` -- verified to agree across `git hash-object` on the worktree file,
`git rev-parse HEAD:<path>` and the wave's own `HASHES.json` before any other work began.

## THE BAR

R-34, verbatim: *"The outcome is graded on what the wave reaches plus its carded set -- `reached + carded ==
steps`, denominators printed."* This run takes the 49 Financial subject through
`infra/logic/10_ONBOARDING_CHECKLIST.md`'s 16 steps, exercising each one as a READ against 49financial's already-live
state or as a pure/dry-run function call, never as a live act. **No demonstration firm was invented** and **nothing
live moved**: no `safe-apply`, no Terraform apply, no AWS write, no bucket mint, no IAM change, no route change, no
promote, no portal write. `live_acts` in the run record is `[]`.

```
  steps in the checklist ................................. 16
  REACHED ................................................. 12   (1,2,3,4,5,6,7,8,9,11,12,15)
  CARDED ................................................... 4   (10,13,14,16)
  reached + carded ......................................... 16  == steps
```

## WHY 49FINANCIAL, AND WHAT "REACHED" MEANS HERE

49 Financial is an EXISTING, already-onboarded firm. There was nothing new to write for most steps, so "REACHED"
here means: read the artifact Step *n* would have produced, or call the pure function Step *n* names, and confirm it
matches the checklist's own shape -- never a fresh write, mint or apply. Where a step's action is inherently a live
act (a Terraform apply, an actual deploy, an authenticated sign-in), or depends on an input this run was never given,
it is CARDED with its owner and the reason, and the run continues.

## STEP BY STEP

1. **Identity row (R2,R5,R7).** REACHED. 49financial's row in `scopes.json` already carries every field Step 1
   describes; `python lib/opal_naming.py validate` printed `VALIDATE: OK 25 system row(s), 9 scope row(s), 17
   warning(s)`, 0 REFUSED.
2. **Two forms in the schema (R1).** REACHED. `org/standards/NAMING_SCHEMA.json` is v1.10 and carries no
   `firm_forms` key at all -- the firm list moved to the registry (LGIC_ENFORCE EN-r-3) -- and `validate` printed no
   WARN naming 49financial. Step 2's own "if the line is not printed" branch applies; no edit needed.
3. **Vendor masters + pipeline tree (R3,R7).** REACHED. The row already carries both master ids, the
   `monolith_scopes` entry and the `pipeline_trees` entry whose `dir` (`data/black_diamond/`) is the FAMILY's, read
   rather than invented (R22).
4. **Regenerate the generated views (R1,R6).** REACHED via DRY RUN. `generate --out .scratch/gen_preview` wrote 10
   files; 8 of 10 are byte-identical to what is committed, 2 differ only by this worktree's CRLF rendering (a known
   checkout artifact, content-equal after normalizing line endings), and 2 more differ only in an embedded registry
   hash comment (the registry moved for a reason unrelated to those two files' actual values, which are unchanged).
   Nothing was written to a tracked path.
5. **Exemption list (R6,R7).** REACHED. `infra/logic/registry/exemptions.json` already carries the key
   `"opal-data-49financial"` with 16 already-declared, already-reasoned principals.
6. **Mint the bucket from the template (R1,R5,R6).** REACHED via READ. `s3-49financial.tf` IS the template; its
   bucket is already in `local.org_trail_read_logged_buckets` and in the generated `scope_bucket` map, and
   `bucket_provisioned` is `true`. No apply was run.
7. **Name every resource (R1,R7).** REACHED. `name('blackdiamond', '49financial', 'gold-runner', 'runner')` ->
   `blackdiamond-49f-gold-runner-runner` -- a pure call, the SHORT form lands in the scope slot as required.
8. **Bronze/silver via `address()` (R4,R9,R10).** REACHED. Bronze and silver addresses both resolve into
   `opal-data-assets` as the tier-home rule requires -- pure calls, no write.
9. **Gold/state/code via `address()` (R5,R11,R13,R16,R21).** REACHED. Gold and state addresses both resolve into
   `opal-data-49financial` -- pure calls, no write.
10. **Platinum via `address()` (R6,R12,R14).** **CARDED, owner `ADVI_FIRMBKTS`.** The checklist's own STOP: the
    edge auth validator and the shared advisor router still read the legacy tier-first keys `address()` cannot
    produce. Confirmed live for 49financial itself: its served `ownership_map.json` and `mix_summary.json` are read
    from `opal-data-portal-v2/platinum/advi/49financial/`, never from `address()`'s `opal-data-49financial` output.
    R-34 releases the project-level wait on `ADVI_FIRMBKTS`; it does not change this mechanical fact, which the
    checklist still states correctly.
11. **Commit through the naming flagger (R1,R20).** REACHED. A synthetic diff carrying a hand-typed literal
    (`opal-data-49f`) was graded with `.tools/naming-gate.py --diff` and REFUSED (exit 1) *without* passing
    `--enforce`, because `org/mcp/naming-gate.enforce` exists at HEAD. This step's own text was stale (row
    `LGIC_CANON-S19`: it said the kill switch was absent and the stage would warn and pass) and is corrected in this
    commit.
12. **Apply through `safe-apply` (R1,R18).** REACHED via DRY RUN. `grade('opal-data-49financial', 'S3_BUCKET')` ->
    `('CONFORMANT', 'opal-data-49financial')`, the exact grading call Step 12 names, run against an already-declared
    resource. No `terraform apply` and no `safe-apply` were run.
13. **Census the firm's names (R1).** **CARDED, owner `LGIC_ENFORCE`.** Step 13's own text was ALSO stale: it said
    cell `EN-s-1` had not closed and both its task orders were pending. At this tree both `LGIC_ENFORCE.TO-EN-s-1`
    and `-r2` read `complete -- proof-of-spec VALID (rc=0)`, re-verified by re-running `proof-of-spec-check.py`.
    Corrected in this commit (row `LGIC_CANON-W1-S7`). Because it is now available, the census mode was actually
    RUN: `python lib/opal_naming.py census --repo --live --budget 60 --report .scratch/census_c6.md` STOPPED on its
    first RAISE, an unrelated resource (`sentiment-query-api`), before reaching any `49financial`/`49f` row. The
    step is carded on that new, unrelated gap (Rule 30: fixed at its own row), not on the old `EN-s-1` one.
14. **Sign-in (R6).** **CARDED, owner Andrew (portal paths, row `LGIC_CANON-W6-S2`) and `1.0.0_SA_CTO` (register
    entry X8, for a firm not already declared).** The portal-paths sub-bullet is a SOVEREIGN input this practice run
    was never given (no demonstration firm was invented, and nobody asked Andrew for a fresh grant). Separately,
    49financial's own partner table is already one of register entry X8's four declared names (confirmed:
    `infra/aws/terraform/partner-firms/49financial.tf` already exists), so the mint sub-bullet's STOP does not fire
    for THIS subject specifically -- but the step as a whole still needs the missing sovereign input.
15. **Open the routes (R6,R12).** REACHED. `FIRM_CONFIG` already carries 49financial's entry. The bucket-uniqueness
    check the step names does NOT hold cleanly today (`opal-data-bd` is shared by 49financial and `mockadv`), but
    this is an ALREADY-DOCUMENTED, ALREADY-RULED exception recorded in the same file (CTO ruling 65047, AE-lane
    remedy pending) -- not a new finding, so no fresh row was filed for it. No deploy was run because Step 4 already
    showed nothing changed.
16. **Confirm the served dashboard (R6,R12,R14).** **CARDED, owner `ADVI_FIRMBKTS` (same repoint as Step 10) and a
    live portal sign-in.** The step's bar needs HTTP 200 from `opal-data-<LONG>` via `address()`; the content
    actually served today is read from the legacy tree in `opal-data-portal-v2` (confirmed live, read-only:
    `HeadObject` on `platinum/advi/49financial/ownership_map.json` -> 566205 bytes, and `mix_summary.json` -> 11129
    bytes, matching `firm-config.mjs`'s own 2026-08-21 measurement exactly). An authenticated sign-in and its 401
    negative control are also live acts this cell's bounds forbid.

## WHAT THE CARDED SET MEANS FOR FWD-5

FWD-5's DONE-WHEN needs the checklist run end to end AND the firm's people able to see their dashboard. This cell
reaches 12 of 16 steps and cards the remaining 4 with real, closeable owners: `ADVI_FIRMBKTS`'s router repoint
(Steps 10 and 16, the same root cause), Andrew's still-missing portal-paths grant plus `1.0.0_SA_CTO`'s register
extension for a genuinely new firm (Step 14), and one unrelated registry RAISE that the now-available census hit
before it could grade this firm's own names (Step 13, owned by `LGIC_ENFORCE`). None of the four are inherited from
this run's own choices -- three trace to `ADVI_FIRMBKTS`/sovereign-input gaps the checklist already named, and the
fourth is a fresh, narrow, already-diagnosed registry defect. As the decomposition states, FWD-5 reaches EXERCISED
when this carded set closes, not when this cell drains.

## TWO STALENESSES FOUND AND CORRECTED IN THIS RUN

- **Step 11** (row `LGIC_CANON-S19`, filed by the issuer): said the naming kill switch was absent and the stage
  would warn and pass. It exists and the stage refuses. Corrected.
- **Step 13** (row `LGIC_CANON-W1-S7`, filed by this run): said `EN-s-1` was pending. It has closed. Corrected, and
  running the now-available census surfaced a second, unrelated gap (a registry RAISE), also recorded.

A third, minor discrepancy (row `LGIC_CANON-W1-S6`): the round's own pinned context said the checklist carries 2
`built: no` steps; it carries exactly 1 (Step 13), at the pinned commit and at this cell's HEAD alike. No arm reads
this number; filed for the record.

## NOTHING LIVE MOVED

`live_acts: []`. The one artifact this run could have touched without meaning to -- the served routes definition,
`infra/aws/lambda-edge/_shared/firm-config.mjs` -- was read only; its `git hash-object` is identical before and
after this run (`07412e484cc304d5bcbb727ff11aa0296e5389d6`).
