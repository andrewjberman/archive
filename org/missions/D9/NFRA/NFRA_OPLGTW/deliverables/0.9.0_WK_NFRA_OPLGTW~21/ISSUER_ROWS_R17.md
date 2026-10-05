# ISSUER_ROWS_R17 -- the issuer's seven OPEN rows (OG-ar-2)

Pin CLOUD @4e84fd3f2e. No remediation row edited. Source of truth: `ISSUER_ROWS_R17.json`.

## remediated_by -- 0
None whole. W6-S2 is remediated for dim_position and dim_asset (OG-gr-3 + OG-rl-5, served 4b6b823fae) but narrowed to dim_balance, so it sits under moves_when.

## closure -- 0

## moves_when -- 7
- W6-S2 (narrowed to dim_balance): GR4_BALANCE_GRAIN.json reports 0 duplicates -> close; duplicates -> CTO rules a grain. Actor COO~O / CTO~O.
- W1-S9: a registry row or R20 entry Andrew acknowledges; fires only on a plan adding one of the three role names. Re-measured: 0 files in infra/logic name them. Actor 1.0.0_SA_CTO~O.
- W2-S6: Andrew's word to delete 8 probe items (or a CTO keep-as-fixture ruling). Re-measured read-only: 8 of 386 items. Actor 1.0.0_SA_CTO~O relays; CloudOps deletes.
- Z-W13-S5: MDPF_CANON fixes 16 key lines, then one `git add --renormalize`. Re-measured: still i/crlf, -text. Actor MDPF_CANON then COO~O.
- Z-W12-S7: DATED: the operator re-authorizes the upload client before ~2026-10-18. Actor Andrew; COO~O records.
- S63: moves when the pilot-walkthrough grading cell re-enters; the issuer records the seal of record. Actor COO~O.
- Z-W15-S31: next order touching tr.AC1.sh rewrites arm 4 to 50 keys. Re-measured: "48 keys" at lines 7 and 32. Actor COO~O.
