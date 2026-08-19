# MSTR~Z seat plan — S10 split, four site-Z workstreams (2026-08-19 19:1xZ)

**Frame:** laptop MSTR 2fe512a8 (COO split CONVERGED @a02f9ff5a4). TOs arrive individually
through laptop MSTR with (prd, workstream, head_version); never-implicit. **GATE: nothing
lands before the 08-20 07:00 WDAC acceptance this seat owns.** Spawn-on-TO, not now.

| ws | work | seat | why this seat | new session? |
|---|---|---|---|---|
| D9 | Tax-SMA whole-assessment (repo/records/AWS-reads + SharePoint local-disk leg, ZERO applies; 0.5.0_AE_OpalETL~A stall resolves inside the TO text) | **0.4.0_DS_ClientPlatform~Z** (folder exists) | client/tax domain = DS ClientPlatform lane; assessment-class = records+reads wheelhouse; keeps the 0.5.0 lane free for D7. If the TO text names the 0.5.0 family for ~A continuity, swap D9/D7 seats — both mappings work, the TO disposes. | YES (1) |
| D7 | TO-A+TO-C Analyst intake at the box (box identity + Teams presence + persistent memory; intake schedule shaped 07:00-ET-light) | **0.5.0_AE_OpalETL~Z** | the Analyst-program family on this box (OPAL_ANALYST atom-decomp ran CVO~Z + 0.5.0_AE_OpalETL~Z); persistent-memory conventions exist in-family | YES (2) |
| D6 | TO-C SharePoint binding + TO-D BBG standing read (SITEZ-ONLY: opal-gateway-bbg identity) | **0.0.3_BG_BBGTerminal** (existing seat) | the gateway-bbg identity is registered ONLY there; standing-read + binding is low-load and duty-adjacent to the concierge charter. Corroborate liveness at TO arrival (event-driven seats read broker-absent by structure) | NO — rides existing |
| D2 | parity harness-build + classification analytics + census-report authoring (S3 device-neutral, zero applies; probe PULL leg stays laptop) | **0.8.0_AE_CloudComp~Z** | harness/census/analytics is the CloudComp lane exactly; prior ~Z seats precedent | YES (3) |

**Census vs ceiling:** me + BG (existing) + 3 new = **5 sustained live sessions, ONE slot
spare** (reserved for D3's spec leg) — exactly the budgeted shape against the 6-sustained /
8-burst ceiling. D7's intake schedule and all heavy work keep 07:00 ET ±30m light.
**Nothing here is TF-apply class** (and site Z is not a TF-apply site — flagged in the
device answers).

**Spawn mechanics per seat:** /mstr-spawn on TO+GO arrival; each seat registers full
suffixed serial, arms /watcher once, zero crons; lane logs/deliverables go in the BASE
folder lane-prefixed (site-Z owned-paths rule); D9/D7/D2 seats get the WDAC census pointer
+ the pip-owned-pins note in their first message (env law for cma).
