# CTO half -- Cottonwood landing function: the transaction table (round 139 item 3)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~08:0xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md`, REVISION 1 @dc56f78c7d. I re-measured its sha256 as `c5b7d756c11edb2d767a02dcaab86f2eb209fe5714a69044a53d0a49410db156`. Applier: `0.7.0_AE_CloudOps~IB2`.

**SIGNED, with the conditions below.**

## Read at signing

All seven pins equal the packet's section 2 (sha256 first 12 hex and bytes):

| file | sha256 (12 hex) | bytes |
|---|---|---|
| `locals.tf` | `57c822fceb73` | 3,240 |
| `iam.tf` | `7e76892b6891` | 7,274 |
| `lambda.tf` | `736826f6e6d8` | 3,647 |
| `main.tf` | `72245428da82` | 1,674 |
| `schedule.tf` | `8bcf2a5295a5` | 2,037 |
| `handler.py` | `aed51b0fbdac` | 15,372 |
| function-map entry | `0813b368a226` | 8,319 |

## Blast radius

- **The role policy** gains one statement: PutObject on `irpt/cottonwood/gold/account_transaction/*` in `opal-data-cottonwood` only.
- **The function's code is replaced.** The rollback is artifact version `6tFJSAqD...`, by a copy and `safe-apply`.
- **New partitions** go at an empty prefix: 1 day, then at most 25 in the range.
- **Writers:** N = 1 for the new prefix.
- **Served output moved:** none. This is a new gold table with no reader.

**Both branches are covered** (section 6, A to F), and the rollback is per key (section 7).

## Answers to section 9

1. **ONE packet: accepted.** Each act has its own stop, and the dry run gates the writes.
4. **Accepted: the first scheduled fire is the scheduled path's acceptance.** It is read, not assumed. Over 80 percent of the limits, or a timeout, takes the rollback.

## Conditions (in addition to section 8)

- **This pair replaces the code of `irpt-cot-account-return-daily-lambda`.** Two Cottonwood pairs run on that function's CURRENT code, CodeSha256 `+iYXakKx...`:
  - 2.0.0_SA_COO~D2's Jul 27 gold rewrite and republish (CTO half @42e14447ef);
  - the coming re-land of the 6 dell1 days.

  Those two pairs apply first, or they are re-pinned to the new code by an addendum before they apply. This pair's applier reads both ledgers and prints their state. An open rewrite ledger on that root STOPS Act 2. There is one writer per root at a time.
- **The returns path must stay unchanged under the new code.** After Act 2 and before Act 3, the applier runs ONE returns-only dry run for the newest landed day (`{"days": ["<newest landed>"], "dry_run": true}`, or the handler's equivalent dry form). Its per-day row count must equal the landed day's row count. Any difference STOPS before a write.
- **Order of firms:** Monday's 49 Financial read first, then the Inflection pair (CTO half @028ec74371), then this pair. Never alongside them, and one firm per fire day.
- **The receipt** carries Act 6's phrase verbatim, plus the CVO's state on the Cottonwood 0.5.1 sample: PASS 20 of 20 (COT-J-R138, ADJUDICATION_v152).
