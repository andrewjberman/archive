# NFRA_COMPEFFICACY -- CE-g-4, the Codex-runtime rail: DESIGN (v1, the design half; the exercise half is not attempted)

**Author:** `3.0.0_SA_CVO` (decomp CE-g-4: "CVO drives, CloudComp executes"; serves FWD-9). **Written:** 2026-09-04
~07:2xZ on `1.0.0_SA_CTO`'s adjudication (a) of 07:15Z: CE-g-4 stays HELD by Andrew's ruling 2(b) and does not block
the close; the CVO lands the DESIGN with the closing pass; the EXERCISE ("a rail EXERCISED at a Codex seat: a DENY
observed as the BODY NOT EXECUTING") is not attempted, weakened or simulated here -- no Codex seat exists since
Andrew's "kill all the codex runtimes" (~21:0xZ 2026-09-03), and FWD-9 grades NOT_EVALUATED at the close for that reason.
**What this is:** a design a Claude seat can write and a CloudComp lane can build; not a gate on any seat's word.

## 1. The problem, in the terms the T1 rail already solved

The Claude rail is a **PreToolUse hook** (`.tools/hooks/comp-tool-hud.sh`): every Bash call is classified per segment
(`&&` / `;` / newline), a standalone repo search (`grep/rg/egrep/fgrep/findstr/ack/ag` recursive or directory-scoped,
`find` with anything) is DENIED and routed to `comp-find`, a single-file grep to `comp-read`, raw `aws` inspection is
classified on its own segment, and every decision is a row in `org/mcp/comp-which-rail.log`. The hook sits BETWEEN the
model's intent and the shell, so a DENY means the body never runs.

A Codex seat has no PreToolUse hook. Its tool calls reach a PowerShell or bash process directly, so the only places a
rail can stand are **in the process the call reaches** or **in the sandbox that admits the binaries**. Finding
`FINDING_COMPRAIL_DENY_NOT_ENFORCED_20260902.md` addendum 2 measured the consequence: a DENY on that runtime was a
log row and nothing else.

## 2. The three places a rail can stand on the Codex runtime, and what each can and cannot do

| Place | Mechanism | Sees | Cannot see | Cost |
|---|---|---|---|---|
| **A. PATH-first verb shims** (recommended) | the launcher already prepends `%USERPROFILE%\bin` to the seat's PATH and adds `.CMD` to PATHEXT (`ajb2/start-codex-seat.ps1:116-121`, read in NFRA_CLDGRPH-S30); add `grep.cmd`, `rg.cmd`, `egrep.cmd`, `fgrep.cmd`, `findstr.cmd`, `ack.cmd`, `ag.cmd`, `find.cmd` (and the extensionless bash twins) that call ONE classifier with the full argv, write the rail row, and on DENY print the routing line and exit 2 WITHOUT exec'ing the real binary; on ALLOW exec the real binary by absolute path | the exact argv of the search verb; whether it is recursive / directory-scoped / a pipe-receiver cannot be seen from argv alone (see below) | a `bash -c "..."` body in which the verb is resolved by an absolute path (`/usr/bin/grep`), or a Python `subprocess` naming the binary; the pipe-RECEIVER carve-out (`cmd \| grep`) is invisible to a per-binary shim, which sees only its own argv | one shim pair per verb (8 verbs x 2 forms), the classifier extracted from `comp-tool-hud.sh` into a callable that takes argv rather than a Bash body; same log, same kill switch `org/mcp/comprail-gate1.enforce` |
| **B. A PowerShell profile / command-line pre-parser** | a `PSReadLine`/prompt hook or a `Set-PSReadLineKeyHandler` on Enter that classifies the whole line the way the HUD classifies a Bash body, per segment, before it runs | the whole command line including pipes, so the pipe-receiver carve-out and per-segment classification are preserved | a bash body the seat launches (`bash -c`), and any call the seat makes without a console (headless invocation); profiles "never load" on this estate by measured history (CLAUDE.md Git section) | a profile the launcher must inject and prove loaded on every launch; the class of failure this estate already knows (a profile that does not load fails OPEN) |
| **C. Sandbox denial** | the Codex sandbox already runs under `Andrew\CodexSandboxUsers`; deny that group EXECUTE on the raw search binaries (Git's `usr/bin/grep.exe`, `find.exe`, ripgrep) and leave the shims of A executable | everything -- an absolute-path invocation, a subprocess, a bash body: the binary does not run for that token | nothing about WHY (no rail row, no routing line: the seat sees "Access is denied" and cannot tell the rail from the DACL rot NFRA_CLDGRPH-S26 spent a night on); and `find`/`grep` are used by tools that are not searches (the estate's own scripts) -- a blanket deny breaks them for the sandbox token | one icacls act per binary, reversible; a documented exception list; the S26 provisioner lesson applies (the DACL must survive the next provisioning run) |

## 3. The design: A, with C as the backstop, never B

1. **The classifier becomes a callable.** `.tools/hooks/comp-tool-hud.sh`'s segment classifier is extracted (or
   wrapped) into `.tools/comprail_classify.py argv...` returning ALLOW / DENY / ALLOW-SEARCH-shape with the same
   reasons and the same rail-log row the Claude hook writes, so the two runtimes share ONE law and ONE log (a second
   classifier would drift -- the two-carrier defect). The kill switch stays `org/mcp/comprail-gate1.enforce`.
2. **PATH-first shims for the eight verbs** in `%USERPROFILE%\bin`, written by `provision-path-shims.sh` beside the
   comp-* forwarders (so they inherit the S26 fix: inheritance restored after the chmod, the run's own DACL read
   printing `protected 0 of N`). Each shim: build argv, call the classifier, on DENY print the routing line
   (`comp-find` / `comp-read`) and exit 2; on ALLOW exec the real binary by the absolute path the shim resolved at
   provisioning time. `# rail-checked:` is honoured as on Claude (an argv token, since a Codex shim has no body to
   scan for a trailing comment -- the marker must be an argument: `--rail-checked=<why>`; stated as a grammar
   difference, not hidden).
3. **The pipe-receiver limb is declared, not faked.** A per-binary shim cannot see that its `grep` is a receiver. The
   design admits a receiver-shaped argv (a grep with a PATTERN and no PATH, or `-` as the path) as ALLOW-RECEIVER
   and logs it as such; a grep with a directory or recursive flag is the DENY class regardless. This is the T1 shape
   applied to argv rather than to a body, and the residual (a receiver given a path) is named as the rail's known
   blind spot on this runtime.
4. **C as backstop for the absolute-path escape**: the sandbox group is denied EXECUTE on the raw `grep.exe`,
   `rg.exe`, `find.exe` only AFTER A is live and exercised, with the exception list measured by a census of
   estate scripts that call those binaries by absolute path under the sandbox token (expected: 0; the census is
   the control). Without A, C is S26 again: a deny with no voice.
5. **B is not built**: a profile-loaded rail fails OPEN on the runtime it targets, by this estate's own measurement.

## 4. Acceptance -- the closes-on, unchanged, and the arms that can fail

- **The exercise (FWD-9, the cell's closes-on):** at a FRESH Codex seat launched only through
  `ajb2/start-codex-seat.ps1`, `grep -r "pattern" org/` from the seat -> the shim's DENY line, rc 2, and the BODY
  NOT EXECUTING (no output from grep, no process for `grep.exe` in the Win32 table for that call); the rail log carries
  the row with `runtime=codex`. Positive control: `comp-find` from the same seat runs. Negative control: `cmd | grep
  x` (a receiver) runs. This is the arm that needs a Codex seat, and it is the one Andrew's word gates.
- **The design's own arms, runnable on this runtime today:** the classifier callable returns DENY for the 18 red
  cases of `.tools/comprail-gate1-fptest.sh` and ALLOW for its 25 green ones when fed argv instead of a body
  (the falsifier already exists, 43 cases); a shim invoked with a recursive grep exits 2 and spawns nothing.

## 5. Cost and non-application, stated because a rule without them only ratchets

**Cost:** ~16 shim files, one classifier extraction, one provisioning run; one extra process spawn per search verb on
the Codex runtime. **Non-application:** Claude seats (the PreToolUse hook is the rail there and stays); tools that call
the binaries by absolute path from within the estate's own scripts (the census in step 4 measures them; the shims do
not sit on those paths); and the exercise half of this cell until a Codex seat exists -- which is a carried call to
Andrew (one Codex seat closes this exercise and NFRA_CLDGRPH-S26's gate in one sitting), not a gate this design
implements.
