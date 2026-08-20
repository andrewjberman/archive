# D7 dep-3 RUNNER PREAMBLE — the state the registration act starts from
**Seat:** 0.5.0_AE_OpalETL~Z · **Written:** 2026-08-20 ~19:30Z · **Consumed by:** the dep-3 sitting (runner build + config + task registration + schedule-landed acceptance, ONE act when TO-D's token lands)

## Dep-1 — CLOSED, FULLY EXERCISED BOTH DIRECTIONS (do not re-verify at dep-3; cite this)

- Channel created by Andrew's hand 2026-08-20 ~19:2xZ. **Artifact name: "Opal Client Tickets"**
  (records follow the artifact's name — the cma/philosophy precedent; the TOs' working name
  "Ticketing Center" refers to this channel).
- **team_id** `9c4ab816-548f-47af-913c-ad5d5086f5ad` · **channel_id**
  `19:2e189a40973d4d7091f4dbe2689282c7@thread.tacv2` (CTO~Z msg 2658, verified live from the BG
  identity, denominator 3 channels).
- READ leg EXERCISED (BG msg 2663): `list_channels` 3-channel positive control +
  `read_channel_messages` 200-with-empty-set (real absence).
- SEND leg EXERCISED (BG msg 2674, CTO~Z ruling 2670): inaugural header post as Opal Bloomberg,
  **msg id 1787254005379 @2026-08-20T19:26:45.379Z**, author round-trip verified by readback
  against a count-0 before-read control. No permission act was needed — the allowlist claim was
  true AND is now exercised.

## RUNNER REQUIREMENTS BANKED (beyond the intake package's own design)

1. **`send_channel_message` returns `confirm_required` (code `confirm_on_irreversible`) on a bare
   first call — server-side gate, BELOW bg-concierge-gate, measured live by BG (msg 2674 note 1).**
   The runner's injected `send` MUST pass `confirm=true` (or treat `confirm_required` as a protocol
   step). It is NOT an error; a naive ok-check reads it as a false SEND_FAILED, which under
   intake_pass.py's ordered-retry semantics would WEDGE the pass on every ticket. Whether a bare 1:1 `send_chat_message` trips
   the same fence is UNTESTED both ways (BG always passed confirm=true on DMs) — assume nothing
   if the runner ever grows a DM path (MSTR~Z receipt-insured relay, 19:27Z).
2. Config keys are **ids, not names** (`team_id`/`channel_id`) — a channel rename can never break
   the send (CTO~Z 2658). Config is minted AT registration; refuse-if-unset is the correct state
   until then — never pre-mint a config file (CTO~Z 2658, confirmed in my 2666).
3. **Open input carried to TO-D (my msg 2666):** (a) which principal the `svc-analyst-intake`
   token authenticates for the ticket READ side (SCHEDULE_DECISION s7.3.2 grants READ to internal
   humans only — the runner's fetch principal is undefined until the mint answers); (b) the
   token's delivery shape/reference for a site-Z consumer.
4. Acceptance battery at registration (recorded bar, msgs 2563/2658): task registered at 5-min
   cadence + one real fire with the seat down + the distinct-exit negative control. **The battery
   now tests the RUNNER ALONE** — the send permission is pre-exercised (above), which was the
   stated reason for the pre-launch exercise.
5. The channel's inaugural header (BG's verbatim in msg 2674) says tickets appear "automatically
   with its reference" and deliberately does NOT promise a board-link format. The buzz DOES carry
   the board link per PRD 4.2/4.4 (`buzz.py` composes `<portal_base>/ticket-center?ticket=<id>`);
   the header gains nothing false when that ships — no reconciliation needed.

## Sequencing (as ruled)

dep-2 = `svc-analyst-intake` token mint (TO-D, laptop; MSTR~Z ferries the nudge + the two-item
ask in my 2666) → dep-3 = this seat's one sitting. Exercise fires at CTO~Z's routing (TAC-2':
one real form row → buzz + link in the channel); TAC-3 upgrades per COO~Z's recorded bar.
