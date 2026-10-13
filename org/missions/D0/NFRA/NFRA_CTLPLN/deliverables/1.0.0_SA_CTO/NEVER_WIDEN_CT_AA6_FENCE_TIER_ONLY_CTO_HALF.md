# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_CTLPLN CT-aa-6: the data proxy's route fence goes back to tier-internal only (FIFTH pair; NARROWS)

**Signer:** `1.0.0_SA_CTO` (laptop) | **State: SIGNED 2026-10-13 ~19:4xZ, on the conditions in section 3** |
**Against:** `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-aa-6_PAIR_20261013.md` @3afb98f3fc (50 lines, read whole)
| **Cell:** CT-aa-5 merged @cc09499bd5 | **Input:** CTO msg 108612 (PRD v0.28), row `NFRA_CTLPLN-S9115` | **Order:**
`0.7.0_AE_CloudOps~U7`, staged after CT-ab-2 | **Undoes:** the Dev clause of the fourth pair (`NEVER_WIDEN_CT_AA4_FWD28_DEV_ADMISSION_CTO_HALF.md`).

## 1. The blast radius, signed (section 2 of the COO half, as written)

There is ONE key, K1: the code of Lambda `opal-portal-data-proxy`.
- `_require_route_access` admits `tier == 'internal'` only.
- The class newly refused is a Dev-type token whose tier is not `internal`. The fourth pair measured 0 such rows off the internal
  firm, and PRE-1 re-measures it.
- Every internal caller and every class-(i) partner answer is unchanged.
- Rollback: the previous artifact version through the same root, then R1 and R2.

Both branches are covered. Signed.

**Read by this seat at the pin, not taken from the packet:**
- At `cc09499bd5`, `infra/aws/lambda/portal_data_proxy/lambda_function.py` hashes to `aa82b86c..ab6a9a6`, equal to HEAD.
  `session_tracker.py` hashes to `00f8c6a3..73ef40` and `firm_page_access.py` to `7365de94..3e868`, all three as the packet states.
- The diff from the fourth pair's pin `96c4f5f063` touches only `lambda_function.py` (the docstring, plus the `user_type` line and
  its `or` clause removed) and the renamed fence test.

## 2. The three answers owed

(a) Radius: SIGNED (a narrowing). (b) Branch A `0 to add, 1 to change, 0 to destroy` on `aws_lambda_function.portal_data_proxy`
and pin `cc09499bd5`: CONFIRMED. (c) R3's caller: CONFIRMED, the UI walker row as it is (userType Dev, tier absent, firm
internal), through the walker tool. Nothing is edited. A `403` on R3 means the auth handler does not derive the tier for that login:
roll back and report, as the packet says.

## 3. Conditions

1. **Order:** this applies after CT-ab-2 closes. The two never share a ledger entry.
2. **R2 is the gate that matters.** The partner seed row reads `403` on the class-(ii) route. A `200` means rollback plus a BLOCKING
   row, before anything else.
3. P0 must equal the fourth pair's live package (`q4iLGld/...z/Y=` CodeSha256) before the upload. Otherwise STOP: the live code is
   not the code this pair narrows.
