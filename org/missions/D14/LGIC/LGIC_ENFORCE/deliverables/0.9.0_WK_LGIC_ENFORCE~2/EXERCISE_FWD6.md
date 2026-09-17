# LGIC_ENFORCE -- FWD-6 ON A PRACTICE COPY (EN-p-1)

**Cell:** `EN-p-1` (PRD candidate E10; DEC-8, *"A remediation is data"*) | **Order:** `LGIC_ENFORCE.TO-EN-p-1` |
**Worker:** `0.9.0_WK_LGIC_ENFORCE~2` | **Vintage:** slot branch `wk-lgic-enforce-1-2-p1` @39aae459ed (cut from `CLOUD`,
carrying EN-r-1 and EN-g-1). Scratch branch `prac-lgic-enforce-p1`, cut from the same commit. Never pushed, never merged.

## 1. The rule's result

The order's rule: take `CARRIER_CENSUS.md`'s json `carriers`, sorted by (path, line). The first whose `token`
`grade(token, "S3Key")` marks OUT-OF-PATTERN is the SURFACE.

- **12,953 carriers**, sorted by (path, line).
- Carriers 1-22 are not OUT-OF-PATTERN. **18 raise `RaiseDefect`** (a RAISE is a rule or registry defect, not a verdict of
  OUT-OF-PATTERN, so the rule passes over them) and **4 grade CONFORMANT**.
- **Carrier 23 is the SURFACE:** `.claude/skills/mdpf-refresh/mdpf_refresh.py`, line 292, token
  `platinum/mdpf/inflection/aggregate-aua-timeseries.json`, graded OUT-OF-PATTERN with canonical
  `mdpf/inflection/platinum/aggregate-aua-timeseries.json`. The file is tracked, and the string occurs in it once.
- The checker `check_en.py p1-surface` stops on carrier 1's `RaiseDefect` and prints FAIL-NOT-EVALUABLE, so it cannot
  confirm this result (row `LGIC_ENFORCE-W2-S7`).

## 2. The plant

One row, `PRAC_FWD6REM`, a fictitious remediation project owning `s3-prefix opal-data-portal-v2 platinum/mdpf/inflection/`.
The surface reads the object from `Bucket=PORTAL`, i.e. `opal-data-portal-v2`. It was committed on the scratch branch as
**`plant` = `6640c8153d`**, with every safe-commit stage clean.

**The row sits FIRST in the array, and that placement is the exercise's discriminator.** A live remediation, MDPF_CANON
(`s3-prefix opal-data-portal-v2 platinum/mdpf/`), already owns this key. So the touching diff is refused **before** any row
is planted, and the limb names the first matching project (row `LGIC_ENFORCE-W2-S8`). A REFUSE alone therefore cannot show
that the planted row was read. The name printed in the refusal can: MDPF_CANON before the plant, PRAC_FWD6REM after it.

The registry's validator refuses the planted row, because `PRAC_FWD6REM` is not a project in `DIRECTIVES.yaml`. The limb
loads the registry without validating and honours the row anyway (row `LGIC_ENFORCE-W2-S9`).

## 3. The three arms

Every arm ran `python .tools/naming-gate.py --enforce --diff <the git diff>` in the practice copy against the diff of one
uncommitted edit, and the edit was then discarded. After each arm, `git status --porcelain` on the surface read empty.

| arm | commit | edit to line 292 | gate | rc | project named |
|---|---|---|---|---|---|
| 0, control | 39aae459ed (pre-plant) | touch: trailing comment, string kept | `NAMING-GATE: REFUSE 1 graded` | 1 | MDPF_CANON |
| 1, touching | 6640c8153d (plant) | touch: trailing comment, string kept | `NAMING-GATE: REFUSE 1 graded` | 1 | **PRAC_FWD6REM** |
| 2, removing | 6640c8153d (plant) | remove: the literal replaced by `key("mdpf", "inflection", "platinum", "aggregate-aua-timeseries.json")` | `NAMING-GATE: PASS 0 graded` | 0 | none |

Arm 2 grades 0 strings because a `key()` call's arguments are a permitted context. It passes because the old-style string
has left the post-image. Arm 1, on the same line, is the positive control that the line is graded when the string stays.
The two edits were graded as diffs and never committed. Both diffs are verbatim in the json.

## 4. The practice copy

Removed with `git worktree remove` once it was clean. The branch `prac-lgic-enforce-p1` is left in place, holding `plant`.

## 5. The record

```json
{
  "scratch_branch": "prac-lgic-enforce-p1",
  "surface": ".claude/skills/mdpf-refresh/mdpf_refresh.py",
  "surface_line": 292,
  "surface_token": "platinum/mdpf/inflection/aggregate-aua-timeseries.json",
  "rule_result": {
    "carriers_sorted": 12953,
    "index_selected": 23,
    "before_it": {
      "RAISE": 18,
      "CONFORMANT": 4
    },
    "grade": [
      "OUT-OF-PATTERN",
      "mdpf/inflection/platinum/aggregate-aua-timeseries.json"
    ]
  },
  "planted_row": {
    "project": "PRAC_FWD6REM",
    "owner_directive": "D14",
    "ranking_row": "FICTITIOUS -- LGIC_ENFORCE EN-p-1 (FWD-6) practice row on scratch branch prac-lgic-enforce-p1 only, never merged; placed first so the commit limb names it",
    "surfaces": [
      {
        "kind": "s3-prefix",
        "bucket": "opal-data-portal-v2",
        "prefix": "platinum/mdpf/inflection/"
      }
    ],
    "register": "FICTITIOUS: no project.json, so .tools/naming-gate.py _live reads the row as live ('no register path')"
  },
  "planted_row_position": 0,
  "commits": {
    "plant": "6640c8153d4367520e8c1ea52f000d2f74f3d6fd",
    "base": "39aae459ed4e60dcaae479beb95cad12146240ae"
  },
  "outputs": {
    "refused": "NAMING REFUSE .claude/skills/mdpf-refresh/mdpf_refresh.py:292 platinum/mdpf/inflection/aggregate-aua-timeseries.json -> mdpf/inflection/platinum/aggregate-aua-timeseries.json\n  why: EXISTING and OUT-OF-PATTERN as S3Key in a surface remediations.json assigns to the live remediation PRAC_FWD6REM: REFUSE unless the diff removes it; hand-kept carrier of 'inflection' outside every permitted context: read it through lookup('inflection')\nNAMING-GATE: REFUSE 1 graded\n",
    "passed": "NAMING-GATE: PASS 0 graded\n",
    "preplant_control": "NAMING REFUSE .claude/skills/mdpf-refresh/mdpf_refresh.py:292 platinum/mdpf/inflection/aggregate-aua-timeseries.json -> mdpf/inflection/platinum/aggregate-aua-timeseries.json\n  why: EXISTING and OUT-OF-PATTERN as S3Key in a surface remediations.json assigns to the live remediation MDPF_CANON: REFUSE unless the diff removes it; hand-kept carrier of 'inflection' outside every permitted context: read it through lookup('inflection')\nNAMING-GATE: REFUSE 1 graded\n"
  },
  "diffs": {
    "touch": "diff --git a/.claude/skills/mdpf-refresh/mdpf_refresh.py b/.claude/skills/mdpf-refresh/mdpf_refresh.py\nindex 6244a1b83b..a48632655c 100644\n--- a/.claude/skills/mdpf-refresh/mdpf_refresh.py\n+++ b/.claude/skills/mdpf-refresh/mdpf_refresh.py\n@@ -289,7 +289,7 @@ def gold_publish(t1: str) -> int:\n     # inflection reconstructed-date transparency (EVR)\n     try:\n         o = _s3.get_object(Bucket=PORTAL,\n-                           Key=\"platinum/mdpf/inflection/aggregate-aua-timeseries.json\")\n+                           Key=\"platinum/mdpf/inflection/aggregate-aua-timeseries.json\")  # FWD-6 practice: touched, string kept\n         doc = json.loads(o[\"Body\"].read())\n         rec = ((doc.get(\"meta\") or {}).get(\"reconstructed\") or {}).get(\"dates\") or []\n         empty = [doc[\"dates\"][i] for i in range(len(doc.get(\"dates\", [])))\n",
    "remove": "diff --git a/.claude/skills/mdpf-refresh/mdpf_refresh.py b/.claude/skills/mdpf-refresh/mdpf_refresh.py\nindex 6244a1b83b..3fffdcc37a 100644\n--- a/.claude/skills/mdpf-refresh/mdpf_refresh.py\n+++ b/.claude/skills/mdpf-refresh/mdpf_refresh.py\n@@ -289,7 +289,7 @@ def gold_publish(t1: str) -> int:\n     # inflection reconstructed-date transparency (EVR)\n     try:\n         o = _s3.get_object(Bucket=PORTAL,\n-                           Key=\"platinum/mdpf/inflection/aggregate-aua-timeseries.json\")\n+                           Key=key(\"mdpf\", \"inflection\", \"platinum\", \"aggregate-aua-timeseries.json\"))\n         doc = json.loads(o[\"Body\"].read())\n         rec = ((doc.get(\"meta\") or {}).get(\"reconstructed\") or {}).get(\"dates\") or []\n         empty = [doc[\"dates\"][i] for i in range(len(doc.get(\"dates\", [])))\n"
  },
  "gate_rc": {
    "preplant_control": 1,
    "refused": 1,
    "passed": 0
  },
  "rows": [
    "LGIC_ENFORCE-W2-S7",
    "LGIC_ENFORCE-W2-S8",
    "LGIC_ENFORCE-W2-S9"
  ]
}
```
