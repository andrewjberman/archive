# G-O READ-BACK -- NFRA_OPLGTW `OG-r-1` (the first Gateway release), for MDPF_TAXSMA `TX-r-2`

Author: `2.0.0_SA_COO~O`, re-seated 2026-09-21 ~02:0xZ on Andrew-direct (via 0.0.0_AB_MSTR 98889) for two acts, scope
per 1.0.0_SA_CTO msg 98896 as corrected by 98911. Measured 2026-09-21 02:1xZ-02:5xZ.

G-O, verbatim from `org/missions/D8/MDPF/MDPF_TAXSMA/decompositions/MDPF_TAXSMA_DECOMP.md` s.6: *"NFRA_OPLGTW's first
release (`OG-r-1`) deployed and read back"*; its carrier: *"one Gateway host, one release in flight; `OG-r-1` carries
the OAuth cutover and must not be interleaved"*; owner `2.0.0_SA_COO~O`; holds `TX-r-2`.

**This record states the gate's INPUT. It does not grade `TX-r-2`.** Whether it satisfies `TX-r-2`'s first acceptance
line is read at that cell, by its issuer `2.0.0_SA_COO~T`, against the cell's own text.

---

## 1. DEPLOYED -- read from the host, not from the order

| fact | value | instrument |
|---|---|---|
| deployed commit | `1764e54a16b7bb12d34b36eec7866589b6ea785e`, deployed 2026-09-18T05:58:16Z by `0.9.0_WK_NFRA_OPLGTW~2` | `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway` at HEAD, written by manifest commit `ef11656176` |
| later Gateway releases | **none**: `ef11656176` is the only manifest commit since 2026-09-17 | `git log --since=2026-09-17 -- infra/aws/ec2/EC2_MANIFEST.json` |
| host service | `active` | SSM `ac4c9695-ed88-4fa9-9b6b-ceb13eb122f4` on `i-07dccb1615503ac99`, Success |
| entitlement guard on host | `/opt/opal-gateway/app/data_entitlement.py` present, 27085 bytes, mtime 2026-09-18 04:20:27Z | same SSM command |
| Schwab flag | **OFF**: `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph` | same SSM command. The same line lists three other integrations, so this read could have shown `schwab` if it were there (positive control) |

## 2. NO RELEASE IN FLIGHT -- the sequencing half of G-O

Open-deploy entries under `org/critical_paths/.open_deploys/`, read in **every** live worktree (`git worktree list`,
17 trees, `ls-tree` at each HEAD), plus the shared tree on disk (10 entries). Entries naming gateway, oplgtw or taxsma:
**0 in 16 of 17 trees and 0 on shared disk.** The 17th, `C:/tmp/wk-oplgtw-2r2` (OG-r-2's drained worktree, HEAD
`63571440b1`, an ancestor of CLOUD), shows `nfra-oplgtw-gw-runtime-deleteitem.json` as OPEN. That tree's HEAD is older
than the close: on CLOUD, the entry was opened at `c298ed4b68` and closed at `df9e05cb55` (0.7.0_AE_CloudOps,
"APPLIED, EXERCISED"). It is not in flight.

Known concurrent writer (notice, not a release): `2.0.0_SA_COO~T` msg 98920. `TX-g-2` may write
`infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` and does not deploy. Act 2 below writes nothing, so there is no merge
between the two.

## 3. READ BACK -- terminality and the three non-PASS criteria, each with where its disposition lives

`OG-r-1` `<status>complete</status>`, flipped at `be38a0f475` under the order's flip bound as amended per R-58 item 1:
terminality is read from the **proof**, never from the status word (`.tools/surprise-row-gate.py` `_proof_terminal`).
The proof instance is
`org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/NFRA_OPLGTW.TO-OG-r-1.first-release-cutover.proof_of_spec.json`:
**21 criteria, 18 PASS, 2 FAIL, 1 N/A-BY-CONSTRUCTION** (read from its `acceptance` array, all 21 ids).

| criterion | graded | disposition, by whom | residual |
|---|---|---|---|
| `OGR1-AC4` digest parity | **FAIL**: 9 of 68 files differ (CRLF vs LF blobs; the deploying worktree has `core.autocrlf=true` and `.gitattributes` `eol=lf` covers `*.py` only) | **R-56 item 3, `1.0.0_SA_CTO`** (msg 97864 @`853a37edd1`; text in `org/tier1_exec/1.0.0_SA_CTO/deliverables/SELF_DRIVE_LGIC_RULINGS_20260917.md` "R-56"): FAIL stays as written; the class fix is a separate act with its own printed blast radius | row `NFRA_OPLGTW-W2-S8` |
| `OGR1-AC9` error count vs baseline | **N/A-BY-CONSTRUCTION**: OG-p-1's `BASELINE.json` has no error-count metric | **R-56 item 4, `1.0.0_SA_CTO`**: graded not-evaluated | none |
| `OGR1-AC10` previous-release restorability | **FAIL**, 4 of 5 checks: the recorded prior release `7bd89b5d71` lacks `app/data_entitlement.py`. The content-hash mechanism passed (recorded = read-back = `1556d6e979`) | **R-56 item 2, `1.0.0_SA_CTO`**: the remedy landed at the point of use. `infra/aws/ec2/opal-gateway/runbooks/SCHWAB_PILOT_RUNBOOK.md:252` says in bold that this release **has NO VALID ROLLBACK** under s.7.2, and `OGR1-AC19` PASSES on that statement (7 ever-deployed commits censused, 0 valid candidates) | row `NFRA_OPLGTW-W2-S7`, ARMED. The ordinary rollback, s.7.1 (disable the flag), is unaffected |

**Scope of that column:** all three dispositions are `1.0.0_SA_CTO` rulings made at the round-analysis step. **No
`3.0.0_SA_CVO` L9 adjudication of NFRA_OPLGTW round 1 exists.** The round is not terminal, because `OG-v-4` and
`OG-v-5` are pending on G-C..G-F. 98911 s.2(a) corrects 98896's pointer to a CVO L9 on these grounds.

**Read-back verdict: DEPLOYED AND READ BACK.** The host runs `1764e54a16` with the guard present and the flag off. No
Gateway release is in flight. Every non-PASS criterion has a named disposition, and the one live exposure (no binary
rollback) is disclosed in bold in the runbook the operator would use.

---

## 4. ACT 2 -- the five Schwab tools for NFRA_MCPINDEX FWD-3: NOT ENABLED, and not enable-able by this lane

The five tools register only when `schwab` is in the host's `ENABLED_INTEGRATIONS` (runbook s.7.1; `app/config.py`).
Measured above: **OFF**. Nothing about the flag is unknown, so this is a gate question and not a build question.
Each of the following stops the flip, and none is this lane's to clear:

1. **The spec forbids it.** `NFRA_OPLGTW_DECOMP.md` frozen rule 9: *"The feature flag stays off and profiles stay
   pending except where G-C and G-E record otherwise."*
2. **G-C is absent** at HEAD (`deliverables/1.0.0_SA_CTO~A/G-C_CONTROLLED_IDENTITY_AND_GRANT.md`: not tracked, not on
   disk; checked against a positive control on a known-tracked file). G-E, G-D and G-F are absent too. G-C's closing
   owner is `1.0.0_SA_CTO`. Its evidence comes from the identity administrator, `0.7.0_AE_CloudOps` (Andrew-direct
   2026-09-20 ~18:0xZ, @`768e6df290`, *"we will handle that shortly"*). It is a person's act against the live
   tenant.
3. **Capacity is measured INSUFFICIENT.** `OG-r-2` AC8, `CAPACITY.json`: the export peaked at 270581760 bytes against
   the 268435456 job cap. R-OG-22 is open at `1.0.0_SA_CTO`'s L4 (is 250000 rows / 50 MiB a consumer requirement?).
   The PRD's own enablement text requires benchmarking the candidate before enablement.
4. **Registering five tools changes what the live Gateway serves**, on a release with no binary rollback. That needs
   Andrew's word; it cannot be inferred from a scope message.

So V.5 in `NFRA_MCPINDEX_PRD.md` stays unmet. As that PRD itself states, this gates FWD-3's EXERCISE only, never
NFRA_MCPINDEX's halves or its L5. **Unblock path, in order:** G-C recorded (1.0.0_SA_CTO + 0.7.0_AE_CloudOps) ->
OG-v-4 graded -> R-OG-22 ruled -> Andrew's word to flip the flag through `safe-ec2-deploy.sh` under a change-management
entry. None of that is this seat's, and per Andrew-direct 02:4xZ (MSTR 98918) this seat closes on this report.
