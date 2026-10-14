# COO never-widen half -- COMM_ASSIST round 17, cell CA-i-12: deploy the replay fix (one targeted apply of `module.ldo_001`, CODE ONLY, one file)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-14 ~01:0xZ (laptop). **Read at:** `box/laptop` `8a480805e5` (THE PIN). Root `infra/aws/terraform/transcripts/`.
**Counterparts owed:** a CTO half (`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO~L`). **Authority:** the CVO half of the first r17 deploy (carried row `COMM_ASSIST-C-S5`, ARMED, disarm owner the issuer: a signed muse answer
can be replayed against a later draft under the same chat tag; must be closed before the forwarder is installed); CTO round-16 analysis @6e9e2fc1ff; PRD v0.7.

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by the CloudOps seat `0.7.0_AE_CloudOps~CA` on the laptop, outside 20:00Z-21:45Z. The package is BUILT FROM A CLEAN DETACHED CHECKOUT AT `8a480805e5`. It changes
**code only**: no variable, no environment value, no policy. The first r17 deploy (ledger `comm-assist-r17-deploy`, CLOSED @4df21cf33f) already set `MUSE_ANSWER_PUBKEY`.

**Live pre-state, read by this seat at ~01:0xZ:** both `teams-global-chat-assist-handler-lambda` and `-ingress-lambda` carry `CodeSha256` `lRKObLMbn1kTWSXtohLxZ33HYVq7aBd1o/fjLfaA1Rw=` (LastModified 2026-10-14T00:37:49Z / 00:37:43Z), 291179 bytes:
the package of the first r17 deploy (pin `b19849b51c`), verified by the issuer's own `check_i4_live` read (PASS). The root's Terraform is unchanged since that pin (0 lines under `infra/aws/terraform/transcripts` and `.../modules/ldo`).

## What becomes live: the packaged-path diff `b19849b51c..8a480805e5` (C-PACKAGE)

Packaged set, read out of `infra/aws/lambda/teams-chat-assist/build.sh`. **ONE file, +32 -6: `data/transcripts/scripts/teams_chat/tenant.py` (CA-i-10, commit `1fc13dc4ba`, merged `8a480805e5`).** `numstat` over every other packaged path
and over both Terraform folders: 0 lines. **No foreign file rides this package** (the first deploy carried `lib/opal_naming.py` and eight registry files; nothing has moved there since).

| change | what it does live |
|---|---|
| `_muse_fields` | a signed muse answer MUST carry `version` as a whole number for every action (else refused `bad-payload`); `seq` is a whole number or null |
| `on_muse_reply` | `replayed`: the sha256 of payload + newline + signature, if already in `state["muse_acted"]`, is refused; `seq-mismatch`: a chat draft's answer must carry THAT draft's `seq`; a result that moved a draft (`sent`, `dropped`, `redrafted`, `approved`, `posted`, `mail-approved`, `job-opened`, `expired`, `already-posted`, `test-not-posted`) records the hash (last 200). The text path (`sms.reply`) is untouched |

New state key: `state["muse_acted"]` (hashes), written only after a muse answer moved a draft, which cannot happen until a forwarder is installed (cell CA-i-5, which waits on this deploy).

## What changes for Andrew

Nothing he sees. A muse answer is still refused until the forwarder is installed; this deploy removes the replay hole before anything can reach it.

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 2 to change, 0 to destroy`. Exactly `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`; changed keys a subset of {`source_code_hash`, `last_modified`} (NO `environment` key: the environment is unchanged); the after-hash equals the built package. No policy, key, reader or other address. Then apply that saved plan.
- **B:** anything else, in which case apply NOTHING and report: an add, destroy or replacement, or any other argument or address; an `environment` change; an `init` migrate or reconfigure prompt; a pre-state hash other than `lRKObLMb...`; the build not made from a clean checkout at `8a480805e5`; `check_i12_equiv.py` not reading `ok=True`;
  the import test failing against the built `dist/pkg`; the End of Day window 20:00Z-21:45Z or an End of Day event in flight; any `-var`.

## Rollback, per key

- **Code:** the live zip downloaded before the act (`lRKObLMb...`, 291179 B), copied over `dist/teams-chat-assist.zip`, then the same targeted apply. The plan then reads 0/2/0 back to that hash. No `-var`.
- **State:** `muse_acted` is new and unwritten until a forwarder exists; nothing to restore.

## Conditions

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`, never `aws lambda update-function-code`.
2. BEFORE: both `CodeSha256`/`LastModified`, both functions' environment KEY NAMES (never values) and the live zip saved with hashes. The NEVER-2 entry `comm-assist-r17b-deploy`, naming both functions (code only; no image), is opened, and its entry AND sentinel are committed before the act.
3. BEFORE the act: `check_i12_equiv.py` reads `ok=True` (it also asserts the packaged-path diff from `b19849b51c` is exactly `tenant.py`). AFTER, live: `check_i12_live.py` reads PASS (one new package; the served zip's four files equal the pin's; both environments as recorded; the served code routes `muse.reply`, accepts a real signature, refuses another key, stamps `ldo-001`, refuses a payload without version, carries seq, and holds the acted-set guard). A targeted re-plan reads no changes. Within 10 minutes the ingress logs still show `ingress_poll` and the mail step `polled`.
4. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.

**SIGNED** -- `2.0.0_SA_COO~CA`
