# DSGN_AMGTV1 -- ROUND 32 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-03 ~18:0xZ) -- ONE DIRECT ACT: THE LEAD PANEL'S WORDS AT EVERY WINDOW

**Input:** decomposition v32 and the issuance are @02ca233d65, over PRD v0.13 @e398ee2294 (ADMITTED). The base is portal 76a15c1b,
which the CTO APPROVED (msg 28898, @f722662a3f).

## 1. THE ORDER (1 of 1 terminal, drained)

| order | cell | worker | portal | AC1 / AC2 | outer drain |
|---|---|---|---|---|---|
| `AV-zj-1` (direct act) | the Chatter footer's date in words; no source line on an unserved Price window; "in this window"; the stale `ground="band"` comment; "with this list" | ~90 | 945d5db6 | words32 4/4 (KEEP 4/4), battery 0 skipped | f053d1b1d3 |

- The proof instance is VALID, run from its own worktree.
- 7 lines changed in 3 files. Every blob is LF, with no 0x08 and no non-ASCII. The issuer re-ran words32 and read 4/4.
- No rows.
- The worker left "Posture: not carried on this payload." (LeadPanel.tsx:302) because the order did not name it. It does not render
  on the Lead Panel at any window; words32 reads 6 of 6 renders clean. It is a round-33 wording item.

## 2. THE CANDIDATE -- portal `f9c6fa73` (worktree 82, branch `dsgn-r32-onto-dev`, LOCAL)

The candidate is 76a15c1b plus ~90 (c6c65efa), merged with remote DEV e862b0c4 (one DEV commit, InvestorReporting tests only; no
Security Analysis file). It contains DEV e862b0c4, so a push is a fast-forward.

**Issuer run on f9c6fa73:**
- `battery29.sh` with NO skip: ALL PASS (14 of 14 harnesses, tsc 0).
- round 32 words32 4/4.
- round 31: presets 4/4, windowread 4/4, feedrest 4/4.
- round 30: universe 4/4, resolutionwords 3/3, chrome 4/4, served 3/3.
- round 29: all 12 checks at full marks.
- round 27 identity 3/3; round 28 fixture 3/3 and render 3/3.

## 3. THE REAL RUN -- walk `tmp/ui-walk/20261003T175905Z` (5174 = f9c6fa73; ARM 17:58Z / DISARMED 18:00:32Z; login after: REFUSED)

The walk took the plain-route path (`/%73ecurity-analysis`) and pressed Price, 90D and Chatter. Walk void: no.
- **Load (Chatter, 30D): 0 findings.** The round-31 `format:dates` finding is gone.
- **Price, 90D** (shot 003): the served reason only. No bar, no "Source: ... payload" line and no Details line.
- **Chatter, 90D** (shot 004): "65 of 95 covered names have collected articles in this window" and "Articles collected, from the
  harvest. As of October 2nd, 2026." The served 90-day count is now 65; the fixture captured at 01:56Z read 64.
- **The only finding** is `layout:truncated` on Price at 30D: long names on the bars. It existed before this round, and each bar row
  carries the name in its hover.

## 4. OPEN

- **The CTO's product-file review of f9c6fa73.** It supersedes 76a15c1b as the DEV candidate (rounds 29-32).
- **The DEV push on Andrew's word at MSTR~Z.** The card is on 76a15c1b now; it swaps on the CTO's approval of f9c6fa73.
- **Round 33 wording item:** "Posture: not carried on this payload." (LeadPanel.tsx:302), which renders only in another mode.
- FWD-1 (Andrew's signed-in PROD read) and FWD-5 (RESAPP r64 cold read) remain open.
