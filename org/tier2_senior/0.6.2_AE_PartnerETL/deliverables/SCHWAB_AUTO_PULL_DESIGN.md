# Schwab Auto Pull — Design of Record (canonical-schwab-si2 daily REST ingest)

**Owner:** 0.6.2_AE_PartnerETL · **Domain:** ADVI_SCHWABAUTO / OPAL_ASSETS C3 · **Status:** LIVE
**Grounded @ `27a229d17`** (working tree, 2026-07-14). Every claim below cites the source that carries it; where a
claim is about live AWS state it says so and names the check. This is an architecture record, not a self-report —
read the cited line, not this prose, when the two could disagree.

---

## 0. What this is, in one paragraph

The Schwab Auto Pull is a **credential-riding REST ingest**: a standing, human-established SI2 Desktop (SDD) session
lives on one EC2 box, and a PowerShell puller reuses that session's refresh token to call Schwab's SDDServices REST
backend directly — list files by date range, download the raw vendor zips, land them byte-for-byte in S3 bronze.
There is **no login, no MFA, no OTP, and no browser** in the daily path: it rides an already-authenticated session
rather than re-establishing one. Two master accounts (0824 SmartX, 0833 Black Diamond) are pulled on staggered daily
EventBridge schedules; both land in the consolidation monolith `opal-data-assets`. The design's spine is a single
lesson — **a pipeline that grades its own homework can die silently** — so every "nothing to do" path that could mask
a dead feed is instead a loud FATAL.

It **replaced** the SI2 GUI auto-download channel, which exited `rc=0` on ~22 consecutive cycles over 11 days while
landing nothing (delivery folder frozen at 2026-07-02; its log rationalized the silence as "vendor likely not
posted" — the vendor **had** posted). `sdd-daily-pull.ps1:3-5`.

---

## 1. End-to-end flow

```
                          EventBridge rule (per master, daily cron)
                          canonical-schwab-si2-{08242234,08335338}-daily-pull
                                    |  (aws_cloudwatch_event_target)
                                    v
                          SSM RunPowerShellScript  --> instance i-0f3d57a97f14727af  (the SI2 box)
                          role: canonical-schwab-si2-daily-events-ssm-role
                          (SendCommand scoped to EXACTLY that one document + that one instance)
                                    |
                                    v  on the box:
              aws s3 cp s3://opal-data-schwab/_ops/canonical-schwab-si2/sdd-daily-pull.ps1  (Rule 12: code from S3, never baked)
              & sdd-daily-pull.ps1 -Master <m> -Target monolith -SnsTopicArn <opal-critical-surface-alerts>
                                    |
        +---------------------------+-------------------------------------------------+
        | 1. acquire box-wide SDD session lock (refuse-if-sibling-live)               |
        | 2. CredRead 'SDDSecure' from Windows Credential Manager -> refresh token    |
        | 3. load SI2 app DLLs in-proc (same user, same session)                      |
        | 4. ONE wide date-range search (lookback 30d) -> enumerate distinct files    |
        | 5. canonicalize partition date from API AsOfDATE (never the filename)       |
        | 6. skip-if-already-landed index (idempotent + self-healing)                 |
        | 7. per file: download raw zip -> VALIDATE master+date vs vendor -> s3 cp    |
        | 8. denominator reconciliation (enumerated == downloaded+skipped+failed)     |
        | 9. write run manifest to _ops; release lock                                 |
        +---------------------------------------------------------------------------+
                                    |
                                    v
        s3://opal-data-assets/schwab/{master}/bronze/{type}/{YYYYMMDD}/{vendor}.zip   (RAW artifact of record)
```

Identity/deploy layer: `infra/aws/terraform/canonical-schwab-ec2/monolith-daily-schedule.tf`
Puller:               `infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1`
IAM:                  `infra/aws/terraform/canonical-schwab-ec2/monolith-iam.tf`

---

## 2. Component inventory

| Component | Path | Role |
|---|---|---|
| **Puller** | `infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1` | The whole ingest: auth, enumerate, download, validate, land, reconcile. 441 lines. |
| **Schedules (2)** | `.../terraform/canonical-schwab-ec2/monolith-daily-schedule.tf:41-75` | One EventBridge rule + SSM target per master; CREATE-NEW, staggered. |
| **Schedule invoke role** | same file `:78-103` | `events.amazonaws.com` assumes it; `ssm:SendCommand` scoped to one document + one instance ARN (not `*`). |
| **Box write identity** | `.../monolith-iam.tf:36-98` | `quartz-si2-monolith-write` on the box role — **write-only** (`PutObject`) to `schwab/{master}/bronze/*` + `_ops/*`, masters enumerated. NO GetObject, NO Delete. |
| **Remap role** | `.../monolith-iam.tf:106-266` | `opal-schwab-monolith-remap-role` — one-time staging→monolith prefix remap + the 01_raw pre-floor Glacier leg. Read staging, write monolith, verify by LISTING, cannot read monolith, cannot delete. |
| **Puller artifact in S3** | `s3://opal-data-schwab/_ops/canonical-schwab-si2/sdd-daily-pull.ps1` | The code the box pulls fresh each run (Rule 12). 27,198 bytes (live-verified). |
| **Alert topic** | `arn:aws:sns:us-east-1:313476888478:opal-critical-surface-alerts` | FATAL paths page here (SQS→COO + SMS). |

---

## 3. The auth mechanism — "ride the standing session," and why there's no OTP here

The daily path performs **no interactive authentication**. Mechanism, grounded:

- A human-established SI2 Desktop session persists on the box; its **refresh token** is stored in the Windows
  Credential Manager under target `SDDSecure`. The puller reads it via a P/Invoke `CredReadW` shim
  (`sdd-daily-pull.ps1:152-174`), then attaches it as the `x-refresh-token` header on every SDDServices call
  (`:207`). If the CredRead fails, the session is dead and the run **pages and dies** — it does not shrug (`:179`):
  *"This is a SINGLE POINT OF FRESHNESS and it must page, not shrug."*
- The REST backend is `https://si2.schwabinstitutional.com/fileservices/SDDServices/` (`:199`), reached over TLS 1.2
  (`:200`). Requests are the SI2 app's own compressed-XML contracts, serialized via the app's `XmlHelper`
  (`SerializeWithCompression`, `:203`); the puller loads the actual `Schwab.SI.Framework.dll` /
  `Schwab.SI.SI2Desktop.Contract.Download.dll` in-process (`:182-198`) so it speaks the vendor's exact wire format
  rather than reverse-engineering it.
- Two endpoints: `FetchDetails/SpecificFileDetails.aspx` (search/enumerate, `:230`) and
  `Download/SpecificFile.aspx` (download, `:354`).

**Why no OTP / re-mint layer** (contrast the Black Diamond mechanism, documented separately in
`BLACKDIAMOND_LOGIN_MECHANISM.md`): the SDD session is long-lived and re-established by a human when it lapses, and
the token is refreshed mid-run every 500 files (`:343`). The **cost** of that simplicity is the single-point-of-
freshness: when the standing session eventually dies, the daily pull FATALs (loud) rather than silently self-re-
minting the way BD does via an OTP gateway. That is a deliberate trade for the current stage — BD's self-re-mint is
the reference design if/when Schwab needs to remove the human-in-the-loop, but it is **not** wired here today.

---

## 4. Load-bearing design decisions (the invariants that must not be "simplified" away)

Each of these encodes a specific failure that was measured, not hypothesized.

### 4.1 Fail LOUD — "nothing to do" is a claim that must be earned
The predecessor's fatal flaw was a benign `rc=0` on a dead channel. So:
- **Zero files enumerated over a window that contains a trading day is FATAL** (`:243-248`), not an empty success.
  "The vendor does not publish nothing for 30 days. This is a DEAD CHANNEL, not a quiet one."
- **Search HTTP ≠ 200 is FATAL** — "a FAILURE, not an empty day" (`:231`).
- A dead CredRead FATALs (`:179`); an SI2 type-load failure FATALs (`:198`).
- Every FATAL publishes to SNS before exiting (`Die`, `:74-82`).

### 4.2 Trading calendar resolved FIRST (NEVER#1)
Staleness is reasoned in trading days, never wall-clock: the puller computes the T-1 frontier with weekends +
2026 holidays resolved (`:135-150`) *before* deciding whether zero-files is a failure. Friday's data is Monday's
correct answer.

### 4.3 One WIDE search, NEVER chunked — the search is boundary-lossy
Grounded on the 0833 backfill (`:14-20`): one wide 2023→now search returned 6,933 rows; year-chunked 6,903;
month-chunked 6,669 — **more chunks = more silent loss, zero HTTP errors**. A one-day window is the most-chunked
search possible and therefore the worst case of the bug. A wide rolling window (`LookbackDays=30`, `:33`) +
skip-if-already-landed is immune to it *and* self-heals every previously-missed day for free. **One mechanism =
daily pull + backfill + self-heal.** This is also why the design does not need a separate "fetch specific missing
date" self-heal pass (the original ADVI_SCHWABAUTO GUI mechanism) — the wide-window re-scan subsumes it.

### 4.4 Partition date from the API's AsOfDATE, never the filename
2 of 18 types (fam, slm — 14.5% of the corpus) ship as `{master}.CS{MMDDYY}.{TYPE}.zip`, not the normal
`{master}.CRS{YYYYMMDD}.{TYPE}.zip` (`:22-26`). A `CRS(\d{8})` regex silently drops or mis-dates exactly the two
types nobody spot-checks. So the partition date comes from the API `AsOfDATE` field and an **unparseable AsOfDATE
RAISES** — it never skips, defaults, or best-efforts (`:250-265`). The vendor-embedded filename date is used only as
an independent **cross-check**; a disagreement is a hard quarantine (`:381-384`).

### 4.5 Observe the master from the VENDOR, never the request — quarantine on mismatch
The `{master}/` top-level prefix exists to make commingling 0824 and 0833 **structurally impossible**. That guarantee
is worthless if the master is decided by the folder we *meant* to write to. So before any write, the master is read
from the vendor's physical filename prefix and **must equal** the requested master, else QUARANTINE (`:361-376`):
*"A default is an assumption with a shorter name." (CTO~B)*.

### 4.6 Raw only — the puller does NOT unzip (Rule 17a)
Bronze is raw. The `.zip` is the artifact of record (`:7-12`, `:287-333`). Two independent reasons, same conclusion:
- **Measured:** Schwab writes ZIP64 archives whose local headers carry the `0xFFFFFFFF` sentinel; .NET's
  `System.IO.Compression` throws "local file header is corrupt" on **every** Schwab zip. This is the Windows
  platform, not a patchable bug (`:294-300`).
- **Architectural:** unzipping at ingest duplicates silver's job, ~20×'s storage, and — because a failed extract
  throws — makes a *convenience* step fail the *load-bearing* one. The raw zip is uploaded **before** any extract is
  attempted, so when the extractor failed on 100% of files, **nothing was lost** (`:302-311`).
- **Stated gap:** the H1 header cross-check (declared Business_Date + master) needs the payload, so it cannot run at
  ingest — it **moves to silver**, the first layer that decompresses. A control moving layers, named here so nobody
  discovers the gap by accident (`:313-316`).

### 4.7 Denominator discipline — reconcile against the SOURCE, not the selection
`enumerated` must equal `downloaded + skipped + failed`; a mismatch means files vanished between enumeration and the
loop, and that is FATAL (`:401-408`). The denominator printed is the vendor's count, never the loop's — the
2026-07-13 lesson that a self-consistent check over a truncated read passes.

### 4.8 The SDD session lock — the single point of freshness, protected by construction
The SDD credential is **one standing session shared across both masters** on the box. Two concurrent pullers can
invalidate each other's refresh, and the blast radius is a live multi-billion-dollar backfill dying mid-run. Source
cannot prove concurrent-refresh is safe, so the puller **refuses to gamble**:
- Box-wide atomic lockfile `C:\schwab-sdd\.sdd-session.lock`, acquired via `FileMode::CreateNew` **before** the first
  token read (`:105-131`, `:175-177`).
- A live sibling holding it → **exit 7, page** (`:127`) — refuse, don't risk.
- Stale-safe: a lock whose holder pid is dead, or older than 2h, is reclaimed (`:121-124`), so a crashed pull cannot
  wedge the box forever.
- A contention-Die must **not** free the sibling's lock — `Release-SessionLock` only releases if *we* own it
  (`$script:LockOwned`, `:98-104`, `:126`).

This is why concurrency is safe **by construction**, not by timing. The stagger (§5) is defense-in-depth; the lock is
the guarantee. CTO ruled this a design requirement, not a flag: *"the guard has to be right BEFORE the failure."*

---

## 5. The both-masters daily pattern (deployment)

Andrew-direct 2026-07-14: *"We need daily rest pattern for both 0833 and 0824 on that box, yes."*
(`monolith-daily-schedule.tf:1-3`). CREATE-NEW, not a repoint (CTO ruling 20260714T030017Z, new-territory rule): the
dead GUI schedule and every pre-existing scheduler are untouched; the plan is pure "to add" (`:5-9`).

| Master | Label | Cron (UTC) | Live state |
|---|---|---|---|
| 08242234 | 49F SmartX | `cron(15 10,22 * * ? *)` | Rule ENABLED (live `describe-rule`, verified 2026-07-14 04:3xZ) |
| 08335338 | 49F Black Diamond | `cron(45 9,21 * * ? *)` | Rule ENABLED (live `describe-rule`, verified 2026-07-14 04:3xZ) |

Staggered ≥30 min apart (`:29-38`) so in normal operation they never contend and the lock never fires. Windows are a
first estimate; the puller's zero-files-on-a-trading-day FATAL is the tuning signal (`:30-33`). Each schedule fires
SSM RunPowerShellScript on `i-0f3d57a97f14727af`, pulls the puller fresh from S3 `_ops` (Rule 12), and runs it
`-Master <m> -Target monolith` (`:59-74`). Twice-daily cadence (9/21, 10/22) gives a same-day retry; skip-if-landed
makes the second fire a cheap no-op.

> **NOTE on the in-flight 0824 wide backfill** (`:24-27`): it runs the OLD lock-less script and does **not** hold the
> lockfile; the daily schedules' first fires (09:45+/10:15+) are well after it completes, so there is no first-fire
> collision. Once the wide pull is done, every subsequent pull on this box runs the locked script.

---

## 6. Identity model — least privilege, three separate roles

Deliberately three identities, never sharing a grant (`monolith-iam.tf:9-26`):

1. **The box (`quartz-si2-monolith-write`)** — WRITE-ONLY. `PutObject` to `schwab/{master}/bronze/*` and `_ops/*`,
   **masters enumerated, never wildcarded** (`:66-95`). A `schwab/*/bronze/*` grant would let a mis-scoped run invent
   a master prefix and write successfully, handing back the exact guarantee the master-scoped keyspace exists to
   provide. NO GetObject (an internet-facing Windows GUI box with vendor creds does not read back the consolidated
   estate), NO Delete (bronze is additive-only). Firm-sep DenyBd/Cot/Inf planes from `quartz-si2-spike-inline` still
   govern the role (explicit Deny wins across policies).
   - The `ListBucket` grant for the skip-index is **prefix-conditioned** to the schwab tree only (`:53-65`) — a
     ListBucket that could enumerate every source in the monolith is a firm-boundary hole opened by omission, and *a
     ListBucket deny is the dangerous one*: PutObject deny screams, but an idempotency check that cannot read its
     destination silently loops.

2. **The schedule invoke role (`canonical-schwab-si2-daily-events-ssm-role`)** — `ssm:SendCommand` scoped to exactly
   the RunPowerShellScript document **and** the single instance ARN (`monolith-daily-schedule.tf:86-103`). Not `*`: a
   schedule role that can SendCommand to any instance is a lateral-movement primitive.

3. **The remap role (`opal-schwab-monolith-remap-role`)** — the one-time migration identity: read staging bronze,
   write monolith bronze, **verify by LISTING** (ETag+Size from ListObjectsV2, so it needs NO GetObject on the
   monolith — `:156-177`), cannot read the monolith, cannot delete anything. Includes the 01_raw pre-floor Glacier
   leg: `RestoreObject` (BULK, Days=14) scoped to `01_raw/*` **on this role only, never the box** (`:207-222`), plus
   the `GetObject` on `01_raw/*` that the H1-observed-master rule and the tier-3 MD5 verify actually require
   (`:223-242`). **Closure step, ruled:** the restore grant is removed at migration completion, removal evidenced by
   a live simulate showing implicitDeny (`:215-217`).

### Verification note (Rule 22a)
IAM here was proven on the **live primitive**, not `comp-iam` (which models `(action)` not `(action,resource)` and
fails green on new ARNs): `aws iam simulate-principal-policy`, one `--resource-arns` per call, positive controls run
separately — the conditioned-ListBucket `--context-entries` trap reproduces exactly if you skip it. The box role and
remap role were each simulated; every never-widen property (firm-sep explicitDeny, cannot-read-a-peer, enumeration
holds against a non-enumerated master) came back denied.

---

## 7. Known gaps / deferred, stated plainly

- **H1 header cross-check moved to silver** (§4.6). Silver must implement declared-Business_Date/master validation;
  it is not done at ingest and cannot be.
- **SSE fork** (`monolith-iam.tf:272-298`): the grants say nothing about encryption. The monolith is SSE-S3/AES256
  (ruling 13a, adopted-then-reversed to AES256-only at v1.3.4), so the puller sends `--sse AES256` unconditionally
  (`sdd-daily-pull.ps1:48-53`) — required on `opal-data-schwab` (which forces it), a harmless no-op on the monolith.
  Had the monolith been SSE-KMS, both producer roles would additionally need `kms:GenerateDataKey` on the exact CMK,
  and the deny would arrive as a runtime AccessDenied from an IAM policy that reads perfectly. No speculative KMS
  statement was authored (no key ARN → the only blind way to write one is a wildcard = the never-widen failure).
- **Single point of freshness** (§3): when the human-established SDD session finally lapses, the daily pull FATALs
  (loud) rather than self-re-minting. Removing the human-in-the-loop = porting BD's OTP-gateway self-re-mint pattern;
  it is scoped as a reference, not built here.
- **Windows date-window cadence** (§5) is a first estimate; the zero-files FATAL is the tuning signal.

---

## 8. TO reconciliation note

`ADVI_SCHWABAUTO.ae-fetch-by-date-selfheal-finish-the-box` was pre-scoped around a GUI-driver, then pivoted
(Andrew-ratified 2026-07-02) to **A-PRIME: ride the standing SI2 session, fetch via SDDServices REST**. The mechanism
documented here **is** A-PRIME, now live for both masters. The wide-window re-scan (§4.3) subsumes the TO's
"fetch specific missing date self-heal" leg. Recommend reconciling that TO's status against the C3(b)/C3(c)
deliverables rather than tracking it as open-uncovered.

---

## Appendix — where the numbers come from

Live-state claims in this doc were checked against AWS on 2026-07-14 ~04:3xZ, not read from memory:
`describe-rule` (both rules ENABLED + crons), `head-object` on the S3 puller (27,198 bytes),
`list-objects-v2` on `opal-data-assets/schwab/08335338/bronze/` (6,932 objects). Source claims cite
`file:line @ 27a229d17`.
