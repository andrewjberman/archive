# T2-3 / dim 436 -- THE DENOMINATOR COO ASKED FOR, ON THE CURRENT VINTAGE

**Seat:** `0.4.0_DS_ClientPlatform~B` | **Date:** 2026-09-01 | **TO:** `ADVI_BDPARITY.T2-DIMS`
**Answers:** `2.0.0_SA_COO` msg 20260819T224419Z -- *"'dim 436 absent' needs its DENOMINATOR before
I escalate it. Absent from WHAT, searched HOW, against what denominator? Run it with a POSITIVE
CONTROL."*

Every line below is tagged **MEASURED-BY-ME** (this seat, this session, at the cited artifact) or
**RELAYED** (another seat's claim, carried with its owner). Nothing is inferred silently.

---

## 0. THE HEADLINE, AND IT IS NOT ONE OF THE THREE OPTIONS THAT WERE OFFERED

COO's question offered three: absent from the export header / absent only from our local
materialization / absent under a different name. **The answer is the first one, and the escalation
that follows from it is NOT the one the question was shaped for.**

> **The daily allocation export does not carry a primary-group key, at the CURRENT vintage, and
> that is MEASURED on the vendor's own bytes with a live positive control.**
> **Whether BD *has* dim 436 at all is a SEPARATE claim, it is RELAYED from `4.0.0_SA_CRO~A`, and
> the artifact that seat staged does NOT carry the evidence for it.**

So the sentence *"the ruled basis has no source"* is **too strong to forward**. The survivable
sentence is: *the ruled basis has no source IN THE FEED WE PULL DAILY; whether it has one at the
vendor is unverified in-estate and costs one egress act to settle.* Those route differently -- the
first is a sovereign alarm, the second is a scoped request for one pull.

---

## 1. ABSENT FROM WHAT -- three planes, three reads, MEASURED-BY-ME

| # | Plane | Artifact read | Denominator | `primary` | POSITIVE CONTROL `portfolio` |
|---|---|---|---|---|---|
| 1 | **Vendor's delivered bytes**, current | `s3://opal-data-assets/blackdiamond/49f/bronze/allocation_390224/**2026-08-31**/data.xlsx` (pulled 2026-09-01T06:30:40Z) | **92 header columns** | **0 of 92** | **8 of 92** |
| 2 | **Our silver parse**, as built for T2 | `s3://opal-data-assets/blackdiamond/49f/silver/fact_bd_allocation/date=2026-08-18/data.parquet` | **92 vendor + 4 provenance = 96** | **0 of 92** | **8 of 92** |
| 3 | **The pull's own sidecar**, current | `.../allocation_390224/2026-08-31/_meta/pull_complete.json` | `column_extent: 92` | `level_selected_census -> "Portfolio Group": 2` | `template_id 390224`, `run_id 524910` |

**The positive control fires on both data planes (8 of 92), so the zero discriminates.** The two
reads are NOT one substrate: plane 1 is the vendor's xlsx at one vintage, plane 2 our parquet parse
at a different vintage and a different format.

**AND I READ ALL 92 HEADER NAMES UNSCOPED** (both planes), because a token census cannot see a flag
under a name I did not guess. There is no primacy key under any spelling. The only account-to-advisor
columns are the **role-split set** -- `Architect`, `Consultant`, `Implementor`, `Local Ops`,
`Additional Advisor`, `49 House Split %` -- which is the **role-attribution basis**, i.e. explicitly
the OTHER basis, the one Andrew retained as an attribute view. It is not a group partition and cannot
be made into one.

---

## 2. COO's THREE OPTIONS, ANSWERED

| Option as put | Verdict | Evidence |
|---|---|---|
| (a) absent from the 92-column export header | **YES** | row 1 above -- the vendor's own xlsx, today's pull, 0 of 92, PC 8 of 92 |
| (b) absent only from our local materialization | **NO -- refuted** | I read the **vendor's xlsx** (plane 1), one plane ABOVE silver. The absence is upstream of anything we build. *(Corroborating and RELAYED: `0.4.0_DS_ClientPlatform` value-tied silver to bronze at 30,577 rows / 0 mismatches with a +1-shift negative control.)* |
| (c) absent under a different name | **NO candidate exists** | the unscoped read of all 92 names, both planes |

**(d) THE OPTION NOT ON THE LIST, AND IT IS THE ONE THAT MATTERS:** the 92 columns are **a persisted
template's SELECTION**, not the vendor's catalogue. `template_id 390224` selects 92 columns with
`"Portfolio Group": 2` at that level. **"Not selected" and "does not exist" are different facts with
different owners and different costs, and only the first is measured here.**

---

## 3. THE CLAIM I COULD NOT CORROBORATE -- and I am flagging it rather than passing it on

**RELAYED**, `4.0.0_SA_CRO~A`, `BD_PORTFOLIO_GROUP_KEYING_SCAN_20260819.md` s.2:
> *"The disambiguator exists in the catalog: `Primary Portfolio Group` (dim id 436, Portfolio level)"*

**I tried to re-derive this at source and COULD NOT.** That seat staged its catalog sweep to
`s3://opal-data-bd/code/bronze/endpoint_catalog/` (2 objects, 13,940 + 3,567 bytes). **MEASURED-BY-ME:
those files carry only per-querytype COUNTS and MEASURE names** -- qt6 reads
`{"queryTypeId": 6, "n_levels": 7, "n_dims": 150, "n_measures": 16, "measure_names": [...]}`.
**The 150 dimension names and ids are NOT in the staged artifact.**

**My positive control caught this and it is why I am not reporting a second absence:** I searched the
staged catalog for `436`, for `primary`, **and for `1140`** -- the Portfolio Group dim id that seat's
own probe used, which MUST be there if dim ids are there at all. **All three returned zero, including
the control.** A dead arm and a true absence read identically; the control says this arm is dead. So
**that read produced NO evidence in either direction**, and I am recording it as such rather than as
a finding.

>> **CONSEQUENCE: dim 436's existence is a single-carrier claim.** It is almost certainly right --
that seat ran a live catalog pass and quoted an id and a level -- but **the estate cannot check it**,
and it is currently load-bearing for a basis Andrew has RULED. Re-deriving it costs one read-scoped
catalog call under CRO~A's standing grant, and that seat is the owner. <<

---

## 4. WHAT WOULD ACTUALLY CLOSE T2-3 -- named precisely, so the word can be a scoped one

**One vendor-side act:** amend persisted template **390224** to select **dim 436 `Primary Portfolio
Group`** at the **Portfolio** level (its current Portfolio-Group-level selection is 2 dims), then
re-pull. That is **VENDOR EGRESS -> Andrew's explicit per-use word.** Not this seat's, and not taken.

**The build half is now DONE AND OUT OF THE WAY -- that is this session's deliverable.** The producer
`data/assets/scripts/gold/runners_49f/bd49f_dim_portfolio_group.py` now **consumes dim 436 when it
appears** (`attach_is_primary` / `assert_primary_partitions_accounts`). **So the blocker has reduced
from "build + egress" to "egress".** On the first pull that carries the column, T2-3's partition half
closes on a **re-run with no code change**.

**IT IS EXERCISED, NOT DECLARED** (a declared-but-unrun falsifier is a promise, not a control):

| Arm | Result |
|---|---|
| **POSITIVE** -- clean synthetic partition | 6,155 accounts, one primary each; primary-only total **$1,550,733,057.94** vs distinct-account universe **$1,550,733,057.94**, **residual $0.00** |
| **FALSIFIER A** -- one account given TWO primaries | **FIRED**, named the account, refused |
| **FALSIFIER B** -- one account given NONE | **FIRED**, named the account, refused |
| **INERTNESS** -- pre-edit file vs post-edit, same input | both tables **FRAME-EQUAL**; manifest differs only by 3 ADDED informational fields |

⛔ **WHAT THE EXERCISE DOES NOT PROVE, stated because it is the half that would travel wrongly:** the
column does not exist, so I exercised against **one I wrote myself**. This validates **the consumer**.
It says **nothing** about the vendor's real semantics -- specifically whether BD's `Primary Portfolio
Group` asserts primacy **per ACCOUNT** (what the consumer assumes) or **per PORTFOLIO**. That must be
read off the first real pull **before any partitioned figure is quoted**, and the arm's assertion will
refuse loudly if it is the latter rather than silently producing a wrong partition.

---

## 5. TWO RECORD CORRECTIONS I OWE, BOTH AGAINST MY OWN LANE'S DELIVERED ARTIFACT

**(i) `declared_exclusions[1]` in `ADVI_BDPARITY.T2-DIMS_PROOF_OF_SPEC.json` IS STALE.** It reads
*"THE S3 GOLD MINT of both tables -- Withheld deliberately."* **MEASURED-BY-ME against live S3 today:
both tables are MINTED** --
`gold/advi/dimensions/dim_portfolio_group/date=2026-08-18/data.parquet` (10,411 B, etag
`b26d6cce17f530ade96abb86e8ccba92`) and `bridge_group_account/...` (197,188 B, etag
`d937238efba43e2d97d102e6bf4c2a7e`), both `2026-08-19T22:50:1xZ`. The withhold was discharged three
minutes after `0.4.0_DS_ClientPlatform` minted the silver upstream at 22:46:03Z. **T2-1's PASS row is
correct and the exclusion beside it contradicts it** -- the same file asserts both. Corrected in the
instance this session.

**(ii) A thing I checked that turned out NOT to be a defect, recorded so nobody re-chases it.** Both
tables' `manifest.json` carry an **identical ETag** (`4573a26d...`), which is the signature of one
manifest written to two table paths. **It is deliberate:** the manifest is a RUN manifest with a
`tables` key carrying each table's own grain, rows and measures. Verified by sha256 on both downloaded
objects (identical) and by reading the content. **No defect. Not chased further.**

---

## 6. OBSERVATION, SURFACED NOT CHASED (build-only fence, correctly)

The allocation export lands **DAILY** (66 objects; partitions through **2026-08-31**, pulled today).
The T2 gold tables exist at **date=2026-08-18 ONLY**. That is **correct under the BUILD-ONLY fence** --
T2-4 asserts 0 references in `chain_49f_entrypoint.py:_stage_list` and the WP-2 absorption puts
scheduling under "P2's floor ... NO new trigger machinery." **So the tables are stale-by-design, not
stale-by-defect.** Recording it because "frozen at 08-18" and "broken" look identical from outside,
and the day the serve gate opens, this is the first thing that must move. **No act taken.**

---

## 7. WHAT THIS SEAT DID NOT DO

- **No vendor call.** No template amendment, no re-pull, no BD egress of any kind.
- **No serving.** Gold only; the P4-class CTO gate is untouched and is stamped in both manifests.
- **No re-mint** of the 08-18 gold. The change is inert on the absent-column path (proved above), so
  re-minting would move a live artifact for three informational manifest fields and zero data delta.
- **No heuristic `is_primary`.** The TO forbids it; the arm reads the vendor or reports ABSENT.

---

## 8. STATUS

**T2-3 remains FAIL, and it is still the right record.** The structural half was already delivered and
verified; the partition half is blocked on one egress act that is Andrew's word. **What changed today:
the absence is re-measured at the current vintage on the vendor's own bytes with a live positive
control and an unscoped name read; the escalation is correctly scoped; and the build half is finished
and exercised, so the criterion closes on a re-run the moment the column arrives.**

T2-DIMS stands at **4 of 5**. T1-ORACLE stands at **4 of 4**.
