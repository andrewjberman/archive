# AMGT_RESAPP round 106, AIFILL workstream -- drain-end packet (L8), `2.0.0_SA_COO~R2` to `3.0.0_SA_CVO`

**STATE: FILLED 2026-10-15 ~21:1xZ. All eight orders terminal (`gr-1`..`gr-8`).** Keys: the CTO's round-105 AIFILL list, issued at 2026-10-14 under this lane (`~R2`). `~R1`'s packet (`deliverables/2.0.0_SA_COO~R1/round106/DRAIN_END_PACKET.md`) covers `bm-1`..`bm-5` and does not cover these.
Every head below was read as an ancestor of `box/dell1` HEAD `df2ca8f0a9` with `git merge-base --is-ancestor`. Push state: LOCAL (origin `box/dell1` read `7c7b412279`, which is not this HEAD).

## 1. Orders and cells

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-gr-1` | whole-text real sentence ends and joined answer segments | complete | worker ~450, merged `0cea476a94` (re-proved after a reopen), VALID; AC1 28 of 28, AC2 98 passed, AC3 12 of 12 |
| `AMGT-gr-2` | fetch a cited source and say what happened to it | complete | worker ~451, merged `f57f6e049a`, VALID; AC1 21 of 21, AC2 99 passed; row W451-S1 ruled (a 2xx non-text body is UNSUPPORTED) |
| `AMGT-gr-3` | the grounding step checks every sentence against its sources | complete | worker ~452, merged `209635af42`, VALID; AC1 18 of 18, AC2 47 passed |
| `AMGT-gr-4` | the contract carries a grounding record and can refuse a block without one | complete | worker ~453, merged `0516c67e6d`, VALID; AC1 26 of 26, AC2 534 passed, AC3 FC-2 43 of 43 and FA-1 31 of 31 |
| `AMGT-gr-5` | the orchestrator grounds every filled block; the run command supplies the fetcher | complete | worker ~454 (re-seated on AMENDMENT 1), merged `9d9642d362`, VALID; AC1 20 of 20, AC2 755 passed |
| `AMGT-gr-6` | the five builders use the shared cut; the bio never restates the pack | complete | worker ~455 (re-seated), merged `9e8272e0f6`, VALID; AC1 15 of 15, AC2 179 passed, AC3 four controls YES |
| `AMGT-gr-7` | the About-this-data panel reads the AI-fill input it renders | complete | worker ~456, merged `1bcb4a12e0`, VALID; AC1 11 of 11, AC2 green with 0 regressions, AC3 2 files. Portal branch `cand/dell1/aifill-provenance` @`31337460` on PROD `7db035e4`: LOCAL, NOT pushed, no approval row |
| `AMGT-gr-8` | the contract requires the grounding record; the tests follow | complete | worker ~457, merged `2d39f15e66`, VALID; AC1 10 of 10, AC2 774 passed, AC3 39 passed |

Issuer amendments (the gate limb that graded each: none, existing orders, no new criteria): `gr-5` AMENDMENT 1 @`69aa86048d`, `gr-6` AMENDMENT 1 @`6a3ed75519` with grant @`881c17420d`.

## 2. The issuer's real run

`lib.research.aifill.revalidate` over the 95 stored round-105 documents, run at the merged head: checked 95, passed 0, refused 95, every refusal reading "grounding record is missing". File: `deliverables/2.0.0_SA_COO~R2/round106_aifill_close/REVALIDATE_REAL_RUN_20261015.json` (17,634 bytes, sha256 prefix `898ffad8f99c4642`).
Drain checks at the merged head: aifill suite plus api serve test 813 passed; ruff clean.
**What the run says and does not say:** the stored round-105 documents were written before the contract required a record, so 95 of 95 refusing is the contract working on old data. It is NOT a reading of any freshly generated block. No block has been generated and grounded under the new contract by this seat.

## 3. Rows

- W450-S1 (a round-105 test pinned the old no-separator join): DISARMED, one assertion updated (`ad9eaa7fc8`).
- W451-S1 (a 2xx image or zip body reads OK with binary text): goes to the CTO's round-107 list beside items (g) and (h).
- W456-S1: tooling note, no act.
- W452-S1..S3, W454-S2, W457-S1..S3: OBSERVATIONS, ruled in the drain commits, no act.
- Channel disposition: `a0c8143b39` (D1-S33).

## 4. Held and open

- **The AI-fill hold stands.** Nothing in this workstream lifts it; that is the CVO's five-new-name re-read, which I have not run and do not predict.
- `gr-7`'s portal change is unpushed and unregistered; this seat registers it after the CVO's re-read is MET. It is an Opal-internal page by the order's text; the class is not re-measured here.
- Not mine: `round-close-check` reads REFUSED on `bm-5` AC5 (the CVO's grade, ADJUDICATION_v131), per `~R1`.
- Left on disk: none from this lane that I measured; one crashed worktree init (stale `index.lock`, 2026-10-14 02:21) was repaired for `gr-5`.

## 5. Ask

Send the L10 slug. Nothing is owed from this seat to unblock REMEDIATION_v44 except this packet.
