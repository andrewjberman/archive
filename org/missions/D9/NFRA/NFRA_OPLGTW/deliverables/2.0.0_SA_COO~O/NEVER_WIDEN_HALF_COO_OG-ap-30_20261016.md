# Never-widen half (COO) -- OG-ap-30, delete the two `email_deny` records that the OG-mg-1 restriction put on the Opal owners (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-16 ~19:2xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-30.md` (`~NFRA1` Phase A, commit `e884bfe5aa`, merged `4bb14eb50c`), sha256 `c9032e35de62d86c0e7ccc1efa17cc7cf53340f890bf90f9d3526eae6095212e` (recomputed by this seat from the file: equal).

## SIGNED, on conditions C1-C5

What this seat read at signing:
- **`ap30.AC1`, issuer re-run: PASS** against the LIVE table: the ask has three half headings, names exactly `andrew@opalinvest.com` and `opalbloomberg@opalinvest.com` as the write set and `alyssa@opalinvest.com` only as untouched, and carries no other e-mail address; the before-record has `write_set` `[andrew, opalbloomberg]`, `writes` 2, one sha256 per item for all three, `email_deny_total_before` 3; the live strongly consistent read shows all three records present and active, count 3. The check was dry-run at the base (FAIL) and on real shapes (PASS plus controls) before the order was cut.
- **The widening, stated plainly:** a NARROWING reversal. Two items are deleted from `gateway-access-state-table`; the four email-only browser routes (`/login`, `/sprint*`, `/rivalfunds*`, `/yearinreview*`) are open again to the two Opal owner e-mails, as they were before 11:22Z. The restricted profiles and grants of `OG-mg-1` R1 and R2 stay as signed, so both owner principals remain restricted on the MCP surface. No data scope changes.
- **My part in the defect:** the `OG-mg-1` ask and my COO half named the `email_deny` records for the rollback only and did not state that the owners lose the browser routes (row Z-S312). This order reverses exactly that effect and no more.
- **Both branches:** one `TransactWriteItems`: records present and active at the recorded hashes, it lands; any difference, no key is written and the applier stops. Alyssa's record is read-checked inside the same transaction, so it fails closed if she moved.
- **Rollback per key:** put the saved item back from the git-excluded `DENY_ROLLBACK_ITEMS.json`, or `deny-backfill` for that e-mail; seconds.
- **The applier's identity:** simulation read by the applier: `DeleteItem` and `ConditionCheckItem` allowed; the gateway operator role (no `DeleteItem` by design) is not used.

**C1 -- the ask stays at its bytes through the GO** (sha256 above). Any change re-opens all three halves.
**C2 -- the write set is the literal two-key list;** `alyssa@` is a condition check only. Any other key, or a third e-mail in any message of this act, stops it.
**C3 -- Phase B step 1 re-reads the three records** at the recorded hashes and `active`, and the count 3; else STOP.
**C4 -- `ap30.AC2` is read by this seat** from the live table before `OG-ap-30` is flipped, and Z-S312 is disarmed only when the owner account's browser run (via MC Portal) reads non-deny on `/sprint` and `/rivalfunds`.
**C5 -- no key hash, `oid`, `tid` or client identifier** in any file or message; `DENY_ROLLBACK_ITEMS.json` is never committed, imaged or mailed.

## Not covered

- Any other principal or email_deny record (Alyssa's stays).
- The durable route-class guard (`OG-en-14`, rides the next batched release).

-- 2.0.0_SA_COO~O
