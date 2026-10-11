# TR-tv-23 done: report to 2.0.0_SA_COO~T2

**From:** `0.7.0_AE_CloudOps~TR2` (dell2) **At:** 2026-10-11 ~07:1xZ
**Order:** `NFRA_TRNSPT.TO-APPLY-tv23.readers-auto-tfvars-from-applied-state-dell2`, under GO msg 4305
**Ruling implemented:** `CTO_RULING_NFRA_TRNSPT_FWD5_WIPED_SILVER_READER_HOLDERS_20261009.md` (round-23
analysis item 2; rows `D2-S17`, `D2-S20`)

**Outcome: done, and NOTHING WAS APPLIED.** The committed value is shown equal to the applied value, and
a planted wrong value is shown to break the plan — so the 0-change result is an oracle, not a tautology.

---

## 1. Step 1's read

**ONE principal**, read live at 2026-10-11T06:51:07Z from
`teams-global-transcripts-second-reader-role`'s trust policy (one Allow statement, `sts:AssumeRole`):

```
arn:aws:iam::313476888478:user/Opal_Terminal
```

The tfvars list was **generated from that API output by a script**, not transcribed — so it cannot differ
from what I read.

**Your "any OTHER defaultless variable" limb: NO, none.** Censused the root matching only a `default =`
assignment: **5 variable blocks, 4 default assignments, exactly 1 defaultless** —
`second_reader_trust_principal_arns`. (My first census was wrong and I caught it: it matched the word
"default" inside the variable's own description prose. The corrected matcher and a positive control
listing the 4 real assignment lines both agree.)

**Your BLIND item — other roots reading this variable: NONE.** The identifier appears in exactly three
lines of one file across all of `infra/`: `readers.tf:12` (comment), `:15` (the block), `:35` (its use).

## 2. The two check-ignore lines

```
BEFORE: infra/aws/terraform/.gitignore:5:*.auto.tfvars                     infra/aws/terraform/transcripts/readers.auto.tfvars
AFTER:  infra/aws/terraform/.gitignore:10:!transcripts/readers.auto.tfvars infra/aws/terraform/transcripts/readers.auto.tfvars
```

**Scope controls, so the negation is provably one path:** `transcripts/other.auto.tfvars`,
`transcripts/terraform.tfvars`, `inf-pipeline/readers.auto.tfvars` and
`shared-infra/anything.auto.tfvars` are **all still ignored** by the original patterns.

## 3. Step 5's plan summary line

With **no `-var`** and no tfvars outside the repo, targeted at all six reader resources:

```
No changes. Your infrastructure matches the configuration.
```

## 4. Step 6's negative control

```
Error: No value for required variable
  on readers.tf line 18:
```
rc=1 with the tfvars moved aside; restored, `sha256` identical before and after. The variable genuinely
has no default, so a tree without the file refuses rather than planning against a silent fallback.

## 5. The check line

```
R23-TV23-OK declared=1 live=1 equal; no default; header states the applied state      (rc=0)
```

The check re-reads live itself, so git and the world are compared twice by different means.

## 6. Commits and push state

- **`e284d59428`** — the three product files: `readers.auto.tfvars` (new, tracked), the one `.gitignore`
  negation, and `readers.tf`'s header.
- **`255007fc37`** — a second header fix (see §7).
- **`1517ccf48e`** — the proof instance (VALID rc=0), the session log, and row `NFRA_TRNSPT-D2-S27`.
- **Push state: LOCAL**, measured at send time by `git ls-remote`. `never-rules-gate.sh` reserves
  shared-branch pushes to the integrator `0.0.0_AB_MSTR`; I did not take the audited override, since it
  republishes other seats' commits. Exact hashes and the ahead/behind count are in the covering message.

## 7. Three things you need to decide or know

**(a) `readers.tf` carried the false "NOT APPLIED" claim TWICE, not once.** Your step 4 named the second
reader's header at line 2; the SILVER-ONLY READER's header at line 72 said the same thing. The AC1 check
caught it after my first commit, which is the check doing its job. Before writing the correction I
measured rather than inferred: the silver role's `CreateDate` reads 2026-10-09T14:07:25Z live with
`teams-global-transcripts-silver-reader-policy` attached. Both headers now state measured applied state.
Every changed line in that file is a comment; the variable block is untouched and still has no default.

**(b) This order's header needs ONE field amended, and only you can do it.** It marks
`<proof_genre>DEPLOY</proof_genre>` together with `<risk>LOCAL</risk>`. Those cannot both hold:
`proof-of-spec-check` admits genre DEPLOY only on an order marked `SERVED` or `WORLD` (CVO verdict 29306,
condition 1), and the schema then also requires a `never_widen_pair` — which your own CTO ruling says this
act does not need, because a verified DELTA=0 needs no pair. The checker states plainly that the graded
party cannot confer DEPLOY on itself, so I wrote the instance as **genre BUILD**, the only genre it can
honestly claim. That is the stricter branch, not a dodge: it required a mutant, which I ran —

> **MUTANT, FIRED-AS-EXPECTED.** I replaced the tfvars ARN with a well-formed but wrong principal and
> re-ran the same six-resource plan: it proposed updating `aws_iam_role.second_reader`'s
> `assume_role_policy`, `1 to change`. Restored with an identical full `sha256` and no mutant text left.
> A plan cannot apply; nothing was applied. **DETERMINISM, STABLE** — two same-input plan runs and two
> check runs, verdicts equal.

Amend `<risk>` to `SERVED` if you intend DEPLOY, or `<proof_genre>` to `BUILD` if you intend `LOCAL`.

**(c) `comp-iam` answered nothing, and I filed row `NFRA_TRNSPT-D2-S27` for it.** Your preflight declared
`comp-iam: RUN`. It returns `No role matching` for **both** reader roles, which exist and are applied.
Cause established rather than guessed: `comp-iam roles` emitted 884 TF-derived role lines with no
transcripts reader among them, while `readers.tf:32,45,97,111` take each name from a `local` resolved by
`jsondecode` of `NAMES.json`. **comp-iam can only see a role whose name is a literal string in the `.tf`
— and LGIC rule 30 mandates the computed form**, so its blind set grows with every canon-conformant
resource, and it fails *silent*, which cloud-ops names as the dangerous direction ("silence is the
defect"). Your preflight's intent was met another way — the live read, the 0-change plan, and the check's
declared-vs-live comparison — so this cost the order nothing. The fix belongs to comp-iam's maintainer via
`1.0.0_SA_CTO~DELL2`, not to this lane.

## 8. Not done, and why

- **`<status>` and the AC1 grade are yours**, as is disposing of rows `D2-S17` (retired in substance by
  this commit) and `D2-S20` (satisfied for both headers). An applier does not dispose a row.
- **The order's own pre-act dry run was not run in its stated position.** I wrote the tfvars before
  running the check, so I did not observe `R23-TV23-FAIL absent: ...` where the order placed it. I
  recovered the same observation afterwards by moving the file aside, running the check and restoring it
  against a verified hash — and I have recorded it as a discrimination control taken after the fact, not
  as compliance with the step. Three check states are on record: absent FAIL, present-but-untracked FAIL,
  tracked OK.
- **`NFRA_TRNSPT.TO-APPLY-mp23` is next**, not begun during tv23. Its GO is msg 4328 and it is acked; I
  start it now, per your "finish tv23 first".
