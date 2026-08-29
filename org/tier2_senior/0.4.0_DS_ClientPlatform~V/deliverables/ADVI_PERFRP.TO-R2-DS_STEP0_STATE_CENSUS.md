# ADVI_PERFRP.TO-R2-DS — STEP 0 / AC0 STATE CENSUS

**Seat:** `0.4.0_DS_ClientPlatform~V` · **TO:** `ADVI_PERFRP.TO-R2-DS` @`700fc7d53b` (face re-read at
`700e89d50b`, which applied the two issuer clauses from CVO cert 78734)
**Census window:** 2026-08-28T18:56Z – 19:13Z · **Repo HEAD at close:** `b79db0b935`
**Distribution:** NOT TO `4.0.0_SA_CRO` (ADVI_PERFRP PRD restriction).
**No code changed. No leaf touched. No S3 write. This commit is the census only.**

---

## VERDICT IN ONE LINE

All 11 round-1 leaves have **ZERO persisted emissions on every plane I can read** (disk, served S3,
git history — three instruments, each with a positive control). The DE-side emptiness is the
**SERVING GATE**, not a build gap this TO can close — but the gate is **narrower than the pitch
assumed**: `PERFRP_AVAILABLE_LEAVES` hides exactly **1 of 5** cards, not 5 of 5. The build proceeds
against the campaign at **63 of 534** committed (`7c6aa7cea7`), **85 of 534** in the live working tree.

---

## (a) THE 11 ROUND-1 LEAVES × LAST EMISSION VINTAGE

**Denominator: 11 leaf emitter families**, confirmed on disk two ways — 11 `perfrp_*_{relationship,
account,advisor}.py` files in `data/assets/scripts/gold/runners_49f/`, and 11 `EMITTERS` entries in
`d_publisher_port.py:150–190`. This matches round 1's AC13 ("every leaf an EMITTERS entry").

| # | leaf family | emitter file | EMITTERS entry | **last emission** |
|---|---|---|---|---|
| 1 | `perfrp_activity_relationship` | present | `:150` | **NONE — never emitted** |
| 2 | `perfrp_activity_account` | present | `:153` | **NONE — never emitted** |
| 3 | `perfrp_performance_relationship` | present | `:156` | **NONE — never emitted** |
| 4 | `perfrp_performance_account` | present | `:159` | **NONE — never emitted** |
| 5 | `perfrp_allocation_relationship` | present | `:162` | **NONE — never emitted** |
| 6 | `perfrp_allocation_account` | present | `:165` | **NONE — never emitted** |
| 7 | `perfrp_gainloss_relationship` | present | `:168` | **NONE — never emitted** |
| 8 | `perfrp_gainloss_account` | present | `:171` | **NONE — never emitted** |
| 9 | `perfrp_transactions_relationship` | present | `:179` | **NONE — never emitted** |
| 10 | `perfrp_roster_relationship` | present | `:185` | **NONE — never emitted** |
| 11 | `perfrp_book_advisor` | present | `:188` | **NONE — never emitted** |

**11 of 11 UNEMITTED. 0 of 11 carry a vintage, because there is no emission to carry one.**

### Why this is a TRUE ABSENCE and not a failed search — three instruments, three positive controls

| instrument | result | POSITIVE CONTROL (proves the instrument can find a real artifact) |
|---|---|---|
| `find . -name "perfrp_*.json"` (excl. `node_modules`, `.git`) | **1 hit, 0 emissions** | The 1 hit is `portal/.frontend-dev/testing/perfrp_books_l3.json` (13,067 B, 2026-08-25) — a **DE fixture**, not a leaf emission. The instrument DOES return perfrp-named JSON when it exists. |
| `s3api list-objects-v2 platinum/advi/49financial/` | **12 objects, 0 perfrp** | All 12 enumerate and print with `LastModified`; the 10 data objects are the d01–d14 firm-dashboard leaves. The listing works and is non-empty. |
| `git log --all --diff-filter=A -- "*perfrp_*.json"` | **0 commits, all branches** | Same command shape returns commits for other paths; `--all` spans every ref, so a deleted-after-commit emission would still appear. |

**Vintage of the served plane argues the same way:** every one of the 12 platinum objects is
`LastModified 2026-08-21T15:03–15:04Z` — **three days BEFORE the round-1 emitters were authored**
(emitter files dated 2026-08-24/25). The served plane predates the emitters entirely.
`_manifests/latest.json` (20,948 B, 2026-08-21T15:04:19Z) contains the substring `perfrp`
**0 times**.

### Corroborated by round 1's own close record — a DIFFERENT instrument (prose, not filesystem)

`org/tier2_senior/0.4.0_DS_ClientPlatform~G/logs/2026-08-25/SESSION_ADVI_PERFRP_TO-R1-DS_COMPLETE.md`:
> "**Nothing is published.**" … "AE~G wires the publisher; **my first emission is their start
> condition.**"

Round 1 closed 14/14 PASS *without ever emitting* — by design. `perfrp_emit_core.py:21–25` states it
directly: *"THIS EMITS LOCALLY. It writes the file the port asks for and touches no S3 key … this
module has no S3 write path at all."* Its `--out` is a **required caller-supplied argument**
(`:343`), so round-1 exercises wrote to ephemeral paths that were never persisted. **The absence is
the designed round-1 end state, not a defect and not a regression.**

### ⚠ THE BRIEF'S FRAMING DOES NOT SURVIVE MEASUREMENT — surfaced, not chased

The D2 brief (`docs/briefs/d2-critical-path-sequencing-20260827.md` sec 4 P4.1), quoted on this TO's
own face, says: *"the 2 deferred performance leaves (**Activity/Allocation already ship**)"*.

**Measured: Activity and Allocation do NOT ship.** They have the same emission state as the other
nine — none — on disk, on the served plane, and in git history. There is no plane on which any perfrp
leaf ships.

**Consequence for the TO, stated so the issuer can rule rather than discover it at AC1:** the face
instructs that the two deferred performance leaves be *"identified BY THIS MEASUREMENT, not by
name."* The measurement does not identify **two** — it identifies **eleven**, all in the same state.
The b-series scope (b-2..b-7) is unaffected and I am proceeding on it unchanged; what is affected is
any downstream expectation that 9 leaves are already serving and only 2 remain. **No action taken.
Surfaced to `3.0.0_SA_CVO` cc `2.0.0_SA_COO` per the surprise channel; reported here to the issuer.**

---

## (b) WHY `PERFRP_AVAILABLE_LEAVES` IS EMPTY — measured at the consumer

### The three candidate mechanisms, each measured separately

**1. The contract handshake — MEASURED, NOT THE GAP.**

| side | file:line | value |
|---|---|---|
| producer | `data/assets/scripts/gold/runners_49f/perfrp_contract.py:37` | `CONTRACT_VERSION = "perfrp-contract-0.5.0-skeleton"` |
| consumer | `portal/src/pages/AdvisorIntelligence/_shared/perfrp/contract.ts:18` | `PERFRP_CONTRACT_VERSION_BUILT_AGAINST = 'perfrp-contract-0.5.0-skeleton'` |

**Byte-identical. The versions MATCH**, so `assertContractVersion` (`contract.ts:206`) would not
refuse a payload. The handshake is **not** what empties the set — this rules out the branch the TO
named as "a registration/contract handshake gap this TO closes on the build side."

**2. The frontend constant — MEASURED, and it gates FAR LESS than assumed.**

`AdvisorBookView.tsx:71` is a hardcoded empty literal:
```ts
const PERFRP_AVAILABLE_LEAVES: ReadonlySet<PerfrpCardId> = new Set<PerfrpCardId>()
```
It is consumed at `:77`, `:554`, `:619` through `visibleCards()` (`perfrp/cards.ts:107–109`):
```ts
return PERFRP_CARDS.filter((c) => !c.requiresLeaf || availableLeaves.has(c.id))
```
**`requiresLeaf` census — denominator stated:** 6 matching lines in `cards.ts`, of which **1 is the
interface type declaration** (`:50 requiresLeaf: boolean`) and **5 are card definitions**. Of those
5 cards: **1 true** (`gain_loss`, `:77`), **4 false** (`activity_summary :59`, `performance :65`,
`allocation :71`, `transactions :83`).

> **So an empty `PERFRP_AVAILABLE_LEAVES` hides exactly ONE of five cards — `gain_loss`.** The other
> four render today regardless of leaf availability. `cards.ts:105–106` says so in its own words:
> *"Leaf-gated cards drop out until their producer exists; **every other ruled card renders
> regardless of value state**."*

**This corrects a premise carried in the pitch chain.** CTO 78619, CVO 78644 and this TO's
`decomp_context` each cite the empty Set as *the* thing blocking the DE lane. It blocks one card.

**3. The absent payload — MEASURED, and this is what actually empties the four visible cards.**

`AdvisorBookView.tsx:868` passes `payload={null}` — a hardcoded literal, the file's only `payload=`
site. Its own comment (`:858–859`) names the reason: *"payload is ABSENT: the b-6 leaf has not
emitted, so the tiles render their shells with no figures — the correct state before the producer
emits, not an error."* Four cards render **shells**; there is no fetch of a served artifact because
**no served artifact exists** (see (a)).

### NAMED, per the face's required dichotomy: **SERVING GATE** — this TO cannot close it

| link in the chain | state | why this TO cannot move it |
|---|---|---|
| leaf → local file | **available now** | `perfrp_emit_core` writes locally; this is what round 2 builds. |
| local file → platinum key | **BLOCKED** | `perfrp_emit_core` has **no S3 write path at all** (`:21–25`). Only `d_publisher_port` writes platinum (`:615`, `:617`) — and that is the **DISABLED-by-design** `advi-49f-publisher`, forbidden by the BUILD-ONLY CAP. |
| platinum key → render path | **BLOCKED** | No served key may be minted or moved under the cap; the serve word is P4I-3 / Andrew's arm-(a). |
| `PERFRP_AVAILABLE_LEAVES` → `gain_loss` visible | **BLOCKED, and NOT A DS ACT** | It is a **frontend constant in the portal tree** — a DE edit, out of this lane either way. |

**Every link that could carry a build-side leaf to the render path is closed by the build-only cap or
sits in the DE lane. There is no build gap here for this TO to close.**

⇒ **The issuer's pre-decided SERVING-GATE branch applies** (`700e89d50b`, on CVO 78734 P2-2 + CTO
78741): the build proceeds unchanged, and DE~D's re-seat trigger is the first **fixture-consumable**
QA emission of a b-series leaf, or the serve word, whichever is first. **Accordingly AC1–AC5 will
report each leaf's artifact path and pins in a fixture-loadable form** (the shape
`portal/.frontend-dev/testing/perfrp_books_l3.json` already demonstrates is consumable).

---

## (c) THE CAMPAIGN POSITION — the vintage this build proceeds against

Ledger: `org/tier2_senior/0.7.0_AE_CloudOps~L/deliverables/ADVI_49F.P14-VEHICLE_CAMPAIGN_LEDGER.jsonl`
(read-only; `0.7.0_AE_CloudOps~L`'s artifact — this seat never writes it).

**⛔ TWO PLANES, AND ONLY ONE IS PINNABLE.** The ledger is `M` (dirty) in the working tree: the
campaign is writing to it live. A pin must cite the **committed** vintage.

| | **PLANE A — COMMITTED (pinnable)** | **PLANE B — WORKING TREE (live, unpinnable)** |
|---|---|---|
| `campaign_ledger_commit` | **`7c6aa7cea757e6f64873b4239e73599c45659858`** | *(uncommitted — no hash exists)* |
| rows parsed | 65 (0 unparseable) | 87 (0 unparseable) |
| `ARTIFACT-COMPLETE` | 63 | 85 |
| `ARTIFACT-INCOMPLETE` | 1 | 1 |
| `HARD-STOP-REFUSAL` | 1 | 1 |
| **`dates_complete_of_534`** | **63 of 534** | **85 of 534** |
| oldest / newest complete date | 2024-07-08 / **2024-10-03** | 2024-07-08 / **2024-11-04** |
| newest `ledger_written_utc` | 2026-08-28T18:30:38Z | 2026-08-28T19:13:14Z |

Re-verified at two different repo HEADs (`5d9531729b`, then `b79db0b935`): **PLANE A held at 63 both
times**, and `git log -1` for the ledger path returned `7c6aa7cea7` at both — the committed blob did
not move while HEAD did. Positive control on the read: `git show HEAD:<ledger>` returned 102,442
bytes (a non-empty blob, so the path resolves and an empty result would have been visible as empty).

**Two dates carry more than one row** (working tree): `2024-07-08` (×2) and `2024-10-04` (×2). The
`2024-10-04` pair is the campaign's halt-class row — `ARTIFACT-INCOMPLETE` from the 2024-10-04 runner
**host death**, plus its concurred re-drive (`968090b2fc`, `7c6aa7cea7`). Counting distinct dates at
`ARTIFACT-COMPLETE` rather than rows is what keeps the re-drive from double-counting.

**THE VINTAGE THIS BUILD PROCEEDS AGAINST:** `campaign_ledger_commit = 7c6aa7cea7`,
`dates_complete_of_534 = 63`, newest complete date `2024-10-03`. Every AC1–AC5 acceptance row will
re-read and re-pin this at its own emission time — **this value is perishable by design and is a
snapshot, not a constant.**

**Rate — INFERRED, two points only, stated as such:** 81 complete at 19:06:02Z → 85 at 19:13:14Z
= 4 dates / 7.2 min. Naive extrapolation over the remaining 449 dates is ≈13h. **Two points are not
a rate**, the campaign has already taken one host-death halt, and this number is offered only as a
rough order of magnitude for AC6 sequencing — **not** as a completion estimate anyone should plan on.

---

## AC7 BASELINE (not the AC7 read — that is at round close)

Recorded now because it is free and makes the round-close negative read a **delta** rather than a
bare assertion: `platinum/advi/49financial/` holds **12 objects, 0 of them perfrp**, newest
`LastModified 2026-08-21T15:04:19Z`. At round close AC7 must show this prefix still carrying **zero
perfrp keys**, plus the live `advi-49f-publisher` Scheduler state and `OPAL_ADVI_PUBLISH_GRANT`
unset.

---

## STATE OF THE ACCEPTANCE ROWS

| id | state | note |
|---|---|---|
| `PRFR2DS-AC0` | **DISCHARGED by this census** | (a) 11/11 unemitted w/ 3 controlled instruments; (b) SERVING GATE, measured at the consumer; (c) campaign pinned on the committed plane. No code changed. |
| `PRFR2DS-AC1..AC5` | NOT STARTED | Unblocked. Begin at b-2 in the face's order. |
| `PRFR2DS-AC6` | **UNCOMPUTABLE pending the campaign** | 63 of 534 committed. Never N/A (Rule 24 iv). |
| `PRFR2DS-AC7` | NOT DUE | Round close. Baseline recorded above. |
| `PRFR2DS-AC8` | NOT STARTED | Proof instance at round close. |

## COMPILER TOOLS RUN IN THIS CENSUS

| tool | result |
|---|---|
| `comp-pipescript io d_publisher_port.py --pipeline advi` | rc=0. **OUT-OF-GRAPH** — the curated `advi` DAG does not carry this file; answered by AST derivation. 12 I/O call sites; WRITES `s3://opal-data-portal-v2/{?}` `:615` and `.../platinum/advi/49financial/_manifests/latest.json` `:617`; **6 UNRESOLVED** dynamic targets, which are NOT absent I/O. |
| `comp-find` (`PERFRP_AVAILABLE_LEAVES`, `PERFRP_CONTRACT_VERSION_BUILT_AGAINST`) | `--corpus raw --all`, no `head`. Both DEF lines located; the `.runtmp/portal-promote-*` copies are a promote scratch tree, not a second live definition. |
| `.tools/aws s3api list-objects-v2` / `get-object` | `s3api` (UTC, not `s3 ls` local time). Denominator printed (12), not a page. |
| `git log --all --diff-filter=A` | Spans every ref, so a since-deleted emission would still surface. |

**Not run, and why:** `comp-pipescript deployed` / `postdeps` / `comp-validate` are **before-run and
before-commit-of-code** gates. This commit changes **no `.py`** and runs **no gold script**, so they
have no subject yet. They bind from AC1 onward, where the first emission happens.

---

## SURPRISE-CHANNEL ITEMS (routed to `3.0.0_SA_CVO` cc `2.0.0_SA_COO`; no action taken)

1. **OBSERVATION / INERT** — the D2 brief's *"Activity/Allocation already ship"* is false on every
   plane measured. See (a).
2. **OBSERVATION / INERT** — the empty `PERFRP_AVAILABLE_LEAVES` gates **1 of 5** cards, not the card
   set; the pitch chain (78619 → 78644 → this face) reads it as the DE lane's whole block. The DE
   lane's own 7 UNCOMPUTABLE rows may therefore have a different cause than the one on record.
3. **OBSERVATION / INERT** — startup `audit-archive-invoker` rc=1: `org/to-pos-override-audit.log`
   uncovered by MANIFEST; baseline `2026-08-20T042433Z` 206.5h stale with an uncaptured tail.
   **Neither is the device-axis tamper-vocabulary class** the `org/XXX.md` A.2 note pre-clears (zero
   NON-APPEND-EDIT shrink rows), so that standing note does not cover them. Owner
   `0.7.0_AE_CloudOps`, gate `1.0.0_SA_CTO`.
