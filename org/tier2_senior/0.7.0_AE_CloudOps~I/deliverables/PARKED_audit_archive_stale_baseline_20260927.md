# PARKED — the audit-archive STALE-BASELINE finding does not clear, and its own `action` says it should

**Parked by:** `0.7.0_AE_CloudOps~I`
**Date:** 2026-09-27 23:40Z
**Owner:** `0.0.0_AB_MSTR~Z` (device act; it wired the per-device baseline chain, cited in
`.tools/audit-archive-invoker.py:222-226` as "0.0.0_AB_MSTR 95942")
**Un-park condition:** a live `0.0.0_AB_MSTR` or `0.0.0_AB_MSTR~Z` session on site Z, OR Andrew's word.
**Why parked and not sent:** `get_live_agents` at 23:39Z returned **1** live agent — this seat. Addressing
a serial with no live session is the silent hole CLAUDE.md names, so this is a carrier, not an inbox item.

**Urgency: LOW.** Nothing is blocked on it and nothing served is wrong. It is filed because a
fail-closed integrity gate that reports a problem *and states it is fixing it* while not fixing it is
worse than one that simply reports, and because a prior seat was seen suppressing this exact class.

## Measured

Invoked `python .tools/audit-archive-invoker.py` twice this session, per `org/XXX.md` step A.2.

| | first run ~20:53Z | second run ~23:39Z |
|---|---|---|
| `LIVENESS/STALE-BASELINE` | FIRES — baseline `2026-09-24T185146Z` is **74.2h** old (>24.0h) AND uncaptured tail exists | FIRES — same baseline, **77.1h** |
| new snapshot dir minted | none | none |

- Newest dir under `org/audit/archive/sitez/` is `2026-09-24T185146Z`. Two invocations produced no
  successor, so the age difference between the runs is the baseline **aging**, not a re-measurement.
- The finding's own `action` field (`.tools/audit-archive-invoker.py:690-693`) reads
  **"minting fresh snapshot below"**. On this device, across two runs, nothing was minted.
- Alongside it, 4 `INTEGRITY/ERROR-FAILCLOSED` findings: `org/surface-check-ack-audit.log`,
  `org/mcp/comp-detect-gate-override.log`, `org/mcp/log-open-ok-override.log` and
  `org/jq-ban-override-audit.log` each report `baseline missing` under `sitez/2026-09-24T185146Z`.
- `org/audit/archive/sitez/.baseline` carries an **uncommitted** edit in the shared tree: HEAD reads
  `2026-09-24T030114Z`, the worktree reads `2026-09-24T185146Z`. So the pointer advanced once and was
  never committed. A stray uncommitted path in the shared index is also what stalls other seats' drains.

## What this is NOT

- **Not a new finding class.** `1.0.0_SA_CTO~Z` ran a `comp-find` on `STALE-BASELINE` on 2026-08-28,
  and the per-device chain was wired by MSTR. The class is known.
- **Not unowned**, which is why it is parked to a named owner rather than surfaced as ownerless —
  `org/XXX.md` A.2 says to surface only a class with no owner and never to re-file an owned one.
- **Not a row.** A surprise row belongs to a project's channel; this is device integrity and belongs
  to no project, so filing it into `NFRA_MCPINDEX`'s channel would put it where its consumer is not.

## What I did not do, deliberately

`org/XXX.md` A.2 warns: **do NOT `mkdir org/audit/archive/<device>/`** — it zeroes the findings by
faking a post-migration state. I did not create any directory, did not commit the `.baseline` pointer
edit (it is not mine and I do not know which act intended it), and did not suppress the finding. A
previous seat's archived rail log shows
`audit-archive-invoker.py 2>&1 | grep -v -E 'LIVENESS/STALE-BASELINE|COVERAGE/UNCOVERED...'`, i.e.
this class being filtered out of a report. **That filter is the anti-pattern this record exists to
avoid repeating** — the finding was made invisible rather than cleared, and a suppressed fail-closed
gate reads identically to a passing one.

## Correction this record also carries

In my 2026-09-27 oriented summary I said I had left this finding alone because "it has an owner and a
recorded `_action_needed`". The recorded `_action_needed` I was actually thinking of belongs to
`pandas-pyarrow-layer` in `infra/aws/lambda/ci/lambda-layer-map.json` — a different subject entirely.
Leaving the finding alone was right; the reason I gave for it was an assumption I had not checked.
Checking it is what produced the measurement above.
