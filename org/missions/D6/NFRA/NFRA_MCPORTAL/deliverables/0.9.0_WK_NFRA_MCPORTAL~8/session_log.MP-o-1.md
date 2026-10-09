# session log -- 0.9.0_WK_NFRA_MCPORTAL~8 on NFRA_MCPORTAL.TO-MP-o-1

- Tree OK on wk-NFRA_MCPORTAL-cp2-8. Premises re-grounded: admin_fabric.py exposes BUCKET, _s3_client, _roster, _list_keys, _read_records; the capture holds 931 activity objects and 4 open_deploys.json (open-deploys/1).
- Built app/admin_fabric_overlap.py, app/refs/overlap_rules.json, tests/test_admin_fabric_overlap.py in commit 638b8ae057. No other file touched.
- Real capture, hours=6, now pinned 2026-10-09T08:00:00Z: 31 overlaps (INFRA 1, CODE 3, TOOL 1, RECORD 18, APPEND 8); tf:transcripts rated 60, no open deploy names it in the capture.
- Route line for the issuer: Route("/fabric/overlap", admin_fabric_overlap.overlap, methods=["GET"]) in app/admin_api.py.
