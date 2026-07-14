# `opal-data-bd/ajb_workspace/` — read-only inventory

**GO:** Andrew (accepted CTO's rec) → COO relay, 2026-07-14. **Scope: THIS PREFIX ONLY.**
**Author:** `0.4.0_DS_ClientPlatform` · **Enumerated:** 2026-07-14 02:57Z (run-time denominator)
**Actions taken: ZERO.** No disposal, no move, no deletion, no lifecycle rule, no other bd prefix touched.
The bd sovereign prohibition otherwise stands whole; Andrew's acceptance is the explicit ask **for this
scope and nothing wider.**

---

## The finding, first

> ### It reads as bulk junk. **11 objects in it exist nowhere else on earth.**
>
> | | |
> |---|---:|
> | objects under the prefix | **703** |
> | recoverable from git history (**proven**, not assumed) | **692 (98.4%)** |
> | **present ONLY in this bucket** | **11 (122.8 KB)** |
> | referenced by any code, anywhere | **0** (21,504 files scanned) |
>
> **This is the same shape as `01_raw`, twelve hours later:** a prefix that looks entirely disposable —
> 703 duplicated agent logs nothing reads — with a small irreplaceable core hidden inside it. There, 257
> of 7,142. Here, 11 of 703. **The percentage is the disguise. In both cases the honest move and the
> cheap move are the same move: preserve the few, then dispose of the rest.**

### The 11 sole-copy objects

```
 11,856b  logs/sessions/2025-11-20/data_scientist/schwab_aum_carving_investigation.md
 10,247b  logs/sessions/2026-02-19/devops_technician/smartx-pipeline-validation.md
 12,193b  logs/sessions/2026-02-19/devops_technician/yang-complete-configuration-audit.md
 14,118b  logs/sessions/2026-02-19/devops_technician/yang-consolidation-phase2-3.md
 14,716b  logs/sessions/2026-02-19/devops_technician/yang-discovery-phase1.md
 12,093b  logs/sessions/2026-02-19/devops_technician/yang-function-audit-deployed-vs-local.md
  9,890b  logs/sessions/2026-02-19/devops_technician/yang-phase4-validation.md
 12,265b  logs/sessions/2026-02-19/devops_technician/yang-rescoping-risk-assessment.md
  9,232b  logs/sessions/2026-02-20/data_scientist/silver_layer_backfill_and_canonical_prices.md
  9,284b  logs/sessions/2026-02-20/devops_technician/moltbot-architecture-and-github-wiring.md
  9,830b  logs/sessions/2026-02-20/devops_technician/moltbot-devsecops-session.md
```

They are not random: **eight of eleven are the Feb-2026 `yang` audit + consolidation series** (discovery →
config audit → deployed-vs-local → phase2-3 → phase4 → risk assessment). That is a complete
investigation arc, and it is the kind of record someone goes looking for exactly once, years later,
when the question it answers comes back.

---

## What it is

| property | value |
|---|---|
| objects | **703** (enumerated at run time 02:57Z; 1 write-date, so this one is *not* moving) |
| size | 9.9 MB |
| composition | 701 `.md` + 1 `.jpg` + 1 `.png` |
| structure | `ajb_workspace/logs/sessions/{YYYY-MM-DD}/{role}/*.md` — **the workspace's own v1-era agent session logs** |
| content dates | 2025-11-17 … 2026-02-23 (58 distinct days) |
| roles | aws_engineer 271 · dashboard_engineer 125 · react_designer 90 · systems_architect 80 · data_scientist 79 · devops_technician 45 |
| S3 write date | **2026-02-23, all 703** — a single one-shot bulk upload, never added to since |

**It is not client data and it is not a pipeline artifact.** It is Opal's internal operational history,
bulk-copied once into a client-custody bucket and then forgotten. `logs/sessions/` was later deleted from
the repo in a 7-part cleanup series (`chore(cleanup): delete deprecated root logs/ tree [4/7]`), which is
why the bucket copy became load-bearing for the 11 without anyone deciding that it should.

## Referencers: **none**

`comp-grep --include-held 'opal-data-bd/ajb_workspace'` over the repo → **0 matches in 21,504 files.**
Nothing reads it, nothing writes it. The 8 hits for `ajb_workspace/logs` are **filesystem paths**
(`/home/ajb327/ajb_workspace/logs/sessions/…`) inside archived docs — citations of a local path, not S3
reads. **No consumer to repoint.**

---

## Disposition — NOT MINE, and I am not proposing one

The GO is **inventory only.** bd is under the standing prohibition; disposal is Andrew's and nobody
else's. What the inventory establishes, and stops at:

- **692 of 703 are redundant.** Deleting them destroys nothing.
- **11 are not.** They exist in no git commit, no working tree, and no other bucket I am permitted to
  look in.
- **If a disposal ever happens, the 11 come out first.** They are 122.8 KB. The cost of preserving them
  is nil and the cost of not preserving them is total and permanent.

**I have not moved them, copied them, or "rescued" them.** Copying an object *out* of a held bucket is a
verb the prohibition covers, and a helpful agent quietly rescuing files is precisely the second failure
mode COO named when he put this on the board. It waits for Andrew.

---

## How the "692 recoverable" claim was proven (because it nearly wasn't)

My first recoverability probe **reported success and had retrieved nothing.** It ran
`git show <commit>:<path> | head -3` and tested the **pipe's** exit status — which is `head`'s, always 0 —
so it printed the success branch under an empty output. It also asked the wrong commit: the *last* commit
touching `logs/sessions/` is the one that **deleted** it, whose tree contains zero files.

The corrected probe takes git's own return code and asks the commit that **ADDED** each file:

```
logs/sessions/2025-11-17/aws_engineer/schwab_s3_complete_archive_upload.md
  added in 3a9819e40 → git show rc=0, bytes=7114 → RECOVERABLE: True
```

**This is the fourth instrument to lie to me tonight, and it is the one CLAUDE.md warns about by name**
(*"`git show <bad-ref> | grep -c foo` prints 0 — put the control on the RETRIEVAL, not the pattern"*).
Had I not re-checked, I would have filed "703 objects, all safely in git" — and the 11 would have been
deleted on my evidence.

## Gaps

| gap | why |
|---|---|
| whether the 11 contain anything sensitive | **not opened.** The GO is enumerate-and-find-referencers; reading content is characterization beyond it. |
| whether copies exist outside git + this bucket | not established — I am not permitted to sweep other bd prefixes, and did not. |
| disposal recommendation | **not mine.** Andrew's, under the prohibition. |
