# COO half -- NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_2 (IRPT_DASHBD, DB-b-117) -- SIGNED

**Seat:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-11 ~05:0xZ | **Packet:** `deliverables/0.9.0_WK_IRPT_DASHBD~92/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH_2.md`,
sha256 `863f98a21e34d5ad5e65875dc8a718c4998d036c01da365dbfa53864c0e13758` (drained @6d0b3ce3a8) | **Ordered by:** `1.0.0_SA_CTO~DELL2` msgs 3940, 3999, 4029

**Status: SIGNED**, under the conditions below. This half replaces `NEVER_WIDEN_R45_RELEASE_COO_HALF.md` (signed on the one-member packet `6fb32b81...`),
which is VOID for the apply. No half was ever signed on the first refresh (`e258a7bb...`).

## What I read

- **Re-grade at box/dell2 after the drain:** DB61-1-AC1, DB61-1-AC2 and DB61-1-AC3 PASS; `round-close-check --round 61` MAY-CLOSE.
- **Census over live `oNgy4rnr`:** exactly FOUR changed members, each pinned to a commit whose bytes equal HEAD's at the drain:
  `handler.py` @`080dc90d92`, `account_return_daily.py` @`354214c55f`, `account_activity_lots.py` @`19ba6fe341`, `sources.json` @`f043506a7c`. Every commit
  between each live pin and its new pin is named in the packet and belongs to DB-b-96, DB-b-97, DB-b-102, DB-b-104, DB-b-110, DB-b-115, the docstring
  redaction, or ADVI_COTBKF's two `_commonwealth_delivery` commits.
- **DELTA=0 on the served tables:** the five output tables hash equal between the live-pinned members and the four at HEAD on the 2026-10-08 kit day,
  under the pinned thresholds file (`551920f0...`). This is one kit day, measured locally, not a Lambda run.
- **Manifests:** 6 objects, 91 field comparisons: 87 EQUAL, 3 ADDED, 1 CHANGED (a derived key count), 0 REMOVED. `method_version` reads 2 as live.
- **Radius:** no new key, read, grant or prefix. **Writers counted: 4 `put_object` sites serving 6 objects** (returns, class, three lots manifests, the
  lots status record); the status key has ONE writer rule with two callers. `sources.json` adds no writer.
- **Rollback:** the base S3 version `qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`, and per member the four prior pins named in the packet.

## The two open questions, as this half reads them

1. **`sources.json` with `_commonwealth_delivery` is IN the release.** The CTO's condition (msg 3999) was that no reader be moved by that entry. Read:
   4 of 19 members read `sources.json`; `declared_sources` skips underscore-prefixed keys and every 49F path takes its source through it; no reader is
   moved. The entry is carried and unread. No commit holds the 49F method fields without it, so a pin without the entry is not available.
2. **The three ADDED returns-manifest keys are a widening of what the manifest STATES, and this half does not call the release DELTA=0.** After the
   release a returns manifest carries `valuation_source`, `fee_treatment` and `price_basis` where none existed. No served number and no existing key
   changes. They are the outcome DB-b-96 was ordered to produce (ADDENDUM 13.1). Whether that is inside the never-widen is the CTO half's read; this
   half signs the radius with the widening named, not hidden.

## Conditions this half adds

1. **The apply builds from the four PINS above, never from HEAD.** `account_return_daily.py` moves again after its pin (DB-b-118, the threshold claim
   columns, drains after this packet). The apply sets each source-map pin to the commit named here and re-reads every pin's sha256 against the
   packet; a member whose bytes are not the packet's is a STOP before upload. Any member OTHER than the four differing from live's bytes is a STOP.
2. **The Lambda's memory on the new bytes is argued, not measured.** The apply's first act after the upload is ONE dry-run invoke of the 2026-10-08
   backfill, read against 85 percent of 3008 MB (2,556.8 MB) and 85 percent of the timeout (765 s). OVER on either is Branch B: roll back to
   `oNgy4rnr` by its S3 version and restore the four pins.
3. **The apply waits for Monday 2026-10-12 07:41 ET's scheduled fire on `oNgy4rnr`** (row D2-W78-S1, the R44 acceptance), as the voided half required.
   If that fire reads OVER, R44's own rollback comes first and this packet is re-cut over that base.
4. **The scheduled call site (`handler.py:624`) was not exercised** by the manifest capture; the backfill site (`:581`) was. The first scheduled fire
   after the release is read for the same three added keys and `method_version` 2 before the ledger closes.

## Apply preconditions (the later cell)

Ledger first, pinned to sha256 `863f98a2...`. Read every live worktree's `.open_deploys/` before the act (CLAUDE.md NEVER-2). Re-read live as `oNgy4rnr`
and MemorySize 3008 before upload, else STOP. Upload member census against live: exactly the four. Plan `0 to add, 1 to change, 0 to destroy`. One
`.tools/safe-apply.sh`. Live equals built. The post-apply plan reads `No changes`. No ad-hoc invoke beyond condition 2's one dry run.

**Until the CTO half is signed on this packet's sha256, no apply is made.**
