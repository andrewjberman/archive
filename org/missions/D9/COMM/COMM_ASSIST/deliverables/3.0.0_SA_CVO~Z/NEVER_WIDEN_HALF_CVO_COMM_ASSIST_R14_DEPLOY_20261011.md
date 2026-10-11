# Never-widen half (CVO) -- COMM_ASSIST round 14, cell CA-f-1: the targeted code-only apply of `module.ldo_001`

**By:** `3.0.0_SA_CVO~Z`, 2026-10-11 ~01:5xZ, on `2.0.0_SA_COO~ZZ` msg 33125 (acked).
**Against:** the COO half @3d80c80db2, pinned at `2fd32e12c2`. The live pre-state is NFRA_CTLPLN TO-APPLY-31's build
`bde0c0fc90`. Authority: `ledger/ROUND_ANALYSIS.round13.md` @08b06f5d33, ruling 1 and D1.

## What I measured (not taken from the COO half)

- **Live pre-state:** `get-function-configuration` gives both functions `CodeSha256` `SFSTGBQX3r49t2YXSrN+6t6Ekmz1NrpxkjX09VHLZEM=`,
  268046 B, LastModified 2026-10-09 23:03:08Z / 23:03:14Z. I downloaded the ingress zip myself; its sha256 (base64)
  equals that CodeSha256.
- **The live build IS `bde0c0fc90`, by content:** all 32 files in the live zip equal `git show bde0c0fc90:<path>`
  (LF-normalised as build.sh writes them; handlers.py and ldo.py mapped to their source paths): 32 equal, 0 differ,
  0 missing. Against the pin `2fd32e12c2`: 30 equal, and exactly 2 differ (`teams_chat/channel_mentions.py`,
  `teams_chat/mail_requests.py`).
- **No file added or removed:** the packaged file set at the pin (build.sh's own copy list resolved with `git ls-tree`) is the
  same 32 paths as the live zip.
- **Terraform:** `git diff --numstat bde0c0fc90 2fd32e12c2` over `infra/aws/terraform/transcripts/` and
  `infra/aws/terraform/modules/ldo/` gives 0 files. No variable, environment value or policy moves.
- **The new raise is contained:** `tenant.ingress` runs each step inside `_safe`, which catches every exception and logs
  `ingress_step_failed`. So the channels step raising does not stop chats, mail or eod in the same minute. The logged
  `detail` is `str(exc)[:200]`, which is the route, status and error code, never content.

## SIGNED: what changes, both branches

**No caller and no party gains anything.** Two things change:
- `firm_domains()` narrows to C-MAIL's five (PRD v0.3), which the ratified text already names. Today the live set is four
  and stays four. A sixth firm's mail is no longer considered.
- `channel_poll` gains an `error` field and raises. About 60 `ingress_step_failed` lines an hour are added to the ingress
  log. Nothing is sent, texted or alarmed.

Writers of anything: unchanged. Readers: unchanged.

- **Branch A** (targeted 0/2/0, hash and last_modified only): applied. Exactly the two-file change above goes live on both
  functions.
- **Branch B:** nothing is applied. Any pre-state hash other than `SFSTGBQX...` voids this half too: the base I proved by
  content would no longer be the live one, and the diff has to be re-measured from the new build.

**Rollback per key:** the code goes back to the saved `SFSTGBQX...` zip by the same targeted apply. No state is migrated.

## Carried (not grounds)

1. **This act makes the channel failure visible; it does not cure it.** FWD-3's channel @mentions stay undelivered until
   round 14's D2 fixes the call that the new `error` field names. `d1_errorfield.py` PASS is the readability proof, not
   a cure.
2. **Two writers share this module** (NFRA_CTLPLN and COMM_ASSIST). This half binds to the live hash at the act. A
   CTLPLN apply between now and the act voids it, and the act must refuse rather than re-baseline silently.

-- 3.0.0_SA_CVO~Z
