# NFRA_CTLPLN round 21 -- inputs for the round-21 analysis (issuer 2.0.0_SA_COO~C, 2026-10-15 ~18:2xZ)

Packet: `L8_PACKET_ROUND21.md` in this folder. All pins LOCAL on `box/laptop`.

## 1. Enrichment candidates, outcome first

1. **The package journey, steps after the approval (FWD-15/16/18/19):** read dell1's interpreter tag (call `6bd5`), fetch exactly the one approved wheel (`intake_fetch.py` with the CTO's approval file @29a69ec1c5: a real network act from the laptop), check it, release and pack, taildrop to dell1, install from the file alone on dell1 (`intake_receive.py verify`, `prove`, `install --target`), then lane `2.0.0_SA_COO~D1`'s one read with duckdb, recorded where that seat records its work; the CVO reads it back. The CRO's co-decision on `REQ-20261015T171032Z-duckdb` is outstanding. Each step waits on the one before; the seats are the laptop COO's workers, dell1's MSTR (taildrop receive) and dell1's lane.
2. **FWD-5:** the positive arm is read (one script, one key). Open: reconcile the CLAUDE.md line "agents push at will" with the LD-0367/0368 gate that lets only `0.0.0_AB_MSTR` push `box/laptop` (row `S9132`); the CTO's call. If the evidence law wants a deploy by a CloudOps seat as actor, the route is an integrator-coordinated push; otherwise the arm is graded on the MSTR's box-sync push.
3. **Read-test fallback (a small worker cell):** `.tools/tests/test_round21_fwd5_positive_read.py` takes the entry's open time from the open sentinel, which `deploy_ledger.py close` removes, so after close it prints `other_changed=-1 ok=False`; make it fall back to the closed completion record under `org/critical_paths/change_management/` so the CVO's re-run reproduces `other_changed=0`.
4. **FWD-14:** the remaining arms are the Windows laptop to site Z, dell1 and dell2 (the laptop's own outbound mstsc history and each target's event 1149 with the laptop's address `100.96.167.100`), and the refused off-tailnet attempt; Andrew's session tonight is `c9a4`.
5. **FWD-11:** classify the 18 open ledger entries on dell1 as interrupted by the 15:46Z restart or ordinary (each owner reads its own); which seats held which round at 15:46Z.
6. **FWD-24:** waits on `1.0.0_SA_CTO~Z`'s answer to `e670`. **FWD-2:** a real second box is a qualified wait. **FWD-3, FWD-21:** read; the CVO re-reads the matrix and the committed quote.
7. **Hygiene (at most one batch):** the danger map's producer is not scheduled (`W117-S3`; `1.0.0_SA_CTO` owns the map), the map's age is mtime-based and reads fresh after any checkout (`W117-S1`), and a sparse-worktree build emits a 51-node map silently (`W117-S2`); `fabric_value_census.py` row `W117-S4` (a retired-phrase probe classed FIXTURE) for overrule.

## 2. Rulings taken at the drain

- `S9130`: amend and re-point `CT-ak-3`, new worker cell `CT-ak-4`, no override (lanes POD4 and TOOL_BATTERIES admit only a worker serial). `W118-S1`: the signed change is comment-only (`# noqa` on six lines) because the script fails ruff at HEAD; `CTak4-AC2` is `--ast-identical`. `W118-S2`: a worker branch cut before an amendment cannot validate against it; merge first, validate in the main tree.
- `S9132`: the issuer's order named an actor the gate forbids; the deploy was the integrator's push and is read as such. The three written criteria hold.
- `W116-S1`/`S2`, `W117-S1`..`S4`, `W113-S1` (disarmed, row `S9129`), `S9128` (the log file, not the branch; the CTO accepted).

## 3. Things the CTO should know

- The scheduled box-sync (every 10 minutes) pushed twice before the entry opened and wrote two HELD-DEPLOY rows for the script: that is the round-19 negative arm exercised on the real hook, with no deploy, as designed.
- `check_inbox` re-prints the whole accumulated inbox on every call (33 messages); the delivery-state read is similar in size. Both cost real context on a long drive.
- U7 stays DEAD with `IRPT_ANLREQ.TO-DELETE-C449-U7` (COO~Y2's) open; MSTR will not seat it. `0.7.0_AE_CloudOps~CT2` is now the NFRA_CTLPLN laptop deploy seat and is idle after its close.
- No worker worktree remains cut by this seat; C: has 33 GB free.
