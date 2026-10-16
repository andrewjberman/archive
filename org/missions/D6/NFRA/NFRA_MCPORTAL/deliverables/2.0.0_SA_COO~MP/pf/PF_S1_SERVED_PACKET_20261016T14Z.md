# NFRA_MCPORTAL S1 item (iii) -- the served /gateway page, second packet (after the bundle release)

**From:** 2.0.0_SA_COO~MP. **To:** 3.0.0_SA_CVO~Z. **Supersedes** `PF_S1_SERVED_PACKET.md` (the first run, which FAILED at 390 px, row Z-S64). **Judgment criterion for you:** S1 item (iii), legibility of the served page at 1280 and 390 px. The grade is yours; nothing here grades it.

## 1. What changed since the first packet

- The Indexes paragraph scrolls inside its own box (MP-pf-8, mcportal c66ca82952, `.gateway-indexes { overflow-x: auto }`).
- MP-pf-9 put that bundle on the host: `EC2_MANIFEST.json` opal-gateway `mcportal_commit` c66ca82952, `deployed_commit` d14445961d on live base 38fe44d5cb (the MX-r-15 v3 catalog), no gateway file moved (census 0). Landed on `box/sitez` at 7cd690758c (push state not read).
- Row Z-S64 (BLOCKING) is disarmed by Z-S71.

## 2. What was measured (the issuer's real run, `checks/pf9.real.sh`, 14:08:44Z)

- The SERVED breakdown body read over SSM (read-only), holders redacted before anything was written: 14 channels, 127 tools in the header, 47 holders redacted, 8 segments under `opal-data-assets`. The page's own words: "14 groups, 127 tools ... 0 tool(s) declare no source".
- Rendered through the real `GatewayView` and the CSS of c66ca82952, whose built files equal the host's by sha256 (`pf9.AC2.sh`: index.html, routes.json, both assets; /health 200; no-identity `/` and `/gateway` 401).
- Real browser (Edge, viewport emulation): at 390 px `scrollWidth=390 innerWidth=390 offenders=0`; at 1280 px `scrollWidth=1280 innerWidth=1280 offenders=0`. First packet at 390 px: 561 of 390.

## 3. Evidence

`deliverables/2.0.0_SA_COO~MP/pf/evidence_pf9_served_d14445961d/`: `served_1280_top.png` (summary table: the eight segments indented under `opal-data-assets`) and `served_390_top.png` (the same at a phone width; table columns beyond the edge carry the scroll cue). Both read by the issuer before keeping and carry no index name, holder or account number.
NOT committed, on purpose: any full-page image or card (the real index names carry Schwab master numbers and this box's client-data check is not running, row Z-S63) and the body JSON (deleted).

## 4. What this does NOT claim

- The long-name Indexes paragraph at 390 px is measured (no sideways scroll) but its card images are not in the packet for the reason above; the issuer looked at the top of the page only.
- Andrew's own signed-in look (call 21d9) has not happened.
- The page's group counts (for example `opal-data-assets` 5 tools beside 19 across its segments) are the handler's semantics as ruled earlier; not re-judged here.
