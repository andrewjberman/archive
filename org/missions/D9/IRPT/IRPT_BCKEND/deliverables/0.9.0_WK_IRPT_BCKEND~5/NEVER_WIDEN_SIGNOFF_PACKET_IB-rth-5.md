# NEVER-WIDEN SIGN-OFF PACKET -- IB-rth-5: session-establishment tooling for the export render
host -- `render_export.cjs` learns to REUSE an operator-captured session; the host also gains a
new interactive capture tool

**For:** the two halves required before ANY deploy to this host (CLAUDE.md never-widen: CTO + COO):
`1.0.0_SA_CTO` and `2.0.0_SA_COO~B`.

**Prepared by:** `0.9.0_WK_IRPT_BCKEND~5` (`IRPT_BCKEND.TO-IB-rth-5`, first pass).

**Supersedes:** nothing. First packet on this cell.

**Unblocks (indirectly):** row `IRPT_BCKEND-W3-S52` -- the render-latency question (row
`IRPT_BCKEND-W2-S62`) that stalled on `BLOCKED: SESSION_ABSENT` before any PDF render began, 4.483s
after send, host `i-0167fd745ad906a66`. This cell does not itself measure latency; it builds what
an operator needs to give the render a session to measure it against.

**NOTHING IS APPLIED OR DEPLOYED BY THIS PACKET.** All four touched files are committed on the
branch only. Nothing is uploaded to `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/`.
The host (`i-0167fd745ad906a66`) was not started, and no SSM command or session was sent against
it by this worker. No change-management ledger is opened (none is owed until a deploy is
attempted, per this project's own standing discipline).

A half signs the **blast radius**: what the key may touch, and the rollback. It does not sign an
intention.

---

## 0. Scope, and the boundary this packet does NOT cross

This cell is TOOLING ONLY. It never completes an MFA login, never scripts a sign-in, never
synthesizes a fake session that a later reader could mistake for a real one, and never touches
`portal/src/contexts/AuthContext*`, `portal/src/App.tsx`, or any portal-side auth source (BOUNDS,
`IRPT_BCKEND.TO-IB-rth-5`). The non-MFA service-account path is not investigated, proposed, or
built toward anywhere in this packet (reserved to Andrew, CTO ruling addendum 2 @afc015b4b2).

## 1. The design choice, and why (arm a)

**`browser.newContext({ storageState: <path> })` over `launchPersistentContext(userDataDir)`.**
Both are legitimate Playwright session-reuse mechanisms; this cell picked the narrower one because
this script's own invocation model is one-shot and SSM-dispatched, not long-lived:

- `launchPersistentContext` persists a WHOLE profile directory (cache, service workers, extension
  state, IndexedDB) across runs -- more surface than a render needs, and every future render would
  read and potentially WRITE into that directory, so a broken run could corrupt the very session it
  was handed. `storageState` is a single, inert JSON snapshot (cookies + `localStorage` per
  origin): a render only ever READS it (via `browser.newContext`), never mutates it, so a bad
  render cannot damage a good session.
- The declared, stable path this cell picked -- `/opt/investor-reporting-export/session/storageState.json`
  -- is writable and survives across render invocations for a measured reason, not an assumed one:
  the render document's own deploy step (`infra/aws/terraform/investor-reporting/export/ssm.tf:49-52`,
  read this session, out of this order's `<paths>` and unmodified) is `aws s3 cp
  s3://.../ec2/investor-reporting-export/ ${export_app_dir}/ --recursive` -- **no `--delete`** -- so
  it can only ever ADD or OVERWRITE paths that exist in this cell's own S3-synced tree. No file
  under `session/` is committed to `infra/aws/ec2/investor-reporting-export/` (confirmed:
  `git ls-tree HEAD` before this cell's commit lists exactly `README.md`, `package.json`,
  `render_export.cjs`, `run-export-render.sh` -- no `session/` entry, and this cell adds none), so a
  file an operator writes there on the host is never touched by any future sync.
- `--chown -R $(id -u):$(id -g) ${export_app_dir}` runs before every sync (`ssm.tf:50`), so the SSM
  run user owns the directory tree and can write into a new `session/` subdirectory without a
  further grant.

## 2. The code change, exactly (arm b)

`infra/aws/ec2/investor-reporting-export/render_export.cjs`. ONE new function
(`loadSessionContextOptions`), ONE new constant (`SESSION_STATE_PATH`), and the browser-context
creation in `main()` changed from `browser.newPage()` (an implicit default context) to
`browser.newContext(contextOptions)` then `context.newPage()` -- functionally IDENTICAL to the
old call when `contextOptions === {}` (Playwright's own `browser.newPage()` is documented as this
exact convenience wrapper). Every failure path of `loadSessionContextOptions` (file absent, file
unreadable, invalid JSON, well-formed-but-wrong-shape) returns `{}`, reproducing today's fresh
context. **No other function, and no other line, changed.**

Proven structurally, not asserted: `battery_ib_rth_5.py` diffs seven byte-identical anchors
(`VENDOR_HOSTS`, `assertNoVendorHost`, `need`, `awsJson`, the `GUARD` object literal,
`guardSummary`, and the top-level `main().catch` handler) against the file's own pre-cell HEAD
text -- **7 of 7 unchanged**.

`infra/aws/ec2/investor-reporting-export/capture-session.cjs` (NEW) and
`infra/aws/ec2/investor-reporting-export/capture-session.sh` (NEW) implement arm (c) -- the
interactive capture tool an operator runs to actually produce a `storageState.json` (full runbook
in `README.md`'s new "Session establishment" section, this same commit). `package.json` gained one
`"capture"` npm script alias; no new dependency (still only `playwright`, already declared, still
resolved from the host's own `NODE_PATH`, never installed).

**COMMITTED-FILE-SHA256 (this worktree, matches what this packet's own commit will contain):**

| file | sha256 | bytes | change |
|---|---|---|---|
| `render_export.cjs` | `7df36a961598cce9725bfd963a6e1c3c78ce05bde52c7ff8c8b13017ac41f1df` | 13169 | edited (additive) |
| `capture-session.cjs` | `edf76b2dc151d18ca5278e93634bf834042063ba6029d489a6a550a05d1458aa` | 5544 | NEW |
| `capture-session.sh` | `21555558becd383f3a78908461611718fd87afe8f60e51cace07b9dd6a997ef7` | 1724 | NEW |
| `package.json` | `9c7ca836f2c37bd985b15fc234bca42944b82f2b7f052255abccb94ba38c0c7f` | 1124 | edited (one script alias) |
| `run-export-render.sh` | `e52661229c1583223b72f6f2a7b01dbf28729ff1d501c0bee83b543bbb5b3797` | 1330 | UNCHANGED (byte-identical to what is already live) |

`README.md` also gained a documentation section (not part of the S3-synced deploy set -- confirmed
against the established deploy-completion record for this same directory,
`org/critical_paths/change_management/20260911T1530Z_irpt-bckend-rt8-render_deploy_completion.md`
leg L2: only `render_export.cjs`, `run-export-render.sh`, `package.json` were ever uploaded to
`s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/`; `README.md` never has
been).

## 3. Verification at rest (no deploy)

- `node --check render_export.cjs` -- clean. `node --check capture-session.cjs` -- clean.
  `bash -n capture-session.sh` -- clean.
- **Live, VS.-served bytes measured, not assumed**: `aws s3api list-objects-v2 --bucket
  opal-313476888478-lambda-artifacts --prefix ec2/investor-reporting-export/` (this session) lists
  exactly 3 objects (`package.json` 1066 bytes, `render_export.cjs` 9622 bytes,
  `run-export-render.sh` 1330 bytes), each fetched via `get-object` and sha256'd this session:
  `render_export.cjs` live = `37b8c4010c29d808f1e54173d7d6c3c647b45d72e204b5e1b058ed2a0d369aac`,
  `package.json` live = `2fd9400408ef3186e7918e459cae541d1e2d6988862332d444bf8aa71ca43051` --
  **both BYTE-IDENTICAL to `git show HEAD:<path>`** for the same two files (diffed this session,
  zero output). So the pre-change rollback target below is not a git-log inference; it is what is
  actually served today, confirmed against the live object.
- **The in-process proof, on the REAL, unmodified `render_export.cjs` source, over a synthetic
  session only** (`battery_ib_rth_5.py`, output `IB-rth-5_R80-AC1_battery_output.txt`, token
  `IBR80-STORAGESTATE-LOAD-PATH-WIRED-AND-DISCRIMINATING`):
  1. No storageState file -> `browser.newContext` called with `{}`, `SESSION_ABSENT` refusal,
     the SAME log line the file printed before this cell. **Unchanged.**
  2. A well-formed, clearly-labelled SYNTHETIC storageState file -> `browser.newContext` called
     WITH `{ storageState: <path> }` (asserted on the fake module's OWN recorded call arguments,
     not a log-message guess), a DIFFERENT, distinguishing log line prints, and the script STILL
     refuses `SESSION_ABSENT` because the fake session is not real. **The fix, and it never claims
     false success.**
  3. Corrupt (invalid JSON) storageState file -> a `WARN`, falls through to the SAME `{}` call and
     the same refusal. **Never a crash, never a different failure mode.**
  4. Well-formed JSON, wrong shape (no `cookies[]`/`origins[]`) -> a `WARN`, same fall-through.
     **Never a crash.**
  5. **NEGATIVE CONTROL**: the same synthetic-session scenario run against a deliberately UNWIRED
     copy of the file (the `storageState` pass-through stripped back out) -- the harness correctly
     shows NO session-loaded signal and NO `storageState` in the `newContext` call.
     **Confirms this battery can tell a wired implementation from an unwired one**, not just match
     a hoped-for string; sanity-checked live this session by temporarily sabotaging the REAL file's
     wiring and confirming the battery FAILS LOUD (rc=1, no success token) before the real file was
     restored and re-verified.
  4 of 4 scenarios plus 1 of 1 negative control hold. No arm here runs against, or claims anything
  about, a real portal session, a real host, or a real MFA login.

## 4. The blast radius, both branches

**BRANCH -- BUILT AND DEPLOYED** (not done by this packet; this section covers what a deploy WOULD do):

- **Which host is touched.** Exactly ONE: `i-0167fd745ad906a66` (`irpt-ycharts-runner`). No other
  instance runs this script.
- **What changes in served behaviour, per case:**
  - **No `storageState.json` file ever exists on the host** (the state at deploy time, and the
    state until an operator completes arm (c)'s runbook): **NO OBSERVABLE CHANGE.** Every render
    still hits `SESSION_ABSENT` exactly as it does today -- proven structurally (section 2) and
    behaviourally (section 3, scenario 1), not merely argued.
  - **An operator completes the capture runbook and a VALID session file exists:** a render that
    would have hit `SESSION_ABSENT` can now reach the print route authenticated. This is a REAL,
    INTENDED behaviour change and it is the entire point of this cell -- it is what unblocks the
    render-latency measurement row `IRPT_BCKEND-W3-S52` names as stalled. Nothing about how the
    PDF is produced, where it is written, or the vendor-separation guard changes; only whether the
    print route answers authenticated or not.
  - **A `storageState.json` file exists but is expired or otherwise no longer valid:** the render
    still reaches the print route, the route still answers with a sign-in screen (Playwright
    surfaces an expired-cookie session exactly like no session, from this script's point of view),
    and the SAME `SESSION_ABSENT` refusal fires. No crash, no silent different failure mode.
- **The capture tool's own footprint.** `capture-session.cjs`/`.sh` are INTERACTIVE ONLY -- they
  are never invoked by the `irpt-export-render-run` command document (unchanged, out of this
  order's `<paths>`) and have no scheduled trigger. They open a CDP debug port bound to
  `127.0.0.1` only (never `0.0.0.0`), reachable exclusively through an SSM port-forward the
  operator explicitly starts -- no security-group or network change, and the render host's
  existing security group (`irpt-ycharts-runner-sg`, no inbound at all, SSM-managed) is untouched
  and unneeded for this to work.
- **The cross-firm / vendor bound holds.** Neither the code change nor the capture tool opens any
  origin outside the Opal portal (`assertNoVendorHost`/`VENDOR_HOSTS` byte-identical, section 2);
  `capture-session.cjs` navigates only to the operator-supplied `IRPT_CAPTURE_PORTAL_ORIGIN`, never
  a vendor host, and performs no vendor call itself (the operator's OWN portal sign-in is a
  first-party, MFA-protected act, not the vendor sign-in gate this project's standing doctrine
  protects).
- **The residual risk, disclosed plainly.** A `storageState.json` file is a live session credential
  sitting on disk. It is scoped to the Opal portal origin only (never a vendor), sits under the
  instance role's own filesystem (no new IAM grant reads or writes it -- Playwright's `fs`-level
  read/write, not an AWS API), and is never uploaded to S3, logged, or transmitted anywhere by
  either script. Its blast radius if the host itself were ever compromised is the same class of
  risk as every other credential-bearing state already on that host (the YCharts secrets this
  host's role already reads) -- this cell adds ONE MORE such artifact, not a new class of exposure.
  This trade-off, and whether it is acceptable, is exactly what the two signing halves are asked to
  weigh; it is not this worker's call to make unilaterally.

**BRANCH -- NOT BUILT / NOT DEPLOYED (the current state, and the STOP if a half refuses):**

- The host's live `render_export.cjs`/`package.json`/`run-export-render.sh` stay exactly as
  measured live in section 3 -- every render still hits `SESSION_ABSENT`, exactly as row
  `IRPT_BCKEND-W3-S52` found. `capture-session.cjs`/`.sh` never reach the host; no operator can run
  arm (c)'s runbook against a host that does not carry the script.
- The committed source sits on this branch, verified at rest (section 3), until a deploy follows a
  signed packet.

**ROLLBACK, if built and applied and later reverted:**

- Revert the commit, then re-upload the reverted bytes to
  `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/` via `aws s3 cp` (the
  ESTABLISHED mechanism for this directory -- `org/critical_paths/change_management/20260911T1530Z_irpt-bckend-rt8-render_deploy_completion.md`
  leg L2, never invented here), verified by `head-object` PLUS a host read-back (`ls -la
  /opt/investor-reporting-export` via SSM, the same stronger check that record used, since it
  proves the INSTANCE ROLE could actually fetch the reverted bytes).
- **Pre-change bytes, the rollback target, measured LIVE this session (section 3), not inferred:**

  | file | pre-change (LIVE + git HEAD, byte-identical) sha256 |
  |---|---|
  | `render_export.cjs` | `37b8c4010c29d808f1e54173d7d6c3c647b45d72e204b5e1b058ed2a0d369aac` |
  | `package.json` | `2fd9400408ef3186e7918e459cae541d1e2d6988862332d444bf8aa71ca43051` |
  | `run-export-render.sh` | unchanged by this cell; no rollback needed |

  A rollback DELETES `capture-session.cjs`/`capture-session.sh` from the S3 prefix and the host
  (they did not exist before this cell); it does not need to restore prior bytes for either since
  none existed.
- **The served behaviour on rollback**: identical to today -- every render hits `SESSION_ABSENT`,
  and no capture tool is reachable on the host.
- **A live `storageState.json` an operator may already have captured before a rollback is NOT
  touched by a code rollback** (it lives under `session/`, outside every file this cell's rollback
  restores) -- naming this explicitly so a rollback is never mistaken for revoking a captured
  session; revoking a session is a separate act (delete the file, or let it expire) not covered by
  this packet.

## 5. Writers of the touched property

| property | writers |
|---|---|
| `infra/aws/ec2/investor-reporting-export/*.cjs`/`*.sh`/`package.json` (repo) | this order's own `<paths>` grant is the only one with repo write access to this directory; measured -- no other project's `<paths>` names this path |
| `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/*` (the deployed artifact) | **NOT** the render host's own role (`irpt-ycharts-runner-role` holds `s3:GetObject` only on this prefix -- `iam.tf:230-234`, read this session, unmodified by this cell); every WRITE there is a human/operator `aws s3 cp` under their own AWS credentials, exactly as `IB-rt-8`'s own deploy-completion record shows. This packet did NOT enumerate every AWS principal in the account holding `s3:PutObject` on this shared artifacts bucket -- that census is outside this cell's scope and `<paths>` grant; disclosed as a qualifier, not assumed absent. |
| `/opt/investor-reporting-export/*` on the live host | overwritten on every `irpt-export-render-run` invocation by the S3 sync above (source of truth); a DIRECT host edit via an interactive SSM shell is possible for anyone with `ssm:StartSession` on this instance and is NOT tracked by this project -- it would be overwritten by the next render's sync regardless |
| `/opt/investor-reporting-export/session/storageState.json` on the live host | written ONLY by `capture-session.cjs` (this cell, arm c) when an operator runs it; NEVER by `render_export.cjs` (read-only) and NEVER by the S3 artifact sync (no such path is ever committed to the synced tree, section 1) |

**The qualifier the count cannot remove**: a console or CLI write to the artifact bucket or the
live host is physically possible for any sufficiently-privileged AWS principal and cannot be fully
enumerated from this cell's `<paths>` grant; disclosed, not assumed away.

## 6. The identity line, per arm

| arm | claims a SERVED behaviour? | runs as |
|---|---|---|
| section 1 (design reasoning) | No. A reading of `ssm.tf`/`git ls-tree`, cited by path@this-session. | this worker, read-only |
| section 3 live-bytes check (`s3api list-objects-v2`/`get-object`) | **No** -- confirms what IS served today (the baseline), not a claim about a post-deploy state. | this worker's own AWS credentials (read-only: `ListBucket`/`GetObject` on a prefix this project's own IAM already scopes for reads) |
| section 3 in-process battery | No. Runs entirely in this worktree against a fake `playwright` module and a monkeypatched `execFileSync` -- explicitly never against a real browser, real host, or real portal. | this worker, local `node` |
| a future arm (e), if built+applied | **YES, IF AND ONLY IF a genuinely-captured, real session exists** -- but even then, arm (e)'s OWN acceptance bar (task order, arm e) requires the proof to use a SYNTHETIC storageState and to confirm the script still correctly refuses on it, precisely so no arm of this cell's OWN proof ever claims a real session was established. That claim, if it is ever made, is the NAMED HUMAN OPERATOR's, on their own schedule, never this cell's. | N/A -- not reached by this packet |

**No arm in this packet certifies a served, authenticated path.** That is by design, not an
oversight: this cell's whole acceptance bar (task order arm e) forbids it from ever claiming one.

## 7. What this packet does NOT cover

1. **The deploy itself.** Committed source only; the S3 artifact and the live host are untouched.
2. **Any actual session capture.** No MFA login was attempted, scripted, or synthesized by this
   worker anywhere in this packet, this commit, or this proof.
3. **The residual risk named in section 4** -- disclosed for the signers to weigh, not resolved here.
4. **Any other cell, row, or file in this project.** This packet is `IB-rth-5` only.
5. **Whether the operator's own AWS identity holds `ssm:StartSession`/`AWS-StartPortForwardingSession`
   on the render host.** Named in the runbook as a precondition this cell does not create or verify
   (out of `<paths>`); if absent, that is a separate IAM grant request, not a defect in this tooling.

## 8. What the halves sign against

This file's committed blob, alongside the four touched/new files at the sha256 values in section 2.
Each half names this packet's own blob:
- `org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rth-5_*.md`;
- `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rth-5_*.md`.

If either half is ABSENT, this cell's STOP stands: no deploy, no arm (e), and `R80-AC1` stays
whatever this packet's own proof measures it as (section 3: PASS-by-output on the wiring question
alone -- the CODE PATH is proven; the DEPLOY is not attempted), with this packet named as the carry.
