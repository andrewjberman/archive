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

**Scope is exactly the wound:** `.tools` is PATH position 1 in Git Bash, so the shim wins there; PowerShell
cannot resolve an extensionless bash script (no PATHEXT match) and keeps resolving `Scripts\aws.cmd` --
PowerShell was never broken and is untouched (exercised: `(Get-Command aws).Source` -> aws.cmd, call works).

## Validation (all EXERCISED 2026-07-13)

| Test | Result |
|---|---|
| T1 the fix: `aws logs describe-log-groups --log-group-name-prefix /ecs/globgrph` from bash | PASS -- returns the 4 real log groups (this exact query silent-failed all session pre-shim) |
| T2/T3 baselines: `s3 ls`, `sts get-caller-identity` | PASS (unchanged) |
| T4a existing local path `/c/Windows/win.ini` | converts -> `C:\Windows\win.ini` |
| T4b SSM namespace `/opal/config/x` | LITERAL |
| T4c `fileb:///c/Windows/win.ini` | converts inside scheme -> `fileb://C:\Windows\win.ini` |
| T4d `/aws/lambda/nonexistent` | LITERAL (the fix class) |
| T5 PowerShell | resolves `aws.cmd`, works, shim never in path |
| Debug/rollback | `AWS_SHIM_DEBUG=1 aws ...` prints resolved argv, no exec; rollback = delete `.tools/aws` |

## Residual + provisioning notes

- `.tools/aws` is GITIGNORED (the existing shim-file pattern) -- THIS doc carries the tracked source
  (Appendix A) so it is re-provisionable; a new host copies Appendix A to `.tools/aws` + `chmod +x`.
- The `-e`-exists heuristic could in principle convert an AWS namespace arg that coincidentally exists as a
  local relative-root path -- requires a top-level dir literally named e.g. `/ecs` in the MSYS root;
  accepted + disclosed (drive-letter form is the primary trigger; namespace args do not exist locally).
- Agents who explicitly call `powershell`/`PowerShell tool` for aws keep working identically.
- The known-slow aws-launcher startup (~seconds) gains one bash-script hop: negligible vs launcher cost.

## Proposed CLAUDE.md line (CTO lands; replaces the buried Git-section prose for aws)

> **AWS from Git Bash goes through the `.tools/aws` PATH shim automatically** -- it passes AWS namespace
> args (`/ecs/...`, `/aws/...`, SSM `/...`) literal and converts only real local paths, killing the MSYS
> leading-`/` mangling class; never bare `MSYS_NO_PATHCONV=1 aws` (breaks the launcher). Inspect with
> `AWS_SHIM_DEBUG=1`; PowerShell unaffected. Why/validation:
> `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/AWS_SHIM_MSYS_MANGLING_20260713.md`.

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
