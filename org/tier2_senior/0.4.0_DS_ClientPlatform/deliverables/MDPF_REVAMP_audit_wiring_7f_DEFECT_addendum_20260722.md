# ADDENDUM — THE AUDIT WIRING I PREPARED CARRIES A §7f DEFECT INTO THE MARKER THE CO-SIGN READS

**Author:** `0.4.0_DS_ClientPlatform` · 2026-07-22 ~1635Z · **written UNDER THE HOLD — analysis + record only, NO code change**
**Amends:** `MDPF_REVAMP_dispatch_audit_wiring_for_AE_20260722.diff` (the diff prepared for `0.7.0_AE_CloudOps`)
**Binds:** **R1** — "the count-axis audit wiring lands before the SECOND post-flip cycle." **If R1 fires as prepared, it lands this defect.**
**Trigger:** COO 163007Z flagged doctrine **§7f** (`@f9f6a4c72`) as touching my area. I verified in source rather than accept the characterization. **It does touch my area — and not in the place I was told.**

---

## 1. WHAT I WAS TOLD, AND WHAT IS ACTUALLY TRUE

I was told `count_axis_source_audit`'s hardcoded keys and `keys_staged: 7` were two of §7f's three named instances, "both in your area." **Checked both. The report is half right, and the half that is wrong matters less than the half nobody named.**

| claim | verdict on source |
|---|---|
| `keys_staged: 7` is mine | **NO.** It lives at `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:526` (infra, `0.7.0`). It appears in my diff **only as an unmodified context line.** I did not author it and my diff does not change it. |
| the audit's firm keys are hardcoded | **PARTLY — and the cure is already in the SCRIPT.** `mdpf_revamp_count_source_audit.py:102-109` `unaudited_firms()` lists the live staging prefix and returns `present - AUDITED_FIRMS - DERIVED_SEGMENTS`. That is **a set-difference against a denominator derived from outside the instrument's configuration** — literally §7f.2's prescribed remedy, landed `@6785ce65a` *before* the doctrine was written. |
| **THE ONE NOBODY NAMED** | **THE WIRING DOES NOT CARRY THE CURE INTO THE MARKER.** |

## 2. THE ACTUAL DEFECT

My prepared diff adds this to the cycle-complete marker:

```python
"count_axis_source_audit": {
    "inflection":   _audit("inflection"),
    "49financial":  _audit("49financial"),
},
```

**A hardcoded two-key dict. `unaudited_firms()` is never called here.** So:

- The **script** can detect a landed-but-unaudited firm.
- The **marker** — *the artifact the co-sign reads* — cannot. It enumerates two literals.
- When Cottonwood lands, the marker carries an audit block naming `inflection` and `49financial`. **Cottonwood is absent — NOT EVEN `"did not run"`.** That is §7f's first table row, word for word, in the evidence limb of a co-sign.

**The cure existing in the script does not help, because nothing downstream reads the script — they read the marker.** A remedy that does not reach the artifact the decision is made from is not a remedy.

## 3. MY OWN CONTROLS HAVE THE SAME BLIND SPOT — THIS IS THE PART THAT INDICTS ME

The diff ships four verification steps. **Control 4 is "ABSENT-IS-NOT-CLEAN": delete one `audit_*.json` and confirm the marker records `audit_did_not_run`.** I was pleased with that one.

**It only fires for a MAPPED firm.** Deleting inflection's JSON tests a key that is already in the dict. **There is no control that introduces an UNMAPPED firm and asserts the marker names it.** Every one of my four controls operates *inside* the two-firm denominator — so all four pass on a three-firm cycle with Cottonwood entirely missing.

> **§7f: *"Care operates inside the denominator; the defect is the denominator."* I wrote a careful absence-detector that detects only the absences I had already enumerated. A control chosen from inside the denominator measures the author, not the instrument.**

## 4. THE FIX — NOT MADE (HELD). FOR WHOEVER LANDS R1.

1. **Marker block derives its keys from the world, not the literal.** Iterate the firms `unaudited_firms()` derives from the live staging prefix, union the audited set — so an unmapped firm appears in the marker **as a finding**, not as a silence.
2. **The marker carries `unaudited_firms` explicitly**, as a first-class field. Non-empty = the cycle is **NOT clean**, regardless of every mapped leg being green.
3. **ADD CONTROL 5 — the one that measures the instrument instead of the author:** stage a synthetic third firm prefix under `gold/mdpf_revamp/`, run the stage, **assert the marker NAMES it.** If the marker still reads green and 2-firm, the wiring is self-certifying and must not land. *This is the control whose absence is the finding above.*
4. **Residual, stated plainly and NOT closed by any of the above:** `unaudited_firms()` derives `present` from the **S3 staging prefix** — outside the instrument's *config*, but still **downstream of the very producer being audited.** A firm that should exist and **never lands at all** has no prefix, so the set-difference is empty and the audit reads clean. **Catching "landed but unaudited" is not catching "never landed."** Closing that needs a **firm REGISTRY** as the denominator (§7f.2: *"the denominator is the SUBJECT REGISTRY"*). **This is the same disease as R13's publisher** (`PUBLISH_MAP` hardcoded 9 → `9/9, all_present=True` with Cottonwood never served) — one registry would close both.

## 5. WHY THIS IS BANKED RATHER THAN FIXED

I am **HELD** (Andrew ~1408Z, CTO 151655Z, re-affirmed 163007Z: a priority statement does not authorize execution ahead of the 1552Z gate). **No code changed. No rebuild. Staged set remains a CHECKPOINT, co-sign 0 of 3.**

**This is banked precisely because R1 is a re-sequencing trigger.** The wiring is prepared, queued behind `0.7.0`'s WS-5 apply, and will land when the hold lifts — **carrying this defect into the co-sign's evidence unless whoever lands it reads this first.** A defect known only in a thread, attached to a ruling that fires later, is the exact failure the R1-R12 sweep was written to stop. It has a carrier now.

-- `0.4.0_DS_ClientPlatform`
