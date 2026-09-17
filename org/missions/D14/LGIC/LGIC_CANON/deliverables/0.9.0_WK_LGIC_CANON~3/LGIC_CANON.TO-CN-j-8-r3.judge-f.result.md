# LGIC_CANON.TO-CN-j-8-r3 -- result (judge F, round 3)

**Worker:** `0.9.0_WK_LGIC_CANON~3` · **Issuer:** `2.0.0_SA_COO~G` · **Worktree base:** `1e2a9c931b2e46adc0518ac2c16a2f487619b614`

## What this cell did

Judged the 23 planes of `CN_TREE_R3.md` (the 49FINANCIAL family plus the general-data product bucket
beside it) against `infra/logic/02_DOCTRINE.md` v1.1 on the canon's five axes (A1 INGESTION, A2 BUCKET
STRUCTURE, A3 NAMING, A4 COMPUTE, A5 FORMAT), printed each row's single most-severe finding and its
deciding rule, and printed which of the six named rules (R3, R8, R14, R15, R19, R21) each row's judgment
engaged.

## Sequence, per A-22 (blind, measured on the world)

1. Checked `infra/logic/02_DOCTRINE.md` line 1 reads `v1.1` (it does -- CN-k-5 had drained).
2. Before reading the tree or any canon rule text, wrote `judge-f.base` with
   `base_commit: 1e2a9c931b2e46adc0518ac2c16a2f487619b614` and committed it alone
   (commit `8ffa9f2613`).
3. Read `CN_TREE_R3.md` (23 planes), `infra/logic/02_DOCTRINE.md` (full text, both pages),
   `CN_SEVERITY.md` (the verdict vocabulary and severity order) and `CN_SEVEN_RULES.json` (the reach
   presence definitions).
4. Built `judge-f.tsv`, one row per plane, and committed it alone (commit `b666a55f57`).
5. Ran `check_canon_r3.py j8-rows`, `j8-reach`, `j8-blind` at that commit -- all three PASS (below).

## Notable findings surfaced by this row set (cited `path:line @commit`, canon at `afd81beb8a`)

- **Scope-segment SHORT form where the grammar requires LONG.** `opal-data-assets/blackdiamond/49f/{bronze,silver,gold}/`
  spell the firm's SHORT form (`49f`) in the key's scope segment; N2's per-slot table
  (`infra/logic/02_DOCTRINE.md:244-249`) requires LONG (`49financial`) there. R1's own resolves-R-9(iii)-C2
  line (`:175`) states the blanket 53-of-53 plane-level census does not clear a per-key departure graded
  on its own terms -- these three rows are exactly that per-key departure. `A3 = VIOLATES, R1`.
- **`bronze_legacy`/`silver_legacy` occupy the `{tier}` grammar slot but are not members of the closed
  tier list** (`bronze`, `silver`, `gold`, `platinum`, `state`, `code` -- `:220`). `A3 = VIOLATES, R1`
  for both planes, independent of their 17-day write dormancy.
- **`opal-data-49financial/gold/`'s own tree row states "keys start at the tier"** -- the SUPERSEDED
  collapsed grammar R1's own text struck (`:151-153`, "~~In a per-firm or per-product bucket, the source
  and scope segments collapse...~~ SUPERSEDED 2026-09-13 ~03:2xZ: SOURCE-FIRST everywhere"). Even the
  RULED destination firm bucket is not yet conformant on this axis.
- **`opal-data-bd/gold/`'s `_state/`, `_parity/`, `meta/*_watermark.json` and `manifests/` prefixes are an
  exact match to R21's own census line** (`:580-582`, "gold/_state/, gold/_parity/, gold/meta/*_watermark.json,
  gold/manifests/ ... — VIOLATED-LIVE (state inside tier planes)"), and `opal-data-bd/silver/`'s
  `meta/gap_manifest.json` matches the same census line's `silver/meta/gap_manifest.json in bd/inf/cot`.
- **R-9(iii) C3's unsettled-bucket-identity reasoning** (`:399`, in R6's block, naming R5) is read onto
  `opal-data-bd/{platinum,gold}/`: the legacy short-form bucket is not the ruled firm bucket
  (`opal-data-49financial`), so the plane-level CONFORMANT/VIOLATED tags in R5/R6's own census are
  current-state readings of R19's in-flight migration, never a settled A2 clearance; no register entry
  names this bucket-identity departure, so R20's default applies (VIOLATES, not UNDETERMINED, per C4's own
  ban on a separate "in-flight" UNDETERMINED status, `:557`).
- **A4 COMPUTE reads UNDETERMINED on all 23 rows.** `CN_TREE_R3.md` is built from the ledger record, not
  the live S3 plane (its own Provenance block, `NOT READ: the live S3 plane`), and carries no Lambda/EC2
  fact for any plane; R13's own census line reads `UNMEASURED (compute is not in the plane census)`
  (`:479`). This is the canon's own value for "does not decide," not a filled-in nearest rule.

## Acceptance criteria at commit `b666a55f57`

```
J8R3-AC1 (j8-rows):  ROWS 23 over a tree of 23 plane(s); same set, no duplicates: True
                     row defects, denominator 23: 0 []
                     VERDICT: PASS-J8-ROWS-WELLFORMED

J8R3-AC2 (j8-reach): REACHED 5 of 6: ['R3', 'R8', 'R14', 'R19', 'R21']
                     NOT REACHED 1 of 6: ['R15']
                     VERDICT: PASS-J8-REACH-OVER-SIX

J8R3-AC3 (j8-blind): base 1e2a9c931b ancestor of HEAD: True
                     POSITIVE CONTROL infra/logic/02_DOCTRINE.md visible at base: True
                     sibling answer files PRESENT at base, denominator 3: 0 []
                     canon at base carries v1.1 (CN-k-5 drained first): True
                     VERDICT: PASS-J8-BLIND-AT-BASE

J8R3-AC4: judgment=true, for 3.0.0_SA_CVO at L9. Not self-graded. Recorded
          UNVERIFIABLE-BY-INSTRUMENT with status_reason naming 3.0.0_SA_CVO.
```

R15 (the most-derived-consumer rule) was NOT reached by this tree: `CN_TREE_R3.md` names no source
served raw AND separately consumed by a derived plane within the 49FINANCIAL family or the general-data
bucket beside it -- a legitimate NOT REACHED, not a defect (per the order's own instruction and
`CN_SEVEN_RULES.json`'s own framing that a printed NOT REACHED is never a FAIL).
