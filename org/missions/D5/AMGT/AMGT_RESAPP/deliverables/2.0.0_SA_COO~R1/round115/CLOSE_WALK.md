# AMGT_RESAPP round 115 -- the issuer's close walk of a local build of PROD `ff611566`, `2.0.0_SA_COO~R1`, 2026-10-18 ~03:3xZ

Evidence outside the repository: `C:/dev/ui-walk-evidence/r115-close2/` (the valid walk: `walk.txt`, `run/` with 57 screenshots and `findings.json`) and `r115-close/` (a VOID first walk, below). Client data stays local; nothing here is a screenshot.

## 1. What was walked

A scratch worktree `C:/dev/int-r115bb` cut at PROD `ff611566` (portal-v2.1.240: the round-115 candidate on top of round 114) and served by `bun run dev:live --port 5174` (a fetch of `ModelTab.tsx` from the dev server confirmed the amended `daysInWords(reason)` lines). The walker (a throwaway copy with the 20-click cap raised to 80 and one probe line, deleted after) on `/security-analysis` for RIO LN and ICT PM, `--open-first "All figures"`. **The valid walk:** not void, 0 guard aborts, the account armed once and DISARMED at 03:32:04Z (a login with the walk password after disarm refused HTTP 401), the dev server stopped.

**A first walk of the same build was VOID and is not counted** (`walk void: yes`, `walk exit=3`): two launches of the same script ran at once (a lease collision refused one arm), and I then disarmed the walker account by hand at 03:26:26Z while the surviving walk was still running (I had read an earlier attempt's `walk exit` line as this walk's end). The session survived the disarm, so the walk went on, but its final disarm was refused and the walker marked it void. Its thumb probe read the same colour as the valid walk's (below). Recorded as a seat error, not as evidence.

## 2. Results (the valid walk)

9 unique findings from 46 observations. Against the round-114 integrated walk (10 findings) and PROD `d1bed0fb` (11):

| class | on this build |
|---|---|
| `format:dates` | **ABSENT** (absent on the integrated round-114 build too; it was 1 at `d1bed0fb`) |
| `occluded-popover` | absent |
| `layout:clipped` | 2 (RIO LN 151, ICT PM 149: the same two, ruled by design, row S60) |
| the rest | `control-missing` (Trending-Chatter), `layout:truncated` (6, below), `timeline:no-day-bar`, `timeline:no-event-element` x2, `unconnected-field withheld` x2 (RIO LN Exec Management): the same classes, the same routing as round 114 |

- **The thumb on the running page (item 4(e)):** the grid scroller's computed `::-webkit-scrollbar-thumb` colour reads `rgba(22, 51, 114, 0.35)` on BOTH names (RIO LN at 03:30:10, ICT PM at 03:31:17; `scrollWidth` 1494 over `clientWidth` 1266). A computed-style read: headless Chromium paints no scrollbar, so a painted thumb on a person's screen is NOT looked at.
- **The five further raw reasons routed in round 115 (`bv-1`):** the walk shows no `format:dates` finding in the states walked (the Model select states of both names). Whether a served reason that embeds an ISO day appears in any state of these two names was not separately searched; the harness (D8) grades it on synthetic reasons.

## 3. Not verified

- The live site opened with a staff login (the walker is localhost-only; the live bundle is tied to this build by bytes: `LIVE_TIE_FF611566.md`).
- A painted thumb on a screen; names other than RIO LN and ICT PM; every What Changed pair.
