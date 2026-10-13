# MDPF_HEALGAP HG-t-19 -- SDD session restore determination (round 5)

Worker 0.9.0_WK_MDPF_HEALGAP~16, task order MDPF_HEALGAP.TO-HG-t19, issued by 2.0.0_SA_COO~G1. Read-only: the repository
was read, no AWS call, no SSM command, no access to the box, no secret value read. Base: worktree HEAD fe216d8d06 at start.

## 1. The reader

The SDD puller is `infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1`. It reads the SDD credential `SDDSecure` from the
Windows Credential Manager with a P/Invoke `CredReadW` call, inside `Get-Token`:

- `infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:229` -- `CredReadW('SDDSecure', 1, 0, [ref]$ptr)`. A false return makes `Get-Token` return `$null`.
- `infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:237-238` -- the session lock is acquired first, then `$token = Get-Token`.
- `infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:301` -- the token goes out on every SDDServices call as the `x-refresh-token` header. `:322` and `:448` set it again as `RefreshToken` on the request objects.
- A second reader of the same credential is `infra/aws/ec2/canonical-schwab-si2/sdd-backfill-08335338.ps1:51`, which exits 3 on a null read (`:58`).

What an empty read means to the puller (`infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:239-272`):

- `:239` -- a null token enters the guard. The running identity is read at `:260`.
- `:247-248` and `:262-268` -- the Credential Manager is per-user. If the process is not Administrator, the puller calls `Die 8` and says the failure is a wrong-identity bug, not a dead session.
- `:270-272` -- if the process is Administrator, the puller calls `Die 3`: the standing SI2 session "really IS dead/expired and a human must re-establish it on the box".
- `:252-256` -- an SSM `RunPowerShellScript` runs as `nt authority\system`, which has its own empty vault, so an SSM-driven pull always lands on the wrong-identity branch.
- `infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:134-139` -- `Die` publishes to SNS only when `-SnsTopicArn` is passed (`:34`, default empty). The "must page" wording at `:272` is therefore not a page by itself.

## 2. The writers

SEARCHED: 79389 files

Scope: every tracked file at the worktree HEAD (79,389 by `git ls-files`), searched with `git grep` for `CredWrite`, `cmdkey`,
`StoredCredential`, `vaultcmd`, `CredentialManager` and `SDDSecure`. Untracked and gitignored files were not searched. The native
Grep tool was also run over the SI2 folder (11 tracked files) and returned reads only. The `SDDSecure` search matched 27 files
across the tree: the two `CredReadW` read sites (the puller and the backfill), design notes and briefs, ontology copies of the
puller, and an audit log. The write-API search returned four lines in four files, all prose (two design notes, one recon log,
one investigation row). None is a call to a Credential Manager write API, and none names `SDDSecure` as a write target.

Limit: the SI2 application binaries that the puller loads from the Administrator profile (in `sdd-daily-pull.ps1`, the section
that searches `C:\Users\Administrator\AppData\Local\Apps\2.0` for `Schwab.SI.Framework.dll`) are not in the repository. A writer
inside them cannot be ruled out from code. That gap is why section 5 is a box read.

WRITERS FOUND: 0

## 3. The capture

The census's named act is the scheduled task `SchwabSddCapture`, created by `infra/aws/ec2/canonical-schwab-si2/run-capture.ps1:29`
(`schtasks /Create /TN SchwabSddCapture ... /F`) and started at `:30`. Its principal is the Administrator SID (`:18`), InteractiveToken,
HighestAvailable (`:23`). Its action runs `run-inner.bat` (`:14-15`), which carries `--dry-run` unless the wrapper was invoked with
`-Live` (`:9`). The wrapper's own comment says `-Live` writes `schwab/sdd/session` (`:5`).

The capture program is `infra/aws/ec2/canonical-schwab-si2/schwab_sdd_session_capture.py`. Its docstring says it reads the SI2
WebView2 profile at rest and writes a session blob to Secrets Manager for a consumer named `schwab_sdd_ingest.py` (`:5-8`). It
reads `Local State`, the `Cookies` SQLite file and the `Local Storage` leveldb (`:10-14`). It reads no Credential Manager entry.

What it writes: one Secrets Manager secret, `schwab/sdd/session` (default at `infra/aws/ec2/canonical-schwab-si2/schwab_sdd_session_capture.py:67`).
The only write is `put_secret_value` at `:293`, reached through `_run(profile_dir, do_write=bool(args.live))` at `:347`. The default
mode is `--dry-run` (`:38`); `--live` is gated (`:40-41`). The blob fields are `sdd_cookies`, `oauth_access_token`, `refresh_token`,
`captured_at`, `expires_at`, `source` and `schwab_domains` (`:19-21`, assembled at `:279-282`). The refresh token is the first JWT
whose preceding bytes contain the word "refresh" (`:257-258`). The secret is declared at `infra/aws/terraform/canonical-schwab-ec2/secrets.tf:61`.

The capture's consumer, `schwab_sdd_ingest`, is not a tracked file in the repository (`git ls-files` over the whole tree returns no
match). The system ontology card records the same thing: `schwab/sdd/session` is dormant, with zero consumers
(`infra/system/ontology/worldmodel/10_census/cards/SCHWAB_PROCESS_SWEEP.md:73-75`).

## 4. The same thing?

COMPARISON: UNDETERMINABLE FROM CODE

The two stores differ in kind. `SDDSecure` is one Credential Manager string in the Administrator vault, read as one value
(`infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:229`, `:232-233`) and sent as `x-refresh-token` (`:301`). The capture's
output is a JSON cookie jar and token set in Secrets Manager, with a `refresh_token` picked by a substring match over leveldb
bytes (`infra/aws/ec2/canonical-schwab-si2/schwab_sdd_session_capture.py:257-258`). Section 2 found no code that writes `SDDSecure`,
so no code path shows that the two hold the same value. The one shared word, "refresh", is a label, not a proof of identity.

Two documents disagree and the code cannot settle it. The design note says a human-established session's refresh token sits in
`SDDSecure` (`data/assets/docs/SCHWAB_AUTO_PULL_DESIGN.md:129-131`) and records a `CredRead OK` as Administrator on 07-13
(`data/assets/docs/SCHWAB_AUTO_PULL_DESIGN.md:365`). The brief's negative recon (`docs/briefs/schwab-sdd-rest-ingest-aprime-design-20260702.md:117-120`)
ran by a read-only SSM command (`:111-112`; the 0.6.2 log at `org/tier2_senior/0.6.2_AE_PartnerETL/logs/2026-07-07/schwabauto_gate3_recon_webview2_finding.md:19-20`).
The puller's own comment says SSM runs as SYSTEM (`infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:252-256`), so that recon
read SYSTEM's vault, not the Administrator vault the puller reads. The brief's label "Administrator console" does not match the
method it names. Whether Administrator's vault holds `SDDSecure`, and what it holds, is not readable from code.

## 5. Decision

DECISION: BOX-READ-OWED
READ-COMMAND: `cmdkey /list:SDDSecure`, run from an interactive console session on the box logged on as Administrator, not through SSM. It prints the Target, Type and User of the `SDDSecure` entry in that user's vault, or reports that none is stored. It prints no secret value.
RUNS-AS: Administrator (SID S-1-5-21-3688344540-3788367028-366044801-500, `infra/aws/ec2/canonical-schwab-si2/run-capture.ps1:18`) in an interactive logon (`infra/aws/ec2/canonical-schwab-si2/run-capture.ps1:23`, InteractiveToken, HighestAvailable). Not `nt authority\system`, which SSM runs as and whose vault is empty (`infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:252-256`).

Basis:

- The puller expects a human act on the box (`infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1:270-272`). The code shows only that expectation. It does not show which act writes `SDDSecure`. The only human act the code names is the SI2 sign-in that the capture reads (`infra/aws/ec2/canonical-schwab-si2/schwab_sdd_session_capture.py:5-6`), and no code shows that sign-in writes `SDDSecure`. So NAMED-ACT is not chosen.
- REPOINT is not chosen. Section 4 is UNDETERMINABLE FROM CODE, and the two stores differ in medium and shape.
- The box read settles the one fact the code cannot: whether Administrator's vault holds `SDDSecure`, and under which user it is stored. If the entry is absent, the restore is the human act the puller names and the next decision is NAMED-ACT with a named person. If it is present, the act that wrote it is still unnamed and needs a further read.
