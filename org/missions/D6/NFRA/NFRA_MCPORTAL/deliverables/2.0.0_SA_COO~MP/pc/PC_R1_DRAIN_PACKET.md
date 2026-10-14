# NFRA_MCPORTAL -- WORKSTREAM PC ROUND 1 DRAIN PACKET (L8 input) -- 2.0.0_SA_COO~MP, 2026-10-14 ~17:4xZ

**Workstream:** PC round 1: the People view (FWD-21 read half) and the three-state refusal reading on the fabric git-state page.
**Risk:** WORLD on the release cell (MP-pc-5), SERVED on the close run (MP-pc-6), LOCAL on the build cells.
**Judgment criteria:** one, `MP-pc-4` AC2, for `3.0.0_SA_CVO~Z`. Everything else is mechanical and has a VALID instance.

## Orders: 6 of 6 terminal

| Order | What it built | Drained / landed |
|---|---|---|
| MP-pc-1 | gateway git-state: `integration_refused` reads three states (refused / no / not recorded), basis per box | worker `90ad6bfa00`, `12d990e43d`; drained @94e904d9c1 |
| MP-pc-2 | `GET /api/admin/people`, the per-person view, owner-gated and read-only | worker `33d0604810`; drained @3d9226072f |
| MP-pc-3 | the People page and the three refusal states in the dashboard bundle | mcportal `17dcbb2` (origin DEV); drained @868fe133db |
| MP-pc-4 | the Claude account and limits sources finding (U1) | worker `fe76ebe7a5`; drained @5db04160eb |
| MP-pc-5 | the gateway release of PC.1 and PC.2 plus the bundle | LIVE at `bacec95ccd6cafd2201f7433af24ae2748732355` (previous `7c558b4e21`). Ledger `nfra-mcportal-pc-release` CLOSED 4 of 4, landed @a05cbc4c55. Manifest record @2a8f9ba6be. AC1 PASS, AC2 PASS, tools 70 -> 70, instance VALID. Complete @1d0b2e077e |
| MP-pc-6 | the close run: one real person and the three refusal states read against the stores | worker `553c7efa0f`; merged @33741bf311; complete @669a3e7f1d |

`python .tools/round-close-check.py --project NFRA_MCPORTAL --round 1 --workstream PC` at ~17:4xZ reads: 6 orders, 6
complete, judgment 1, graded 0, ungraded 1, **verdict=REFUSED**. The refusal is exactly the one judgment criterion
below, not a defect. (Round 1 across all workstreams also reads 2 orders not complete: MP-q-1 and MP-z-6, both staged
on Andrew's sitting, call 21d9.)

## THE JUDGMENT CRITERION FOR THE CVO

`MP-pc-4` AC2, in the order's words: does the finding name, for each of the three figures (account, 5-hour limit, weekly
limit), a source a build cell can read on every box without a credential, or say plainly that none exists?
The finding is `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~23/U1_CLAUDE_ACCOUNT_AND_LIMITS_SOURCES.md`.
Its mechanical limb AC1 passed (one JSON block, 0 bad rows, all three figures covered, 0 credential-shaped hits). The
worker recorded AC2 as UNVERIFIABLE-BY-INSTRUMENT, naming the CVO, with no PASS or FAIL.

## The one real run (MP-pc-6, the outcome's real entry point)

The page is owner-gated and no worker holds an owner identity, so the run read the SERVED modules on the host
(`i-07dccb1615503ac99`, over SSM, command `9f354b62-a3d5-40b9-9d2d-07003983a79d`, the host instance role). An earlier send
(`5b64cd1a-...`) failed on a Decimal serialization and produced no data.

| reading | value | against |
|---|---|---|
| person | `alyssa@opalinvest.com` (the grant store's profiled principal) | 5 of 5 data-grant tools equal on the page and in the store |
| channel | `portal_index`, holder `opalbloomberg@opalinvest.com` | 6 of 6 tools equal on the page and in the breakdown |
| laptop pointer | present, rc 0 | served `{"refused": false, "at": "2026-10-14T16:50:57Z"}` |
| sitez pointer | absent | served `"not recorded"` |
| dell1, dell2 | absent (404) | not used as the `not recorded` box |

Issuer re-run on the merged tree at ~17:4xZ: `pc6.AC1.sh` PASS exit=0, instance VALID rc=0, and the pointers re-read
independently with `head-object`: laptop present, sitez, dell1 and dell2 each 404 (rc 254). I did NOT re-run the host SSM probe.

**What the run does not show:** the `rc != 0` branch (a recorded refusal) is read by no box today and was not exercised.
Nobody has looked at the People page in a browser as an owner; that look is Andrew's sitting (call 21d9). The laptop
pointer is rewritten on every integrate pass, so the `no` reading depends on it still reading rc 0 when anyone re-reads.

## Rows filed this round, or touching it

- `Z-W24-S1` (OBSERVATION, INERT): the entitlement command has no read/show subcommand (activate, revoke, deny-backfill
  only), so the grant was read with a raw store get. Ruled ACCEPTED in the drain commit @33741bf311: the criterion needs
  an independent read of the grant, and the checker compares lists.
- `Z-W24-S2` (OBSERVATION, INERT): the store read ran under the host instance role, not the operator role. ACCEPTED with
  the limit stated: store==page compares two code paths over one credential, so it does not test what the operator role may read.
- `Z-W24-S3` (OBSERVATION, INERT): the status flip is outside the worker's paths; the issuer flipped it.
- `Z-S120` (`2.0.0_SA_COO~O`, ARMED, not mine): runbook section 7.2 still names `7c558b4e21`. MP-pc-5's order did not carry that file; I answered `2.0.0_SA_COO~O` (msg 34155) that its OG-ap-18 release rewrites the line.

## Not done here

- FWD-21's write half waits on NFRA_OPLGTW OG-cp-1 (F2).
- GW round 1 (MP-z-6, FWD-20) and the CP2 close run (MP-q-1) wait on Andrew's sitting, call 21d9; FWD-1 (MP-c-2) waits on call def4.
