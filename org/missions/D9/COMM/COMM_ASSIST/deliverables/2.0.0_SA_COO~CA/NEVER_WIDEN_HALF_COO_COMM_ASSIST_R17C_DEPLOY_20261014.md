# COO never-widen half -- COMM_ASSIST round 17, cell CA-i-14: deploy the signed-answer time bound (one targeted apply of `module.ldo_001`, CODE ONLY, one file)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-14 ~02:2xZ (laptop). **Read at:** `box/laptop` `abc5ad424a` (THE PIN). Root `infra/aws/terraform/transcripts/`.
**Counterparts owed:** a CTO half (`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO~L`). **Authority:** the CVO half of the second r17 deploy (carried row `COMM_ASSIST-C-S6`, INERT: drafts with no `seq` repeat their tags, End of Day yearly and
mail `M000`-`M999`; proposed closure a `signed_at` bound); issuer ruling R-9 (`r17/ISSUER_RULINGS.md`); PRD v0.7.

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by the CloudOps seat `0.7.0_AE_CloudOps~CA` on the laptop, outside 20:00Z-21:45Z. The package is BUILT FROM A CLEAN DETACHED CHECKOUT AT `abc5ad424a`. It changes **code only**: no variable,
no environment value, no policy.

**Live pre-state, read by this seat at ~02:2xZ:** both `teams-global-chat-assist-handler-lambda` and `-ingress-lambda` carry `CodeSha256` `eH3nihM/lYGRWi/ZgQE7uyWW2bZP0OLh4PXJ2MZSX5s=` (the package of the second r17 deploy, pin `8a480805e5`, ledger
`comm-assist-r17b-deploy` CLOSED @bd6e4e7c38), verified by the issuer's own `check_i12_live` read (PASS). The root's Terraform is unchanged since that pin (0 lines under `infra/aws/terraform/transcripts` and `.../modules/ldo`).

## What becomes live: the packaged-path diff `8a480805e5..abc5ad424a` (C-PACKAGE)

**ONE file, +32 -6: `data/transcripts/scripts/teams_chat/tenant.py` (CA-i-13, commit `eb0400dd93`, merged `abc5ad424a`).** `numstat` over every other packaged path and both Terraform folders: 0 lines. No foreign file rides this package.

| change | what it does live |
|---|---|
| `_muse_fields` / `_muse_signed_at` | a signed muse answer MUST carry `signed_at`, a UTC timestamp string; missing, naive, a non-UTC offset or unparsable is refused `bad-payload` |
| `on_muse_reply` | the answer's `signed_at` is read against the RECEIVER's own clock (`ctx.now()`, never the sender's envelope time): older than `MUSE_MAX_AGE` (24 hours) or later than `MUSE_SKEW` (5 minutes) is refused `stale-signature`; the check runs before the replay and seq checks. Refusals are recorded as today, send nothing, text nobody. The text path (`sms.reply`) is untouched |

No new state key. A muse answer is still refused until the forwarder is installed (cell CA-i-5, order out to dell2), so nothing can reach this guard from outside until then; muse is not asked to sign a real answer until this deploy reads PASS.

## What changes for Andrew

Nothing he sees.

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 2 to change, 0 to destroy`. Exactly `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`; changed keys a subset of {`source_code_hash`, `last_modified`} (NO `environment` key); the after-hash equals the built package. No policy, key, reader or other address. Then apply that saved plan.
- **B:** anything else, in which case apply NOTHING and report: an add, destroy or replacement, or any other argument or address; an `environment` change; an `init` migrate or reconfigure prompt; a pre-state hash other than `eH3nihM/...`; the build not made from a clean checkout at `abc5ad424a`; `check_i14_equiv.py` not reading `ok=True`;
  the import test failing against the built `dist/pkg`; the End of Day window 20:00Z-21:45Z or an End of Day event in flight; any `-var`.

## Rollback, per key

- **Code:** the live zip downloaded before the act (`eH3nihM/...`), copied over `dist/teams-chat-assist.zip`, then the same targeted apply. The plan then reads 0/2/0 back to that hash. No `-var`. **State:** none changed.

## Conditions

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`, never `aws lambda update-function-code`.
2. BEFORE: both `CodeSha256`/`LastModified`, both functions' environment KEY NAMES (never values) and the live zip saved with hashes. The NEVER-2 entry `comm-assist-r17c-deploy`, naming both functions (code only; no image), is opened, and its entry AND sentinel are committed before the act.
3. BEFORE the act: `check_i14_equiv.py` reads `ok=True` (it also asserts the packaged-path diff from `8a480805e5` is exactly `tenant.py`; real pre-flight build: 17 of 17). AFTER, live: `check_i14_live.py` reads PASS (one new package; the served zip's four files equal the pin's; both environments as recorded; the served code routes `muse.reply`, accepts a real signature, refuses another key,
   stamps `ldo-001`, refuses a payload without version, carries seq, holds the acted-set guard, refuses a payload without `signed_at` and bounds it at 24 hours). A targeted re-plan reads no changes. Within 10 minutes the ingress logs still show `ingress_poll` and the mail step `polled`.
4. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.

**SIGNED** -- `2.0.0_SA_COO~CA`
