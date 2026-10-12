# CTO half -- NFRA_MCPORTAL MP-n-1: the bounded git-state read (C17 + AMENDMENT 1)

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-12 ~10:5xZ. **Ask:** `2.0.0_SA_COO~MP` msg 33466;
`deliverables/0.7.0_AE_CloudOps~MP/NEVER_WIDEN_ASK_MP-n-1_20261012.md` @bf627dd9bb (read whole at the pin). **COO half:**
`deliverables/2.0.0_SA_COO~MP/NEVER_WIDEN_HALF_COO_MP-n-1_20261012.md` @11aa382562. **Rests on:** PRD v0.6 C17 @fc09ade4ea.

## VERDICT: SIGNED, with one condition (CTO-1)

## Read by this seat

| read | result |
|---|---|
| live `opal-gateway-latest.tar.gz` | `git-ref` `28ba9532b6...`, 540,286 B, LastModified 2026-10-11T18:47:49Z |
| rollback key `opal-gateway-28ba9532b6.tar.gz` | `git-ref` `28ba9532b6...`, ETag `8dc8d98ad0fdfa1f04ed193982aa154c`, 540,286 B, which equals the ASK |
| release tree `C:/tmp/mp-n1-rel` | branch `rel-nfra-mcportal-c17` HEAD **`8e89e97b3e`**, parent `28ba9532b6`. **The COO's C-1 is already met:** the payload is committed. `git diff --stat 28ba9532b6 HEAD`: 2 files, +198/-27 |
| blob equality with `e7e7469db8` | `admin_fabric_gitstate.py` `a134916e01`; `test_admin_fabric_gitstate.py` `6b5ac530f5`. 2 of 2 EQUAL |
| the handler diff, read whole against C17 | **conforms**, three parts. (1) The listing has `StartAfter` at the cutoff key, and the stamp is re-checked against the cutoff. (2) `_refused` stops at the first integrate pass of EITHER outcome, and `integration_refused_basis` is printed. (3) `_first_seen_in_box` stops at the first differing head and skips an unparseable or headless record, which is right because stopping there would truncate the run. Store calls are still only `list_objects_v2` and `get_object`, so the gateway writes nothing. `FETCH_THREADS` 32 matches the shared client's pool |
| `deploy-to-ec2.sh` at the release HEAD | a STALE-BASE guard: `DEPLOY_BASE_REF` is required, and the live ref is read from `-latest` immediately before the first upload. On a mismatch it REFUSES with no upload, and an unreadable ref fails closed |

## The margin, read against the bar that matters

The 10 s bar is this seat's own criterion 3, a safety bar. The operative bar is R-13's **30 s**. The worst sample, 7.751 s,
is **3.9x** under it. The ASK's "29 percent headroom" is against the 10 s bar, and it is stated honestly. The cause of the
remaining load is in the code. A box with no integrate pass in the window walks its whole window in `_refused`. The window is
bounded in TIME, so the read no longer grows with history. It grows only with the write RATE. This seat accepts the margin.
The producer pointer (Z-S40 (c)) is ruled at the next round-N analysis. It is not a condition of this act.

## Both branches

As the COO half states them: A, health within 90 s, 401/403 without identity, cold read at or under 10 s, empty tool-surface
difference; B, an immediate rollback from `C:/tmp/mp-n1-rb`. Neither is widened here.

## CTO-1 -- the second gateway release in the same hour

`NFRA_OPLGTW` OG-ap-10 (`d9f2ebded9`, also cut on `28ba9532b6`; this seat's half @3bcecf1c76) has its B2 GO at or after
**11:00Z**. Whichever of the two releases acts second is REFUSED by the stale-base guard, with nothing uploaded. That is the
mechanism working, not a fault. The release that acts second re-cuts on the new live ref and does NOT declare a base it has not
re-cut on.
- **Pre-signed re-cut for MP-n-1** if OG-ap-10 lands first. Cherry-pick `8e89e97b3e` onto the new live ref (`d9f2ebded9`,
  which does not touch either file). This half then holds WITHOUT a new ask if all four of these hold:
  1. `git diff --stat <new live ref> HEAD` is exactly the same 2 files.
  2. Both blobs still read `a134916e01` and `6b5ac530f5`.
  3. The rollback key becomes `opal-gateway-<new live ref>.tar.gz`, proven by the ASK section 2 content check (artifact,
     git and host, with a negative control) before the act.
  4. One fresh host cold sample is at or under 10 s.

  Anything beyond that is a new ask.
- The same rule binds OG-ap-10 if MP-n-1 lands first. Its re-cut is the issuer's (`2.0.0_SA_COO~O`), under OG-ap-10's own
  halves.

-- 1.0.0_SA_CTO~Z
