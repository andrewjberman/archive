# COMM_ASSIST round 13 -- L8 packet (issuer 2.0.0_SA_COO~ZZ, site Z, 2026-10-10 ~23:5xZ)

**Reader:** `3.0.0_SA_CVO~Z` (L9: one judgment criterion, `CAe3-AC3`). Round 13 = the CTO's round-12 analysis
(`ledger/ROUND_ANALYSIS.round12.md` @82f10ddf63), issued @e87fa72a49, decomposition `decompositions/COMM_ASSIST_DECOMP.round13.md`.
`round-close-check --project COMM_ASSIST --round 13`: orders=2 complete, proof_ok=2, judgment=1, graded=0 -> **REFUSED** on
`CAe3-AC3` only (yours).

## The two orders, both terminal, merged

| order | cell | merge | issuer re-run on the merged tree |
|---|---|---|---|
| `TO-CA-e-2` (`0.9.0_WK_COMM_ASSIST~6`, `40d4d71c90`) | E2: `firm_domains()` pinned to the five | `bf8492f48f` | `E2-FIVE ok=True`; `MAIL-POLL ok=True arms=8/8`; `--check-domains` still `firms=4/5` (alongside has no measured domain) |
| `TO-CA-e-3` (`0.9.0_WK_COMM_ASSIST~7`, `1a6df54118`) | E3: `channel_poll` names its failure and raises it; live failure ruled | `25d1247250` | `E3-ESCALATES ok=True` (forced failure: `error='route=teams status=404 error=route not found'`, `ingress_step_failed=1`; healthy control raises nothing); `CHANNEL-MENTIONS ok=True arms=7/7` |

Drain hygiene: `commit-gate.sh` clean on all three `.py` files; investigation file 11 rows, 0 duplicate ids.

**What to grade (`CAe3-AC3`):** `deliverables/0.9.0_WK_COMM_ASSIST~7/CHANNEL_POLL_RULING.md` and row `COMM_ASSIST-Z-W7-S1`. Live:
59 of 59 `channel_poll` lines in the last hour read `failed=1`, `calls=1`, `channels=0` (cap 200, not cut). The failing call is
inferred as `teams`, with moderate confidence; the deployed code logs no error text. The dependent outcome is named: FWD-3 for
channel @mentions. Whose fix: unknown until the new `error` field is read after deploy.

Two form notes. Neither changed a criterion:
- The order named the row `COMM_ASSIST-W7-S1`. The row gate requires the site Z coordinate, so the worker filed it as `Z-W7-S1`
  and said so in the row.
- The naming gate refused a typed tuple of party keys. E2's constant reads three keys through `lib.opal_naming.lookup()` at
  import, so a missing registry now fails the module's import rather than the first call. Either way the mail step fails
  through `_safe`; that is the same outcome.

## Still open in this round

- **E1 (FWD-4 driven mail): HELD at Andrew.** No seat holds a non-Andrew Opal sending identity (row Z-S8). The ask is in front
  of him at the site Z MSTR terminal (`0.0.0_AB_MSTR~Z` msg 33074). On the send the issuer runs
  `r13/checks/check_e1_mail_day.py --day <send day>`, and you grade the INTERNAL flag on his text. The body is bound at the
  base: `check_e1_body_considered.py` passes as text and HTML.
- **Deploy: not cut this round, on purpose.** E2's "done when" names the NEXT apply, and E3's OR-branch is met by the ruling,
  so neither needs an apply to close. If E1's read refuses the mail, its fix also needs an apply. So ONE deploy cell carries
  E2 + E3 (+ an E1 fix if any) after E1's read, with halves measured on a pinned package. This also follows Andrew-direct
  2026-10-10 ~23:xxZ, slower pacing (`LIVE_ARMS.md` @f8c35c7699). E3's live arm (the `error` field naming the call) reads after
  that apply.
