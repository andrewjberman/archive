# NFRA_CTLPLN round 19 -- inputs for the round-19 analysis (issuer 2.0.0_SA_COO~C, 2026-10-15 ~13:3xZ)

Packet: `L8_PACKET_ROUND19.md` in this folder. All pins LOCAL on `box/laptop`.

## 1. Enrichment candidates, outcome first

1. **FWD-16 live use:** file one real request and get one approval and one refusal from the CRO and the CTO with `org/devices/intake/intake_request.py`, read back by a seat that was not part of them. Needs `4.0.0_SA_CRO` and `1.0.0_SA_CTO` to decide.
2. **FWD-19:** `intake_fetch.py` writes a device key into each fetch record (`W111-S1`, the issuer's), then the downloads reader answers per device; a waiting-lane entry for a Dell lane via `open-calls.py add`.
3. **FWD-15:** a Dell lane that really needs a package; `1.0.0_SA_CTO~DELL1` names it, then the fetch, check, taildrop, install and the lane's own run. **FWD-18:** `kit_pip_no_egress.py wrap -- download six` on the laptop and on site Z (a site Z seat via `0.0.0_AB_MSTR~Z`).
4. **FWD-5 positive arm:** a signed change naming a script deploys exactly what it names; needs a CloudOps seat and an open signed change. `D1-S8` (the issuer's) fixes the deploy set bound.
5. **FWD-7:** the one real SPLIT (`.tools/safe_deploy_core.py`, MDPF_SECCLASS on dell1 and IRPT_BCKEND on dell2, `W106-S5`) needs the CTO's ruling on one writer.
6. **FWD-2:** a real second exercise needs a real new box; none is in sight. The 2 tools not reached need a way to point them at a register copy.
7. **FWD-27:** the person arms (rc, muse, laptop account, off-tailnet, password-off) stay Andrew's and MSTR's.
8. **FWD-3 and FWD-24:** read when site Z acknowledges `XB-20261015T121713Z-e670`; the two FWD-24 answers are then compared.
9. **Hygiene (at most one batch):** the risk reflex's map lives in `comp-pulse`, outside `CT-ai-5`'s grant (`W110-S1`); the `.tsx` not-graded line landed in `safe-commit.sh` and `commit-gate.sh`.

## 2. Rulings taken at the drain

- `W106-S3`, `S4`: a directory claim against a file inside it is NOT-SAME-FILE (PRD FWD-7 ACCEPT: "change different files").
- `W109-S1`, `S2`: per-box logins from the CT-ab-7 order; the first run's `key_ok=0` was the default login, not a regression.
- `W108-S1`: my order's fixture path was not a deploy-gated tree; the worker's deploy-scope path stands.
- `W107-S2`: the grade element rides on the round-close output of the project (C-S16, C-S17).
- `W111-S1`: ARMED, a round-20 cell.

## 3. Things the CTO should know

- The CVO's 10-13 pins on FWD-2 (`FABRIC_ENUM` literal) and FWD-3 (open pair dell1 -> sitez) are stale.
- `test_named_commit_deploy.py` is broken on this box after case 7 (`ModuleNotFoundError: git_bash_resolver`).
- The diagnostic `ssh` calls of worker `~109` wrote host keys for site Z and dell1 into the user's `known_hosts`.
- An old untracked `org/devices/state/laptop/seats.json` (2026-10-08) was moved aside to make the merge land; the merged, tracked file replaces it.
- The four old `r18_batch_*` folders under Temp are still on disk (Andrew's word needed for recursive deletion); `CT-ai-5` found the batch test already cleans its own.
