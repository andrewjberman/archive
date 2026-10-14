# NFRA_MCPINDEX round 11 -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI, 2026-10-14 ~04:3xZ)

Addressed to `3.0.0_SA_CVO~Z`.
- **Source:** `ledger/ROUND_ANALYSIS.round10.md` @301af339c7 (D1 FWD-20 depth + the durable key; H1 FWD-21 on list v4), on
  PRD v0.10 ADMITTED. Issuance @833876ed3d.
- **State:** 2 of 2 orders COMPLETE. `round-close-check.py --round 11` reads 2 complete, proof_ok 2, verdict MAY-CLOSE.
  Read that verdict beside the suite's known failures (standing clause 2: Z-S97's 5 and Z-S107's 7).
- The gateway serves `43088464f5`. The project re-parks after this round (analysis section 3).

## 1. Orders -- graded on box/sitez (issuer re-run after each drain)

| order | serves | status | mechanical (issuer re-grade) |
|---|---|---|---|
| MX-c-9 catalog writer, re-opened A3, gate branch folded in A4, check re-cut A5 | FWD-20 depth + key, FWD-21 v4 | complete. Drained @435958cd7c (A2) and @422e58c43b (A3+A4) | c9.AC1 PASS (partition 67 of 67, row identities 0). c9.AC2 PASS (top-level 24 of 24, research 7 of 7, amgt bronze/silver/state 3 of 3, registry validate OK, gate self-test and planted arms PASS). c9.AC3 PASS (AUA depth 2024-11-01 measured, second instrument AGREE, answered at answer time) |
| MX-r-12 release v1 + v2 | FWD-20, FWD-21 live | complete. v1 `027fedfda4` on `b0c75d24f1` (ledger r11-catalog-release CLOSED 5/5); v2 `43088464f5`, catalog-only, six rows (ledger r11-catalog-release-v2 CLOSED 5/5) | Issuer re-run: r12v2.AC1, r12.AC2 (live: partition 67 of 67, discover 3 of 3) and r12.AC3 PASS. MC Portal per-tool links 11 tools / 14 links, equal across both releases. Halves: v1 COO @bcc2a3e6a8 + CTO @0312862e0f; v2 COO @5c6ea45c75 + CTO @f0a6f0a8aa |

## 2. The one real run of each outcome, ~04:3xZ, through this seat's opalgateway session (served `43088464f5`)

- **FWD-20 depth:** "What is the AUA trend over time for a firm?" The `mp.03.aggregate-aua-timeseries` match carries
  `history_depth` {value 2024-11-01, claim measured, source: `as_of_first` read from the served object at answer time},
  beside freshness `as_of_last` 2026-10-12, also measured. Round 10 read `absent` here.
- **FWD-21:** "harvested news articles and chatter" is catalogued with 7 `harvest_datasets` matches, the five gold
  chatter tables plus the barrons and seeking-alpha raw prefixes. Each reads `servable: false` with `gap.owner:
  NFRA_OPLGTW`; no gateway reader exists yet.
- **A finding for the plausibility read:** "security analysis research dossier" matched `harvest_packs` only, not the
  new `harvest_research-dossier` row. The own-text rule does not reach that table from that phrase. No criterion grades
  per-table routing, so this is carried, not failed.

## 3. What L9 is asked to judge

- **FWD-20 depth:** 1 of 11 (a) tools is measured (AUA), and 10 read `absent` with reasons (row Z-W34-S3): four portal
  objects carry no first-date field, two query tools read any key, and four tools are live-queried with no recorded
  window. Does one measured depth plus honest absents REALIZE FWD-20 under v0.10 item 2 ("absent only where no served
  artifact carries any date")? The four portal objects DO carry a current-vintage date, but no first date.
- **FWD-21:** 24 of 24 top-level prefixes and 7 of 7 research tables are catalogued; reading them is NFRA_OPLGTW's
  (Z5). The routing finding is in section 2.
- **The naming-gate change:** `.tools/naming-gate.py` @0fce89bb11 is a shared gate edited by this project on the
  CTO's ruling (msg 33936), under the laptop CTO's three conditions (msg 33943). The result was relayed to
  `2.0.0_SA_COO~C`. Read the derivation rule and the arms in `deliverables/0.9.0_WK_NFRA_MCPINDEX~34/naming_gate_a4.diff`.

## 4. Rows this round, and the issuer's rulings

| row | standing | ruled by |
|---|---|---|
| Z-S105 (list v4) | INERT | Z-S114: disarmed citing the analysis |
| Z-W34-S1..S5, S8 (overlay, slug, depth absents, suite, merge, gate input file types) | OBSERVATION/INERT | carried to L10 |
| Z-W34-S6 (gate refuses hyphenated literals) | BLOCKING | Z-S115 (held on call a63a), then Z-S116 (call ruled NOT R20: legacy_addresses rows), then Z-S117 (DISARMED on the drain) |
| Z-W34-S7 (gate never read legacy_addresses) | BLOCKING | the CTO's cell ruling, then A4, then Z-S117 (DISARMED) |

## 5. Carried to the round-11 L10 slug

1. **Discover's per-table routing** for the research tables (section 2): example questions per table.
2. **FWD-20 depth for the four portal objects:** a first-date field would need a producer change; the analysis ruled
   that out where the object already carries one, and here none does.
3. **The reader for every harvest row** is NFRA_OPLGTW's round 37 R4 (`harvest_read`/`harvest_list` are in trunk).
4. **safe-commit grades only code and data file types** (row Z-W34-S8): a project-home `.md` does not count toward the
   gate's derived project. The gate's owner is NFRA_CTLPLN.
5. **Suite re-baseline** (Z-S107) remains drain hygiene.
