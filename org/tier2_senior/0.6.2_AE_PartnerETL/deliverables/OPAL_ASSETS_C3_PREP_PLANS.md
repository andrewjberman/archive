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

### THE SCRIPT IS WRITTEN, AND ITS PARSER IS EXERCISED ON THE LIVE CORPUS

`infra/aws/ec2/canonical-schwab-si2/remap-bronze-to-monolith.py` — **dry-run by default; `--execute` is
required to copy a byte, and it cannot run at all until C1 and the role exist.**

I wrote it now, unprompted, for one reason: **the hazard in F-2 is not that the remap fails — it is that
someone writes the naive twenty-line `aws s3 cp --recursive` with an ETag-equality check, watches it
"fail" on 52 objects, and loosens the check.** The correct verify existing first is the control. Its
ancestor (`migrate-0833-to-canonical.py`, the exercised 6,932 migration) counted objects and **never
proved a byte** — that gap is closed here.

**EXERCISED, read-only, against every object that exists right now:**

```
08242234   enumerated 1,496   parsed clean 1,496   QUARANTINE 0    multipart ETags  54  <- tier-3
08335338   enumerated 6,932   parsed clean 6,932   QUARANTINE 0    multipart ETags   0  <- tier-2 only
                                                                   single-part     8,374

NEGATIVE CONTROL (must ALL raise):  no-master / bad-date-encoding / no-date   -> all 3 REJECTED
POSITIVE CONTROL (run separately):  CRS20260710 -> 20260710 · CS071026 -> 20260710  -> both exact
```

The multipart asymmetry F-2 predicted is **confirmed on live bytes**: 54 in 0824, 0 in 0833. A decoder
that never refuses anything is a default with extra steps, so it was run against inputs it must reject —
and the positive control was run **separately** from the target, because a control batched with the thing
it validates is corrupted by its own presence.

## 2b. THE 01_raw PRE-FLOOR LEG (Andrew-direct, v1.3.5) — AND WHY IT IS NOT A COPY JOB

> Andrew, verbatim: *"We can keep those unique files in bronze, bring them over in migration."*

These 257 objects predate Schwab's REST floor (2023-07-12). **Schwab can no longer serve them at any
price** — a re-pull is not an option, so this is a copy job or it is nothing. I went to ground-truth them
before writing code, and the ruling **cannot execute as written.** Both blockers are measured, not inferred.

### ⛔ BLOCKER 1 — 217 OF THE 257 ARE IN GLACIER

```
the 257 IRREPLACEABLE pre-floor objects:   GLACIER 217  |  STANDARD  40
all of 01_raw (7,142 objects):             GLACIER 6,075 |  STANDARD 1,067
```

An archived object cannot be server-side `CopyObject`'d — it fails `InvalidObjectState`. I did not reason
my way there; **I hit it: my H1 probe failed on 224 of 257 reads.**

> **AND IT BITES TWICE, WHICH IS THE PART THAT MATTERS.** The landing spec says the master is *observed
> from the H1 header*. **You cannot read the header of an archived object either.** So the restore is not
> a precondition of the *copy* — it is a precondition of knowing **which master the file even belongs to.**

This leg is therefore **RESTORE → WAIT (hours) → COPY → VERIFY**, not a copy. It needs `s3:RestoreObject`,
an action **no role in this estate holds** — mine included. I have **not** authored that grant: it is a new
action on the irreplaceable class, so it goes to CTO rather than quietly into my role. Recommended tier:
**Bulk** — retrieval dollars are noise (largest object 67.9 MB), the cost is latency, and nothing is waiting
on files that have sat frozen for years. Restored copies are **temporary**; the copy must finish inside the
window or we pay for the thaw twice.

**Scheduling consequence:** this cannot be a step inside the C3 remap window. Sequenced as "the 257 land
with the remap," the whole remap blocks on a Glacier thaw. **Recommendation: split it** — the .zip corpus
remaps immediately on C1; the 257 run as their own restore-gated leg that rejoins when thawed. *They are
irreplaceable, not urgent.*

#### ✅ RULED (CTO, v1.3.8) — and the split was adopted: the thaw PARALLELIZES rather than blocking

```
RESTORE     BULK tier, Days=14
GRANT       s3:RestoreObject on opal-data-schwab/01_raw/*  --  the DEDICATED REMAP ROLE ONLY, never the box
TIMING      the restore is SOURCE-SIDE and C1-INDEPENDENT: the moment the grant applies, kick the thaw and
            let the 5-12h Bulk retrieval run in PARALLEL with C1's landing
SEQUENCE    RESTORE -> WAIT -> COPY -> VERIFY, with 13c's tier-3 MD5 run INSIDE the Days=14 window
CLOSURE     >> THE RestoreObject GRANT IS REMOVED WHEN THE MIGRATION COMPLETES. <<
```

> **The closure step is the part that will be forgotten, so it is written here and in the .tf itself.** A
> standing restore grant on the irreplaceable class outlives its job — **and a permission that outlives its
> job is a permission nobody is watching.**

**AUTHORED (`3 to add, 0 to change, 0 to destroy`), NOT APPLIED — and I added two statements CTO did not
name, deliberately and in the open:** `s3:RestoreObject` alone **cannot run this leg.** It also needs
`s3:ListBucket` on `01_raw/*` (the run-time denominator *and* the storage-class read that says which
objects are frozen) and `s3:GetObject` on `01_raw/*` — because **the master exists only in the bytes.** The
filenames carry no account number, which is the entire reason Andrew ruled H1-observed identity; *reading a
header is a `GetObject`, so without it the H1 rule is unimplementable.* Tier-3 verify streams the source
too. **A grant that is two-thirds authored fails at runtime**, so I am naming the addition rather than
letting it surface as an AccessDenied. Still **no** `GetObject` on the monolith — the target stays
write-only, and verification reads the destination ETag from a *listing*.

**Also ratified at the ruling level:** my scan-for-exactly-one-master parser; **positional H1 indexing is
BANNED** (citing the TCF measurement); **firm name as a validation signal is BANNED** (citing the
two-names-one-master measurement); and the 217 archived masters stay **UNASSERTED until read.**

### ⛔ BLOCKER 2 — THE TCF PRODUCT HAS A DIFFERENT H1 LAYOUT, AND THE OBVIOUS FIX BREAKS THE OTHER HALF

```
RLD/RLY/RLU/RTU/RTY :  H1|SCHWAB  |0008242234|49 WEALTH MANAGEMENT LLC|20230117|CBRGLDLT|01.06
                            field 2 = MASTER (10-digit, zero-padded)
TCF (confirms)      :  H1|SCHWAB|CONFIRM |08242234|49 WEALTH MANAGEMENT LLC|20230119|01.01
                            field 2 = "CONFIRM"      field 3 = MASTER (8-digit, unpadded)
```

TCF is **120 of the 257** — the second-largest type (RLD 121, TCF 120, RLY 6, RTY 6, RLU 2, RTU 2).

> **A POSITIONAL PARSER IS WRONG FOR HALF THE SET WHICHEVER INDEX YOU PICK.** `f[2]` hands you the string
> `"CONFIRM"` on a TCF. And the fix — `f[3]` — hands you **`"49 WEALTH MANAGEMENT LLC"` on an RLD, *without
> raising*,** because a firm name is a perfectly good string. **The crash is the lucky case.** The silent
> one mis-attributes an irreplaceable custody file.

**The parser therefore does not index. It SCANS** every field for a value that normalizes to a *known*
master and requires **exactly one** candidate — zero or ambiguous ⇒ quarantine, never a default.

### TWO SMALLER ONES, BOTH REAL

- **THE FIRM NAME IS NOT A CROSS-CHECK.** Master `08242234` appears as **both** `49 WEALTH MANAGEMENT LLC`
  **and** `49 FINANCIAL` in the same corpus — the account was renamed. I nearly used it as a confirming
  signal. It would have been a confident, well-grounded, **wrong** control.
- **11 of the 257 carry multipart ETags** → ruling 13c's tier-3 source-stream-MD5 is **load-bearing here,
  not theoretical** (and it costs a full GetObject of a *restored* object, inside the thaw window).

### EXERCISED (live bytes, read-only)

```
H1 parser, BOTH layouts + 0833            4/4 exact
NEGATIVE CONTROLS (must all raise)        4/4 rejected: not-H1 · unknown master · TWO masters (ambiguous) · no date
01_raw leg, end-to-end dry run            257 enumerated · 40 STANDARD / 217 GLACIER split correctly
                                          40/40 identified from H1 bytes, masters {08242234: 40}
                                          -- INCLUDING the 7 TCF files the positional parse choked on
then BLOCKED, legibly, on s3://opal-data-assets not existing (C1) -- not a defect, a dependency
```

**WHAT I WILL NOT CLAIM:** all readable pre-floor objects attest `08242234`. **I cannot say that about the
217 in Glacier — I have not read them, and I will not assert their master until I have.** If one attests
`08335338` it belongs in the 0833 tree, and that is exactly the case Andrew's H1-observed rule exists to
catch. The leg **returns a non-zero "INCOMPLETE BY DESIGN"** if it copies only the thawed subset — it will
not let a partial run be recorded as a closed one.

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

### ✅ THE SSE FORK — ANSWERED (0.7.0_AE_CloudOps, 01:31Z; source-confirmed by me, not taken on his word)

Neither grant says anything about **encryption** — the one way both APPLY GREEN, read perfectly in every
IAM instrument, and DENY 100% OF CALLS AT RUNTIME. I raised it to CTO as a fork and to 0.7.0 as a
C1 dependency, *before* he landed the bucket. He answered, and I verified the answer against his HCL
rather than his summary:

```
infra/aws/terraform/opal-assets/monolith.tf:129   sse_algorithm = "AES256"
  KMS references in the module source          :  ZERO
  DenyUnencryptedObjectUploads statement       :  ABSENT -- deliberately
```

**MY GRANTS ARE COMPLETE AS AUTHORED. No KMS statement. Nothing widened.**

And he made it better than I asked: the monolith carries **no forced-SSE bucket policy**, so a producer
that omits the header still succeeds *and still lands encrypted* (default encryption applies server-side
regardless). That is the deliberate inverse of `opal-data-schwab`, whose forced-SSE deny returns an
`AccessDenied` **indistinguishable from a permissions bug** — which is precisely how an encryption-header
problem gets "fixed" by widening IAM. (It is also why DS is blocked writing that bucket.) He wrote the
reasoning into the TF comment so the next person cannot helpfully add it back.

He also found that his own first C1 draft granted a blanket `schwab/*` write — which, attached to
anything, could write **both masters**. He enumerated the scope segment instead. *"Do not commingle 0824
and 0833" stops being a rule someone has to remember and becomes a property of the role.*

> **STILL DESIRED, NOT APPLIED — and the distinction is the whole of 22a.** C1 is authored and validated,
> **not gated and not applied**; `opal-data-assets` does not exist (404, live).

### CLOSED — ruling 13 (v1.3.3) then **13a REVERSED** (v1.3.4, `f8ea5725d`)

CTO's first ruling adopted AES256 **plus** the `DenyUnencryptedObjectUploads` statement, citing "the
opal-data-schwab precedent **you measured**." But 0.7.0's HCL deliberately omitted that statement — so
**the ruling and the estate disagreed on a concrete artifact, right now, both citing authority.** I
surfaced that and did not adjudicate it.

I also had to correct a citation that was **leaning on my own evidence in a direction I did not intend**:
I measured the schwab deny as a **HAZARD**, not as a pattern to copy. With default encryption on, it adds
~nothing to encryption-at-rest — an upload omitting the header still lands, and still lands AES256 — while
returning an `AccessDenied` **indistinguishable from a permissions bug**, whose historical fix is
IAM-widening. (It is why DS is blocked writing that bucket.) I gave CTO the honest argument *for* it too —
defense-in-depth if default encryption ever drifts — so he ruled on both sides.

**13a REVERSED.** The monolith carries **AES256 default encryption only** — no deny statement, ever; no
producer header requirement, ever. **My grants stand unamended.**

> The rule this earned: **a verbatim citation without its SCOPE is not a faithful record — it is a future
> contradiction with a citation attached.** My measurement was quoted accurately and used to justify the
> opposite of what it showed. *Correcting a citation that favors your own finding is not modesty; it is the
> only way the record stays load-bearing.*

**Postscript worth keeping (COO, same thread):** running the producer header-sweep I'd flagged, his **first
grep searched for the boto3 parameter and missed the CLI flag** — it FAILED his positive control, and the
widened re-run is what actually verified my `:311/:342/:343` citations. *A sweep that cannot find a known-present
instance is not a clean sweep; it is a broken instrument reporting silence.* The control caught it. The care
would not have.

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
