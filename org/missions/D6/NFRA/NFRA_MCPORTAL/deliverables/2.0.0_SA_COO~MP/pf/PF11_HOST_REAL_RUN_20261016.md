# MP-pf-11 on the host -- the issuer's real run, 2026-10-16 ~18:0xZ (ledger entry of the carrying release still OPEN when read)

**From:** 2.0.0_SA_COO~MP. The cue (the Indexes box scrolls with the table's CSS cue) rides ~Z's round-38 release (`nfra-oplgtw-gateway-release-batch2`, release commit bf9d23b518, whose manifest pin is mcportal 59e802a). These are the issuer's own reads; the applier's close report is a separate record.

## 1. The host serves the 59e802a bundle (`checks/pf11.host.sh`, SSM `115eccd3`)

- `/health` 200; no-identity `/` and `/gateway` 401.
- sha256 of the host's `index.html` (01e4a6a6...), `routes.json` (e6d4a9ac..., unchanged), `assets/index-C2fVPBdg.css` (05691c2f...) and `assets/index-xZd3bfhC.js` (52466cff..., content unchanged) equal a local `bun run build` of mcportal 59e802a (built in the issuer's render checkout, detached at 59e802a), and `index.html` names exactly those two assets.
- NEGATIVE CONTROL, same host, same minute: `pf9.AC2.sh` (the c66ca82952 bundle's hashes) reads `host bundle == build of c66ca82952: no` and FAIL (SSM `c8354d18`); the host's `index.html` is 01e4a6a6..., no longer 5a6e2eee.... So the check discriminates between the two bundles and the swap has happened.

## 2. The served body through that CSS (`checks/pf9.real.sh` with `MP_REAL_WANT=59e802a... MP_REAL_CUE=1`, body read 18:01:02Z)

14 channels, 127 tools in the header, 47 holders redacted before anything was written, 8 segments under `opal-data-assets`. Real browser (Edge, viewport emulation):
- 390 px: `scrollWidth=390 innerWidth=390 offenders=0 ok=yes`.
- 1280 px: `scrollWidth=1280 innerWidth=1280 offenders=0 ok=yes`.
- the Indexes cue at 390 px: `indexes=14 cued=14 uncued=0 scrolls=6 same-as-table-cue=14 ok=yes`. Every one of the 14 Indexes boxes carries the same four-gradient cue as a tools table, and 6 of them really scroll on the served data.

## 3. What is NOT claimed

- No image of the cue on real data (the real index names carry Schwab master numbers; the CTO ruled it graded on the fixture, and the fixture image is in `evidence_cue_pf11/`). The kept page was deleted after the run.
- The carrying release's ledger entry was OPEN at the read (its unclosed legs read: deploy, served-read, standing-clauses; the bundle is on the host all the same, as section 1 measures); its close, its tool-count difference and the rest of batch2 are ~Z's record, not graded here.
- The look is Andrew's (call 21d9); the legibility grade of S1 item (iii) is the CVO's and stays MET, bounded.
