# IRPT_YCDGEN round 11, cell YCD-f-11 -- never-widen packet: ONE equity joins the held-characteristics store

**Author:** `2.0.0_SA_COO~G2`, 2026-10-11, the REQUESTER. **For:** `1.0.0_SA_CTO~DELL2` (CTO half) and the store's owner
(its half; named in section 2). **Ruling:** CTO round-11 analysis @457305b604 section 4 item 6. **Nothing is sent, filed
or edited by this packet.** The request draft stays where it is:
`../r10/BLOOMBERG_REQUEST_ONE_EQUITY_DRAFT_NOT_SENT.json`.

## 1. What is asked, and why it is not a one-time read

One security, `MPC US Equity` (CUSIP 56585A102 by Cottonwood's transactions cache, unconfirmed against the source), with a
country and a sector in the store the Opal Overview reads. One eligible Cottonwood account of 10 positions reads 76.85%
covered by value today and 91.29% with this one row (`../r10/STORE_BY_KIND_AND_THE_ONE_ACCOUNT_20261011.md` @804449eb87).

A reference answer does not reach the report. The Overview reads the LATEST dated `characteristics.parquet` under
`s3://opal-data-etfs/bbg/`, and that file is written once a day by one producer for that producer's own universe. So the
row exists on the page only while the security is IN that universe, every day. The act is a universe change, not a read.

## 2. The one writer, read from its own rule (N = 1, printed)

Writers of "which securities have a row in `characteristics.parquet`": **1**, `integrations/bloomberg/pipeline/etf_daily_pull.py`,
run by a scheduled task at site Z. Its universe is built at lines 205-217: the funds' constituents, the 4 funds, and a
constant `EXTRA_SECURITIES` (line 52), today `["GLD", "VXX"]`.

- **The one row added:** `"MPC"` appended to `EXTRA_SECURITIES`. The pull then queries `MPC US Equity` and writes one more
  row per day.
- **Who may do it:** not this seat. The file's recent commits are MDPF_SECHIST's (`2.0.0_SA_COO~H1` and its workers,
  2026-10-07 to 2026-10-09). `EXTRA_SECURITIES` itself was opened on Andrew's word of 2026-09-14 ("Call 4 Yes", the file's
  own comment at lines 47-51), gated by `1.0.0_SA_CTO~Z`. `integrations/bloomberg/READ_HERE.md` line 104: site-Z scheduled
  tasks run the working tree, so an edit to this file IS a deploy the moment it touches disk.
- **So the owner's half is the site-Z owner's, and whether a third extra security needs Andrew's word again is not mine
  to read wider:** his word of 2026-09-14 opened the list for two named securities for another consumer.

## 3. Blast radius, both branches read from the producer's rule

What the one entry does at the next scheduled run, by the code:

1. **One more query and one more row** in `characteristics` (line 864) and in the run manifest's `extra_securities` (line 882).
2. **A history-depth request for the new security.** The pull asks history for any security whose earliest stored row is
   later than the depth window (lines 54-58, 247, 756). A security with no stored history needs depth, so `MPC` draws a
   one-year history from the one Bloomberg budget on its first run. NOT sized here: the cell count of that draw.
3. **A second consumer sees it.** The file states the extra securities' consumer is "the POSN_ASTTAX satellite
   characteristics aggregation" (line 51). Whether a third extra security changes that aggregation's output was NOT read.

Branches:
- **The source describes it** (expected for a US equity; the store's 127 equity rows all carry both fields): one row with a
  country and a sector; the account reads 91.29%.
- **The source returns the row with an empty field, or refuses the ticker:** the row is absent or carries no sector, the
  account stays at 76.85%, and the pull's own failure handling decides whether the day's file is written. Which of the
  pull's failure paths a refused extra security takes was NOT read; the owner's half must state it, because a failed day
  has no backfill (READ_HERE.md, "CURRENT-DAY ONLY").

## 4. Rollback

Remove the entry. Rows already written stay in their dated folders; the next day's file carries no `MPC` row and the
account reads 76.85% again. History already drawn is not returned to the budget.

## 5. Not established (each one is the owner's to state before any half is signed)

- The size of the history draw, and whether the day's budget holds it.
- What the POSN_ASTTAX aggregation does with a third extra security.
- Which failure path a refused extra security takes, and whether it can cost the four funds their day.
- Whether the demand queue (`org/missions/D8/MDPF/MDPF_DEMQUE/requests/`, 16 files today) is the route for a standing
  universe change, or only for one-time draws. The draft is in the queue's key set; that it is the right carrier is unread.
- That the report then shows it: only an Opal generation exercises that, which only Andrew's sign-in can submit.

## COO HALF (the requester's)

**SIGNED as requester only** -- `2.0.0_SA_COO~G2`: the request is one security, two fields, and this seat edits nothing
at site Z, files nothing in the queue and sends nothing to the source. This half does not sign the producer's decision.

## STORE OWNER'S HALF

(owed: the site-Z owner of `etf_daily_pull.py`, with section 5's first three lines answered)

## CTO HALF

(owed)
