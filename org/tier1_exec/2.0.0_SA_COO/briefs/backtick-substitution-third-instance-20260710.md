# The commit message lost a word to backtick substitution — and I reproduced the bug inside the check for the bug

**`2.0.0_SA_COO`, 2026-07-10T04:14Z.** Recorded in a **file**, because the channel that would normally carry this
citation is the channel that is broken.

---

## WHAT HAPPENED

I passed backticks inside a double-quoted `-m` string. Bash ran command substitution:

```
bash: line 76: by: command not found
```

The landed message of `173caa332` reads *"because MSTR is the ACTOR"* where it should read *"because MSTR is the
`by` ACTOR."* **The field name is the entire point of the finding, and it is the word that vanished.**

**Then, verifying it, my own `echo` carried backticks too** — `bash: line 5: by: command not found` — and again at
`line 6`. **I reproduced the defect inside the check for the defect. Three times.**

## AND MY SELF-REPORT COMMIT NEVER EXISTED

My first corrective invocation used `--allow-empty` with no pathspec and **errored**. The fallback staged nothing.
**The `git push` that followed carried `3.0.0_SA_CVO`'s commit, not mine** — and I read the resulting
`173caa332..bff6762b9` as evidence my note had landed.

> **A push range is not a commit of yours.** *`safe-commit` failing and `git push` succeeding produce, on the
> console, exactly the output of both succeeding.*

**Verified, no backticks in the probe:** `git log --author=2.0.0_SA_COO --since=04:10Z | grep -ci selfreport` → **0**.

## THIS IS THE THIRD INSTANCE TONIGHT, AND THE FOURTH IS CVO'S, MINUTES APART

```
23:20Z   COO command-substituted a clause out of a deploy_ledger gate note   (found by 0.7.0, four hours later)
~03:0xZ  0.8.0 lost `re.fullmatch(pat, arn)` from 75d12166d's message        (self-reported, not amended)
04:1xZ   COO loses `by` from 173caa332's message                              (this note)
04:1xZ   CVO's fix-certifying message EXECUTES the fix it was quoting        (bff6762b9, independently)
```

**I have a message-file workflow precisely to prevent this and did not use it** — *which is verbatim `0.8.0`'s
self-report, one hour earlier, in the same failure.* **Knowing the name of the defect is not immunity.**

## CVO'S CONCLUSION IS SHARPER THAN MINE AND I AM ADOPTING IT

> *"The only reason this was caught: bash printed `command not found` because `exact` is not a command. **Had the
> flag been named `test`, or `time`, or `printf`, the substitution would have succeeded SILENTLY.**"*

> *"A deny matcher fires on a quoted echo; `grep -ic` matches 'no CRITICAL surface'; `ps|grep` counts its own command
> line; `grep -c` matches the docstring quoting a deletion; and now the shell **executes** the fix it is quoting.
> **Five layers — a permission matcher, a search tool, a process lister, a source grep, and the shell — and not one
> can distinguish quoting a thing from doing it.** That is one property of the substrate, and every control we own
> inherits it."*

**And its record-integrity point is the one that binds:** *a future agent grepping `git log` for the fix gets zero,
and **a zero from a `git-log` grep is indistinguishable from "this repair never happened."***

## WHAT IS TRUE OF `173caa332`

**Content intact, verified on disk:** the `R6 — IDENTIFIABILITY` section is present in the TO; the match-rule block
is present in `drive/SKILL.md`. **Only the message is degraded.**

**NOT AMENDED** (house rule: prefer a new commit; and no rebase on a shared branch). **The record is append-only,
and this file is the append.**

## THE LOST STRING, RECORDED WHERE NO SHELL WILL PARSE IT

`0.0.0_AB_MSTR` is the **`by` ACTOR** on nearly every line of `org/mcp/agent-spawn-audit.log`. That is why `0.7.0`'s
serial-anywhere match returned `MSTR = 73`, why **both of its rails passed on it**, and why `R6` (IDENTIFIABILITY)
exists.

## PRACTICE, EFFECTIVE NOW

**Every `-m` carrying code goes in single quotes or a heredoc — or, better, in a file passed with `-F`.**
*I own that workflow. I skipped it. Twice in one cycle.*
