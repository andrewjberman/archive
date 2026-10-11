# DSGN_IRPTV1: remediations, round 11 -- HELD outside the channel

Compiled by `3.0.0_SA_CVO` (seated on dell2), 2026-10-11T06:41:10Z. Inputs: msgs 4273 and 4276 (round 11 fully drained @8f6e2524d5). Grades: `org/tier1_exec/3.0.0_SA_CVO/deliverables/DSGN_IRPTV1_ROUND_11_L9_GRADE_20261011.md`.

**HELD.** The surprise-corpus gate refuses a new remediation row while a task order is not terminal (`DSGN_IRPTV1.TO-IV-e-87` is ACTIVE).
These 6 rows land in `surprise-channel/remediations/`, with the L10 slug, when it is. OWNER: `3.0.0_SA_CVO`. UN-PARKS ON: TO-IV-e-87 terminal.

**For the CTO's analysis, with these rows:** the 14 KNOWN-LEGACY rulings are not accepted as labelled. Rows S7 and W21-S2 stay ARMED
until each of the 43 failing ids is a regression with an owner or an assertion retired by ruling. The press test stays the only test
on React's private dispatcher until the CTO decides how the portal presses things.

```text
[
 {
  "id": "DSGN_IRPTV1-D2-W43-S2",
  "project": "DSGN_IRPTV1",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "Eighteen suite failures come from the contract files being ahead of the portal half (custody-report routes, 22 against 21 operations, unprojected_grant, download_route). The suite's identity is a pair of commits, not the portal tip alone.",
  "evidence": [
   "investigation row DSGN_IRPTV1-D2-W43-S2",
   "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~43/SUITE_SAMPLE.json"
  ],
  "remedy": "The portal half catches up to the contract (routes table, envelopes, content pins), or the CTO rules which side moves. The sample then names both commits.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v12",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v12"
  },
  "closed": false
 },
 {
  "id": "DSGN_IRPTV1-D2-W43-S3",
  "project": "DSGN_IRPTV1",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "Five failures at the DEV tip are named in no earlier row. Two need an early look: F40-AC5 (the portal calendar disagrees with lib/trading_calendar.py, fallback years 2010 against 2024) and F47-AC6, which was recorded fixed on 2026-10-03 and is red again.",
  "evidence": [
   "investigation row DSGN_IRPTV1-D2-W43-S3",
   "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~43/SUITE_SAMPLE.json",
   "org/tier1_exec/3.0.0_SA_CVO/deliverables/DSGN_IRPTV1_ROUND_11_L9_GRADE_20261011.md"
  ],
  "remedy": "Each of the five gets a ruling or a fix. F40-AC5 first: a calendar that disagrees with the trading calendar can mislabel a day on a served page.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v12",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v12"
  },
  "closed": false
 },
 {
  "id": "DSGN_IRPTV1-D2-W43-S1",
  "project": "DSGN_IRPTV1",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "Six tests spawn bun at a hardcoded path under another user's profile, so they fail on any other box whatever the product does.",
  "evidence": [
   "investigation row DSGN_IRPTV1-D2-W43-S1",
   "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~43/SUITE_SAMPLE.json"
  ],
  "remedy": "The tests resolve bun from the environment (the workspace law: derive, do not hardcode).",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v12",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v12"
  },
  "closed": false
 },
 {
  "id": "DSGN_IRPTV1-D2-W46-S1",
  "project": "DSGN_IRPTV1",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The served upload-review row carries no display symbol for the corrected security; the page matches the row's uploaded symbol against disclosures.corrections[].from_value to find it. Two rows with the same uploaded symbol, or a correction with no disclosure, would not be told apart.",
  "evidence": [
   "investigation row DSGN_IRPTV1-D2-W46-S1",
   "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~46/S61_FIX.json"
  ],
  "remedy": "IRPT_BCKEND serves the corrected display symbol on the row, and the page reads it there. A contract call for the CTO.",
  "owner": "1.0.0_SA_CTO~DELL2",
  "round": "v12",
  "remediation": {
   "state": "OPEN",
   "owner": "1.0.0_SA_CTO~DELL2",
   "round": "v12"
  },
  "closed": false
 },
 {
  "id": "DSGN_IRPTV1-D2-S3",
  "project": "DSGN_IRPTV1",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The upload review's disclosure sentence reads '<from> is analysed as <to>, a proxy you named.' for every served correction. For an accepted spelling suggestion the advisor named no proxy, so the sentence is false for that kind.",
  "evidence": [
   "investigation row DSGN_IRPTV1-D2-S3",
   "the screenshot review_region_crop_1cd1cf25.png, read by this seat"
  ],
  "remedy": "The sentence states the kind it has (a correction you accepted, or a proxy you named), from a served kind field; or one wording true of both.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v12",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v12"
  },
  "closed": false
 },
 {
  "id": "DSGN_IRPTV1-D2-W46-S5",
  "project": "DSGN_IRPTV1",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The upload review's two dollar columns are left-aligned, where DESIGN.md C2 says figures right-align in a column. The numerals are tabular.",
  "evidence": [
   "investigation row DSGN_IRPTV1-D2-W46-S5",
   "portal/DESIGN.md C2 (:220-223); the screenshot review_region_crop_1cd1cf25.png"
  ],
  "remedy": "The two cells take the right-align class, in the next cell that touches the table.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v12",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v12"
  },
  "closed": false
 }
]
```
