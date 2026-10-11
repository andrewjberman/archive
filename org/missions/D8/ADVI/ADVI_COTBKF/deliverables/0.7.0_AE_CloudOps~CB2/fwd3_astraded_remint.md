# ADVI_COTBKF.TO-CB-ah-3 -- the as-traded RE-MINT of the three FWD-3 tables

**archetype:** DEPLOY

**Seat:** `0.7.0_AE_CloudOps~CB2` | **Issuer:** `2.0.0_SA_COO~C2` | **Round:** 34 | **Cell:** `CB-ah-3`
**Risk class:** SERVED | **Date:** 2026-10-09 | **Order at:** @513fcb47f3 (AMENDMENT 1, RELEASED)
**Criterion:** `CB34ah3-AC1` -- **PASS** | **Proof:** VALID (rc=0), first pass
**Ledger:** `org/critical_paths/change_management/20261009T1237Z_advi-cotbkf-fwd3-astraded-remint-cb-ah-3-20261009_deploy_completion.md`,
opened @636591ca67, legs committed @ee9d1cd63e, CLOSED with all 5 legs proven.

---

## What this was, and why it is not the round-29 act

Round 29 MINTED these three keys onto empty prefixes. **This one OVERWRITES served output** — a different
risk shape under the same never-widen law. The round-29 tables were built on a price store that is
dividend-adjusted for 2,079 tickers; CTO ADDENDUM 8 rules valuation at the **as-traded** close and
ADDENDUM 9 cut the rebuild. So the evidence that matters here is not only "the new bytes match the new
build" but **"the rollback source survives"** and **"the key no longer carries the old values"**.

| table | new ETag | new VersionId | bytes | prior VersionId (rollback) |
|---|---|---|---|---|
| daily_returns | `26ad8293e2ba2e561dbde60b1aa7eb95` | `w9j5YeV1LnNIakNlRTBX6jW1.SDHqmJR` | 1,651,055 | `rIUTpGUAPNG.rsDWrxpRbnJCmu6NFaXJ` |
| account_day_value | `ca1ac0f48971f6cc0d11a147dcda086e-7` | `qIWjLLwCIh_Gx6IblSgyaint2tfJ37pr` | 54,246,028 | `PcSspTWz8xsreGMTF_coYhbqifk4preA` |
| month_grades | `7269e2607b1e5806058b1136b8c4e36b` | `QI5Ks8vQwGTwnc9ekyh.DOsyN8PKN3PB` | 421,751 | `Y15sJCiA1KM.CksHSitFlsnqkI56N_34` |

Written 12:41:01–03Z. The `-7` suffix is a 7-part multipart upload, so that ETag is **not** an MD5 and is
recorded as an identity handle only. Row counts are unchanged at 1,691,729 / 21,102,041 / 82,593 — this
re-mint moves **values**, not shape.

## The order of operations

1. **Pair first.** Both halves GIVEN and cited in the amendment: CTO half (msg 3271) and COO half
   @e075588a6c. The COO half had been briefly marked superseded under ADDENDUM 10 and was reinstated on
   the CTO's ruling that the HELD bonds make this re-mint independent of the 38-key rewrite; I read the
   reinstatement in the half itself rather than inferring it from the amendment.
2. **Rollback source recorded before any write** (leg P0): versioning `Enabled`, and all three current
   VersionIds already **equal** the half's recorded priors — nothing had moved the keys between the
   signing read at ~11:1xZ and the act.
3. **Held build checked against the pair before being used.** Its manifest carries `run_commit`
   `6f70d5cc01bb`, `price_basis=as_traded` (with `price_basis_before=store`), the three `hold_cusips`,
   `held_account_days=988`, and the three signed hashes.
4. **Ledger opened** with 5 legs, committed per leg.
5. **Dry run on the held build; `--build` never run** (leg B1).
6. **Guarded apply** (legs R1, A1).
7. **`--verify`** (leg V1), then the mutant.

## Why `--build` was never run

The amendment forbids it, and the mechanism agrees: `run_commit` is a **column in all three schemas** and
`content_hash` covers the schema plus every row, so a rebuild at this seat's HEAD would have moved all
three hashes off the pair's signed values. Applying as built is the only way the signed hashes can hold.
My dry run printed `manifest_hash_same=True` on all three and the three hashes equal the issuer's
~12:1xZ run **and** the COO half section 3 exactly — two independent invocations by two seats over the
same bytes.

## CTO condition 1, made mechanical rather than eyeballed

The condition is "re-read the three prior VersionIds immediately before the write, and STOP if any
changed." Reading in one tool call and applying in the next leaves a window in which another writer could
move a key and the apply would still proceed. I put the re-read and the write in **one guarded
invocation where the apply is unreachable unless all three versions match**, so a mismatch stops the act
by construction instead of by me noticing between two calls.

```
R1 RE-READ immediately before the write (boto3 head_object):
  account_day_value  live=PcSspTWz8xsreGMTF_coYhbqifk4preA  same=True
  daily_returns      live=rIUTpGUAPNG.rsDWrxpRbnJCmu6NFaXJ  same=True
  month_grades       live=Y15sJCiA1KM.CksHSitFlsnqkI56N_34  same=True
R1 OK: 3 of 3 versions unchanged -- the write is authorized by the pair.
APPLY rc=0
```

**A failure on the way there, recorded rather than smoothed over.** The guard's first build shelled the
`.tools/aws` shim from Python and died `FileNotFoundError [WinError 2]` — a shell shim is not spawnable by
`CreateProcess`, and CLAUDE.md bars bare unix names in a Python argv. It failed in the version **read**,
before the apply, so **nothing was written** and the fail direction was closed. I rewrote the guard to
read through boto3 (the same credential chain the uploader uses), which removes the subprocess from the
gate entirely. The gate was never bypassed to get past the error.

## What the overwrite is proven to have done

`--verify` gives equality to the new build: `FWD3-VERIFY tables=3 match=True`, every table
`hash_same=True`, `served_rows == local_rows`, 22,876,363 rows compared on content.

But equality against the new build **cannot** show the old values are gone. So, independently of
`--verify`'s own verdict, the served `month_grades` was re-read and re-hashed:

- it hashes to `66ea11a4...`, the COO half's **signed as-traded hash**;
- it **differs** from `ba99ee87...`, the round-29 served hash this same instrument read at this same key
  this morning.

That is the thing a re-mint has to establish, and it is the one claim the criterion alone does not cover.

**Rollback source proven, not assumed.** Versioning being `Enabled` is a property of the bucket, not
evidence about these objects, so after the write each prior version was fetched by `--version-id` and
returned its original ETag and size. The half's `copy-object` rollback is executable right now, and no
key was deleted — which also leaves the CTO half's human-confirmation condition untouched.

## Controls

- **Determinism** — graded as agreement between two seats' invocations over the same held bytes
  (`manifest_hash_same=True` ×3, `manifest_list_same=True`, hashes equal to the issuer's run), plus a
  double re-hash of the served object (`rehash_same=True`). No rebuild, by design.
- **Sealed planted mutant, on the new served bytes** — one cell of the served `month_grades` mutated in
  memory (row 0, `account`), nothing written; the comparator moved to `3d0f3907...`,
  `FIRED-AS-EXPECTED`, with its control arm run **first**. So AC1 is shown capable of failing on these
  bytes, not merely of passing.

## Held and ABSENT — what is deliberately not served

- **988 holding-days BLANK**, reason `HELD_SOURCE_UNDER_REVIEW`, for the three cross-firm bonds
  `05613L3H2` / `651639AX4` / `95000U2D4`. No 49F-contaminated price reaches a served value (D2-S52).
  They re-enter only through the ADDENDUM 10 rewrite plus a later delta — not this cell.
- **5 ABSENT months**, reason `REGRESSED_UNDER_AS_TRADED`, `manifest_list_same=True`, each
  `computed=ABSENT return=ABSENT verdict=ABSENT`: acct#aaeb760c 2022-03 (23 days / 253 holding rows),
  acct#aaeb760c 2022-08 (23/253), acct#f78e8ecd 2026-03 (22/220), acct#df101fce 2021-07 (21/21), acct#df101fce 2021-10
  (21/42). `absent_months=5` was the amendment's bar and it is met on the nose — a 4 or a 6 was a STOP.
  The CTO's "a named row per month" condition is already met upstream by rows D2-S53..S57.
- **The reader gate stays CLOSED.** This seat granted nothing.

## No new surprise row

Nothing diverged from the pair on this order. The order's refusal clause still names the
`ADVI_COTBKF-D2-WCB2-S<k>` id form that `proof-of-spec-check.py`'s `SURPRISE_ID_RE` cannot parse, but
that is the **same** fact already filed as `ADVI_COTBKF-D2-S43` on CB-ac-1 and it never fired here
(no criterion failed), so re-filing it would be a duplicate rather than a finding. The `.tools/aws`
shim failure above is a documented constraint I tripped over, not a property of the world — it belongs
in this log, not in the channel.

One thing did land in my favour: the `deploy_ledger.py` staging defect I routed to `0.0.0_AB_MSTR~DELL2`
after CB-ac-1 is **fixed** — @00d3393ff3 is an ancestor of HEAD, and `open` committed its own two files
and left nothing staged, so no seat's `safe-merge` was blocked by this deploy at any point.

## Compiler Tools

| tool | invocation | result |
|---|---|---|
| `deploy_ledger.py` | `open` / `close-leg` ×5 / `close --slug advi-cotbkf-fwd3-astraded-remint-cb-ah-3-20261009` | 5 legs declared before the write, each closed with proof and committed per leg; CLOSED, sentinel removed, nothing stranded, nothing left staged |
| `proof-of-spec-check.py` | `<instance> CB34ah3-AC1` | **VALID (rc=0)**, first pass — the CB-ac-1 schema lessons (`s3_object`, `DEPLOYED-VERIFIED`, only `determinism`/`mutant` under `controls`) carried over |
| `aws s3api` | `get-bucket-versioning`; `head-object` ×3 before; `head-object --version-id` ×3 after | versioning `Enabled`; priors equalled the pair's before the write; all three priors still return their original ETag and size after it |
| `boto3 head_object` | the guarded apply's gate | `R1 OK: 3 of 3 unchanged` then `APPLY rc=0`; condition 1 enforced by construction |
| `safe-commit.sh` | 2 commits before this one, under this seat's author line, `-F` message files from a non-shell writer | @636591ca67 (ledger OPEN, self-committed by the tool), @ee9d1cd63e (legs P0/B1/R1/A1) |

**What failed / gaps.** (1) The guarded apply's first build shelled `.tools/aws` from Python and died
`WinError 2`; nothing was written and it was rewritten onto boto3 — detail above. (2) `comp-iam` is
declared in the order's preflight for apply time, and as measured on CB-ac-1 the live
`simulate-principal-policy` is **non-discriminating for this principal** (an out-of-grant control also
reads `allowed`), so it was again not cited as the grant's proof; the Put was the oracle. (3) The
`--verify` content comparison is the only instrument that reads all 22.9M served rows; the ETag cannot do
it for `account_day_value` at all, because multipart ETags are not MD5s.

## Push state

MEASURED at write time — see the final report line; a push state in a document ages the moment it is
written, so re-measure at read time.
