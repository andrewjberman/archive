# PHASE 0 — the `infra/` limb of the two-firm enumeration

**Author:** `0.7.0_AE_CloudOps` 2026-07-22 ~1537Z · **Phase 0 owner:** `0.4.0_DE_ClientPlatform`
**Why me:** DE's coverage line names **`infra/` dispatch + IAM as NOT COVERED**, and that is my domain.
**Authority:** carve-out 3 — *"read-only MDPF ANALYSIS continues, especially Phase 0 — enumerating is not
initiating, and it is the input the advisory needs."* **Read-only. Nothing changed, nothing applied.**

---

## COVERAGE — stated first, per R6/R10

| | |
|---|---|
| **COVERED** | the `infra/` tree, token-search on `{49financial, inflection, cottonwood}` via `comp-grep`, **plus a full read of the MDPF dispatch Stage-6 block** (`mdpf-daily-dispatch.sh:425-549`) |
| **NOT COVERED — and this is the important half** | **encodings that name NO firm** — a hardcoded arity, a count literal, a 2-element slice — **are INVISIBLE to a token search.** I caught `keys_staged: 7` only because I read the file, not because the search found it. **Everything outside the block I read is unenumerated for that class.** |
| **NOT COVERED (other limbs, not mine)** | publisher/promote path · `dim_mdpf_account_distribution.py` / `dim_mdpf_aum_{metrics,timeseries}.py` (they live in `data/`, not `infra/`) · FE per-firm path (`portal/`) · IAM (see below, partial) |

> **The token axis is the wrong axis for the sharpest member of this class.** A two-firm assumption written
> as `7` names no firm and survives every grep for a firm name. **Treat this limb as covering the NAMED
> encodings in `infra/` and only the block I actually read for the unnamed ones.**

---

## FINDING 1 — the completion marker's anti-omission guard is ITSELF firm-hardcoded

`infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:508-539`

`_audit()` (`:508-517`) was written **specifically** so a missing audit cannot read as clean:

> *"ABSENT IS NOT CLEAN -- if the file is missing the marker says the audit DID NOT RUN, it does not omit
> the field (an omitted field reads as 'fine')."*

**But the dict it feeds has hardcoded firm keys** (`:536-539`):
```python
"count_axis_source_audit": {
    "inflection":  _audit("inflection"),
    "49financial": _audit("49financial"),
}
```

**So for a third firm the field is not `audit_did_not_run` — the firm is ABSENT FROM THE DICT ENTIRELY.**
The guard delivers exactly the failure it was built to prevent, for any firm it does not name.

> **A guard that enumerates its subjects cannot protect a subject it does not enumerate.** The
> absence-is-not-clean property holds **per named firm**, never **per firm**. Cottonwood joins and the
> marker reports two verdicts for a three-firm cycle, with nothing anywhere saying a verdict is missing.

**This is the R6 principle** (*"the unreached are NOT clean"*) **defeated by a hardcoded key list** — same
shape as my own census finding, one layer down.

---

## FINDING 2 — `keys_staged` is a hardcoded literal, and the marker is what the co-sign reads

`:526` `"keys_staged": 7` · `:434-435` the comment deriving it: aggregate ×3 + account_distribution ×3 +
non_model ×1 = **7**. With Cottonwood the true count is **9** (aggregate ×4 + distribution ×4 + non_model ×1).

**Both halves have to move together, and nothing couples them:**
- loops extended, literal not → marker asserts **7** while **9** landed
- literal changed, loops not → marker asserts **9** while **7** landed

**This is not cosmetic. `gold/mdpf_revamp/meta/cycle-complete.json` is the artifact the parity streak and the
co-sign read.** A marker misreporting its own coverage is a **false completion record** — the same class as
the count-axis defect found *inside* the co-signed frozen-9 this morning.

**Recommendation (a change, therefore NOT made under the hold — DE/DS/CTO's call):** derive `keys_staged`
and `segments` from the same firm list the loops iterate, so the marker cannot disagree with what was staged.
**A count that is asserted rather than derived is a claim, not a measurement.**

---

## FINDING 3 — the staging loops are two-firm literals

`:459` and `:472` — `for firm in 49financial inflection global`.
Cottonwood's `aggregate_aua_timeseries` and `account_distribution` keys are **never staged**, and `:462`'s
`MISSING` guard fires only for firms already in the list. **A firm absent from the loop produces no error —
it produces nothing at all**, which the marker then reports as a clean 7-key cycle (Finding 2).

`:487` / `:495` — the audit legs are per-firm literals with the deliberate CTO-approved asymmetry
(`inflection || return 1` / `49financial || true`). **There is no Cottonwood leg.** *(The asymmetry itself is
correct and must not be collapsed — flagging only that the list is closed at two.)*

---

## FINDING 4 — an argparse whitelist that HARD-REJECTS a third firm

`infra/aws/ec2/smartx-exporter/smartx-workspace/scripts/compute_per_firm_account_distribution.py:362`
```python
ap.add_argument("--firm", choices=["49financial", "inflection", "all"], ...)
```
`--firm cottonwood` **exits 2 at argument parsing** — it cannot reach the code. Per its own docstring
(`:19`) this writes `json/mdpf/{firm}/account-distribution.json`, i.e. the **legacy served path** — the same
`json/mdpf/**` prefix Deliverable 2's deny protects.

**REACHABILITY NOT ESTABLISHED BY THIS LIMB.** I found it in source; I did **not** determine whether the
nightly invokes it or whether `dim_mdpf_account_distribution.py` has superseded it. **Two producers write
per-firm distribution and I have not established which one serves** — that question belongs with DE/DS and
is flagged, not answered. *A hardcoded choices-list in a producer nobody invokes is a different severity
from one on the serving path, and I have not distinguished them.*

---

## IAM — PARTIAL, and I am not claiming it clean

The token sweep surfaced **no** firm-enumerating IAM policy in `infra/`. **That is a weak result, not a pass:**
IAM two-firm encodings would appear as bucket/prefix ARNs (`opal-data-bd`, `opal-data-inf`, `opal-data-cot`),
**which name buckets, not firms** — so the firm-token axis cannot see them. **The IAM limb needs an
ARN-axis sweep and I have not run one.** Recorded as OPEN, not covered.

---

## WHAT THIS MEANS FOR THE DATE

Phase 0 is *"the only unbounded item ... nothing else is unbounded."* This limb closes the **named** `infra/`
dispatch encodings — **6 sites in 2 files** — and leaves two named gaps: the **unnamed-arity class**
(`keys_staged: 7` is one confirmed instance; the population is unmeasured) and the **IAM ARN axis**.

**The unnamed-arity class is the one that should worry the estimate**, because it is invisible to the search
everyone will naturally run, and Finding 2 shows one member of it sitting directly on the co-sign's evidence
artifact.
