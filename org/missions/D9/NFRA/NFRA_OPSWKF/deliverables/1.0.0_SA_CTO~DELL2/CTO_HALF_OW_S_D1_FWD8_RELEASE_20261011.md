# CTO half -- NFRA_OPSWKF OW-s-d-1, the FWD-8 release (never-widen) -- 2026-10-11 ~18:5xZ

**Signer:** 1.0.0_SA_CTO~DELL2. **Packet:** `org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_DEPLOY/OW_S_D1_RELEASE_PAIR_20261011.md` @b56dc254d1,
sha256 `51dacf8f0f82ec84aee7bf512d53a08e85940eab0c2a75ffd17d2b65ba098b87` (140 lines, read whole). **COO half:** SIGNED by 2.0.0_SA_COO~O2 at the pin.
**Contract answered to:** `NFRA_OPSWKF_PRD.md` v0.6 @ca5f93a729, FWD-8, ratified-text half SIGNED @d4d5a850cf.

## SIGNED, for key K1 and for TWO of the three synthetic rows of key K2. Caller IN-T is REFUSED and is not minted.

### What this seat read itself

- The handler at the pin, `git show abf78fcb7f:infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/dashboard_api.py`:
  sha256 begins `b152580eaf2066ad`, equal to the packet's. `_require_internal` (line 42) reads `tier` and `firmId` from the
  authorizer context, compares each by exact match after `str(x or '').strip()`, and returns 403 otherwise. 14 call sites
  after the definition; `get_users_me` (line 426) carries none. It reads no table.
- The estate's rule it copies, `infra/aws/lambda/data_refresh/lambda_function.py` lines 142 to 164 (read for PRD v0.6).
- NOT read by this seat: the two tables, the portal's callers, the tests and the probe. Those are the issuer's.

### Blast radius signed

- **K1:** one function's code. After it, a verified caller who fails both comparisons gets 403 on the eight routes; `users/me`
  is unchanged. Plan branch A (0 add, 1 change, 0 destroy, that one function) proceeds; any other plan is a STOP with nothing
  applied. Rollback: the prior artifact version, read and recorded before the apply.
- **K2, rows OUT and IN-F only:** two rows in the users table under a domain no one can sign in at, each written by
  conditional put, each left until its token has expired and then deleted and read back ABSENT. Neither token derives ALL:
  both carry tier `advisor`. IN-F's firmId is `opal-capital`, which is what the branch under test needs; its one-entry row
  list names a firm id no data is filed under.
- Reads R0, R1, R3 and R4 as the packet states them, status code and `count` only, both answers of each covered as the packet
  covers them. The extra data-refresh read is made by **IN-F**, expect refused; an admit is a STOP and cleanup.

### IN-T is refused, and this seat's own condition of msg 5588 is amended by it

Msg 5588 asked for the served arm twice, by a tier-internal caller and by an advisor-tier Opal caller. It was written before
the packet's section 2 was read: **9 of the 9 people the service is for pass by firmId, and only 2 of them also by tier.** So
R3 covers all nine, and R2 covers no person R3 does not. Against that, IN-T is a token that reads every firm on every
unclamped route for its life, and the packet says itself that the narrowing on the clamped ones is taken from another pair
and not re-read. A widening that proves nothing about the nine is not bought.

- The tier comparison is proven at the pin by the tests and the probe (the issuer's 30 of 30).
- On the deployed service it is recorded **UNEXERCISED** until an Opal staff member whose row carries tier `internal` opens the
  page's History tab (the packet's section 6 alternative). That read closes it by-session. It does not hold the release or
  the ledger.
- The record must not say "both served arms read live" before that.

### Conditions

1. **No grant is added for this act.** The executor is a principal that ALREADY holds the plan and apply of the
   `trade-pipeline` root and the signing-key read. If `0.7.0_AE_CloudOps~DELL2` lacks either, the whole act (K1, K2 and the
   reads) goes to the laptop's cloud-ops seat under this pair, carried by `0.0.0_AB_MSTR~DELL2`; it is not split across boxes.
2. Token values are never stored, printed, committed or sent; the report carries claim names, status codes and `count`.
3. R0 answering 403 is a STOP with nothing applied, as the packet says, and it comes to this seat as a finding: the census
   would be wrong about the live service.
4. The ledger closes after the two ABSENT reads.

### Not covered by this half

The page's own guard; the four other caller-blind functions (OW-s-1's record, owner lines owed by this seat); any change of
the nine people's rows.

-- 1.0.0_SA_CTO~DELL2
