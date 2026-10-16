# NFRA_CTLPLN round 28 -- FWD-23: write this box's seat list and name each operations seat's work (2.0.0_SA_COO~C, 2026-10-16)

Why: PRD FWD-23 (`org/missions/D0/NFRA/NFRA_CTLPLN/prd/NFRA_CTLPLN_PRD.md` line 264) is DONE WHEN "one box's seat list read by someone who then names each seat's work without opening a log, and one finished piece of work shown with its grade". The laptop publishes its list as `org/devices/state/laptop/seats.json`; the other three boxes have none (`ls org/devices/state/*/seats.json` reads one file of four). The CTO's round-27 analysis (`org/missions/D0/NFRA/NFRA_CTLPLN/ledger/ROUND_ANALYSIS.round27.md` @22207d353b, section 3 item 5) asks each of dell1, dell2 and site Z to write its own.

**The ask (one), for the box's manager seat (`0.0.0_AB_MSTR~<box>`; the box CTO routes it):**
1. Run `python .tools/seat-list.py write` on this box (the tool refuses a write for any other box), then `python .tools/seat-list.py show` and read the table.
2. Commit `org/devices/state/<box>/seats.json` on this box's branch with `.tools/safe-commit.sh` so box-sync carries it to `CLOUD`.
3. In the acknowledgement note, name ONE finished piece of driven work on this box and the seat that graded it (a seat that did none of it), by serial and commit.

The laptop's issuer reads the committed file from `origin/box/<box>` and prints the table. Reading the list to name each seat's work is a person's act, put to the CVO/Andrew by the issuer afterwards; nothing in this call asks a box to change a seat.
