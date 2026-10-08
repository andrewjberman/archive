# DSGN_AMGTV1 -- ROUND 52 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-08 ~12:5xZ)

**Round:** one direct act, `AV-zzd-1`, on CTO msg 31721 (the ruling on round 51's F1; candidate bfba701f returned for the wording).
Decomposition v52. No task order.
**Portal candidate, re-offered:** `dbeb6764` in `C:/tmp/wk-dsgn-amgtv1-113/portal` = DEV d1b21c97 + round 51 (`bfba701f`) + two
commits by this seat (`655994d2`, `dbeb6764`). LOCAL; not pushed. Against DEV: 8 product files, no script file. Against bfba701f:
two files (`reasonWords.ts`, `tabs/ThesisTab.tsx`), +9 -4.

## 1. WHAT WAS READ, BY THIS SEAT, ON dbeb6764

| read | result |
|---|---|
| `round52/checks/r52/r52.cjs` | 3 of 3 arms (2 of 3 at the base and at 655994d2) |
| `round51/checks/r51a/r51a.cjs` | 4 of 4 arms |
| `round29/checks/battery29.sh`, no skip | ALL PASS (0 skipped); 14 of 14 harnesses; tsc and eslint rc 0 |
| `round51/walk/walk51.mjs`, served on localhost:5174 against the live function, BA US and BP/ LN | 8 of 8 reads PASS, 0 ERROR (`round51/walk/read-20261008T123449Z/`) |

## 2. THE FIRST RULE WAS WRONG (CTO msg 31737)

`655994d2` turned "no class A report" into "the research team's pack is not on file". The CTO asked what a served "no class A
report is on file for this name" would then read. Run through the rule it read "the research team's pack is not on file is on file
for this name". Two more served shapes also garbled: "the most recent class A report ..." read "the most recent the research
team's pack ...", and "no class-A or class-B report was picked" read "the research team's pack is not on file or earnings update
was picked". `dbeb6764` gives each shape its own form. The shapes come from `lib/research/corpus/continuation.py` and `dossier.py`.
This seat cited that message as 31738 in one sent message and in the portal commit `dbeb6764`; the id is 31737.

## 3. THE PRINT THE CTO ASKED FOR

**Through the rule, six served shapes** (`r52.cjs` prints them on every run):

| served | drawn |
|---|---|
| no class A report is on file for this name | none of the research team's packs is on file for this name |
| the most recent class A report carries no INVESTMENT THESIS block | the research team's most recent pack carries no investment thesis block |
| the most recent class A report is not a docx or pdf extraction this cell can read | the research team's most recent pack is not a docx or pdf extraction this cell can read |
| every pillar lead in the most recent class A report's INVESTMENT THESIS block is empty | every pillar lead in the research team's most recent pack's investment thesis block is empty |
| no class-A or class-B report was picked, so no file was read | neither the research team's pack nor an earnings update was picked, so no file was read |
| no management section in class A heading only or class B missing | no management section in the research team's pack heading only or earnings update missing |

**On the live page, every drawn line naming the team's pack, whole:**

- BA US, above the Thesis tab: "The research team's thesis pillars: the research team's pack is not on file for this security."
- BA US, Exec Management: "The research team on management: no management section, because neither the research team's pack nor
  an earnings update is on file for this name."
- BP/ LN, Model: "SOURCE: THE RESEARCH TEAM'S PACK, BP PLC RESEARCH PACK 2026 04 03_V1" (three times, one per case).

BA: 2 distinct lines. BP/ LN: 1 distinct line. Lines using the withdrawn phrase on either name: 0. No line doubles a verb.

## 4. WHAT STILL READS "RESEARCH PACK"

- The built pack's row above the tabs: "the research pack built for this name" (served; AMGT_RESAPP round 79 cc-6 renames it).
- The team's own file name, printed as the source on BP/ LN ("BP plc Research Pack 2026 04 03_v1").
- `postureCites.ts` still words the built posture pack as "the research pack" in four sentences. It was left alone in round 51
  on the reading that it is the built pack; after the ruling the built thing "loses the word", and those four are page words.
  **Not changed in this cell; named for the CTO's list.** Neither walked name drew one on its Posture tab.

## 5. STATE

Walker account read disarmed (12:40:36Z); dev server stopped; port 5174 read at 0 listeners; one line sent to the CTO.
Open: the CTO's approval on the print, then ONE DEV push on Andrew's word. Unchanged at Andrew: the PROD promote word; his own
signed-in walk on PROD (FWD-1).
