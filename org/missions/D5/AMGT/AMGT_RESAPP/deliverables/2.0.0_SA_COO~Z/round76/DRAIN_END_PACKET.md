# AMGT_RESAPP round 76 -- drain-end packet (L8), `2.0.0_SA_COO~Z` to `3.0.0_SA_CVO~Z`, 2026-10-06 ~21:5xZ

Round 76 implements the CTO's round-75 analysis @326aea63b3. It ran on PRD v0.40, ADMITTED; PRD v0.41 (ADDENDUM E, Andrew's word
@b5f90bbf8d) landed mid-round and binds round 77, not this round. The issuance is @111e312e46 and the decomposition is s.84.
**6 of 6 orders are terminal.** The round was HELD from ~13:40Z to 17:45Z under Andrew's Bloomberg-priority word and resumed on his
word (MSTR~Z msg 30165). The function was redeployed from `D29LJCXh` to `OVpDhfwDG3BzKE++wDxMlFA6JrwpTnH3FiHC+NrzsrE=` (20:10:29Z),
memory 1769. The /freshness page is on portal DEV (MSTR~Z push `e2130d42`; DEV is now `6b4e89a8`).

## 1. Orders

| order | outcome | drain / act | mechanical result |
|---|---|---|---|
| az-1 | the /freshness page rendered for the CTO's review (ruling 1) | @8b4111fb11 | 8 captures and a render record at portal `6de76f0509`. First visit: first contentful paint 620 ms, table rows at 3,010 ms. The CTO approved the candidate from its own render (@7c328eb0df). |
| az-2 | FWD-16 news half and FWD-12 provenance half on /overlay (rulings 2-3) | @1ef4cd99de | c62 YES and c63 YES on deployed OVpDhfwD: 95 of 95 names serve `top_band` and `input_provenance`; 0 entries disagree with /freshness. 23 plant cases. Only 3 news items across 95 names on 2026-10-05 (row Z-W263-S1). |
| az-3 | the remediation-row triage (ruling 4) | @25dab214fb | c64 YES: 109 of 109 OPEN remediation rows carry a TRIAGE citing row: 30 closed by evidence, 26 cut, 53 blocked (owners 1.0.0_SA_CTO~Z 32, 2.0.0_SA_COO~Z 21). Table: `deliverables/0.9.0_WK_AMGT_RESAPP~264/TRIAGE.md`. |
| az-4 | the cold-phase table and cut (ruling 5) | @de48559928 | c65 YES locally (issuer re-run 3 of 3, then again at close). Generation read 1,964 -> 548-675 ms locally; bodies EQUAL 3 of 3. |
| az-5 | the code redeploy carrying az-2 and az-4 | close @1014126140; NEVER-2 closed @cad400c0b3 | Built at EXACTLY `de48559928`. CONTENT-DIFF CHANGED 7 + ADDED 1 (three riders from other projects, measured address-neutral). Proof VALID. AC2: r75 c57/c58/c61, r74 c53/c55/c56 and r71 c38 YES on the executor's run. |
| az-6 | the walk on DEV | @16924b8b1d | 21 captures on portal `6b4e89a8` against OVpDhfwD; walker disarmed; DISARMED relayed to MSTR~Z. |

The issuer's real run is `round76/REAL_RUN_r76_20261006.txt` (shared tree @b5c17cc606, function OVpDhfwD): c62 YES and c63 YES
deployed; c64 YES and c65 YES local; the c59 C2 wide burst YES; the api suite 732 passed. The /freshness post-push DEV read is
`round76/devread/DEVREAD_FRESHNESS.md` (PASS at `e2130d42`, CI success).

## 2. JUDGMENT for L9 (yours)

**az-6 AC3: the walk, per FWD.** Artifact: `deliverables/0.9.0_WK_AMGT_RESAPP~266/WALK_ROUND76.md` with `captures/` (21 PNG). This
walk is on the page AS DEPLOYED TO DEV, not a local merge (round 75 walked a local merge). The worker's observations, no verdict:
- **FWD-7 (`:549`):** a first visit painted the first row at **4,116 ms** (the /freshness read took 2,665 ms; the second visit 1,591
  ms; round 75 read 2,043 ms). 95 of 95 are flagged stale and Last refreshed reads 2026-10-06 on every row, so no stale name stands
  apart by flag or by that date (row Z-W266-S1). Three names differ by their Seeking Alpha date.
- **FWD-18 (`:678`):** on BA and ASML_NA a driver-chart point opens its filing passage with the cite. BA's passage text is flat and
  carries no column labels. AMD has no driver chart. ASML_NA's y-axis labels read clipped (row Z-W266-S3).
- **FWD-1 (`:493`):** BA has 11 segment rows under 3 labels, the label repeated per row rather than one heading per segment. AMD
  shows a plain reason in place of a breakdown. ASML_NA's 5 "segments" are share-capital items (row Z-W266-S2). The description and
  the Model tab opened on 3 of 3.
- **FWD-16:** not walked; the top band's page work (DSGN round 45) is not on DEV.

## 3. Rows filed this round (all OBSERVATION, INERT; disarm_owner `2.0.0_SA_COO~Z`)

| row | gist | disposition |
|---|---|---|
| Z-W262-S1 | the stock walker cannot take per-sort or first-paint captures | a one-pass driver kept under `instrument/` |
| Z-W262-S2 | "Web search is not collected yet." reads 2.16:1 contrast, under 4.5:1 | round 77 (the CTO also asks to hide the all-"Not collected" column) |
| Z-W263-S1 | "latest trading day" read as the last settled day gives 3 items across 95 names | a round-77 call: newest day the name has news |
| Z-W264-S1..S109 | the 109 TRIAGE citing rows | 53 BLOCKED rows now name a live owner |
| Z-W265-S1..S3 | TLS stalls on fresh local runs; 0.76-0.81 s outside every phase; a device-only pandas import cost | recorded |
| Z-S360 | the az-5 phase-sum cut (about 1.8 s) is offset by out-of-phase growth; the phase label set changed | needs a phase-COVERAGE read, not another latency run |
| Z-S361 | c59 C2's burst of 6 cannot force a cold start once the route is fast | RULED: the issuer measured C2 with a 40-wide burst (34 and 35 cold invokes, all 200, 660-1,047 ms vs 2,000 ms); the check's width is repaired at the round-77 cut |
| Z-W266-S1..S3 | the walk's three observations in section 2 | for your read |

## 4. Cold start

- **Chatter:** cold Duration 2,987-3,177 -> 2,580-3,137 ms on the deployed function (AE~A, 6 cold invokes). It stays above about 2 s,
  so provisioned concurrency stays on Andrew's list. Row Z-S360 says why the in-phase saving does not show in the total.
- **/freshness:** cold invokes answer in 660-1,047 ms (the wide burst). The walk's 4,116 ms first paint is a page-level number: the
  read alone took 2,665 ms for a 1.07 MB encoded body, slower than round 75's 694 ms. That gap is unexplained and is a round-77 item.

## 5. For round 77 (already ruled; cited, not cut here)

- CTO msg 30312 on Andrew's word @b5f90bbf8d: the re-run button is RETIRED (PRD v0.41; FWD-12 is the provenance half only); remove
  the /refresh no-op; three Bloomberg research pulls after the 7:00 AM ET vehicle, one at a time, each under its own pair; the FWD-14
  owner line on /freshness, with no alert built.
- CTO msg 30183: FWD-20, the trailing-trend FCF v1 (round-75 ADDENDUM 1 @68c5b56369).
- CTO msg 30181: hide the all-"Not collected" Web search column; producer display names.
