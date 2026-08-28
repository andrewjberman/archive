# D1_CATVIEWS.TO-I1-DS — ASSESSMENT OF THE ENUMERATION DELIVERABLE

**Assessing lane:** `0.4.0_DS_ClientPlatform~T` (successor session; predecessor died 2026-08-26)
**Subject:** `D1_CATVIEWS.TO-I1-DS_PATH_TO_LIVE_CHANNEL_ENUMERATION.md`, 12,072 B, committed `@a6c2bac919`
**TO face read at:** `@756bd9de56` · **assessed at HEAD `88909a657b`** (branch `SITEZ`)
**Why this exists:** the TO face records, twice, that the deliverable **"remains unassessed by anyone"**
(`2.0.0_SA_COO~Z`, 12602 s.3). This is that assessment. **It is a separate artifact: the predecessor's
deliverable is committed evidence and was NOT edited.**

---

## 0. VERDICT

**THE DELIVERABLE'S FOUR CRITERION VERDICTS STAND. ALL FOUR ARE SUPPORTED.**
**Three defects found, all in SUPPORTING material; none overturns a criterion, and one materially
STRENGTHENS `AC1`.**

| criterion | predecessor | this assessment | basis |
|---|---|---|---|
| `I1DS-AC1` | PASS | **PASS — strengthened** | denominator 22 re-derived independently at HEAD **and** at the true running pin |
| `I1DS-AC2` | PASS | **PASS** | third route re-confirmed at source by a different instrument, two independent carriers |
| `I1DS-AC3` | PASS | **PASS** | audited by reading; the episode cited *is* AC3 being honoured, though its stated mechanism is wrong (F2) |
| `I1DS-AC4` | APPLIED-GATED | **APPLIED-GATED** | no re-pin, apply or pin advance by this lane; unchanged |

⛔ **NOT CLAIMED:** that I re-downloaded the deployed zip. I did not. The 23-entry zip enumeration
remains the predecessor's single-hand measurement — **but see F1, where its own arithmetic now
corroborates it against a source I measured independently.**

---

## 1. METHOD — AND WHY IT IS NOT REPETITION

**Rule 22: a second seat confirming via the FIRST seat's method is REPETITION, not corroboration.**
The predecessor's primary instrument was the **downloaded executing zip**. I therefore assessed from
the **BUILD-INPUT side** (Rule 22a CODE layer: resolve deployed code through the build input), which is
a different instrument that can disagree.

| # | claim under test | my instrument | differs from predecessor's? |
|---|---|---|---|
| 1 | the `22` denominator | `git show <ref>:build_package.py` → AST-eval the `PACKAGE` literal at 5 refs | **yes** — build input, not the zip |
| 2 | "19 is a stale vintage" | same, at `a4d71e9544` | **yes** |
| 3 | the third route (EC2) | `comp-find` content sweep, corpus=raw, denominator printed | **yes** — the predecessor read the manifest directly |
| 4 | `trading_calendar.py` NO-WRITER | called `safe_deploy_core.file_to_s3_target` **on the key's preimage**, + existence check | **partly** — same function, **different question** (see F3) |

**Controls on every run.** Vintage reads carried a positive control (`a4d71e9544` resolves) and a
negative control (`zzzznotacommit`); the resolver call carried a positive control (a normal gold
script resolves) and a negative control (a bogus path → `None`).

---

## 2. WHAT I CONFIRMED

**`AC1` — the denominator. CONFIRMED, and the reconciliation is right.**

```
ref               entries  .py   mdpf_category_registry present
HEAD                  22    18   True
14b077f559            22    18   True      <- the TRUE running pin (see F1)
a4d71e9544            19    16   False     <- the TO's "19", dated 2026-08-06
1b96f70ad3         UNRESOLVED                <- the deliverable's claimed "running pin" (F1)
zzzznotacommit     UNRESOLVED                <- NEGATIVE CONTROL, same failure shape
```
**The TO's `19` is a vintage, exactly as the deliverable says.** Denominator **22**, independently
re-derived. `AC1` requires the denominator printed beside the count; it is, throughout.

**`AC2` — the third route. CONFIRMED, two independent carriers.**
`infra/aws/ec2/EC2_MANIFEST.json:440` carries `calendar_distribution` →
`s3://opal-data-mdpf/code/scripts/gold/trading_calendar.py`. Independently corroborated by the deploy
ledger that created it: `org/critical_paths/change_management/20260811T0845Z_mdpf-chain-calendar-distribution.md:37`
("EC2_MANIFEST.json mdpf-daily-runner gains `calendar_distribution` (this commit)"). Sweep denominator
printed: **4 hits across 239,685 files scanned, corpus=raw.**
**The axis is three-valued. That finding holds.**

**`AC4` — CONFIRMED as a negative.** No re-pin, `safe-apply` or pin advance by this lane, and none
proposed as ready. ⚠ `0.7.0_AE_CloudOps~Z` applied `@ecd8bf438b` to `gold-lambda.tf` on 2026-08-28
~01:1xZ; that seat recorded it as **not** a pin advance, with a did-not-move control
(`CodeSha256`/`CodeSize` identical pre/post). **That is an AE act on an AE surface and this lane does
not adjudicate it** — named here only because it post-dates the deliverable and a reader comparing
dates would otherwise wonder.

---

## 3. F1 — ⛔ THE "RUNNING PIN" ROW NAMES A COMMIT THAT RESOLVES TO NOTHING

The deliverable's vintage table (s.0) carries:

> `PACKAGE at the **running pin** 1b96f70ad3` — **21** entries / **17** `.py`

**`1b96f70ad3` resolves to no object in this repo**, measured with both controls (§2). The true pin the
deployed bytes name is **`14b077f559`**, whose `PACKAGE` is **22 / 18**.

⭐ **THE ARITHMETIC IS THE DISCRIMINATOR, AND IT DOES NOT DEPEND ON WHETHER THE OBJECT WAS EVER
RESOLVABLE.** The deliverable measures the executing zip at **23 entries = 22 members + a
builder-generated `BUILD_MANIFEST.json`**. Then:

```
PACKAGE 22 (at 14b077f559)  + 1 generated manifest  = 23   == the measured zip.  RECONCILES.
PACKAGE 21 (claimed row)    + 1 generated manifest  = 22   != the measured zip.  DOES NOT.
```

**So the deliverable's own executing-artifact measurement contradicts its own supporting row, and
agrees exactly with the pin I measured.** The zip enumeration is corroborated; the table row is wrong.

**PROVENANCE, so this is not read as the predecessor inventing a number:** `1b96f70ad3` was the literal
value of `MDPF_GOLD_COMMIT` in `infra/aws/terraform/mdpf-pipeline/gold-lambda.tf` at the time the
deliverable was written. **The predecessor read the declared pin faithfully. The declaration was a
phantom.** It was found unresolvable and corrected to `14b077f559` by `0.7.0_AE_CloudOps~Z` (11437)
and confirmed by `2.0.0_SA_COO~Z` — **~31 hours AFTER this deliverable was filed.**

⛔ **THE ONE THING THAT IS FAIRLY THE PREDECESSOR'S:** the deliverable **cites Rule 22a's ephemeral-pin
clause `@4424c948f7` — "resolved by CONTENT (`git show <pin>:<file>` + negative control)" — and does not
run the negative control that clause prescribes.** A negative control on that pin would have returned
the same failure as `zzzznotacommit` and stopped the row from being written. *Citing a rule is not
applying it.*

⚠ **UNDETERMINED, AND I AM NOT GUESSING:** whether `1b96f70ad3` resolved on 2026-08-26 and became
unreachable, or never resolved. I cannot distinguish those and the distinction does not change F1 —
the arithmetic above settles the row either way.

---

## 4. F2 — INV-5's CONCLUSION IS RIGHT; ITS STATED MECHANISM IS WRONG

The deliverable's `AC3`/`inv-5` centrepiece (s.5):

> reading `build_package.py` **at the running pin** showed `mdpf_category_registry.py` **ABSENT** from
> its `PACKAGE` list … the ZIP BYTES show it **IS** present. *The pin is an ephemeral cherry-pick whose
> `build_package.py` is an older vintage than the builder that actually ran.*

**Measured: at the true running pin `14b077f559`, `mdpf_category_registry.py` IS PRESENT in `PACKAGE`
(22/18).** It is absent only at `a4d71e9544` (2026-08-06).

>> **So there was never a vintage gap between the builder's `PACKAGE` and the zip. The gap was between
   a PHANTOM DECLARATION and reality.** The conclusion — *read the bytes, not the graph* — is right,
   and `AC3` is honoured: the deliverable refused to report a live property from a commit. **But the
   reason it gives for the discrepancy is not the reason.** <<

⭐ **This makes `AC3` stronger, not weaker.** The episode is a real instance of the invariant biting.
It is the *explanation* that needs replacing — and the replacement is a sharper hazard: **a
`MDPF_GOLD_COMMIT` that names no object cannot be caught by reading it, only by resolving it.**

---

## 5. F3 — THE `trading_calendar.py` FINDING IS RIGHT, AND ONE STEP MORE PRECISE THAN STATED

The deliverable states: *"`safe_deploy_core.file_to_s3_target("lib/trading_calendar.py")` returns
`None`. There is **NO DS deploy path that writes that key**."*

**The conclusion holds. The evidence offered does not establish it** — it tests ONE candidate repo
path, not the key's preimage. Testing the preimage:

```
lib/trading_calendar.py                          -> None                                   [tested by predecessor]
data/mdpf/scripts/gold/trading_calendar.py       -> ('opal-data-mdpf',
                                                     'code/scripts/gold/trading_calendar.py',
                                                     'mdpf')                                <- THE KEY *DOES* HAVE A MAPPING
data/mdpf/scripts/gold/mdpf_gold_consolidator.py -> (...)                                   [POSITIVE CONTROL: resolver discriminates]
zzz/no/such/file.py                              -> None                                    [NEGATIVE CONTROL]

git ls-files / working tree:  data/mdpf/scripts/gold/trading_calendar.py  DOES NOT EXIST
                              lib/trading_calendar.py                     EXISTS, 6,979 B
```

>> **THE MECHANISM IS NOT "THE KEY HAS NO WRITER". IT IS "THE WRITER EXISTS AND HAS NO SOURCE FILE
   BEHIND IT."** `file_to_s3_target` is a pure path-mapper — it returns a target for a path that is
   not there. The deploy path is wired to `data/mdpf/scripts/gold/`, and the module lives in `lib/`. <<

⭐ **Corroborating datum the deliverable did not state:** `lib/trading_calendar.py` is **6,979 B**, and
the S3 object the EC2 runner consumes measured **6,979 B**. Equal size is not equal content, but it is
consistent with **the divergence being LATENT and not yet realised** — which is the strongest form of
the warning, not a weakening of it.

**Why the precision matters:** "no writer exists" points at *building* one. "The writer is wired to a
path the module does not occupy" points at *relocating the module or repointing the manifest*.
Different remedies, and the second is one edit.

⚠ **RECORDED, NOT CHASED** per the standing refactoring/migration embargo (Andrew ~20:32Z). No remedy
taken, none proposed as ready.

---

## 6. `cell_status` — HELD FOR THE ISSUER, DELIBERATELY

The TO's `<reporting>` clause asks for `cell_status` **"per cell on this face at close-out."**
**I did not write it to the face, for two measured reasons:**
1. **The face is the issuer's surface** — `git log` on the TO file: **5 of 5 edits by `2.0.0_SA_COO~Z`
   / `2.0.0_SA_COO`.** An executor writing it unilaterally is a lane breach.
2. **We are not at close-out.** The TO remains `ACTIVE`; `AC4` is `APPLIED-GATED` and `3.0.0_SA_CVO~Z`
   has not certified.

**Values, ready to transcribe, unchanged from the predecessor's — I re-derived each from observed
states and concur:**

| cell | status | basis |
|---|---|---|
| `D1-i-1` | **OBSERVED — COMPLETE** | enumeration performed end to end; denominator independently re-derived at two refs by this assessment |
| `D1-i-2` | **OBSERVED — DID NOT EXECUTE** | the fence and the decision not to run were observed; no property of a re-pin was observed, because none occurred |
| `D1-inv-5` | **OBSERVED — HELD** | observed as a binding constraint that changed the executing seat's method mid-task; **not** "verified" as a property of the estate |

⛔ These are **not** synthesised from the criterion verdicts. 4 criteria and 3 cells are different
objects.

---

## 7. SURPRISE-CHANNEL ITEMS — `3.0.0_SA_CVO~Z` as channel owner, cc the issuer

**S-A · OBSERVATION / INERT — `proof-of-spec-check.py`'s content-based TO resolver has never matched
anything, estate-wide.**
`_resolve_governing_to` (`.tools/proof-of-spec-check.py:258`) searches for the needle
`id="<canonical-to-id>"` — **attribute** form. Measured with the tool's own `_canonical_to_id` and its
own tracked-TO set:

```
tracked TOs scanned                      2152
  resolvable by the tool's needle           0
  declare <id>…</id> ELEMENT form only   1469
```

**0 of 2152.** Every instance without an explicit `decomp_ref.to_ref` therefore reads
`governing TO UNRESOLVED`, and on a pipeline-registered project that is a hard violation. It fails
**closed**, so nothing has been laundered — but layer 1's content branch has never run. **The declared
`to_ref` branch works and is the remedy I used.** Not chased; routed.

**S-B · OBSERVATION / INERT — F3 above**, as a refinement of a hazard already recorded by the
predecessor and already in the channel. No new action requested.

---

## 8. PUSH STATE

Stated in the commit report accompanying this deliverable, as a **measured** value
(`git ls-remote` against a fetched ref, with a control) — never a default.
