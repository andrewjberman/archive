# NEVER-WIDEN -- COO HALF, ADDENDUM 8: grounding_check/4 + the CALL 11 re-grade of the 10-02 AI run, at pin CLOUD b973c9fdb9

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~11:5xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-8 half (asked).
**Extends:** the half @4df699fa92 and addenda 1-7. Every gate, key and condition stands.

**Why:** CVO~RV grade 8 (@ab55da6a97) G8-1 (P1, the demo fund): both BASG accounts on the served 2026-10-02 page are
FALSE grounding FAILs. The grader read "10, 13, 15" out of a quoted timestamp "2026-10-01T21:13:15+00:00". Also CTO~Z
addendum-7 condition 4 / CRO~RV CALL 10 (@d7ddc352d9): the unknown_identifier check ships before the next AI run.
CRO~RV CALL 11 (@c0a942f6a1) ACCEPTED re-grading the stored run with /4, under three conditions: every account, once per
grader defect, and the superseded grade kept beside the new one. Code @f1688c2437, drained b973c9fdb9.

## VERDICT: SIGNED (at pin CLOUD b973c9fdb9)

## THE PLAN, MEASURED

**Plan: 0 to add, 5 to change, 0 to destroy** (`/c/tmp/rv_apply9.tfplan`, from `/c/tmp/rv-fast` with HEAD = CLOUD HEAD
b973c9fdb9): the five Lambdas' `source_code_hash` + `last_modified` only; no policy change. Package diff vs the deployed
7ab3b9382f: `ai_accounts.py`, `guardrails.py`, `publish_page.py`, `render.py` (no producer or gold-table code).

## THE MEASUREMENTS

- **Recheck change alone:** an overlay publish of 2026-10-02 at b973c9fdb9 over the served inputs is `unchanged: True`
  (byte-identical to the served fast-a1-publish-1002b). The 2026-10-01 overlay differs from its served page only by the
  publish-page Lambda's missing bronze read (parked below), not by this code.
- **Plant through the real publish path:** TXUE's account rewritten to name "1234 JP Equity" reads TXUE "not updated:
  ... (unknown_identifier: 1234 JP Equity)".
- **Re-grade dry run** of 20261002T110438Z-ai with /4: 20 PASS / 4 FAIL -> 22 / 2. Only BASG's two move (FAIL -> PASS).
  IDVZ ($1.6m, $1.3m) and CGIC ($5.7m) stay FAIL, genuine per CVO~RV. 0 unknown_identifier.
- **The page with the re-graded run** (overlay): differs from the served 1002b only in AI-account content -- 24
  "Re-graded ... Superseded grade: ..." lines, 12 card footers (run id `-rg4`, written time), BASG FAIL -> Grounded x2,
  BASG's analysis_grounding reason. Status OK, 13 of 13; 1,620,342 -> 1,625,040 bytes.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| J1 | the five stage Lambdas' code | 7ab3b9382f (daily 4CO7fRNi.., fetch CW9NGb4Q.., canonical vBcxC7I4.., silver xlvqzIb1.., publish vbHSPOnp..) | in place to b973c9fdb9 | re-apply from a tree at 7ab3b9382f |
| J2 | gold `research_hypotheses` date=2026-10-02 | one object, run 20261002T110438Z-ai | + ONE new object `research_hypotheses-20261002T110438Z-ai-rg4.parquet` (append-only; `write_rows` refuses an existing key; the original stays) | the page selects each fund's newest run, so a revert removes the rg4 object -- an S3 delete, human-confirmed |
| J3 | platinum page 2026-10-02 | batch fast-a1-publish-1002b | republished ONCE, batch fast-a1-publish-1002c, no `refresh_a1` | prior page kept under `revisions/<ts>/` |
| J4 | the 13:00Z sweep and every later scheduled run | would run 7ab3b9382f | run b973c9fdb9 | J1's rollback |

## ORDER AND GATES

1. Plan exactly 0/5/0. 2. Live base equals J1's CodeSha256. 3. NEVER-2 entry `etfs-rivalfunds-fast-a1-r9` opened AND
committed before the apply (`&&`). 4. Nothing in flight, and outside 12:50-13:15Z, the sweep's window. 5. **J1 BEFORE
J2:** the deployed recheck must be /4 before the re-graded rows exist; otherwise /3 rechecks BASG's new PASS rows and
fails them on the same timestamp. 6. J2 is refused if a cited A1 table has moved since the run (built into
`regrade_day`).

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied before 12:50Z:** the served 10-02 page shows BASG's two accounts Grounded, with the superseded FAIL beside
  each, plus the IDVZ and CGIC FAILs. 13 of 13. The 13:00Z sweep then runs b973c9fdb9 over the same newest run.
- **Not applied by 12:50Z:** the sweep runs 7ab3b9382f, and BASG stays shown as FAIL (the stored grade). The act
  follows the sweep, and J3 republishes whatever page the sweep left. The keys and rollbacks are the same.

## PARKED (found off-item, not in this act)

The publish-page Lambda has no GetObject on `issuer-site/etfs/bronze/holdings/*` and `bloomberg/etfs/bronze/holdings/*`;
the daily Lambda has it. Every page the marker-driven publish writes (the scheduled 11:04Z 10-02 page; the 11:12:56Z
10-01 page) shows "source URL unavailable (bronze sidecar unreadable)" x108 and no capture detail. The daily Lambda's
pages (this seat's republishes, the 09:00 ET sweep) do not. The fix is a policy grant in `gen_policies.py`: a plan with a
policy change, its own pair. Owner `2.0.0_SA_COO~RV`.
