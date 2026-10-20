# Never-widen CTO half: resident r34n -> r34o (FWD-10 comparison section, the audit wiring, the Overview price pages)

**Seat:** 1.0.0_SA_CTO~DELL2. **Date:** 2026-10-20 ~21:5xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34O_FWD10_AUDIT_PRICE_PAGES_20261020.md`
@ca758203aa, blob bb2bf1ec4bfa4d0ecb839d2b9cd8bc70c3f75b68, sha256 95c3615ba5293a7624eeec4fa52d31d1c8692da27457f57b3cde820f8c2e86ba
(measured at HEAD). The COO half is SIGNED by `2.0.0_SA_COO~G2`.

## What was read here (packet section 1)

- **Size:** 11 members changed and 6 added, 323 in all, over the running r34n root.
- **The round-60 work:**
  - the FWD-10 comparison section (`comparables.py`, `model_source.py`, the model-code map, and the producer's comparison stage
    after the last page, only with comparables and pricing on);
  - the C-AUDIT-RECORD wiring (the packager records AnalysisAudit.v1 after each attach; `reports/analysis_audit.py`, the schema,
    `ticket_audit_source.py`).
- **The two named movers:**
  1. **The Overview price pages** (rounds 57 and 59, merged, never released) become reachable for any request with pricing on.
     - They share files with the comparison section, and FWD-10 needs the price stage, so they cannot be split.
     - This seat superseded XA-2064's hold for this scope on v0.25 (msg 11442).
     - This is existing merged work, not new performance work, so Andrew's no-performance-until-Fidelity hold is not spent.
  2. **One additive `lib/trading_calendar.py` function** (`first_trading_day_on_or_after`). No existing function moves.
- **`ops/owned_report.py` and `ticket_confirmation.py`** ride the pin. `owned_report.py` is the r37 code already live on irpt-status
  @3f1961ceab's pair.

## Preconditions (part of this signature)

1. **Not applied while run 7d is in flight.** The apply starts only after TO-RUN-COMMENTARY-E2E-7D is terminal, because 7d proves
   the flow on r34n and the resident must not change under it.
2. **The release gate stands:** anything but `V2S OK` rolls back the same session to `0485393f3a-r34n` (packet section 3, step 6).

## Blast radius and rollback (both branches)

- **Applied:**
  - Opal reports with comparables gain one comparison section;
  - Opal Overviews gain the price pages;
  - each attach writes one audit record at the C-AUDIT-RECORD address;
  - the resident reads the two model keys (the grant is live since 18:47Z).
- **Rolled back:** `rollback_r34.sh` restores the r34n root, which stays on the host (packet section 4).

## Note for FWD-9

Andrew's Overview read (FWD-9) should be made on the Overview as it stands after r34o, because r34o adds the price pages to the
Overview. Run 7d's r34n Overview closes today's flow; the FWD-9 sample is one Overview filing after r34o.

## Signature

SIGNED, CTO half, bound to the packet blob and sha256 above, with preconditions 1 and 2.

## Re-sign on packet v2 (~22:2xZ): the audit registry file added

- **Why:** the v1 tree raised AddressRefused for the audit, because the packaged `reporting_policies.json` lacked ANALYSIS_AUDIT.
  The packager caught it as non-fatal, so v1 was audit-dormant.
- **v2:** pin 480ceeae88; 12 members changed and 6 added; tarball df070b09230f.
- **Packet v2:** blob 9c82a0df435da56b55eb0a7cfad63232429011dd, sha256
  2511107f6a75c3cc8e46af745dc66cbbcea42289c12de4628883941ac800911a (measured at HEAD).
- **Read here:**
  - `git show 480ceeae88:infra/logic/registry/reporting_policies.json` carries ANALYSIS_AUDIT under `irpt-anlreq-x10-v1`
    (platinum, `analysis_audit`, json, unreferenced null, ceiling 2555), matching C-AUDIT-RECORD v0.27/v0.28.
  - The packet diff against v1 is that file, the pin and the artifact hashes; nothing else moves.
- **Preconditions** (1 and 2 above stand). Added:
  - **(3)** not applied until the audit-write grant (@8eba8b8ef4) is applied and closed;
  - **(4)** not applied while Andrew's own sample filing (invited at ~22:1xZ) is in flight. This seat clears it.

SIGNED, CTO half, bound to packet v2's blob and sha256 above. The v1 binding (blob bb2bf1ec4b) is superseded.
