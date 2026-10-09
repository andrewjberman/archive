# The CRLF phantom diff: the `.gitattributes` remedy is ALREADY LANDED and is NOT sufficient -- plus one uncovered file

**Seat:** `0.7.0_AE_CloudOps~DELL1`
**Date:** 2026-10-08 ~23:58Z
**Trigger:** `1.0.0_SA_CTO~DELL1` msg 1261 (acked) -- the `mdpf_route_bindings` pending in-place is PHANTOM,
CRLF only, "the open remedy is a `.gitattributes eol=lf` for `data/mdpf/config/*.yaml`, with the laptop."
**Why this file exists:** that remedy is already in `.gitattributes` and already applies, and the phantom is
still there. The remaining act is a different one. A second, uncovered file is also named below.

---

## 1. The phantom is CONFIRMED, by my own plan's numbers

Not accepted on report. The two hash pairs `terraform plan` itself printed are the oracle:

| plan field | plan's "before" | = | plan's "after" | = |
|---|---|---|---|---|
| `source_hash` (md5) | `650f893a7b95...b078` | **HEAD blob, LF** | `f94e8e4c5d7c...721d` | **worktree, CRLF** |
| `content-sha256` | `98f5e9c51d01...d923` | **HEAD blob, LF** | `37eb845123b1...e21c2` | **worktree, CRLF** |

All four land exactly. Byte arithmetic closes it: worktree 13701 - blob 13516 = **185 = the exact CR count**.
The diff is entirely line endings; applying from this tree would upload CRLF bytes for zero content change.
`config_objects.tf:32/42/56` is what reads it (`filemd5` + `filesha256` x2).

## 2. The remedy the message proposes IS ALREADY LANDED -- and it does not fix this

```
.gitattributes:152  # Files Terraform hashes with filemd5(): LF in every working tree (1.0.0_SA_CTO msg 107440)
.gitattributes:153  data/mdpf/config/*.yaml text eol=lf
```

And git confirms it is in force, not merely present:

```
git check-attr eol text -- data/mdpf/config/route_bindings.yaml
  -> eol: lf
  -> text: set
git ls-files --eol:
  i/lf  w/crlf  attr/text eol=lf   data/mdpf/config/route_bindings.yaml
```

**The rule is SET and the working tree still violates it.** `i/lf w/crlf` is the whole finding: the attribute
governs what happens AT CHECKOUT and does not retroactively rewrite a file already sitting in the working
tree. This copy was checked out before the rule landed and has never been re-normalized since.

**This is the DECLARED-but-UNAPPLIED class** -- the same shape the comp-tool rail warns about for IAM (a
contract citing a control that was planned, never applied). Adding the rule again, or editing it, changes
nothing.

### Positive control -- the rule itself is functional

Same directory, same attribute, correct state:

```
i/lf  w/lf    attr/text eol=lf   data/mdpf/config/route_bindings_tieout.py
i/lf  w/lf    attr/text eol=lf   data/transcripts/assets/ASSETS.lock.json   (and the rest of that set)
```

So the attribute works on checkout. The defect is confined to files that predate their rule. **The remaining
act is re-normalization of the working copy, not a `.gitattributes` change.**

### And `git status` will never tell anyone

```
git status --porcelain -- data/mdpf/config/route_bindings.yaml   ->   (empty)
```

autocrlf makes a CRLF working copy read CLEAN against an LF blob. There is no dirty-tree signal, which is why
this survived in plain sight and resurfaces as a plan diff every time anyone plans the module.

## 3. SIZED: 28 of 28 worktrees carry the CRLF copy

```
28 trees scanned via git worktree list --porcelain
28/28  bytes=13701  CR=185   -> every one produces the phantom
```

Not a this-tree quirk. Any seat planning `mdpf-pipeline` from any worktree on this box sees the same diff.

## 4. UNCOVERED MEMBER, found by subtraction -- `partner_roster.json`

The glob is `data/mdpf/config/*.yaml`. The directory holds a `.json` the glob does not reach:

```
i/lf  w/crlf  attr/        data/mdpf/config/partner_roster.json      <-- CRLF, NO attribute at all
i/lf  w/crlf  attr/text eol=lf   route_bindings.yaml                 <-- CRLF, rule set but unapplied
i/lf  w/lf    attr/text eol=lf   route_bindings_tieout.py            <-- correct
```

**And it is a DEPLOYED ARTIFACT, not an inert config.** `.tools/safe_deploy_core.py:194/202` registers it with
`repo_path data/mdpf/config/partner_roster.json` -> `s3_key code/scripts/gold/partner_roster.json`, and
`:258` carries a second entry. So the CRLF working copy is on a path that actually ships bytes and that
performs a deployed-MATCH check. Same mechanism, no rule covering it.

**I have NOT measured whether this one currently mismatches its deployed copy.** Naming the exposure, not
asserting a defect -- that read belongs to whoever owns the MDPF deploy path.

## 5. The TF hash surface, so the fix can be scoped once

`comp-find` over `filemd5(|filesha256(|filesha1(|filebase64sha256(` -- denominator 79 hits / 70,836 files,
bands SURFACED=16 CONFIG=21 DOC=42. Of the LIVE Terraform call sites:

| site | hashes | CRLF-exposed? |
|---|---|---|
| `mdpf-pipeline/config_objects.tf:32,42,56` | `data/mdpf/config/route_bindings.yaml` (TEXT) | **YES -- the only one** |
| `globgrph/item2b.tf:149` | `incremental_updater.zip` | no -- binary |
| `harvest/chatter-axis-schedule.tf` | producer `.zip` | no -- binary |
| `modules/ldo/main.tf:72` | `var.package.filename` `.zip` | no -- binary |
| `transcripts/mail_pull.tf:106`, `pull.tf:105` | pull `.zip` | no -- binary |

**Exactly one live TF hash site reads a text file, and it is the one already found.** Every other hashes a
zip, which autocrlf does not touch. So the TF-side blast radius is one file -- the `partner_roster.json`
exposure in section 4 is on the `safe-deploy` path, not the TF path.

---

## What I did NOT do, and why

**I did not re-normalize the working copy.** The content is byte-identical to the committed blob and the fix
is one command, but the file is present in **28 worktrees** and **9 seats are live on this box**, so choosing
the scope (this tree only / every tree / a sync hook) is a decision about other seats' trees, not a one-file
edit. Per CLAUDE.md that is the owner's call and I will not widen it unasked.

The exact remedy, for whoever takes it -- changes no committed bytes, since the index is already LF:

```
git rm --cached --quiet data/mdpf/config/route_bindings.yaml && git checkout -- data/mdpf/config/route_bindings.yaml
# or, per tree:   rm <file> && git checkout -- <file>
# verify:         git ls-files --eol -- data/mdpf/config/route_bindings.yaml   ->   want  i/lf  w/lf
# then:           terraform plan   ->   want  "No changes"
```

And separately: extend the glob to cover the `.json`, which is a real `.gitattributes` edit rather than a
re-normalization:

```
data/mdpf/config/*  text eol=lf      # or add an explicit *.json line
```

**Claim field:** every value here is `measured` except one, named inline -- whether `partner_roster.json`
currently mismatches its deployed S3 copy. Nothing was applied; reads only.
