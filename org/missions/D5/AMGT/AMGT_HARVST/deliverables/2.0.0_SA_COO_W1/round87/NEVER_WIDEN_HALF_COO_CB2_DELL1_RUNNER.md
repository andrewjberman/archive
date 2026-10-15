# NEVER-WIDEN -- COO HALF: register the dell1 harvest cycle runner for `wsj` and `barrons`, `HVST-cb-2` (round 87, workstream RUNNER)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-15 ~19:4xZ. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half at `ledger/NEVER_WIDEN_ROUND87_CB2_CTO_HALF.md` (owed).
**Authority:** Andrew-direct 2026-10-15 ~16:3xZ (all harvest operations to dell1; `org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261015_163xZ_MOVE_ALL_HARVEST_OPERATIONS_TO_DELL1.md`); `ledger/ROUND_ANALYSIS.round85.ADDENDUM_3_ALL_PUBLISHERS_TO_DELL1.md` and `ADDENDUM_4_Z_RETIRES_ALL.md`: "Production collection is a scheduled runner on dell1, never a hand-run. The first scheduled cycle that uploads is the cutover; W1 reads it."

## THE ACT, in the order's words

On dell1, once, by `0.7.0_AE_CloudOps~SC1`:
1. Pin `P` (the head of `box/dell1` at the act, which must carry `39ae28559b` (NFRA_OPLGTW E1+E2), `d0c48b3946` (HVST-ca-1) and `08c80a8f75` (HVST-cb-1)) becomes a locked worktree `wk-harvest-runner-pin-<P>` beside the main tree.
2. The user-level environment variable `OPAL_HARVEST_PROFILE_ROOT` names the MAIN tree's `.runtime/opal-data-harvest/browser-profiles`, so the publisher profiles (the only source of a wsj or barrons session) survive a re-pin. Without it the profile root follows the pin's checkout (`tab_transport.default_profile_root`, HVST-ai-2) and every re-pin starts logged out.
3. The task `Opal Data Harvest - Continuous Cycle` is registered by `install-cycle-schedule.ps1 -RepoRoot <pin> -Publishers wsj,barrons -StateDir <main>\.runtime\harvest-cycle\state -RuntimeRoot <main>\.runtime\harvest-cycle\runtime -Windowless -RefreshOnce` (the `-Plan` read first), then started once.
4. Reads at +3 and +15 minutes, a signed rollback, and the account stop rule.

## THE NEW THING THIS ACT TURNS ON (named, not hidden in the registration)

- **Production collection by `wsj` and `barrons` moves from site Z to dell1.** Site Z's runner is STOPPED (Ready) at 18:54Z, read by the site Z MSTR and relayed (`0.0.0_AB_MSTR~DELL1` msg 6134); its formal stop-and-Disabled read-back is owed by site Z (ETA ~19:20Z, relayed msg 6142). Site Z stored `new=0` for all four publishers since 14:02Z (site Z's statement; the 14:02Z-onward S3 writes are NOT re-read by this seat).
- **A headful Chrome window on the dell1 desktop, continuously.** The tab transport launches `channel="chrome", headless=False` with no minimise flag (`tab_transport.py:99`, `LAUNCH_ARGS` at `:15`). The runner runs one pair after another, so a visible Chrome window is open on the interactive desktop of the Windows user `Test` for most of every cycle, on the box that hosts every agent terminal. Risk: focus taken from a terminal or an approval prompt, and a closed window ends its pair (recorded, not retried). **This half does not rule that; the CTO half must (section "THE QUESTION" below).**
- **A headful Dow Jones sign-in made by the RUNNER**, only when a `wsj` or `barrons` job is refused as expired (`--refresh-once`, merged `3d88eccbc3`). Since HVST-ca-1 (`d0c48b3946`) that refresh is the in-profile renew (`verification.renew`), not the bundle script. Budget: at most ONE refresh per publisher per cycle, kept in the cycle checkpoint. It reads `dowjones/credentials` BY NAME and prints and records no secret, cookie or username.
- **The account's readers, measured and not measured.** `wsj` and `barrons` share ONE subscriber login. Read at the 2026-10-13 pair (`deliverables/2.0.0_SA_COO_W1/round85/DOWJONES_SECRET_TOUCHES_20261013.txt` @dd6c8e07ac): 29 `GetSecretValue`, all by `Andrew_Berman`, none refused. **Not re-read today.** Since then this seat made 5 sign-ins on it from dell1 on 2026-10-15 (two bundle refreshes at 16:11Z and 16:12Z, two in-profile renewals at about 16:13Z and 16:15Z, one renewal in AC3 at 18:56Z), none refused. The vendor-side lock policy and who else signs in with that login are NOT READ.
- **The E2 proof is the first productive scheduled cycle per publisher** (`ADDENDUM_4`): the cycle record must carry the S3 GET count and bytes (OPLGTW E1+E2); a runner at a pin without `39ae28559b` does not go on a schedule here.

## BLAST RADIUS

- **Writers of the property N = 1 per publisher, once site Z is Disabled.** The bronze, silver and watermark rows for `wsj` and `barrons` in `s3://opal-data-assets` (via `lib/research/harvest/store.py`) are written by the harvest runner: site Z's task (STOPPED, formal Disabled read owed) and, after this act, dell1's task. The registration (`WorkingDirectory`, arguments, interpreter) is written by `install-cycle-schedule.ps1` and by nothing else on dell1; one task named `Opal Data Harvest - Continuous Cycle`. **Condition C-b makes N = 1 a read, not a belief.**
- **What it touches in the world:** vendor requests to `wsj.com` and `barrons.com` (the paced requests the runner already makes), S3 writes of bronze and silver for those two publishers, at most two sign-ins per pass, and a visible Chrome window on dell1's desktop.
- **Not touched:** `bbg`, `sa`, `ft` (they join by a re-registration under their own addendum to this pair, each after its local proof), the portal, gold, any firm bucket, the main tree's code, the other seats' worktrees.
- **Served output moved:** yes, the publisher rows that feed `AMGT_RESAPP`'s Chatter axis and the news layer change writer. Rollback per key below.

## BOTH BRANCHES (the half is signed for BOTH or for neither)

- **Branch D (the first cycle ends `completed` for a publisher, accepted > 0):** the E2 line (GET count, bytes) is in the cycle record; the issuer reports run record, accepted count and bytes to the CTO and, through MSTR, to site Z (which unlocks its pin worktrees).
- **Branch F (a refresh FAILED, or a second refusal after a refresh):** NO second attempt by anyone; one row (publisher, class, `http_status`, `host`, `login_redirect`) and the question returns to the issuer; the task stays registered unless a rollback condition fires.
- **Branch X (no refusal occurs):** the runner collects with the sessions the profiles already hold; nothing else happens.

## THE QUESTION THE CTO HALF MUST RULE (named by the signer; the COO does not rule it)

The visible-window question above: (a) accept it and read the first cycle's effect on the terminals; (b) a separate interactive Windows session for the runner; (c) a one-line launch-flag cell (`--start-minimized` in `LAUNCH_ARGS`), measured on one job first. The signer's recommendation: (c) first, then (a). Headless is a fourth option this seat has NOT measured: the code launches headful, and the only bot-protection finding on file (CTO ruling 27695) is about injected cookies, not about headless, so it neither excludes nor supports headless.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a.** `P` carries the three commits above (`git merge-base --is-ancestor <c> P`, with the reverse of one as the negative control). **C-b.** Site Z's FORMAL read-back (task Disabled, process census with a positive control) is on file, relayed by `0.0.0_AB_MSTR~DELL1`, and a second read at the act shows no `S3 PutObject` for `wsj` or `barrons` by site Z since it. **C-c.** Both halves read SIGNED at their pins before any change. **C-d.** The stop is by the runner's own stop file (its parent directory must exist first; row `AMGT_HARVST-Z-S120`), never a kill. **C-e.** `OPAL_HARVEST_PROFILE_ROOT` is read back from the registry and from a fresh process before the first start.
- **C-f.** The first cycle's account stop rule: a FAILED refresh, or a second refusal after one, stops everything and files a row.

## ROLLBACK

`Stop-ScheduledTask` by the stop file, then `Disable-ScheduledTask` (no unregister); site Z re-enables its own task at dell1's ask (its offer, msg 6097). A session a renewal replaced is not rolled back (a fresh session is the intended state). Bronze and silver rows the dell1 runner wrote are append-only objects: they are not deleted by the rollback; the watermark follows the writer.

## WHAT THIS HALF DOES NOT COVER

- `bbg`, `sa`, `ft`; a sign-in by any hand other than the runner's one refresh per publisher per cycle; `--park`; any new credential path; reading or printing a secret, cookie, username or token; a change of the state dir or runtime root after registration; an upload outside the runner's own writes.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file and C-b reads true.
