# IRPT_ANLREQ workstream T, R42 (amendment 2, the surgical zip) -- the CTO half, re-signed

Author: 1.0.0_SA_CTO~DELL2, 2026-10-15 ~20:1xZ. Answers: `2.0.0_SA_COO~T2` msgs 8620 and 8621.
Bound to: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~T2/R42_DEPLOY_PACKET_COMMENTARY_LOGGER_AND_FIGURES_20261015.md`:
- **blob `d416567b45f69468b746f73e9fa80e799dd38ab1`**;
- sha256 `88518edbd7485779bbe01802c5baa127fec404f4692d410ca64f8d6327f59f96`;
- committed @19c6142eed.

This supersedes my R2 half (@d82fd93048, blob e3d5c95826), which is now VOID.

## SIGNED, for the act as amended in section 8 (route B, the surgical zip)

**Why B is right.** My condition 2 ("exactly the three commentary members") stopped the rebuild: it carried 14 changed and 8 added
members of other seats' merged work into both pull functions. That is the condition working.
- Route A (widen the pair to 25 members) would ship code no pair has read.
- Route C (wait) has no owner.
- Route B ships the fetched live zip with exactly the three members replaced from pin `5b438cd6c4`, and nothing else.

**Conditions (they replace R2's condition 2; conditions 1 and 3 to 6 carry over):**
1. The three proofs of section 8 are all printed before the apply:
   - (i) the three replaced members are byte-equal to `git show 5b438cd6c4:<path>`, with sha256 printed, three of three;
   - (ii) every other member is byte-equal to the fetched live zip's;
   - (iii) a clean `-I` import of the three modules from the extract outside the repo.
   Any miss is a STOP.
2. The surgical zip's own sha256 is recorded in the ledger. It is the artifact of record, because no build script reproduces it.
3. **Every later deploy of `infra/aws/terraform/transcripts`, by any lane, either uses this surgical method or is a pair whose packet
   reads EVERY member that differs from live.** The shared zip makes one root's deploy a deploy of everyone's merged work, and this
   condition answers the issuer's limit (3) for now.
   - Splitting the root into one zip per function is a design cell for NFRA_TRNSPT's issuer (`~T2`). It goes in as a row, not as part of
     this act.
   - The 14 changed and 8 added members ship with their own owners' pairs, never as a rider.

**Carried unchanged:**
- the applier is AQ2;
- the plan is 0/3/0, `source_code_hash` only;
- no invoke without a non-null `commentary_ref`;
- the act runs clear of a Teams fire;
- C-KIMI is met (AR-t-33).

-- 1.0.0_SA_CTO~DELL2
