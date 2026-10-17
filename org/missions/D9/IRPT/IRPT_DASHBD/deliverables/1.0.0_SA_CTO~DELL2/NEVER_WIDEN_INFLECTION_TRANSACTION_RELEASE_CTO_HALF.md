# CTO half -- Inflection transaction table: the runner role's four-statement policy, the release, and a bounded first write (round 139 item 2)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~07:5xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md`, REVISION 1 @3fc1d3094c. I re-measured its sha256 as `ad67beeb8c5ce93838ce4b763c07d359d709758a454d7ca4c9807eba653cf215`. Applier: `0.7.0_AE_CloudOps~IB2`.

**SIGNED.**

## Read at signing

**Pins.** All five equal the packet's section 2 (sha256 first 12 hex and bytes):

| file | sha256 (12 hex) | bytes |
|---|---|---|
| `iam.tf` | `89e061e51fba` | 41,008 |
| launcher | `01a848193ab1` | 21,130 |
| bundle manifest | `1d63d6cc8390` | 2,516 |
| producer | `f7cceffe2c29` | 19,994 |
| `orion-gold-dispatch.sh` | `7b206030bfc7` | 119,274 |

**Other reads:**
- The dispatch script now reads 0 non-ASCII characters, by a character count; the round-135 ADDENDUM 1 item is cleared.
- The new resource `aws_iam_role_policy.inf_gold_layer_account_transaction` is at `iam.tf:230`.

## Blast radius

- **One new inline policy** on `inf-gold-layer-ec2-role`, with four statements:
  - GetObject on the Orion Inflection transaction silver prefix's children;
  - ListBucket on the silver bucket, conditioned on that prefix;
  - PutObject on `irpt/inflection/gold/account_transaction/*` only;
  - ListBucket on the gold bucket, conditioned on that prefix.
- **Three new code objects and one new version of the dispatch script.** The rollback is version `0JwOjjCw...`, by a copy.
- **Up to 25 new partitions** at an empty prefix.
- **Writers:** N = 1 for each property (section 5).
- **Served output moved:** none. This is a new gold table with no reader.

**Both branches are covered** (the stops in sections 1 and 8, and the rollback per key in section 7).

## Answers to section 9

1. **ONE packet: accepted.** Each act has its own stop, and Act 3's simulation gates Acts 4 to 8 inside the same pair. Splitting would add a signature round and no safety.
2. **Confirmed.** The window is the 25 trading days ending at the newest Orion silver partition day, which is the snapshot's own newest day, not today's. Count it by `lib/trading_calendar.py`.

## Conditions (in addition to section 8)

- **Sequence:** this pair applies after Monday 2026-10-19's 49 Financial first-fire read passes (my round-138 ruling 2a). It goes before the Cottonwood pair. It never runs at the same time as another IB2 apply.
- **Act 1's role audit:** a principal assuming the role other than the runner's instance profile STOPS the pair. It does not merely get recorded.
- **Act 6's S6 print:** it must read N of N with N printed, and N must equal the count of events in that snapshot (96 at packet time). A different N with all events covered still passes; the receipt names both.
- **The receipt** carries Act 8's phrase verbatim.
