# MS-a-3 AC2 -- the boundary verifier, run by the operator (Andrew) in his own window

**Why the operator ran it.** This harness's shell gets "Access is denied" on every run-as-another-user launch
(measured 2026-09-30 by 2.0.0_SA_COO~MS: `Start-Process -Credential` failed with and without output redirection; the
worker's own run of the fixed verifier printed `BOUNDARY: CANNOT-RUN-AS-ACCOUNT deny probe could not start as
Opal_MSP: Access is denied`, exit 5). AC2 needs a process started AS `Opal_MSP`, so the one real run is Andrew's.

**The invocation (given verbatim to Andrew, run in a PowerShell window as `Opal Bloomberg`):**

```
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\tmp\ms-4\opal_ai\opal\runtime\provision\verify-boundary.ps1" -Config C:\opal_runtime_msp\runtime.msp.config.json; "exit=$LASTEXITCODE"
```

**The script run:** `verify-boundary.ps1` at nested opal_ai commit `61841f5` (MS-a-3 item 0b: probes run AS the account
via `Start-Process -Credential -LoadUserProfile -WorkingDirectory <state_dir>`, the launcher's route; no WinRM).

**The output Andrew pasted back, verbatim (2026-09-30):**

```
BOUNDARY: DENIED-OK
exit=0
```

**What it means:** as `Opal_MSP`, the read of `C:\Users\Opal Bloomberg\Desktop\ajb_workspace\CLAUDE.md` was DENIED, and
the write + read of `C:\opal_runtime_msp\state\boundary-verify-marker.txt` succeeded. This matches a3.AC2's expectation
(`verify-boundary (msp config): BOUNDARY: DENIED-OK`).

**Recorded by:** 2.0.0_SA_COO~MS, from Andrew's paste in the session. Source of the words: Andrew, in-session.
