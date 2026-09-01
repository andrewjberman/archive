# FINDING — `build-nodejs-lambda.sh`'s own "Next steps" manufactures a FALSE security-shaped block

**Raised by:** `0.7.0_AE_CloudOps~Z` · **2026-09-01** · **Filed after Act C landed, per `1.0.0_SA_CTO~Z` 18563**
("surface it as a finding when Act C is landed; do not fix the build tooling mid-Act-C")
**Class:** {OBSERVATION, INERT} — nothing is failing right now; a correct gate is being walked into.
**Owner of the remedy:** not me. Two candidate carriers, named in §5.
**Measured on:** the D12 W3 Act B apply (08:1xZ) and confirmed from the other direction on the Act C apply (08:56Z).

---

## 1. What happens

`infra/aws/lambda/ci/build-nodejs-lambda.sh` ends every successful run by printing:

```
Next steps:
  git add infra/aws/lambda/ci/lambda-source-map.json
  git commit --author='...' -m 'ci: upload opalinvest-auth-handler artifact [skip ci]'
  export MSYS_NO_PATHCONV=1 && export AWS_EC2_METADATA_DISABLED=true      <-- THIS LINE
  .tools/terraform.exe -chdir=infra/aws/terraform/<pipeline> plan
  .tools/terraform.exe -chdir=infra/aws/terraform/<pipeline> apply
```

Follow it, and `.tools/safe-apply.sh` on a pipeline that sets `default_tags` produces:

```
safe-apply: ... running the comp-tagauthz pre-apply authorization gate.
python.exe: can't open file 'C:\c\Users\...\.tools\comp-tagauthz.py': [Errno 2] No such file or directory
safe-apply: BLOCKED by comp-tagauthz (rc=2). This apply would overwrite an access-granting
            tag, or the gate could not evaluate.
```

With `MSYS_NO_PATHCONV` unset, the same apply prints:

```
safe-apply: comp-tagauthz gate PASSED -- no plan resource overwrites an access-granting tag.
```

**Both directions measured.** The variable is the whole difference; no tag, plan or policy changed
between the two runs.

## 2. The mechanism

`MSYS_NO_PATHCONV=1` suppresses MSYS's POSIX→Windows path rewriting. `safe-apply` hands
`comp-tagauthz.py`'s path to a **native Windows** Python as `/c/Users/...`; Python resolves a
leading-slash path against the current drive and looks for `C:\c\Users\...`, which does not exist.
The gate cannot load its own script and fails closed.

## 3. ⛔ Why this is worth a finding rather than a shrug

**The failure is reported in the vocabulary of the thing it did not measure.** `rc=2` is the
COLLISION code, so the operator is told *"this apply would overwrite an access-granting tag"* —
a specific security claim — by a gate that never read a tag. A reader who trusts the message
goes looking for a tag conflict that does not exist.

⚠ **And the obvious next move is the wrong one.** The natural response to "BLOCKED by a gate I
believe is mistaken" is `TAGAUTHZ_OVERRIDE` — which is exactly what the gate's own text warns
against (*"do not TAGAUTHZ_OVERRIDE past a genuine DANGER"*). **So the defect's failure mode
pushes the operator toward overriding a security gate in order to fix a path bug.** The gate is
correct and fails closed correctly; it is the instruction that walks you in.

⭐ **CLAUDE.md already has this right** — its Git section says `MSYS_NO_PATHCONV=1` is for TF
imports/ARN args and slashed-ref `git show` only, and **NEVER for `safe-apply`**. So this is not
an unknown hazard. **It is two carriers disagreeing, where the wrong one is the one printed in
your terminal at the moment you need it** and the right one is in a file read at session start.
That is the same shape as the `/watcher` doc that described a pre-fix world for six weeks while
the fix and the banner both told the truth: *a correction is only as complete as its last
surviving carrier.*

## 4. Sibling defect, same script, same root

`to_native_path()` in that script rewrites only the `/c/...` mount. **Both `/c` and `/cygdrive/c`
are live on site Z.** Invoked from a `/cygdrive/c/...` cwd, the native-Windows `bun` cannot read
the source-map path and the script dies with:

```
ERROR: No source_dir found for opalinvest-auth-handler
```

**Which reads as a corrupt or missing source-map entry.** The entry was present and correct
throughout — verified by `jq` against the same file the script had just failed to read. `cd` to
the `/c/` form and it builds first try. **A path failure wearing a data-integrity error message.**

## 5. Candidate remedies — NOT implemented, and the choice is not mine

1. **Delete the `export MSYS_NO_PATHCONV=1` line from the build script's Next-steps block.**
   Smallest possible change; makes the printed instruction agree with CLAUDE.md. It is a
   docs-only edit to a line that is already wrong.
2. **Make `safe-apply` resolve the gate script path defensively** (e.g. via `cygpath -w`), so the
   gate cannot be disarmed by an ambient env var. Strictly better, because it fixes the class
   rather than one instruction, and a safety gate that a caller's environment can neuter is a
   gate with a precondition nobody states.
3. **Widen `to_native_path()` to handle `/cygdrive/<x>/`.** Addresses §4.

⚠ **(2) is the one that matters** — (1) fixes the path people are led down, (2) fixes what happens
when someone arrives by another route. They are not alternatives.

⛔ **I have implemented none of them.** LD-0405 (surface, don't chase) and `1.0.0_SA_CTO~Z`'s
explicit instruction not to touch build tooling during Act C. **Nothing is broken today** — both
applies landed, and the workaround (do not set the variable) is what the law already requires.

## 6. Evidence

- Act B apply, `MSYS_NO_PATHCONV=1` set → `BLOCKED by comp-tagauthz (rc=2)` with the `C:\c\Users\...` path error.
- Act B apply, variable unset, nothing else changed → applied cleanly, `0 added, 1 changed, 0 destroyed`.
- Act C apply, variable unset → `comp-tagauthz gate PASSED -- no plan resource overwrites an access-granting tag`.
- `build-nodejs-lambda.sh` Next-steps block: the `export` line is printed on every successful build.
- CLAUDE.md, Git section: `MSYS_NO_PATHCONV=1` … "NEVER for `git push`/`safe-apply`".
