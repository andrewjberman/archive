# DSGN_AMGTV1 round 3 -- the close walk (the COO's one real run)

**Seat:** 2.0.0_SA_COO~D (site Z). **Round:** 3 (decomposition v3, AV-r-1..5, all complete).
**Build walked:** port 5174, 1.0.0_SA_CTO~Z's walk worktree `/c/tmp/amgt-walk-5174` at 80a0df1f, which merges site-Z
portal DEV a93071b8 (every round-3 portal commit: 0102f46f r-2, 4a5ba59d r-4, cb25695b r-1, 060afb45 r-3, 852f6216 r-5).
**Instrument:** `/ui-walk` (walk.mjs), signed in as the dormant walker account, armed and disarmed per walk.

| walk | names | window | artifact (gitignored, site Z only) | verdict on the instrument |
|---|---|---|---|---|
| A | VLO US, INTU US, SAP GY | 11:11:19Z-11:15:39Z | `tmp/ui-walk/20260929T111119Z/` | VLO valid; INTU and SAP GY VOID -- after VLO the session was lost (two HTTP 500 on the INTU/SAP select, then the sign-in page on every later shot, shots 041-052). Disarm printed status=disabled + SSM ABSENT but no REFUSED line. |
| B | INTU US, SAP GY | 11:18:09Z-11:20:44Z | `tmp/ui-walk/20260929T111809Z/` | valid; 0 API issues, 0 guard aborts, console = the 2 login 401s only; disarm proven: "LOGIN WITH THE WALK PASSWORD AFTER DISARM: HTTP 401 -> REFUSED". |

The CVO reads VLO from walk A (shots 010-040) and INTU + SAP GY from walk B (shots 010-072). Screenshots never leave site Z.

## Static checks on the walked portal bytes (a93071b8, repo root, 2026-09-29 ~11:05Z)

```
NAMED MACHINE STRINGS: 0 hit(s) over 4 surfaces          (base 670f29e4: 14)
POSTURE PANEL HEADER: estate band headers=0, white header=yes
MODEL PANEL HEADER: estate band headers=0, white header=yes
THESIS PANEL HEADER: estate band headers=0, white header=yes
TEAM CASE GAP (window): 3 of 3 arms                      (base 1 of 3)
TEAM CASE GAP (model): 3 of 3 arms                       (base 1 of 3)
EXEC ABSENCE IN WORDS: 3 of 3 arms                       (base 2 of 3)
NO UNSERVED DOLLAR: 3 of 3 arms                          (base 2 of 3)
ALL BOUND: 10 of 10 harnesses green                      (every page harness at its floor)
FWD-30 HARNESS READS THE REDESIGNED PAGE: YES            (AMGT_RESAPP vv-5.AC1; base NO)
PARITY CONTROL: a deleted export absence is caught: YES
tsc -b --noEmit: 0 errors
```

## The inverted non-prose census (census.cjs, the CVO's instrument; not a verdict)

```
header: 0 non-prose token(s) of 183
lead: 0 non-prose token(s) of 33
thesis: 0 non-prose token(s) of 174
model: 5 non-prose token(s) of 945 [["P/E",2],["P/B",1],["y/y",1],["Revenue/Sh",1]]
posture: 1 non-prose token(s) of 510 [["2026-2027",1]]
exec: 0 non-prose token(s) of 54
NON-PROSE CENSUS: 6 token(s) over 6 surface(s)
```
Base 670f29e4: 40 tokens. The six left are finance terms of art on the Model sheet and one fiscal-year range inside a
served quote. The census's word class admits an upper-case status word, so it cannot see "REFUSED" or "ABSENT" (below).

## What the walk shows, per judgment criterion (observations for L9; the COO grades none of them)

- **AV-r-1 AC4 (FWD-11, FWD-2, FWD-10).** VLO header: "identity as of 2026-09-25" (no crosswalk/v1), social line "Social: no
  source measured" (no "(S13)"), axis footnote "price: no ranking has been published for this date yet", no Bloomberg
  session badge. Lead panel: "Source: ranked 2026-09-28 from Bloomberg prices (32 names) (requested 2026-09-29)" with a
  collapsed "Details". Posture: white panel header; comparable "Williams Companies, Inc. -- its ticker is not yet identified by
  the research team"; "Snapshot: drafted by a machine on 2026-09-16". Walk shot 035.
- **AV-r-2 AC4 (FWD-6).** On every walked name the Recommendation card and the Model tab read "The research team's Base case
  is not served on this page yet". That sentence is TRUE on today's API: AMGT_RESAPP rolled `vv-4` back (the CVO's own
  ADJUDICATION_v57, @556a5a37f8), so `team_cases` is not served. The INTU arm ("leads with the team's own case") therefore
  cannot be seen on a walk until RESAPP round 48 cell 1 re-lands vv-4. The served-case table and the ABSENT-with-reason arm
  are graded only by team.cjs on the captured fixtures (3 of 3).
- **AV-r-3 AC3 (FWD-30 instrument).** Graded by vv-5.AC1 YES and the parity control YES above. Worker row
  DSGN_AMGTV1-Z-W11-S1: AC1's fixture (1299_HK_Equity) carries no thesis cites, so CITES 0=0 does not exercise the window
  read; the worker exercised it on the tabs fixtures (43/28/30/33/36 cites read).
- **AV-r-4 AC3 (FWD-7).** INTU Exec Management: "No officer list is in this name's pack yet: the company's 10-K had no
  officer section this page could read, and no other source was used." / "The research team fills this once an officer list
  is sourced." The detail sits behind "Read detail" (walk B shot 020 shows it opened by the walker).
- **AV-r-5 AC4 (FWD-11, FWD-4).** SAP GY: Price EUR 184.18, Enterprise value EUR 226B, the machine Base case "159.61 EUR"
  as served; Model panel header white (walk B shot 062). No served chart was on any walked name, so the chart-caption item
  is not visible on this walk.

## Seen on the walk, not in round 3's rectangle (for the round-3 analysis)

1. **Exec Management panel header is still a dark band** (INTU, walk B shot 020): the second full-width band beside the
   identity header. The walker's design:bands check reads 2 bands on the load view as well.
2. **"REFUSED -- The number is in the pack, but this page cannot show it yet because its unit convention is not built."**
   repeats 20 times on SAP GY's Model sheet (walk B shot 062); "ABSENT --" leads the y/y, 2026E and Upside/Downside lines.
   A status word on the face; census.cjs cannot see it (upper-case word class).
3. **Posture evidence coverage says the comparable's missing sources twice** -- once as bullets, once as a run-on sentence
   (VLO, walk A shot 035).
4. **raw-code in SAP GY Posture cites:** "figure OPER_MARGIN FY2025: 26.1332 PERCENT", "figure NET_DEBT: -2213 MILLIONS"
   (walk B, inside a cite `<details>` the walker opened; behind an affordance, but the cite text itself is machine form).
5. **format:money on INTU:** "USD 1,234" and "$1,234" on one page -- the "$" is inside drafted prose (Thesis/Posture
   sentences), which AV-r-5 does not rewrite by contract.
6. The walker's own session loss after the first name (walk A) is an instrument defect, recorded as a surprise row.
