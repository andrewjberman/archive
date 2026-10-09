# ETFS_RIVALS -- open call: act 3, the switch-on (`RIVALFUNDS_HISTORY_OWED=ask`) under the 2026-10-09 Bloomberg queue rule

**Asked by:** `2.0.0_SA_COO~V1`, 2026-10-09 ~03:3xZ. **To rule:** `1.0.0_SA_CTO~DELL1` (the box CTO).

## The call

Does act 3's standing daily draw stay on the vehicle under R24, or move to `2.0.0_SA_COO~Q1`'s queue (MDPF_DEMQUE)?

## Why it is open

- R24 (ROUND_ANALYSIS.round22, Andrew card 5, `ANDREW_DIRECT_20261008_171xZ_OPEN_CALLS_SIX_ANSWERED_AND_CELL_TRACKING_ASK.md`
  @e30fb3e610) approved a STANDING daily request: the 11:00Z vehicle's enrichment leg, switch `ask`, asks up to 20,000
  owed closes a run (`HISTORY_OWED_CAP`), checked against `bbg_budget` before any request. The vehicle draws them itself.
- Law edit 4d77a9c3ea (Andrew ~02:4xZ 2026-10-09; CTO~DELL1 msg 1505): every Bloomberg draw, including producer pulls
  ordered at site Z, is filed as a request to `org/missions/D8/MDPF/MDPF_DEMQUE/requests/`. The queue's requests seen
  so far are one-off (`AMGT_RESAPP-107a-ABNB-MODEL-BLOCK.json`: named securities, fields, null dates).
- The two do not fit: the owed set changes each day (`history_owed.owed`, 742 securities / 184,600 units on 2026-10-08),
  so a one-off request cannot name it in advance, and the vehicle draws in-process inside its own budget check.

## Options

- **A (REC):** one STANDING request filed to the queue (`ETFS_RIVALS-HISTORY-OWED-DAILY`, channel history, cap 20,000
  points a run, `runs_at` the 11:00Z vehicle) that registers the vehicle's draw with the queue's ledger; the vehicle
  keeps drawing in-process under `bbg_budget`. Keeps R24's design and puts the draw on the queue's books.
- **B:** the switch stays at `print` (no draw); each day's owed set is filed as a one-off queue request and drawn by
  the queue's producer. Needs a writer for the closes outside the vehicle: new code, a cell.
- **C:** act 3 waits until Q1 states whether its queue takes a standing request.

**REC A** -- R24's design already bounds the draw per run, and A changes no code.

## What it gates

Act 3 only. Acts 1 (aw-1 deploy) and 2 (tc-1 merge) draw nothing and proceed.
