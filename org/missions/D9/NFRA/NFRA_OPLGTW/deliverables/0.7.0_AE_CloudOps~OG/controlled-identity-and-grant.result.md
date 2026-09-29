# TO-OG-g-1 result -- G-C evidence: the controlled identity and its synthetic grant

**Order:** `NFRA_OPLGTW.TO-OG-g-1` | **Cell:** `OG-g-1` | **Assignee:** `0.7.0_AE_CloudOps~OG`
**Branch:** `ae-og-g1c` cut from `CLOUD` @`b274848977` | **Terminal state:** **REFUSED-BLOCKED** (not `complete`)
**Order vintage:** amendments **A2** @`8bf2bf37c6` (CTO ruling, msg 26461) and **A3** @`b907d17f1c` (msg 26507), both in force
**Date:** 2026-09-29 (first pass `0126a2360c`/`a55ef96d85`, drained; this pass carries A2 + A3)

## Outcome in one line

The grant half is derived, bounded, validated and **now fully quantified under A3**; **the identity half is
blocked on a tenant-administrator act that this order forbids me to improvise**, so `G-C`'s evidence is
incomplete by construction and `<status>` stays `pending`. No live write was made, so no deploy-ledger entry was
opened. **All four failing criteria now trace to ONE cause** -- the absent identity -- where the first pass had
three independent causes; amendments A2 and A3 retired the other two.

## Under amendments A2 and A3

**A3 granted the read I asked for** (msg 26505 -> 26507) and it was taken exactly as bounded: `GetObject` by the
pinned VersionId on the 5 objects `SEALED_EXPECTED_V2.json` records, nothing else, decoded with pyarrow, counts
only. Instrument `probes/og_g1_accounts.py`; 5 of 5 objects read.

**The grant's account COUNT, per master: `08242234` -> 7460; `08335338` -> 7548.**

Three things that measurement settled, none of which was knowable before it:

1. **The count is not in the seal.** `SEALED_EXPECTED_V2.json` carries zero account-level fields -- it pins 5
   objects. That is what made A3 necessary, and flagging it before the amendment was cut saved a round-trip.
2. **The physical column is `account_id`, not the contract's `account_ref`.** The parquet has no `account_ref`:
   it is the Gateway's keyed HMAC over the raw id and exists only in responses
   (`app/integrations/schwab/datasets.json:12`; `app/account_ref.py:3-8`). The first run failed loudly on the
   missing column rather than counting the wrong one. The HMAC is injective per master, so the COUNT is the same
   under either name.
3. **The sealed set is EVERY account in both masters, and the seal forces that.** 15,008 in all. The order asks
   for accounts to "stay a bounded subset"; they cannot, because RQ2-2 .. RQ2-6 are aggregates whose hashes break
   under any subset. Ruling (1) is the only value under which the sealed answers verify. The cost is that the
   account dimension yields **no** refusal discriminator -- every refusal `OG-v-7` grades must come from the
   column or date dimension, which is what the recorded pair does. Filed as row `NFRA_OPLGTW-Z-S14`.

Feasibility, measured rather than assumed: ids are uniformly 10 characters, so `scope.accounts` serialises to
about **195,102 bytes -- 47.6% of DynamoDB's 400 KB item limit**. The ruled grant fits in one item.

`app/account_ref.py:3` also **confirms row `Z-S10` on the code** rather than by inference: *"Accounts are raw
Schwab ids INSIDE the Gateway only: the data_entitlement grant's `scope.accounts` and the source rows."*

## Criterion verdicts

| id | verdict | measurement |
|---|---|---|
| `GCG1-AC1` | **FAIL** | 4 of 4 identity fields located in the evidence file; `controlled_oid` and `controlled_upn` are explicit ABSENT markers, not values. `controlled_tid` = `6810043e-d171-4adc-9975-068b35e179da`, canonical GUID, verified. The probe refused the ABSENT marker as a placeholder, which is the behaviour the criterion asks for |
| `GCG1-AC2` | **FAIL** | deployed rosters read live off `i-07dccb1615503ac99` with the positive control returning: 3 entries across 2 present rosters (`MASTER_ADMIN_EMAILS` 1, `WRITE_CAPABLE_EMAILS` 2), `MASTER_ADMIN_PRINCIPALS` and `WRITE_CAPABLE_PRINCIPALS` both ABSENT. The comparison cannot be made against an absent identity -- an absent identity is not a non-privileged one |
| `GCG1-AC3` | **FAIL** | re-implemented against **A2**'s mechanism: import `ops/schwab_entitlement_admin.py`, call `validate_candidate` on the OFF-REPO candidate, recompute the unredacted scope diff and compare its SHA-256 against the one recorded, then scan the committed evidence for any account identifier of that candidate. The off-repo candidate is ABSENT (denominator: 1 required, 0 present) because it is keyed by the `tid`/`oid` that does not exist. **One cause now, not two** -- A2 retired the `prepare` defect and the AC3/AC6 conflict |
| `GCG1-AC4` | **FAIL** | `POLICY#<tid>#<oid>` is not constructible, and this order performed no live write. The strong-read instrument was proven able to see a present record by a positive control against the one existing principal (3 items, `principal_profile` `status active`), so this FAIL is a true absence and not a blind reader |
| `GCG1-AC5` | **PASS** | 7 of 7 sealed questions inside the grant, read from `SEALED_EXPECTED_V2.json` at HEAD (masters, dataset and business dates each checked per question); A7 step 4 no-date asks 2 of 2; A7 step 3 `download_filtered` 1 of 1 |
| `GCG1-AC6` | **PASS** | 4 files scanned, 0 with a finding |
| `GCG1-J1` | `UNVERIFIABLE-BY-INSTRUMENT` | `3.0.0_SA_CVO~O` at L9. RECORD; NO VERDICT |

`<status>` is **not** flipped: the order admits `complete` only when every mechanical criterion passes by output.

## What blocked it, stated once

No controlled identity exists in the Opal Capital Entra tenant. `az ad user list` returned 85 user objects
(47 external guests, 38 internal); all 38 internal accounts are accounted for by class in the evidence file's
section 2 and **0 qualify** -- 21 are real named employees, 4 are admin or break-glass, 7 are live shared business
mailboxes, 3 are room resources, 2 are security/system objects, and `opalbloomberg@` is on the deployed
`WRITE_CAPABLE_EMAILS`. `menachem@` is the **pilot** identity reserved for `G-E`, not the controlled one.

The one real Entra-keyed principal in the live table resolves to a **write-capable real employee** and carries a
**portal-only** grant from a different project (`NFRA_OPALAI` `OA-g-3`), so it is neither reusable nor widenable.
The `/ui-walk` dormant account is in the portal's own user store with no Entra identity at all, so it cannot key a
Gateway principal.

Creating a tenant identity is an Entra write. This order authorizes one principal's `POLICY#` records in AWS and
"⛔ NOTHING ELSE IN AWS" -- no Entra write at all. The order's own clause governs: that is the answer.

## What a human must do

The evidence file's **section 6** carries the ask in one paragraph a non-technical reader can act on. In short: an
M365 administrator creates one brand-new, unlicensed-for-privilege test user (suggested
`og-controlled@opalinvest.com`), adds it to no admin or write-capable list, gives it a normal work mailbox so it
can complete a browser sign-in, and says which accounts of masters `08242234` and `08335338` it may see.

## Also owed by a seat, not by Andrew

`2.0.0_SA_COO~O` is `disarm_owner` on two ARMED rows. **`-S2` blocks `GCG1-AC3` from ever passing as written,
independently of the identity**, so it needs disposition even after the identity lands.

## Artifacts

| path | what |
|---|---|
| `G-C_CONTROLLED_IDENTITY_AND_GRANT_EVIDENCE.md` | the evidence, in the shape AC1..AC6 grade |
| `grant_candidate_scope.json` | the derived scope as data; `accounts` redacted under AC6 with what the operator substitutes named |
| `probes/og_g1.py` | the probe, six arms, each printing its measurement with its denominator then one VERDICT line |
| `NFRA_OPLGTW.TO-OG-g-1.controlled-identity-and-grant.proof_of_spec.json` | the proof-of-spec instance |
| `surprise-channel/investigations/INVESTIGATION_v1.md` | rows `NFRA_OPLGTW-Z-S9`, `-S10`, `-S11`, `-S12` appended |

## Surprise rows filed

- **`-S9`** OBSERVATION / INERT -- `GCG1-AC3` names `schwab_entitlement_admin.py prepare`; the CLI has only
  `activate`, `revoke`, `deny-backfill`. `prepare` is an internal function, and it is what prints the scope diff on
  the `activate` path. The probe calls the committed module's own validator, so nothing was invented.
- **`-S10`** OBSERVATION / **ARMED** -- `GCG1-AC3` (scope diff verbatim) and `GCG1-AC6` (no raw account identifier in
  any committed artifact) cannot both hold, because `parse_scope` requires non-empty per-master account lists.
- **`-S11`** OBSERVATION / **ARMED** -- a `fixed_dates` grant bounds the latest qualified date it can report, so once a
  closure marker later than `2026-09-25` lands, A7 step 4's "newest marker at ask time" half stops holding for a
  reason that is the date mode, not the system under test.
- **`-S12`** OBSERVATION / INERT -- the order mandates row ids of the form `NFRA_OPLGTW-Z-OG-S<k>`, and that shape is
  rejected by BOTH gates' anchored id patterns (`surprise-row-gate.py:104`, `proof-of-spec-check.py:1127`), which admit
  only `Z-`, `W<n>-` or `C-` before `S<k>`. Filed with the order's literal ids, the commit would have been refused and
  the findings would have read as unfiled. These rows use the admitted seat-row shape `NFRA_OPLGTW-Z-S9..S12`,
  continuing the existing `Z-S1..Z-S8` series; 0 of the channel's 191 rows carry a `-OG-` segment.

**All four are now DISPOSITIONED** by `2.0.0_SA_COO~O`'s row `NFRA_OPLGTW-Z-S13` (2026-09-29T06:20Z,
`DISMISSED_WITH_REASON`, "Disarmed by amendment, as disarm_owner"): `-S9` and `-S12` folded into A2; `-S10`
ruled by `1.0.0_SA_CTO~O` @`8bf2bf37c6` with AC6 winning; `-S11` fixed by amending **`OG-v-7`'s `OGV7-AC6` to
the grant's dates** @`ce520eb13e` -- one of the two routes the row named. Nothing from the first pass is left open.

- **`-S14`** OBSERVATION / INERT (new this pass) -- measured under A3: the sealed account set is **every** account
  in both masters (7460 + 7548 = 15,008), so the grant cannot be the "bounded subset" of accounts the order asks
  for -- and the seal **forces** that, because RQ2-2 .. RQ2-6 are aggregates whose hashes break under any account
  subset. Ruling (1) is therefore the only value that lets the sealed answers verify. The cost, stated so
  `OG-v-7`'s grader does not hunt for something that cannot exist: **the account dimension yields no refusal
  discriminator**; every refusal must come from the column or date dimension. Checked that no A-row depends on an
  account-scoped refusal (A6 step 4 is a column refusal; A6 step 3 is about not revealing other principals; A10 is
  about download links).

## Compiler tools

| tool | invocation | result |
|---|---|---|
| `comp-read` | on the decomposition, then on `ops/schwab_entitlement_admin.py` | located `G-C` in s.6 (774-790) and the command's subcommand surface; its QUALIFIERS limb surfaced the "never imported by app/tools.py" and identity-refusal clauses |
| `comp-find` | `--corpus all` on the roster and walker tokens | usable from the main worktree; **timed out at 60 s against the sparse worktree** (`git ls-files` on the sparse index), so repo-corpus censuses were run from the main tree and single-module reads used `sed`/`grep` under `# rail-checked:` markers |
| `.tools/commit-gate.sh` | on `probes/og_g1.py` | rc 0, "All checks passed!", "no unguarded strict-utf8 log reads", clean for 1 of 1 file |
| `.tools/surprise-row-gate.py` | in the worktree before staging, then as the commit hook | standalone: "no surprise-channel rows in this commit (denominator: 0 dispatched path(s))" -- an **empty read, not a pass**, because it validates STAGED rows. At the hook, after the cone was widened: "4 new row(s) of 192 total checked (188 pre-existing, NOT re-graded)", "OK: all new rows carry their step-7/step-10 fields" |
| `.tools/safe-commit.sh` | the commit | rc 0 at `0126a2360c` after four gate refusals, **every one of them a sparse-cone gap rather than a defect in this work** -- see below |

### A SPARSE-CONE WORKTREE FAILS FOUR GATES, AND EACH READS AS A DEFECT IN YOUR WORK

Recorded here because the record and git history are where this belongs, and because three of the four
refusals name a remedy that would have damaged something if followed literally.

| gate | refusal text | the path it actually wanted |
|---|---|---|
| `commit-gate.sh` | `ModuleNotFoundError: No module named 'comp_constants_cli'` | `org/modules/graph` |
| naming limb (LGIC_ENFORCE DEC-6) | `registry.file: unreadable: FileNotFoundError ... infra/logic/registry/systems.json` | `infra/logic` |
| `surprise-row-gate.py` | `standing corpus pass could not run (FileNotFoundError ...)` -- fail-closed **twice, naming a different missing file each time** | `org/surprise_channel` (its schemas), then **all of `org/missions`**, because it reads every project's channel |
| `missions-tree-check` | **29** `[INDEX-MISSING] no org/projects/<CODE>.json`, for every project in the repo including ones never touched | `org/projects` |

Two traps worth naming. The 29 `INDEX-MISSING` lines carry the remedy `derive --write`, which would have
**written 29 index files** to fix what was one absent directory. And the row gate offers an audited
override (`# surprise-row-override: <reason>`) exactly where a sparse cone trips it -- taking it would
have committed four rows **UNGRADED**, the opposite of what a row is for. Both were declined; the cone was
widened and the gates then passed on their own terms.

Working cone for a commit touching a project tree plus a surprise channel: `org/missions org/projects
org/surprise_channel org/modules/graph org/standards org/critical_paths org/mcp infra/logic .tools lib`
plus the code under test.
| `comp-schedule` / `comp-iam` / `comp-adversary` | -- | DECLARED-NOT-APPLICABLE by the order's own preflight; no AWS operation, policy, principal or role is added or changed here |

## AWS and tenant calls this run

Read-only throughout except where stated; **no write of any kind was made**. `sts get-caller-identity`
(`user/Andrew_Berman` -- note: **not** the `opal-gateway-access-admin` role the operator command requires, which is
a second thing the activation will need); `dynamodb scan` of `POLICY#` (10 items, `ScannedCount` 213, no
`LastEvaluatedKey`) and one `dynamodb query` with `--consistent-read`; `ec2 describe-instances`; two
`ssm send-command` roster reads on `i-07dccb1615503ac99` extracting only the roster keys, never the
secret-bearing lines of that `.env`; `s3api list-objects-v2` on the two `meta/complete/` prefixes (19 markers each).
Entra: `az account list`, `az ad user list`, `az ad user show` -- the one authoritative tenant read the order's
declared egress class admits. No vendor API.
