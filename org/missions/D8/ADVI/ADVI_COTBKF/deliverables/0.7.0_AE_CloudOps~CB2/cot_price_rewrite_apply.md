# ADVI_COTBKF.TO-CB-aj-2 -- the 38-key cot price rewrite, 49F rows out

**archetype:** DEPLOY

**Seat:** `0.7.0_AE_CloudOps~CB2` | **Issuer:** `2.0.0_SA_COO~C2` | **Round:** 36 | **Cell:** `CB-aj-2`
**Risk class:** SERVED | **Date:** 2026-10-09 | **Order at:** @11870bd837 (AMENDMENT 1 @732138aa45)
**Criterion:** `CB36aj2-AC1` -- **PASS** | **Proof:** VALID (rc=0), first pass
**Ledger:** `org/critical_paths/change_management/20261009T1320Z_advi-cotbkf-cot-price-rewrite-cb-aj-2-20261009_deploy_completion.md`
-- 5 legs, CLOSED, all proven.

---

## Outcome

38 keys in `opal-data-cot` under `silver/prices/` each carry **one new version** with the 49 Financial
rows removed (1,734 rows: 111 across the 37 daily files, 1,623 in `canonical_prices.parquet`) and the
three cross-firm bonds left **UNPRICED**. `COT-PRICE-REWRITE-VERIFY keys=38 match=38/38`, rc 0.
**No version was deleted** and all 38 priors are proven still retrievable.

This closes D2-S52: Cottonwood's price store no longer carries another firm's prices.

## The three pre-write gates, and the one I refused to decide

The order put three gates before the first write. Two I proved; the third I would not read on my own.

### C3 -- the schedule census

Called the rewrite script's own `census()`/`scheduled_count()` directly, because a rebuild is forbidden
and there is no census CLI mode. `writers=7 scheduled=0`, identical to CB-aj-1. The part that matters is
**why** it is 0 with the chain ENABLED: `scheduled_count()` counts only writers the live
`opal-cot-gold-run` SSM document actually runs, and the wired set is **empty**. Of the 7 candidates only
one is a cot script; the other six are `data/black_diamond` and `data/inf` scripts writing their own
firms' artifacts.

### C2 -- the missing-price line, which nearly went the other way

The cited line is `price_holdings()` in the **deployed** `code/gold/B_00.canonical_holdings.py`: `:689`
maps price by `asset_name`, `:702` computes `market_value = units * price`. A `.map()` miss gives NaN and
NaN propagates. **There is no `fillna(0)` on `price` or `market_value` anywhere in the file** -- the only
`fillna(0)` is on `units`, a different field. So the chain marks a priceless holding NaN. That is the
amendment's proceed branch.

But the same file carries an **unflagged stale-price carry-forward** at `:1339-1378` (`_ff_worker`): it
takes prior-day prices for assets absent from the target date, concatenates them with today's, and logs
only above 10% fallback -- and the served row gets **no claim field**. Worse, after this rewrite the three
bonds are absent from `canonical_prices`, so they would land in exactly that fallback set and the removed
49F-derived prices would be **re-injected silently**, on the three CUSIPs this act exists to clean. That
is verbatim the condition's STOP branch.

**It is unreachable for cot, and I measured that rather than trusting the comment that asserts it.**
`_ff_worker` runs only over `non_schwab_dates` (`:1404`), and `:1266-1276` sets that list empty on the
single-custodian branch. `schwab_cache` is built from `schwab/silver/rps/` in the cot bucket, and that
prefix holds **0 objects**, as does `schwab/` -- while a **positive control** with the same lister on
`silver/prices/` reads **90**. So the zeros are the world, not a broken lister, and the carry-forward
cannot touch Cottonwood today.

**The count condition 3 requires: 99 gold account-days.** Denominators printed -- 133
`gold/canonical/holdings/` date files, all 133 read, 1,515,703 gold rows scanned, 103 files holding a bond
row. Per bond, by `asset_name` resolved from the removed rows themselves (`source = bd_txn_price`,
`ticker = CUSIP_<cusip>`, read out of the prior version of a daily file):

| CUSIP | asset_name | account-days | priced | current market value |
|---|---|---|---|---|
| 95000U2D4 | WELLS FARGO & CO 4.15% 01/24/2029 | 103 | **99** | $2,458,385.58 |
| 05613L3H2 | BNP PARIBAS SA | 0 | 0 | -- |
| 651639AX4 | NEWMONT CORP 2.8% 10/01/2029 | 0 | 0 | -- |

So the next gold run turns **99 account-days on one account** to NaN, withdrawing about **$2.46M**.
The two zeros carry a control, because exact `asset_name` matching would read a spelling difference as
absence: a substring sweep over the same 133 files found 0 BNP names, one `NEWMONT CORP COM` (the
**equity**, 1,417 rows) and three WELLS FARGO names of which only ours is the 2029 bond -- the others
being the equity and a **different** 2028 bond. None is touched by this rewrite, so the 99 is not an
understatement.

### C1 -- the gate that could not be satisfied as written

Condition 2 makes **any** writer of `silver/prices/` found in the `code/gold` mirror a STOP. The mirror
**is** the deployment of the repo's gold scripts, so it necessarily contains
`build_canonical_prices_v2.py` -- the one cot writer the same half's own Read section counts among "7 in
code, 0 scheduled" and calls manual-silver-prep only. **The literal gate refuses the act the half signs
GIVEN.**

I measured everything first so the question would carry its own answer:

- **107 mirror objects**, denominator printed, paginated to exhaustion, **107 of 107 fetched with its own
  `get_object`** -- one object at a time, never a bulk sync, as the condition asks.
- **Exactly 1 writer** of `silver/prices/`, and it is the named one. 24 other objects *mention*
  `silver/prices`; a mention is not a write, and each was separated by a write-verb window check.
- **0 readers of another firm's price input**, graded against the **ratified** cross-firm enumeration for
  a `data/cot/` script rather than a pattern list I invented. The only cross-firm hits in 107 objects are
  two lines of `README_BUILD_SEQUENCE.md`, a non-executable doc pointing at a bd **code** prefix.
- A **planted probe** confirmed the scanner can see both a foreign bucket and a `silver/prices` write, so
  the zero is a real absence rather than a blind scanner.

Then I stopped. CLAUDE.md bars the receiving seat from adjudicating scope, and this is a SERVED overwrite
of 38 keys, so I wrote **nothing** (0 of 38), filed row `ADVI_COTBKF-D2-S60` ARMED on the CTO
@`f550170df0`, and sent the measurement with a recommendation to the gate's author, copy to the issuer.
The issuer confirmed the routing and the hold. The CTO ruled (msg 3386, CTO half AMENDMENT 1
@`fa3cabc1ea`): condition 2 reaches only a writer **beyond** the named census, so it is **MET**, and
D2-S60 is disarmed by that amendment. The write began only then.

The same ruling put `_ff_worker`'s carry-forward on COTBKF's enrichment list as **its own cell** -- a code
change under COTBKF's own pair, not a rider on this rewrite. That is the right home for it.

## The write

38 keys, each **version-gated before** its write and **sha256-verified after** it, in one guarded pass per
key so no window opens between the check and the write. Per key: `head_object` and STOP unless the live
VersionId equals the manifest's `version_before`; hash the **local** file and STOP unless it equals
`sha256_after` (checked on all 38, not sampled -- this is what "as built, no rebuild" means
mechanically); `put_object` preserving the object's own `ServerSideEncryption` (AES256 on each, so nothing
but the bytes changed); record the new VersionId; `get_object` back and STOP unless the **served** bytes
hash to `sha256_after`.

No STOP fired. All 38 printed `local_sha == served_sha == manifest`, `match=True`. The rollback path was
armed throughout and never needed: on any STOP it would have restored every key already written to its
prior version by `copy-object`, deleting nothing.

Condition 1 was met **per key**, not once for the batch -- a single up-front census would have left 37
unguarded windows.

**Condition 5 proven, not assumed.** After all 38 writes, every prior version was fetched by VersionId:
**38 of 38 still retrievable**. With a control, because "retrievable" means nothing if the check cannot
fail -- a bogus VersionId on a real key was rejected with `ClientError`.

## AC1, graded above its own expect

`COT-PRICE-REWRITE-VERIFY keys=38 match=38/38`, rc 0, 38 `MATCH` and 0 `MISMATCH` counted with `grep -c`.

The criterion's `expect` is the substring `COT-PRICE-REWRITE-VERIFY keys=38` -- and `verify_served()`
prints that same `keys=38` **even when every key mismatches**, because `keys=` is just the manifest
length. The expect string is satisfiable by a total failure. I declared the real bar at ledger-open
(`keys=38` **and** `match=38/38` **and** rc 0) and all three hold; `verify_served` returns 0 only when
`match == len(keys)`, so rc is an independent oracle on the same claim. It changed no outcome here, but a
future round reusing this criterion would not be so lucky.

The read-back is also independent of the writer: `verify_served` does its own `get_object` per key and
hashes in 1 MiB chunks, so all 38 served objects were read twice by two code paths, both agreeing.

## Compiler Tools

| tool | invocation | result |
|---|---|---|
| `deploy_ledger.py` | `open` / `close-leg` x5 / `close`; `hold` attempted | 5 legs before the write; C2+C3 proven and committed **during** the hold; CLOSED all 5 proven. `hold` refused both ways (plain refuses with an apply leg open, `--pre-apply` refuses once any leg is proven), so the entry stayed honestly OPEN through the ruling |
| `proof-of-spec-check.py` | `<instance> CB36aj2-AC1` | **VALID (rc=0)** first pass; D2-S60 resolves to a channel row |
| script `census()`/`scheduled_count()` | imported and called directly (no CLI mode; rebuild forbidden) | `writers=7 scheduled=0`; wired-into-live-gold-doc empty; 780 files scanned, 17 tf files, 9 live resources read one at a time |
| `boto3` / `aws s3api` | 107 `get_object` (mirror); 133 gold files; 38 x (head+put+get); 38 head-by-prior-version | every count with its denominator, every zero with a positive control |
| `safe-commit.sh` | 2 commits before this one, `-F` from a non-shell writer | @`f550170df0` (row + C2/C3 legs), ledger open self-committed by the tool |

**What failed / gaps.** (1) The comp rail denied two `find`/`grep -rn` calls (F1, blind recursive search);
native `Glob`/`Grep` answered both -- the rail was right and I should have reached for them first.
(2) `deploy_ledger.py` has no state for "pre-apply gates partly proven, act not started, awaiting a
ruling"; I left the entry OPEN rather than closing a leg with a proof I did not have, and it would have
gone RED past its window, which is the truthful signal. Worth a tool note. (3) The AC1 expect string is
weaker than the claim it is meant to carry, recorded above. (4) `comp-iam` was declared in the preflight;
as measured on CB-ac-1 the live simulator is non-discriminating for this principal, so the Put was again
the oracle.

## Push state

MEASURED at write time -- see the final report line. A push state in a document ages the moment it is
written; re-measure at read time.
