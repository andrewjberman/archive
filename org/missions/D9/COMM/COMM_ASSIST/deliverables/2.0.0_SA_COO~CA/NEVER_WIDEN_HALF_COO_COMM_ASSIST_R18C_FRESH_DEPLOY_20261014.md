# COO never-widen half -- COMM_ASSIST round 18, cell CA-j-10: deploy the four-hour ingress mark (one targeted apply of `module.ldo_001`, CODE ONLY, two files)

**Author:** `2.0.0_SA_COO~CA`, 2026-10-14 ~11:3xZ (laptop). **Read at:** `box/laptop` `afa8752f44` (THE PIN). Root `infra/aws/terraform/transcripts/`.
**Counterparts owed:** a CTO half (`1.0.0_SA_CTO`) and a CVO half (`3.0.0_SA_CVO~L`). **Authority:** the CTO's ruling on call 847f, `CTO_RULING_20261014_104xZ_COMM_ASSIST_MARK_FRESHNESS_4H.md` (msg 109095): `MAX_AGE_S` to 4 hours as a LOCAL code cell with its own deploy pair BEFORE the flip to `enforce`, `marks_seen` pruned by age with no count cap, a refusal recording kind and tag; round-18 decomposition AMENDMENTS 5 and 6; PRD v0.8.

## The act

ONE `safe-apply` of the root, TARGETED at exactly `module.ldo_001`, by the CloudOps seat `0.7.0_AE_CloudOps~CA` on the laptop, outside 20:00Z-21:45Z. The package is BUILT FROM A CLEAN DETACHED CHECKOUT AT `afa8752f44`. It changes **code only**: no variable, no environment value, no policy, no secret, no Terraform resource.

**Live pre-state, read by this seat at ~11:3xZ:** both `teams-global-chat-assist-handler-lambda` and `-ingress-lambda` carry `CodeSha256` `nX67q2k05fh77lG2gBLsNlp6HLAZeELPq85CJpWCVhA=` (the CA-j-3 package, ledger `comm-assist-r18-deploy` CLOSED @1daa4a97ce; LastModified 04:52Z, unmoved since), `INGRESS_MARK_MODE=record`; the secret `teams/global/ingress-mark` has a current version (value never read) and its resource policy is live (CA-j-8, ledger `comm-assist-r18-key-deploy` CLOSED @df7f6f6c55). `check_j5_obs.py` reads `NO-EVIDENCE` (608 items scanned, 0 state rows carrying mark counters), so no state written by the old code exists to migrate.

## What becomes live: the packaged-path diff `38ce5a7981..afa8752f44` (C-PACKAGE)

| path | lines | what it does live |
|---|---|---|
| `data/transcripts/scripts/teams_chat/ingress_mark.py` | +1 -1 | `MAX_AGE_S` from 15 minutes to 4 hours (a mark dated more than 5 minutes ahead is still stale) |
| `data/transcripts/scripts/teams_chat/tenant.py` | +29 -7 | `marks_seen` becomes `{mark, at}` entries kept by AGE (every mark younger than the window is held, none dropped by count; a legacy bare string is held, dated now), so a mark cannot be replayed inside the wider window; a refusal records `kind` and the payload's string `tag` beside the reason and time, never a note, text, mark or secret |

`numstat` over every other packaged path and `infra/aws/terraform/modules/ldo`: 0 lines. `infra/aws/terraform/transcripts/chat_assist.tf` (+17) is in the root diff but is the CA-j-7 policy resource, ALREADY APPLIED by CA-j-8; it is not packaged and this act does not touch it. No foreign file rides the package.

## What changes for Andrew

Nothing he sees. In `record` mode every text still acts as today; the handler only counts. The one behavioural difference the wider bound makes: a failed event redelivered an hour later is now fresh instead of stale (in `record` mode it acted either way). The mode stays `record`; flipping it is cell CA-j-5 under its own pair.

## Expected plan, BOTH branches

- **A:** targeted `0 to add, 2 to change, 0 to destroy`. Exactly `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`; changed keys a subset of {`source_code_hash`, `last_modified`} (NO `environment` key); the after-hash equals the built package. No policy, role, secret, key or other address. Then apply that saved plan.
- **B:** anything else, in which case apply NOTHING and report: an add, destroy or replacement; any other address or argument; an `environment` change; an `init` migrate or reconfigure prompt; a pre-state hash other than `nX67q...` or a mode other than `record`; the build not made from a clean checkout at `afa8752f44`; `check_j10_equiv.py` not reading `ok=True`; the import test failing against the built `dist/pkg`; the End of Day window 20:00Z-21:45Z or an End of Day event in flight; any `-var`.

## Rollback, per key

- **Code:** the live zip downloaded before the act (`nX67q...`), copied over `dist/teams-chat-assist.zip`, then the same targeted apply. The plan then reads 0/2/0 back to that hash. No `-var`.
- **State:** the only state key this code writes differently is `marks_seen` (dict entries instead of bare strings) on objects that receive a marked text; none exists today. If the code is rolled back after such an entry exists, the CA-j-1 code does not fail on it (its `payload["mark"] in seen` test is simply False against a dict entry), so it treats that mark as unseen: a bounded replay exposure for the marks held at that moment, named here and acceptable in `record` mode, where every text acts anyway.

## Conditions

1. Branch A read immediately before the apply, the lock taken. Never untargeted, never bare `terraform`, never `aws lambda update-function-code`.
2. BEFORE: both `CodeSha256`/`LastModified`, both functions' environment KEY NAMES (never values) and the live zip saved with hashes. The NEVER-2 entry `comm-assist-r18-fresh-deploy`, naming both functions (code only; no image), is opened, and its entry AND sentinel are committed before the act.
3. BEFORE the act: `check_j10_equiv.py` reads `ok=True` with `J10_PIN=afa8752f44` (it asserts the two code files are in the packaged diff and equal the pin's bytes, counts the one non-packaged Terraform path as foreign, and compares 17 S3 and mail-party probes between the built and the live package; the issuer's own pre-flight build read `J10-EQUIV ok=True files=2 foreign=1 probes=17 same=17`). AFTER, live: `check_j10_live.py` reads PASS (one new package; the served zip equals the pin on six files; `INGRESS_MARK_MODE=record` in both environments and the other keys as recorded; the secret has a current version and both roles may read it; the served code bounds a mark at 4 hours (3h59m ok, 4h01m stale), holds marks by age (a legacy string held, a 5-hour entry dropped), round-trips a mark, refuses a tampered one and parses the modes). A targeted re-plan reads no changes. Within 10 minutes the ingress logs still show `ingress_poll` and the mail step `polled`, and neither function log shows an error for the mark secret.
4. The secret's VALUE is never read, printed or logged. The applier reads no message content, sends no test mail, texts nobody and invokes nothing.
5. The mode stays `record`. Flipping it to `enforce`, by any route, is not this act.

**SIGNED** -- `2.0.0_SA_COO~CA`
