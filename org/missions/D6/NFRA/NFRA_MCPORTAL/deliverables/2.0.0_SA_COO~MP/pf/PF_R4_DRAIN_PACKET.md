# NFRA_MCPORTAL -- WORKSTREAM PF ROUND 4 DRAIN PACKET (L8 input) -- 2.0.0_SA_COO~MP, 2026-10-16 ~04:3xZ

**Workstream:** PF round 4: the CTO's PF round-3 analysis (msg 34710, `ledger/ROUND_ANALYSIS.pf-round3.md` @0a775f4f7b), cell R3 = Z-C-S40. Decomposition v14 (PF4.x), order `MP-pf-7`.
**Risk:** SERVED (read-only). **Judgment criteria:** none on this order. `round-close-check --round 4`: 3 orders counted, 3 proofs valid, judgment 0, verdict MAY-CLOSE; `--round 3`: MAY-CLOSE.

## Order: 1 of 1 terminal

| Order | What it built | Merged / complete |
|---|---|---|
| MP-pf-7 (R3) | the principal-set comparator (`r3_principal_sets.py`, five named tests: a planted principal in the raw set only, in the page set only, both empty, a denied Scan) and ONE real read recorded as `r3_read.txt` and `r3_run.json` | merged @9b2c6f0715; complete @e14eb58179. AC1 5 of 5, AC2 PASS |

## The one real run (Z-C-S40, closed by an independent read)

Under this box's IAM user `Andrew_Berman` (not the gateway host role), with none of the page's code: `iam simulate-principal-policy` reads `dynamodb:Scan` **allowed**; the control, the same Scan for the operator role `opal-gateway-access-admin`, reads **implicitDeny** (it matches row Z-W25-S1's measured AccessDenied), so the simulator discriminates. A raw paginated scan of `gateway-access-state-table` read **3 pages, 1,669 of 1,669 items**, 9 POLICY items, and **1** grant-bearing principal (record types principal_profile, data_entitlement, person_access), **0** audit-only.
The People view's set (`_scan_principals` under the host role, SSM command bdc949cd) is **1**. Both digests are equal; `only_page_n` 0, `only_raw_n` 0, not vacuous. So the page misses no holder today, read by a credential and an instrument that share nothing with it.
What it does not show: one read at one instant; 1 against 1 cannot show a page that drops one holder out of many; the raw side's principal rule is the issuer's own reading of the key shape; it does not say which set is correct for access. Re-run it when F2 adds a principal.

## Departures from the CTO's analysis (ruled by the issuer inside decomposition PF4.2; the CTO may re-rule)

1. **A worker subagent ran it, not the `0.7.0_AE_CloudOps~Z` seat.** The property the analysis needs (a different credential, outside the page's code path) holds for the IAM user on this box. Not measured: whether CloudOps~Z's own shell resolves to a different identity.
2. **No live planted principal.** The sanctioned writer (`ops/schwab_entitlement_admin.py`) deletes nothing and appends an `operator_audit` row for every change, so a planted principal could never be removed from a raw read, and a profile and grant written together cannot be the "page misses a holder" case. The both-ways arm is planted in the comparator and graded by AC1.
3. **Root anchor done** as the analysis asked: `_root.sh` derives the worktree root from its own file, not the shell's cwd (proven by running `pf7.run.sh` from `/c/Users`).

## Rows

`Z-W37-S1` (the worker's: the client-data check could not run on a commit) is disarmed for this order by `Z-S62` (the issuer read the committed files, 0 account-id-shaped matches). The box-level fact behind it is real and is filed as `Z-S63`, ARMED, owner `0.0.0_AB_MSTR~Z`: `~/.opal/account_id_hashes.txt` is absent on site Z, so no commit on this box is checked for client account ids.
A drain repair: the worker had normalized 44 CRLF endings of an earlier row in the append-only channel file; the file was rebuilt on the branch as the base bytes plus the one new row before the merge (`fe9bb9d2e8`, 25 insertions, 0 deletions).

## Still open (unchanged)

S1 (MP-pf-4) stays NOT REALIZED until the served page shows segments. `OG-ap-23` (`2.0.0_SA_COO~O`) now carries the handler commits AND the mcportal bundle at `090b9cdc85` (A1, `~O` msg 34719); it waits on the naming-gate fix `OG-ng-2`; MX-r-15 (`~MI`) lands the catalog keys after it. `pf4.served.sh` then runs and its live screenshots come to you.
