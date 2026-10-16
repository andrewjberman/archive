# IRPT_ANLREQ FWD-1 run, ADDENDUM 3 AMENDMENT 4 -- R0e re-pinned from the resident r34d (rolled back at V2S) to the resident r34e, and the in-service V2 must show both sides -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No run-3 order is lifted from HOLD until the CTO half of THIS amendment and of the r34e packet are signed, and AQ2's r34e install has closed with `V2S OK`.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-16. CTO half: owed, `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Amends: addendum 3 (COO blob `64884b3338965c79a962c3f40cdb5cde44ad5811`) section 5 read R0e, as amended by amendment 1 (blob `7a4e8735155f871b8f8573d0d4d0f3cc63704bec`) and re-pinned by amendment 3 (blob `0975453cd1e992d8244ba9abccda90bb3e0f308b`, CTO half @b8554e2112) section 4. **Only R0e's pins change.** Everything else stands as signed: amendment 3's second probe set (the same five candidates, the new viewer `irpt-r3q-iv-<YYYYMMDD>@opal.invalid`, the amendment-2 re-post rule, ten posts at most), its corrected storage claim (MEASURED: one `original_holdings` CSV per correction answer) and the objects joining the delete row `dc59`, the CTO's stop conditions of msg 9337 (ZQXWVK must read NOT_FOUND or the window stops; all five CHECK_FAILED stops before the run user), R0d (r35L), R0f (order amendment 1), the inputs, W7.

Claim words: MEASURED = this seat read it in this session; RECORD = a committed record this seat opened (named); RELAYED = carried by another seat; INFERRED = said so; ABSENT = not read.

## 1. Why R0e moves again (RECORD)

Amendment 3 pinned the r34d resident (root `0485393f3a-r34d`, tar sha256 `9a088a5c...78ab`). AQ2 installed it and its V2 INSIDE the service's own environment FAILED: ZQXWVK still read CHECK_FAILED, reason EXCEPTION; the install rolled back to r34c the same session (ledger `irpt-resident-r34d-20261016`, records `42452bc86b`, `a0b1890490`). AQ2's read-only `EXCCLASS_READ.txt` (MEASURED by this seat): in the service ZQXWVK raises `curl_cffi.requests.exceptions.HTTPError` ("HTTP Error 404") from the quote fetch, not `YFTickerMissingError`. The r34e rule (CTO msgs 9345 and 9354, approved with one tightening) and its fix (cell `AR-g-125`, commit `101124c70c`, read by this seat) map NOT_KEPT only for a `YFTickerMissingError` by name, or a curl_cffi `HTTPError` with response status 404 on that symbol's own quoteSummary URL on finance.yahoo.com; every other exception stays CHECK_FAILED, tests on both sides.

## 2. R0e re-pinned (replaces R0e of addendum 3 as re-pinned by amendment 3)

R0e: the resident root is **`0485393f3a-r34e`** installed from the r34e tar (sha256 **`a96fbfb74db2caf6ad55d93ab35c3b7dd419cf54f4a4dba444bb3268e68e9227`**, **1,121,099 bytes**, 314 members, 311 identical to r34c; package pin `f9f851d215b1bcbb83ebe9c7a110e66d700d2191`; RELAYED `~G2` msg 9370 and MEASURED by this seat: packet `NEVER_WIDEN_PACKET_RESIDENT_R34E_SYMBOL_404_20261016.md`, COO half git blob **`fd4c17188b4e4b5432c00c3d434258025d66d494`** at this writing, to be re-measured at the CTO's signing and equal to his re-signed binding); the applier's install record (ledger `irpt-resident-r34e-20261016`) reads V1 green AND the two lines **`V2S OK SPY KEPT and ZQXWVK NOT_KEPT`** and **`V2S CONTROLS OK 4 of 4`** (CTO msg 9374: anything else rolls back to r34c the same session) from `v2_service_env_r34e.sh` (sha256 `32d52a15e6c12198f6d328a3a9b859bd68a55c8b28368902e90ece61534d5ea6`) run INSIDE the service's own environment (a shell run does not count), and that V2S prints **both sides**: ZQXWVK `NOT_KEPT`; and four controls with no Yahoo call using the host's real curl_cffi `HTTPError`: a 404 on its own quoteSummary URL reads NOT_KEPT; a 429, a 404 on another symbol's URL and a 404 on the chart endpoint stay CHECK_FAILED (any CHECK_FAILED prints its class and status) (RELAYED `~G2` msg 9370, in answer to this seat's msg 9365); the library delivery record reads CLOSED with `yfinance` importable by the resident's interpreter; `opal_pricing` false; the producer list `andrew@opalinvest.com` and `fwd1-staff-r41b@opal.invalid`; the r34c root kept as the rollback. A record naming the r34c, r34d or earlier tar or root as the running one, any V2S other than OK, a V2S that lacks the four controls, or a V1 that is not green, ABORTS.

## 3. Blast radius delta

Nothing is added to what the window moves (amendment 3 section 5 stands). The resident differs from r34c by three members only (the checker and its two companions per the packet's table); no new Yahoo call path.

## 4. Limits named

NOT read: whether the r34e install and its V2S have closed (gates, read at R0); whether the r34e fix reads NOT_FOUND for ZQXWVK through the door's whole path (the service-environment proof is the checker; the door's answer is what SET 2 shows); whether the packet's blob changes before the CTO signs.

## 5. Owed before the order is lifted from HOLD

1. The CTO halves: the r34e packet (blob above) and THIS amendment (this file's blob).
2. AQ2's r34e install closed: ledger `irpt-resident-r34e-20261016` CLOSED with `V2S OK` and the four controls.
3. This seat's order amendment: lift the HOLD with R0e at r34e and the second probe set (staged in the order, amendment 3; its R0e names r34d and is superseded by this amendment). Cut only after (1) and (2).
