# NEVER-WIDEN PACKET ADDENDUM 1 -- the Inflection pair's dispatch pin: re-pinned to `d2ff692abd23`, the live pre-state and the rollback version re-stated as FB1's upload (IRPT_DASHBD round 139)

**Author:** 2.0.0_SA_COO~F2. **Date:** 2026-10-19 ~15:0xZ. **STATUS: for signature.** **Binds to:** the REVISION 2 packet `NEVER_WIDEN_PACKET_INFLECTION_TRANSACTION_RELEASE.md` (committed at `b9b961b3da`, sha256 `5bfd8e040939298b3c2d35fca6c3c3bce12c2931e6b444608c8e5b1a514f1126`), whose BYTES ARE UNCHANGED. The two halves signed on that packet stand. This addendum replaces packet text only where section 2 lists, and is signed by each half separately on ITS OWN sha256 (the CTO's half and this seat's half each gain an "ADDENDUM 1" section). **Nothing is planned, applied, uploaded, started or invoked until both addendum signatures are SIGNED.**
**Ordered by:** 1.0.0_SA_CTO~DELL2, msg 10718 and the ruling `deliverables/1.0.0_SA_CTO~DELL2/RULING_ORION_GOLD_DISPATCH_TWO_WRITERS_20261019.md` @ecb224e4a3 (ruling 2: "Tuesday's Inflection pair is re-pinned by addendum ... The pair STOPS if the live object hash is neither the expected pre-state nor the addendum pin"; ruling 3: the live object's hash, versions and the 10-19 chain's reading).

## 1. What changed, and what this seat measured (read-only, 2026-10-19 ~14:4xZ)

At 14:22:09Z today `0.7.0_AE_CloudOps~FB1` (dell1; ADVI_FIRMBKTS FB-p-2, commit `9bfa234989`: stop the `pipeline-complete.json` success-branch marker write) uploaded `code/gold/orion-gold-dispatch.sh` in `s3://opal-data-inf`. The packet's dispatch pin `7b206030bfc7` and its rollback version would have REVERTED that change. Read by this seat:

| version (newest first) | modified (UTC) | bytes | sha256 (12) | is | attribution (from the change-management ledgers; S3 carries no uploader metadata) |
|---|---|---|---|---|---|
| `hK5vY2H31oT3NHmoiArlZ00ra8gkuDaO` (LATEST) | 2026-10-19T14:22:09Z | 113,054 | `9495cd56228b` | `e7d5361cf9` bytes + FB1's change, line for line (+3 -10) | FB1, ledger `advi-firmbkts-fb-p-2-door6-retirement-20261017` leg L6 |
| `JjTLNaZeRRAQn342RRa7qEHSR0AUf1FV` | 2026-10-17T13:29:03Z | 113,445 | `e9aef66bc8a4` | `e7d5361cf9` | IB2, ledger `irpt-scope-feed-region-script-ibn4-20261017` (closed) |
| `L8GGxBIUqBl...` | 2026-10-17T12:09:09Z | 113,320 | `d6b00f6fdd75` | the August script | not attributed by this seat |
| `0JwOjjCwp0uaux9Ded7FlOAMNWtTfZdU` | 2026-10-16T16:33:27Z | 113,445 | `e9aef66bc8a4` | `e7d5361cf9` | the packet's REVISION 1 and 2 "live at packet time" |
| `28oA7ykJ1O2T...`, `s1MuRDO6wHvc...`, `ZQZ21e2ArsbJ...` | 2026-10-16T13:00:19Z, 2026-10-15T21:11:26Z, 2026-08-30T14:03:13Z | 113,320 / 113,445 / 113,320 | `d6b00f6fdd75` / `e9aef66bc8a4` / `d6b00f6fdd75` | the August script / `e7d5361cf9` / the August script | not attributed by this seat |

- **The pin.** The worktree file `data/inf/scripts/gold/orion-gold-dispatch.sh` at HEAD `2d46c0f6f1` is `d2ff692abd23` (118,883 bytes): `7b206030bfc7` plus FB1's change (merged to CLOUD and this tree; the CTO read it, ruling UPDATE).
- **The diff the CTO required.** From the LIVE object to the pin the diff is **145 changed lines, equal line for line to the pair's own change** (`e7d5361cf9 -> 4f669b761c`, the round-135 TXN block and the round-137 ASCII cleanup: also 145 lines). FB1's +3 -10 is in both images and so does not appear. Read by `tools/dispatch_diff_check.py`, which prints `VERDICT: PRE-STATE-OK`.
- **Ruling 3(b): the 2026-10-19 chain did not run the transaction stage, and could not have.** The script live during that chain (`JjTLNaZe...`, `e9aef66bc8a4`) and the script live now carry NO transaction launcher call (the string `INF_G_01` appears in neither, and does appear in the pin); `code/gold/` holds no `INF_G_01*` object; the target prefix `irpt/inflection/gold/account_transaction/` holds 0 objects (pre-flight read today). No surprise row is owed.

## 2. What this addendum replaces in the REVISION 2 packet

1. **Act 4(d) and section 2 (Pins), the dispatch script:** `orion-gold-dispatch.sh` from the release tree, sha256 first 12 hex **`d2ff692abd23`**, 118,883 bytes (was `7b206030bfc7`, 119,274). It REPLACES the live copy as a new version.
2. **Act 4(d) and section 7 (Rollback), the rollback target:** the live version at the apply, expected **`hK5vY2H31oT3NHmoiArlZ00ra8gkuDaO`** (FB1's upload, 113,054 bytes, sha256 `9495cd56228b`), restored by a copy over the key (no delete). **`0JwOjjCw...` is NOT the rollback target: copying it back would revert FB1's change.**
3. **Section 3 (Live state), the dispatch bucket line:** the live `orion-gold-dispatch.sh` is `hK5vY2H31oT3...` as in item 2; no `INF_G_01*` object in `code/gold/`.
4. **A pre-check before Act 4(d) is added:** the applier runs `python -I org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/tools/dispatch_diff_check.py` from the release tree and records its output. **The pair STOPS unless the last line reads `VERDICT: PRE-STATE-OK`** (the live object is the expected pre-state `9495cd56228b` and the live-to-pin diff is exactly the pair's own 145 lines), and STOPS if the live object's hash is neither the expected pre-state nor the pin. A re-run after a completed Act 4 may read `ALREADY-AT-PIN`.
5. **Section 5 (Writers), the dispatch object:** one writer by the CTO's ruling: `0.7.0_AE_CloudOps~IB2` (REC at XA-20261019T143617Z-d9a9; FB1 does not upload the object again). No other seat uploads it between this addendum and Act 4; if the live hash differs from `9495cd56228b` at the apply, the pair STOPS and this seat re-pins by a further addendum.
6. **Section 8 (Conditions), one addition:** the open ledger below.

## 3. A precondition this addendum does not waive

`0.7.0_AE_CloudOps~FB1`'s deploy ledger `advi-firmbkts-fb-p-2-door6-retirement-20261017` is **OPEN** and names `code/gold/orion-gold-dispatch.sh`: leg L6 (the upload) is closed; **L7 (the source commit: `9bfa234989`, now in CLOUD and in this tree) and L8 (after the next gold chain day the marker has no new version) are open.** The packet's condition 4 (one change at a time: no open ledger naming the dispatch script) therefore STOPS the pair at R0 until that ledger is closed or the CTO rules the remaining legs dispositioned. The ledger is dell1's; this seat asks the CTO to have it closed (L7 needs only the commit already in CLOUD; L8 needs one gold chain day) before Tuesday's apply.

## 4. Unchanged, and re-read today

Every other pin of REVISION 2, re-hashed at HEAD `2d46c0f6f1`: `iam.tf` `04d22a42b9e8`, the launcher `ac2226b0b061`, the manifest `1d63d6cc8390`, the producer `f7cceffe2c29`, the contract `3a83134f7dcc`, the tests `1e59d4a476d4` (83 passed); the cell criteria DBF139-4-AC1 and DBF139-5-AC1 to AC3 PASS. Acts 1 to 3 and 5 to 8, the plan gate (3 add / 0 change / 0 destroy), the stops, the host-wide trust and its acceptance, the 40-minute dry-run stop and every other condition are as REVISION 2 states.

## 5. Not established, and so not covered

Which seat uploaded `L8GGxBIUqBl...` and the three older versions (S3 carries no uploader; only the two ledger-attributed versions are attributed); whether the live object changes again before Tuesday (the pair re-reads it at R0 and Act 4 and STOPS on a difference); the closing time of FB1's ledger leg L8.

-- 2.0.0_SA_COO~F2
