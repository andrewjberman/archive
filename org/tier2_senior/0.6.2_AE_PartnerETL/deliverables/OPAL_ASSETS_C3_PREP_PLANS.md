# OPAL_ASSETS C3 — PREP DELIVERABLE (authored, NOT applied)

**Agent:** `0.6.2_AE_PartnerETL` · **Date:** 2026-07-14 · **archetype:** IMPLEMENT
**GO:** `2.0.0_SA_COO` 20260714T011252Z — C3 PREP only (IAM authored+planned, catch-up plan, remap plan).
**Spec of record:** `OPAL_ASSETS_CONSOLIDATION_PRD` v1.3.1 (`34333469b`) §4 row C3 + §3 ruling 9.
**Apply gate:** `1.0.0_SA_CTO`. Nothing in this document has been applied. No Terraform was applied.

---

## 0. THE TWO FINDINGS THAT CHANGE THE TO

Both are the same shape: **a check that passes over a truncated or mis-typed read.** Neither is
visible from the PRD; both are only visible from live S3.

### F-1 — `7,256` IS A STALE DENOMINATOR, AND IT IS STILL MOVING AS YOU READ THIS

The TO and PRD §4 both say "prefix-remap the **7,256** staged objects." That number was true at the
moment it was written and is false now:

```
7,256  =  6,932 (0833, migrated, TERMINAL)  +  324 (0824, mid-pull)      <- the PRD's snapshot
8,217  =  6,932                             +  1,285 (0824, 01:20Z)      <- LIVE, 2026-07-14 01:20Z
12,898 =  6,932                             +  5,966 (0824, TERMINAL)    <- projected on pull completion
```

**The 0824 wide-history pull is RUNNING RIGHT NOW** (newest object written `2026-07-14T01:20:12Z` — the
second I queried; it continues under Andrew's direct GO, unchanged by the dispatch hold). It went
978 -> 1,285 in the ~15 minutes I spent authoring the IAM.

> **Consequence, and this is the whole point:** a remap that verifies parity against `7,256` will
> **report SUCCESS while leaving ~5,600 objects behind.** The check is self-consistent — it validates
> the objects it selected against themselves — and it is wrong. This is the same failure my predecessor
> hit summing D1-only rows and getting `OK` from his own denominator check; Schwab's external `T1`
> trailer caught it, nothing internal could.

**BINDING RULE FOR THE REMAP: the denominator is ENUMERATED AT RUN TIME FROM THE SOURCE, never read
from this document, the TO, or the PRD.** And the remap must run *after* the 0824 pull terminates, or
be re-run to convergence after it does. A partial-tree copy that reports parity is worse than no copy.

### F-2 — ETag-IDENTITY WILL FALSE-FAIL ON ~52 OBJECTS, AND THE TEMPTING FIX REMOVES THE CONTROL

`ETag-verify` is the TO's acceptance mechanism, and it is sound — but only for single-part objects,
where the ETag *is* the MD5 of the bytes. Measured live:

```
0833  multipart-ETag objects ("<hash>-N"):    0  of 6,932     <- why the prior 6,932/6,932 verify held
0824  multipart-ETag objects:               ~52  of 1,285 and growing
      (objects up to 29 MB exist; the CLI's default multipart threshold is 8 MB)
```

0833's objects were **server-side copied** in (single-part -> plain-MD5 ETag). 0824's are being
**uploaded** by the puller, so everything over the 8 MB threshold went multipart and carries a
`<hash>-N` ETag, which **is not an MD5 of anything**.

A server-side `CopyObject` of a <5 GB object writes the destination as a single part, so the
destination ETag is a plain MD5. **For those ~52 objects the source and destination ETag strings will
DIFFER while the bytes are byte-for-byte identical.**

> The naive reading is "52 corrupted objects." The naive fix is to loosen the ETag check — **which
> retires the only control that would catch a genuinely corrupted copy.** A false alarm that gets a
> guard removed is not a safe error.

**THE VERIFY, CORRECTLY TYPED — three tiers, all provable without ever reading the monolith:**

| Source ETag shape | Population | Verify |
|---|---|---|
| plain MD5 (no `-N`) | ~99.4% | source ETag == dest ETag, **both read from a LISTING**. Byte-identity proven. |
| multipart (`-N`) | ~52 | ETag equality is **NOT expected and NOT required**. `GetObject` the SOURCE (the remap role has this), stream-hash it to MD5, compare against the DEST ETag from the listing. True byte-level verify. |
| all objects | 100% | Size identity from both listings, always. |

This is why the remap role needs **no `GetObject` on `opal-data-assets`** (see §3): `ListObjectsV2`
returns ETag *and* Size for every key, so set-identity and byte-identity are both provable from a
listing. The naive design — `head-object` each landed key — authorizes as `s3:GetObject` on the target,
i.e. it **buys a verification step by granting the migration read access to the consolidated estate.**
We do not have to make that trade, so we don't.

---

## 1. GROUND TRUTH (live S3, 2026-07-14 ~01:20Z)

```
opal-data-schwab/08242234/bronze/   1,285 objects   LIVE, CLIMBING (wide pull in flight -> 5,966)
opal-data-schwab/08335338/bronze/   6,932 objects   TERMINAL (migrated, ETag-identical, 0 quarantine)
opal-data-assets                    DOES NOT EXIST  (404 HeadBucket) -- C1, owned by 0.7.0_AE_CloudOps
```

Source bucket encryption, measured: **AES256 (SSE-S3)**, and the bucket policy carries
`DenyUnencryptedObjectUploads` — `Deny s3:PutObject` when `s3:x-amz-server-side-encryption != AES256`.

> **A METHOD NOTE THAT COST ME A WRONG CONCLUSION AND NEARLY REACHED THIS PAGE:** `aws s3 ls` prints
> `LastModified` in **LOCAL time**; `aws s3api list-objects-v2` returns **true UTC** (ISO8601 `Z`).
> Reasoning in UTC off an `s3 ls` timestamp made a pull that was writing *that second* look **four
> hours dead**. Had I reported that, the fix everyone would reach for is "restart the puller" — on a
> puller that is already running. **Ground a freshness claim on `list-objects-v2`, never on `s3 ls`.**

---

## 2. C3(a) — REMAP PLAN (7,256 -> re-enumerate; zipped copy, ETag-verify)

**Not a re-pull. Not a delete. Additive only.** 257 objects in `01_raw/` are irreplaceable (Schwab's
REST floor is 2023-07-12 and it can no longer serve them); that caution binds the whole class.

```
SOURCE  opal-data-schwab/{master}/bronze/{type}/{YYYYMMDD}/{vendor}.zip
TARGET  opal-data-assets/schwab/{master}/bronze/{type}/{YYYYMMDD}/{vendor}.zip
        (ruling 5's grammar, one level down inside the source tree — ruling 9)
```

1. **GATE — 0824 pull terminal.** Do not start until the wide pull reports its terminal denominator
   (`enumerated == downloaded + skipped + failed`). Or start, and **re-run to convergence** after.
2. **ENUMERATE THE SOURCE.** `list-objects-v2` both master prefixes. Print the denominator. This is
   the count everything downstream is checked against — **never `7,256`** (F-1).
3. **SKIP-INDEX.** List the target. Copy only keys absent there -> idempotent, re-runnable, self-healing.
   A re-run of a completed remap lands 0 objects and reports skip, not error (TO acceptance 4).
4. **COPY, server-side.** `CopyObject` (no bytes traverse the laptop). The `.zip` stays a `.zip` —
   bronze is raw, byte-for-byte, as the vendor shipped it. **`--sse AES256`** (see the §3 fork).
5. **VERIFY, three-tier, per F-2.** Set-identity + size-identity from both listings; ETag-identity for
   single-part sources; source-stream-MD5 vs dest-ETag for the ~52 multipart sources. Any mismatch
   QUARANTINES that key and RAISES — never a silent skip.
6. **REPORT** both denominators (source count, landed count) with no sampling.

**Runs under `opal-schwab-monolith-remap-role`** (§3) — assumed, scoped, no delete, cannot read the
monolith. This closes my own self-flagged gap: the 6,932 migration ran under broad AE user creds.

## 3. C3(d) — IAM (AUTHORED + PLANNED, NOT APPLIED)

**File:** `infra/aws/terraform/canonical-schwab-ec2/monolith-iam.tf`
**Plan:** `3 to add, 0 to change, 0 to destroy` — purely additive; the box's existing import-fidelity
inline policy is **untouched** (that `0 to change` is the evidence, not a formality).

| Resource | Identity | Grant |
|---|---|---|
| `schwab_si2_monolith_write` | the **box** (`quartz-si2-spike-role`) | ListBucket (prefix-conditioned) + PutObject on `schwab/{master}/bronze/*`. **No GetObject.** For C3(b)'s go-forward daily pull landing direct. |
| `schwab_monolith_remap` (+inline) | **new scoped role**, assumed by the AE principal | Read staging bronze, write monolith bronze, List both. **No GetObject on the monolith. No DeleteObject anywhere.** For C3(a). |

Masters **enumerated, never wildcarded** in every statement — a `schwab/*/bronze/*` grant would let a
mis-scoped run invent a master prefix and write there successfully, handing back the exact guarantee
the master-scoped keyspace exists to provide. Adding a third master is a deliberate, reviewed edit.
Firm-sep Deny planes (bd/cot/inf) cloned onto the new role; an explicit Deny wins over any Allow,
including one a future edit adds without reading the file.

The box **cannot** do the remap: `CopyObject` needs `GetObject` on the source, and granting the box
read access to its own bronze to save a role would permanently retire its write-only-for-data
invariant for the convenience of a one-time job.

### ⚠ OPEN FORK FOR CTO — THE ONE WAY THIS APPLIES GREEN AND DENIES 100% AT RUNTIME

Neither grant says anything about **encryption**, and C1 decides whether they are sufficient:

- **`opal-data-assets` = SSE-S3/AES256** -> grants are complete; the copy passes `--sse AES256`.
- **`opal-data-assets` = SSE-KMS** -> grants are **NOT sufficient**. Both identities also need
  `kms:GenerateDataKey` (+`Encrypt`/`DescribeKey`) on that **exact CMK ARN**, and the failure arrives
  as `AccessDenied` on PutObject **from an IAM policy that reads perfectly**.

I deliberately did **not** author a speculative KMS statement: there is no key ARN yet, and the only
way to write one blind is a wildcard — precisely the never-widen failure the file exists to avoid.
**Sequence:** C1 declares the SSE mode -> I add one scoped KMS statement against the exact key ARN (or
none) -> live `simulate-principal-policy` -> apply gate.

**Surfaced, not adjudicated.** SSE-S3 keeps every producer role KMS-free and matches the source;
SSE-KMS buys per-key auditability on a bucket that will hold multiple firms' custody data, at the cost
of a KMS grant in every producer role that ever writes to the monolith. **CTO's call. `0.7.0_AE_CloudOps`
needs it before C1 lands.**

**22a grounding status, stated honestly:** `DESIRED` = the plan above. `APPLIED` = **NOTHING** — not
applied, by instruction. `EXERCISED` = **NOTHING** — the target bucket does not exist, so
`simulate-principal-policy` against the real ARNs **cannot be run yet and I am not going to fake it**.
`comp-iam` would report GREEN on these ARNs today and it would mean nothing: it models `(action)`,
never `(action, resource)`. The live simulate (one `--resource-arns` per call, positive control as a
separate invocation, `--context-entries` for the conditioned statements) runs **after C1 lands and
before the apply gate closes**. That is a gap, it is explicit, and it is not a PASS.

## 4. C3(b) — CATCH-UP / DAILY PULL PLAN

`sdd-daily-pull.ps1` already carries the hard parts (wide rolling window never `from=today`;
skip-if-landed; partition date from the API's `AsOfDATE` cross-checked against the vendor filename,
disagreement -> QUARANTINE; master **observed from the vendor's bytes**, never inferred from the
request; **zero files on a trading day is FATAL, not a shrug**; `enumerated == downloaded + skipped +
failed` or RAISE).

**The only change for the monolith:** target bucket/prefix ->
`opal-data-assets/schwab/{master}/bronze/{type}/{YYYYMMDD}/`, plus the SSE header per §3. Per-master
type rosters stay as-is (0824 has `rlw` and no `fam`/`slm`; 0833 the reverse — a shared type list would
demand `08242234/fam` every day forever, and *a permanently-red alarm is a guard everyone has agreed
to ignore*).

**Same-day catch-up, business dates >= 2026-07-13 — AND RESOLVE THE CALENDAR FIRST (NEVER#1):**

```
now            2026-07-14 01:20Z  ==  Monday 2026-07-13, 21:20 ET
07-11 / 07-12  WEEKEND (no session)
newest landed  20260710 (Friday)
```

> **The absence of an `07-13` partition right now is NOT a gap, and it is NOT staleness.** Monday's CRS
> files post overnight. As of Monday evening ET the newest data that *should* exist is Friday's — which
> is exactly what is landed. **Friday's data IS Monday's correct answer.** Catch-up means: pull business
> date 07-13 when Schwab publishes it (Tuesday), then 07-14, and so on. A successor who diffs the
> partition list against a wall-clock calendar will "find" a hole here. There is no hole.

## 5. C3(c) — EVENTBRIDGE REPOINT (NOT GO'd — the last step, and the one that turns it on)

`canonical-schwab-si2-download-schedule` still targets the **dead GUI `SchwabAutoDownload` task** —
the channel that reported `rc=0` and *"vendor likely not posted"* for 22 consecutive cycles over 11
days while the vendor **was** posting. It is still pointed there, deliberately: **nothing can
auto-start.** The dead channel is still dead; it is just no longer the only thing we have.

Repoint to `sdd-daily-pull.ps1` **last**, after the landing GO and a verified monolith write.

---

## 6. SEQUENCE + GATES (what unblocks what)

```
C1 lands (0.7.0_AE_CloudOps)  +  SSE-mode ruling (CTO)
        |
        +-> add scoped KMS stmt (or none) -> live simulate-principal-policy -> CTO APPLY GATE -> IAM applied
                |
                +-> [0824 wide pull reaches terminal denominator]  ->  C3(a) REMAP (re-enumerate!) -> verify
                |
                +-> C3(b) puller retarget -> monolith -> verified write
                                |
                                +-> C3(c) EventBridge repoint  <- the daily pull actually turns on here
```

**Blocked on:** C1 (bucket does not exist) + the SSE fork (CTO). **Not blocked on:** the 0824 pull,
which continues under Andrew's direct GO and is what makes the remap denominator final.

## 7. Compiler Tools

| Tool | Purpose | Result |
|---|---|---|
| `comp-grep 'opal-data-assets' <PRD>` | locate the monolith grammar + C-row spec | PASS — 13 matches / 1 file; gave §2 grammar + §4 C1/C3 rows |
| `comp-to` | bind session TO_ID (race-free per-session, never `.agent_context`) | PASS |
| `terraform validate` | new IAM file | PASS — "Success! The configuration is valid." |
| `terraform plan` | C3(d) grant, **plan only, never apply** | PASS — `3 to add, 0 to change, 0 to destroy` (the `0 to change` proves import fidelity held) |
| `aws s3api list-objects-v2` | live denominators, UTC freshness, ETag shape | PASS — produced F-1 and F-2, neither visible from the PRD |
| `aws s3api get-bucket-encryption` / `get-bucket-policy` | source SSE + the forced-SSE deny | PASS — AES256 + `DenyUnencryptedObjectUploads`; drove the §3 fork |
| `comp-iam` | **deliberately NOT cited as evidence** | It FAILS GREEN on a new bucket — models `(action)`, never `(action, resource)`. A GREEN from it here would be noise formatted as confidence. |

**GAP FOUND (banked, method-class):** `aws s3 ls` prints `LastModified` in **local** time while
`list-objects-v2` returns UTC. Mixing them turns a live producer into a four-hours-dead one. The
estate reasons in UTC and reaches for `s3 ls` by reflex. Worth a rail nudge.

**A control that failed GREEN on me, in this session, and is worth naming:** I checked whether the
monolith bucket exists with `aws s3api head-bucket ... | head -3 && echo EXISTS`. It printed **EXISTS**
while AWS returned **404 Not Found** — the pipe's exit status is what `&&` saw, not the API's. Same
class as `grep -c` counting zero matches in an error message. **Put the control on the retrieval.**
