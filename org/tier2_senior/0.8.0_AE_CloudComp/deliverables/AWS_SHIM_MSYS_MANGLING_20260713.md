# .tools/aws -- the MSYS path-mangling guard shim (Andrew-direct 2026-07-13)

**Author:** 0.8.0_AE_CloudComp | **Status:** LIVE on this host (gitignored PATH shim, deployed + validated
2026-07-13T03:0xZ). **Routing:** COO -> CTO/BASE_EXEC for (a) ratification, (b) tracked provisioning,
(c) the CLAUDE.md line (proposed text below).

## Andrew-direct (verbatim)

> "the msys path-mangling trap is a gotcha that has fucked with us for months, there has to be a way to
> manage this in claude.md or somewhere so we do not deal with this every single time we query AWS"

## The class

Git Bash (MSYS) rewrites leading-`/` args at the bash->native-exe boundary: `--log-group-name-prefix
/ecs/globgrph` becomes `C:/Program Files/Git/ecs/globgrph`. AWS then errors -- or worse, returns empty and
reads as "resource absent". Exercised THIS session (2026-07-13): three consecutive silent-empty reads during
the COMPLEARN P3a audit nearly recorded "producer log group ABSENT" for a log group that exists with 3
nightly streams. CLAUDE.md's prose remedy ("use PowerShell for leading-/ aws args", Git section) is correct
and was forgotten anyway -- prose taxes every session; a shim teaches nobody because nobody needs teaching.

The documented anti-remedy is ALSO a trap: bare `MSYS_NO_PATHCONV=1 aws` breaks the launcher itself (the
pip `Scripts/aws` entry is a python script reached via shebang; with pathconv off, python receives an
unconverted POSIX script path: `can't open file 'C:\\c\\Users\\...'`). Both edges exercised 2026-07-13.

## The mechanism (why the shim is correct-by-construction)

MSYS mangles ONLY at the bash->NATIVE-exe crossing. A bash-script shim receives argv UNMANGLED
(bash->bash converts nothing). The shim then does the conversion RIGHT, deterministically:

1. **Local paths convert** (preserving the only behavior anyone wanted): an arg is local iff drive-letter
   POSIX form (`^/[A-Za-z]/`) OR it exists on disk -> `cygpath -w`. Also inside `file://`/`fileb://`.
2. **Everything else passes LITERAL** -- `/ecs/...`, `/aws/lambda/...`, SSM `/param/...` (the fix).
3. **Exec with `MSYS_NO_PATHCONV=1`** so MSYS converts nothing further; the launcher-breakage is sidestepped
   by invoking the real entry as `python <WINDOWS-FORM script path>` (or a native `.exe` directly), resolved
   dynamically as the first non-shim `aws` on PATH.

~~**Scope is exactly the wound:** `.tools` is PATH position 1 in Git Bash, so the shim wins there; PowerShell
cannot resolve an extensionless bash script (no PATHEXT match) and keeps resolving `Scripts\aws.cmd` --
PowerShell was never broken and is untouched (exercised: `(Get-Command aws).Source` -> aws.cmd, call works).~~

**^^ FALSE ON BOTH COUNTS. CORRECTED 2026-07-13 (see REGRESSION).** (1) PowerShell **CAN** resolve an
extensionless file -- it discovers it as an `Application`; `Get-Command aws -All` from a bash-spawned shell
lists `.tools\aws` **ahead of** `Scripts\aws.cmd`. (2) The scope was NOT "exactly the wound": a PATH shim is
scoped to **every process that inherits the PATH**, not to the shell that installs it. **And the exercise that
"proved" this paragraph is the reason it survived** -- I ran `(Get-Command aws).Source` in an INDEPENDENT
PowerShell, which does not have `.tools` on its PATH, so it could not have failed. *A control that cannot
fail is not a control.* The scope is now made true by construction with `.tools/aws.cmd` (Appendix B),
rather than asserted.

## Validation (all EXERCISED 2026-07-13)

| Test | Result |
|---|---|
| T1 the fix: `aws logs describe-log-groups --log-group-name-prefix /ecs/globgrph` from bash | PASS -- returns the 4 real log groups (this exact query silent-failed all session pre-shim) |
| T2/T3 baselines: `s3 ls`, `sts get-caller-identity` | PASS (unchanged) |
| T4a existing local path `/c/Windows/win.ini` | converts -> `C:\Windows\win.ini` |
| T4b SSM namespace `/opal/config/x` | LITERAL |
| T4c `fileb:///c/Windows/win.ini` | converts inside scheme -> `fileb://C:\Windows\win.ini` |
| T4d `/aws/lambda/nonexistent` | LITERAL (the fix class) |
| ~~T5 PowerShell~~ | ~~resolves `aws.cmd`, works, shim never in path~~ **VOID -- THE TEST WAS RIGGED, NOT PASSED.** Run from an INDEPENDENT PowerShell, which has no `.tools` on PATH, so it could not have detected the fault. The real case -- `powershell.exe` spawned FROM bash, inheriting `.tools` -- **HANGS**. See REGRESSION. |
| **T5' PowerShell (CORRECTED, post-`aws.cmd`)** | from BASH: `powershell.exe -NoProfile -Command "aws --version"` -> `aws-cli/1.44.44` (was a 120s hang); `aws s3 ls s3://opal-data-etfs/daily/` -> real objects. **This is the test T5 should always have been.** |
| Debug/rollback | `AWS_SHIM_DEBUG=1 aws ...` prints resolved argv, no exec; rollback = delete `.tools/aws` **AND `.tools/aws.cmd`** (both or neither) |

## Residual + provisioning notes

- `.tools/aws` is GITIGNORED (the existing shim-file pattern) -- THIS doc carries the tracked source
  (Appendix A) so it is re-provisionable; a new host copies Appendix A to `.tools/aws` + `chmod +x`.
- The `-e`-exists heuristic could in principle convert an AWS namespace arg that coincidentally exists as a
  local relative-root path -- requires a top-level dir literally named e.g. `/ecs` in the MSYS root;
  accepted + disclosed (drive-letter form is the primary trigger; namespace args do not exist locally).
- ~~Agents who explicitly call `powershell`/`PowerShell tool` for aws keep working identically.~~
  **FALSIFIED 2026-07-13 -- THIS LINE WAS THE DEFECT. See "REGRESSION" below.** It is true for a
  PowerShell session started *independently* (`.tools` is not on its PATH). It is FALSE for a
  `powershell.exe` **spawned FROM Git Bash**, which INHERITS bash's PATH with `.tools` FIRST.
- The known-slow aws-launcher startup (~seconds) gains one bash-script hop: negligible vs launcher cost.

## REGRESSION -- this shim SILENTLY BROKE every bash -> powershell -> `aws` call (found + fixed 2026-07-13)

**Owned by me. My shim caused it; my doc's "PowerShell unaffected" claim is what let it through.**

**Mechanism (REPRODUCED, not inferred):** a `powershell.exe` spawned from Git Bash inherits bash's PATH,
where `.tools` is **first**. Windows command resolution then finds the **extensionless** bash script
`.tools/aws` and tries to run it as an Application:

```
$ command -v aws                      -> /c/.../.tools/aws           (bash: correct, the guard)
$ powershell.exe -c "Get-Command aws" -> C:\...\.tools\aws           (<-- the BASH SCRIPT, ahead of aws.cmd)
$ powershell.exe -c "aws --version"   -> HANGS (killed at 120s)      (<-- not a clean failure. A HANG.)
```

**Why it was silent:** the affected call sites all pass `--quiet`, and none checked rc. A hung/failed
`aws s3 cp` therefore reported success while S3 kept the OLD artifact.

**Blast radius (4 call sites, `aws` bare inside a `powershell.exe -Command` string):**

| Call site | Guarded? |
|---|---|
| `infra/aws/lambda/ci/build-and-upload.sh:295` | **YES** -- base-AE's upload-verify gate caught it (`da5af3c8c`). This is the only reason we know. |
| `infra/aws/lambda/layers/find-insure-deps/build-layer.sh:102` | **NO** |
| `infra/aws/lambda/layers/find-insure-browser-deps/build-layer.sh:122` | **NO** |
| `infra/aws/lambda/layers/find-insure-parse-deps/build-layer.sh:105` | **NO** |

The three **layer** builds are unguarded: a silent no-op there ships a Lambda layer whose dependencies
never actually updated, and nothing detects it. Exposure window opens at the shim's landing (`19fde37de`,
2026-07-12). **Whether any layer build actually ran inside that window is NOT established -- do not quote
an incident count. A silent no-op leaves no scar, so historical incidence here is UNKNOWABLE.**

**FIX: `.tools/aws.cmd` (Appendix B).** PATHEXT makes Windows shells prefer the `.cmd` over the
extensionless file, so each shell gets a working `aws`: bash -> `.tools/aws` (the MSYS guard),
PowerShell/cmd -> `.tools/aws.cmd` -> the real CLI. Absolute forward target, so it can never re-enter
`.tools` and recurse. **EXERCISED:** bash resolution unchanged; `powershell.exe -c "aws --version"` from
bash returns `aws-cli/1.44.44` (was: 2-minute hang); a real `aws s3 ls` through that path returns objects.

**The lesson, which is the same one this project has produced five times tonight:** I validated the shim
in the shell I was *thinking* about and asserted the other one was unaffected **without exercising it**.
A PATH shim is not scoped to the shell that installs it -- it is scoped to every process that inherits
that PATH. *"Unaffected" is a claim about a system, and it needs a test, not a sentence.*

## Proposed CLAUDE.md line (CTO lands; replaces the buried Git-section prose for aws)

> **AWS from Git Bash goes through the `.tools/aws` PATH shim automatically** -- it passes AWS namespace
> args (`/ecs/...`, `/aws/...`, SSM `/...`) literal and converts only real local paths, killing the MSYS
> leading-`/` mangling class; never bare `MSYS_NO_PATHCONV=1 aws` (breaks the launcher). Inspect with
> `AWS_SHIM_DEBUG=1`. **`.tools/aws.cmd` MUST be provisioned alongside it** -- a `powershell.exe` spawned
> FROM bash inherits bash's PATH and would otherwise resolve the extensionless bash shim and HANG
> (silently, under `--quiet`). Both files or neither. Why/validation + the regression:
> `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/AWS_SHIM_MSYS_MANGLING_20260713.md`.

*(The earlier draft of this line said "PowerShell unaffected." That was false and it is what shipped the
regression. Corrected here rather than quietly dropped.)*

## Appendix A -- the shim source (tracked copy; deploy target `.tools/aws`, chmod +x)

```bash
#!/usr/bin/env bash
# aws -- MSYS path-mangling guard shim (Andrew-direct 2026-07-13, 0.8.0_AE_CloudComp).
# See org/tier2_senior/0.8.0_AE_CloudComp/deliverables/AWS_SHIM_MSYS_MANGLING_20260713.md
set -uo pipefail

_self="${BASH_SOURCE[0]}"
REAL=""
while IFS= read -r c; do
    [ "$c" = "$_self" ] && continue
    case "$c" in */.tools/aws) continue ;; esac
    REAL="$c"; break
done < <(which -a aws 2>/dev/null)
if [ -z "$REAL" ]; then
    echo "aws-shim ERROR: no real aws launcher found on PATH beyond the shim" >&2
    exit 127
fi

_convert_if_local() {
    local p="$1"
    if [[ "$p" =~ ^/[A-Za-z]/ ]] || [ -e "$p" ]; then
        cygpath -w "$p" 2>/dev/null || printf '%s' "$p"
    else
        printf '%s' "$p"
    fi
}

args=()
for a in "$@"; do
    case "$a" in
        file:///*|fileb:///*)
            scheme="${a%%//*}//"
            p="${a#*//}"
            args+=("${scheme}$(_convert_if_local "$p")")
            ;;
        /*)
            args+=("$(_convert_if_local "$a")")
            ;;
        *)
            args+=("$a")
            ;;
    esac
done

if [ "${AWS_SHIM_DEBUG:-0}" = "1" ]; then
    printf 'aws-shim real-entry: %s\n' "$REAL"
    printf 'aws-shim argv: '
    printf '[%s] ' "${args[@]}"
    printf '\n'
    exit 0
fi

case "$REAL" in
    *.exe)
        MSYS_NO_PATHCONV=1 exec "$REAL" "${args[@]}"
        ;;
    *)
        MSYS_NO_PATHCONV=1 exec python "$(cygpath -w "$REAL")" "${args[@]}"
        ;;
esac
```

## Appendix B -- `.tools/aws.cmd` (tracked copy; deploy target `.tools/aws.cmd`)

**Provision BOTH or NEITHER.** `.tools/aws` alone is the regression above; `.tools/aws.cmd` alone loses
the MSYS guard. `.tools/` is gitignored, so this Appendix is the only durable copy -- a new host copies
Appendix A to `.tools/aws` (+ `chmod +x`) and Appendix B to `.tools/aws.cmd`.

The forward target is the real AWS CLI's own `aws.cmd`, by ABSOLUTE path -- it must never resolve back
through PATH, or it would re-enter `.tools` and recurse.

```bat
@echo off
@rem aws.cmd -- Windows-shell companion to the .tools/aws bash shim (0.8.0_AE_CloudComp).
@rem
@rem WHY THIS FILE EXISTS: a powershell.exe/cmd.exe spawned FROM Git Bash inherits bash's
@rem PATH, which puts .tools FIRST. Windows then resolves the EXTENSIONLESS bash script
@rem `.tools/aws` as an Application -- and it HANGS (reproduced 2026-07-13: `aws --version`
@rem from a bash-spawned powershell never returned). Under `--quiet` that hang/failure is a
@rem SILENT NO-OP: infra/aws/lambda/ci/build-and-upload.sh reported a successful upload
@rem while S3 kept the OLD zip. Caught only by the upload-verify gate.
@rem
@rem PATHEXT makes Windows shells prefer this .cmd over the extensionless file, so both
@rem shells now get a WORKING aws: bash -> .tools/aws (MSYS path-mangling guard),
@rem Windows shells -> here -> the real CLI. Absolute target: never re-enters .tools.
"%LOCALAPPDATA%\Programs\Python\Python312\Scripts\aws.cmd" %*
```

**Host assumption, stated:** the forward hard-codes the CLI at
`%LOCALAPPDATA%\Programs\Python\Python312\Scripts\aws.cmd` (this host's install). A host whose CLI lives
elsewhere must edit that one line. A dynamic `where.exe`-based lookup was considered and rejected: it
would have to *exclude* `.tools` to avoid recursing into itself, and a self-excluding PATH search is
exactly the kind of cleverness that fails silently -- which is the failure class this whole document is about.

## Verification (re-run after any re-provision -- both shells, or you have only tested half of it)

```bash
command -v aws                                          # -> .tools/aws            (bash keeps the guard)
powershell.exe -NoProfile -Command "aws --version"      # -> aws-cli/...           (NOT a hang)
powershell.exe -NoProfile -Command "aws s3 ls s3://opal-data-etfs/daily/"   # -> real objects
```
The middle line is the one that regressed. **Run it from BASH, not from an independent PowerShell --
an independent PowerShell does not have `.tools` on PATH and will pass while the real path is broken.**
