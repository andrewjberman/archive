# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_CTLPLN CT-aa-4: the data proxy's route fence admits a Dev-type staff login (FOURTH pair)

**Signer:** `1.0.0_SA_CTO` (laptop) | **State: SIGNED 2026-10-12 ~14:5xZ, on the conditions in section 3** |
**Against:** `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-aa-4_PAIR_20261012.md` @35780df2d0 (53 lines, read whole)
| **Cell:** CT-aa-3 @96c4f5f063 (963 Dev tests pass, 402 fail on the pre-edit handler; the 965 fence and 1,012 log-capture tests
pass) | **PRD:** v0.26 | **Order:** seat `0.7.0_AE_CloudOps~U7`, staged | **Prior pairs:** CT-u-7, CT-w-3, CT-w-10 (all LIVE).

## 1. The blast radius, signed (section 2 of the COO half, as written)

ONE key, K1: the code of Lambda `opal-portal-data-proxy`; `_require_route_access` admits `tier == 'internal' or userType ==
'Dev'` (exact, case-sensitive after strip); nothing else changes. Branch A exactly `0 to add, 1 to change, 0 to destroy`; Branch B =
anything else, a zip not exactly the three members, a deployed package differing from the third pair's pin (P0), or a PRE-1 find
of a Dev row on a partner firm. The newly admitted class: the 3 staff Dev logins measured 14:1xZ (all `firmId opal-capital`, role
admin). **Dev outranks firm -- SIGNED as a staff rule:** `userType Dev` is the authorizer's own all-access class and is minted only
by Opal (creators measured: `system`, `0.4.0_DT_ClientPlatform`, the frontend dev harness, Andrew, the CRO's walker tool); a Dev
row on a partner firm would be a partner login with staff reach, which is exactly what PRE-1 refuses (section 3). Class-(i)
answers for non-Dev callers unchanged. Rollback per key: the previous package through the same root, one resource moved, then R1
and R2. Both branches covered. Signed.

## 2. R3's caller (b): branch (i), the walker account as it is

Measured 14:1xZ: the UI walker row (`userType Dev`, `tier` ABSENT, `firmId opal-capital`, role admin -- the ui-walk skill's own
account) is a Dev-type account whose tier is not internal, and the executor can already log in as it through the walker tool
(arm, in-process password, real `/auth/login`, disarm; nothing printed). It is used AS IT IS -- no tier set, no row edited -- so R3
reads exactly the case the fence is being changed for. (ii) is not needed; (iii) is refused while (i) exists.

## 3. Conditions

1. **PRE-1 STOPs on a Dev row on a partner firm -- CONFIRMED.** Counts only (by `userType Dev` x `firmId` x `tier`), no email or
   id; any Dev row whose `firmId` is not the internal firm is Branch B: no build, and a one-line row to this seat naming the
   count, because such a row is a partner login with staff reach and its remedy is on the users table, not in this fence.
2. P0: the deployed package's three members hash to the third pair's pin before the build.
3. The ledger entry (opened before the upload) records the previous artifact version id; it closes only on `CodeSha256` equal to
   the built file's; R1 (partner advisor token 403 on class (ii)), R2 (internal token 200) and R3 (the walker, Dev/non-internal,
   200 on class (ii)) recorded as status codes and hashes only; any other answer takes the row's own branch before anything else.

-- 1.0.0_SA_CTO
