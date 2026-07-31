# WS-C7 SPECIMEN 1 -- RESOLVED-BUT-CANNOT-RUN (canonical shell-reachability specimen)

**Captured:** 2026-07-31 by `0.7.0_AE_CloudOps~Z` (site Z)
**Scope authority:** `1.0.0_SA_CTO~Z` ruling `20260731T030549Z` -- WS-C7 specimen capture and fixture
authoring. **This fixture CAPTURES; it does not set the WS-C7 contract** (that is P2, CTO-owned).
**Observed:** 2026-07-31T~01:5xZ, during the NFRA_BBGMCP gate-4 / gateway-rename work.
**Status:** FIXED (`b27e756a1`). The specimen is preserved re-derivably below because the fix
removes the instance, not the class.

---

## THESIS

> **The check that resolves is the check everybody writes, and it is the one that cannot fail in the
> state it exists to detect.**

A name resolving is not a tool running. Every reachability probe in the estate that stops at
resolution is blind to this specimen by construction -- not by oversight, but because resolution
*succeeded*.

---

## OBSERVATION

`.tools/aws.cmd` is a **tracked, cross-device** file. It delegated to a single hardcoded absolute
target:

```
"%LOCALAPPDATA%\Programs\Python\Python312\Scripts\aws.cmd" %*
```

That is a **pip-installed AWS CLI**. It exists on the primary laptop. It **does not exist on site
Z**, where the CLI is the native v2 installer at
`%LOCALAPPDATA%\Programs\AWSCLIV2\Amazon\AWSCLIV2\aws.exe`.

**The four-layer chain, and the layer each check can see:**

| Layer | Resolves? | Runs? |
|---|---|---|
| `shutil.which("aws")` -> `C:\Users\Opal Bloomberg\bin\aws.CMD` | YES | -- |
| `~/bin/aws.cmd` -> `call .tools\aws.cmd` | YES | YES |
| `.tools\aws.cmd` -> `%LOCALAPPDATA%\...\Python312\Scripts\aws.cmd` | YES (the .cmd exists) | **NO -- target absent** |
| the target | **DOES NOT EXIST** | -- |

**Measured, both directions, same session:**

```
shutil.which('aws')                          -> C:\Users\Opal Bloomberg\bin\aws.CMD   (resolves)
subprocess.run([that_path, '--version'])     -> rc=1  "The system cannot find the path specified."
subprocess.run(['aws', '--version'])         -> rc=0  aws-cli/2.35.21 ...
```

**The two invocation shapes disagree, and the HARDENED one is the broken one.** A bare-argv call
lets Windows `CreateProcess` apply its own `PATHEXT` search and reach a working binary. An
explicitly-resolved call is pinned to the dead chain.

---

## FAILURE DIRECTION -- TWO LIMBS, POINTING OPPOSITE WAYS

Recorded separately rather than flattened, because the interaction is the finding.

| Limb | Instrument | Direction |
|---|---|---|
| A | the availability check (`shutil.which` / `command -v`) | **OVER-REPORT** -- claims a tool that cannot run |
| B | the authorization gate (`comp-tagauthz`) it feeds | **UNDER-REPORT** -- produces NO verdict at all (`rc=1`) |

**An over-reporting availability check manufactures an under-reporting authorization check.** Limb B
is not a second independent defect; it is limb A's output consumed downstream. Any recall standard
that scores instruments individually will grade A as healthy (it returned a true path) and B as
merely failing -- and will miss that A *caused* B.

---

## BLAST RADIUS (measured, not estimated)

`comp-tagauthz` returned `rc=1` "could not evaluate" -> `safe-apply.sh` **fail-closed** ->
**no Terraform module setting `default_tags` was appliable on this device.**

It presented as a **tag-authz gate failure**, which reads like a policy collision. It was a missing
file three layers down. **The error surface named the wrong subsystem**, which is itself a WS-C7-
relevant property: the instrument that failed was not the instrument that reported.

---

## THE CONTROL THAT CAUGHT IT -- AND WHY THE OBVIOUS CHECK COULD NOT

**What caught it:** running the *exact failing shape* in isolation and comparing it against the
*working* shape, then reading the DIFFERENCE rather than either result alone.

**What could not have caught it, and this is the specimen's whole point:**

- `command -v aws` -- PASSES. The forwarder file exists.
- `shutil.which("aws")` -- PASSES, and returns a real, absolute, existing path.
- `aws --version` **from bash** -- PASSES. Bash resolves the *other* shim (`.tools/aws`, the MSYS
  guard), which is a different file on a different chain. **Every hand-run AWS call on this box
  worked the entire time the estate was broken.**
- A registration check -- PASSES. The tool is registered and its file is present.

**Only a caller that resolves explicitly AND then executes fails.** That is `comp-tagauthz`'s `sh()`
-- and it resolves explicitly *by design*, with a docstring stating it does so to avoid a silent
`FileNotFoundError`. **The hardening selected the failure.** The naive form worked.

---

## RE-DERIVATION (works on a fresh session; the fix removes the instance, not the class)

The class is re-derivable on any device where a `~/bin` forwarder chain terminates in a
device-specific absolute path. To reproduce the *shape* deliberately:

```bash
# 1. Confirm the two shapes can disagree at all on this platform:
python -c "
import shutil, subprocess
w = shutil.which('aws')
print('resolved   :', w)
print('explicit rc:', subprocess.run([w,'--version'],capture_output=True,text=True).returncode)
print('bare rc    :', subprocess.run(['aws','--version'],capture_output=True,text=True).returncode)
"
# A DIFFERENCE between 'explicit rc' and 'bare rc' IS the specimen.

# 2. Walk the chain to the first non-existent target:
cat ~/bin/aws.cmd            # -> delegates to .tools/aws.cmd
cat .tools/aws.cmd           # -> the absolute target; test whether it exists
```

**Historical evidence, if the live chain is repaired:** `git show b27e756a1^:.tools/aws.cmd` carries
the single-hardcoded-target form; `b27e756a1` is the resolve-don't-assume fix.

---

## OBSERVATION ROUTED TO WS-C7 DESIGN (not built here, per scope)

Recorded as a routed observation for `1.0.0_SA_CTO~Z`; **this fixture does not set the contract.**

1. **A reachability limb must EXERCISE, not RESOLVE.** This specimen passes every resolution-based
   check that exists. Exercising means: run it and score the OUTPUT, not the exit code and not the
   path.
2. **The exercise must use the caller's own invocation shape.** Bash-exercising a tool that native
   Python will call proves nothing here -- the two shapes reached *different files*. A reachability
   result is only valid for the invocation shape it was measured with.
3. **A tool that is reported reachable but whose CONSUMER then fails to produce a verdict should be
   scored as a single event, not two.** Otherwise the causing instrument grades healthy.

*(XXX.md Step 1b A.3 already carries the resolution-vs-execution lesson from the 2026-07-29
`PATH: 93 of 93 ... ZERO of them ran` incident. This specimen is the SECOND instance of that class
in three days, on the same device, through a different chain -- which is itself evidence that the
mandatory-exercise instruction is load-bearing and not yet sufficient: A.3 exercises `comp-which`,
and `comp-which` was never the broken member.)*

---

## PROVENANCE

Fix `b27e756a1`. Session log `5fffc922d`
(`org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-07-31/session_close_lane_Z_2116-0215Z.md`).
Scope grant: CTO~Z `20260731T030549Z`. Handover: `20260731T024616Z`.
