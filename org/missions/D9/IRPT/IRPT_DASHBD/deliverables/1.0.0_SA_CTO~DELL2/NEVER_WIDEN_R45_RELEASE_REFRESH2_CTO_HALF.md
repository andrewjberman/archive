# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_DASHBD R45 release, refresh 2 (DB-b-117)

**Signer:** 1.0.0_SA_CTO~DELL2 | **Date:** 2026-10-11 ~05:1xZ | **Verdict: SIGNED,** on the conditions of section 4.

**Signed against:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~92/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_2.md`,
sha256 `863f98a21e34d5ad5e65875dc8a718c4998d036c01da365dbfa53864c0e13758` (`sha256sum` by this seat on the tree file: equal), and
the COO half `deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_R45_RELEASE_REFRESH2_COO_HALF.md` @212d7ad3f9. Any half of this seat on
the two earlier R45 packets is VOID for the apply.

## 1. The act and its blast radius

ONE Lambda's code, `irpt-49f-reporting-gold-lambda`, over live `oNgy4rnr...`, changing exactly four members at their PINS:
`handler.py` @080dc90d92, `account_return_daily.py` @354214c55f, `account_activity_lots.py` @19ba6fe341, `sources.json`
@f043506a7c. No key, read, grant, prefix, schedule or memory change. Writers on the handler's path: 4 `put_object` sites
serving 6 objects, as the packet counts them.

## 2. The two questions the packet leaves to the halves

1. **`sources.json`, carrying `_commonwealth_delivery`, is IN the release.** This seat's condition (msg 3999) was that no
   reader be moved by that entry. The packet reads `declared_sources` (`account_return_daily.py:311-317`) as skipping every
   underscore-prefixed key, with every 49F path taking its source through it. Accepted on that reading, which this seat did
   not re-read. The entry is carried and unread.
2. **The three ADDED returns-manifest keys are a WIDENING of what the served manifest states, and this half signs it by
   name:** `valuation_source` = `custodian_reported`, `fee_treatment` = `gross_of_advisory_fees`, `price_basis` =
   `custodian_closing_price`. They are the outcome DB-b-96 was ordered to produce. No served number, no existing key and no
   table byte changes. **This release is not DELTA=0 and is not described as such anywhere it is recorded.**

## 3. What this seat read itself, and what it took as filed

- **Read here:** the packet and the COO half in full; the packet's sha256; and one census of the three new key names over
  the repo (`comp-find valuation_source`, corpus default: 146 hits in 52 files of 70,647 scanned). Outside tests, records
  and the producer, the name appears in `sources.json`, `cottonwood_aua.py` and `commonwealth_account_return_daily.py`.
  No file under `portal/` or `infra/aws/lambda/` reads it except the handler's own test.
- **What that census does NOT show:** who reads the returns MANIFEST. A reader that validates the manifest's key set
  strictly would break on a key it has never seen, and it would not name the key. The packet counts the readers of
  `sources.json` (4 of 19) and the writers of the manifest; it does not count the manifest's readers. Condition 1 closes it.
- **Taken as filed:** the five table hashes (one kit day, local runs), the 91 field comparisons, the member census and
  pins, the live digest and S3 version, and the memory figures. The Lambda's memory on the new bytes is argued, not
  measured, as both documents say.

## 4. Conditions

1. **Readers of the returns manifest are counted before the apply.** Every reader of
   `account_return_daily`'s `manifest.json`, in served code, gold consumers and the portal, named with file and line, count
   printed; for each, whether it accepts a key it does not know. A reader that refuses unknown keys is a STOP and comes
   back to this seat. Zero readers, or all tolerant: proceed. This may ride the apply order's preflight.
2. **The COO half's four conditions stand as this half's:** build from the four pins, never HEAD, each pin's sha256
   re-read against the packet; one dry-run invoke after the upload read against 85 percent of memory and of the timeout,
   OVER is Branch B; the apply waits for Monday 2026-10-12's scheduled fire on `oNgy4rnr` (row D2-W78-S1); the first
   scheduled fire after the release is read for the three added keys and `method_version` 2 before the ledger closes.
3. **The plan reads 0 to add, 1 to change, 0 to destroy.** Any other count: stop.
4. **Rollback is the packet's:** the base S3 version `qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ` and the four prior pins. A returns
   manifest rewritten after the release is restored by copying its prior version; removing a new `date=` key with no prior
   object is an S3 delete on Andrew's word.
5. **Not covered:** DB-b-118's later change to `account_return_daily.py`; any member beyond the four; any Cottonwood
   write; `dim_return_method`.

Both branches A and B are the packet's, including its stated limit that a day a backfill refuses is not owed again by the
scheduled catch-up.

-- 1.0.0_SA_CTO~DELL2
