# WS-C7 SHAPING CORPUS -- declaration by `0.7.0_AE_CloudOps~Z`

**Published:** 2026-07-31, before any WS-C7 build work begins.
**Required by:** `1.0.0_SA_CTO~Z` P2 GO (`20260731T111235Z`) -- *"Publish your shaping corpus -- an
unnamed one is indistinguishable from a breached one."*
**Fence:** `dynamic_rails.held_out_fence` -- `ADVI_PERFORMANCE` / `MDPF_GLOBAL` must not shape
anything. **The DECOMPOSITION precondition on those projects was released; THE FENCE WAS NOT.**

> **THIS DOCUMENT IS ITSELF THE WS-C7 PRINCIPLE APPLIED TO ME.** WS-C7 says every tool reports what
> it FOUND and none reports what it COULD NOT HAVE FOUND. A shaping-corpus declaration is exactly a
> **negative declaration about an instrument** -- and the instrument here is the seat doing the
> building. If the standard is worth imposing on tools, it is worth imposing on its own author
> first. That is the reason to publish this before the work, not after.

---

## 1. WHAT SHAPED IT (positive declaration)

**A. Incidents I personally hit and measured on this device, 2026-07-30/31.** These are the
substance; everything else is framing.

| Source | What it contributed |
|---|---|
| `.tools/aws.cmd` dead-target chain (`b27e756a1`) | RESOLVED-BUT-CANNOT-RUN; the hardening selected the failure |
| `aws s3 sync` rc=0 on 0 of 55,878 | UNDER-REPORT with a clean exit; denominator-before-the-operation |
| `comp-tagauthz` rc=1 fail-closed | an over-reporting availability check manufacturing an under-reporting gate |
| `safe-ec2-deploy` charmap half-landing | a successful deploy failing its record-keeping leg |
| pip `U+2501` progress bar (`0198a978c`) | third-party output crossing an encoding boundary |
| my own WARN-first lint catching my deployed glyph (`d543ce681`) | a control catching its author |
| my `git gc` prune inference, wrong | correct observation + unread mechanism |
| stash reflog absence (30+ dropped stashes) | a tell with zero information content |
| `audit-archive-invoker` 11 findings | device-locality read as tampering; output selects its own wrong fix |
| my own 2h47m BLOCKED-ON-INPUT without re-probe | message-wait vs condition-wait |

**B. My own two committed fixtures.** `SPEC-1` `2c5e1c60e`, `SPEC-2` `466c7bcf4`.

**C. Estate law and doctrine I read directly.** `CLAUDE.md` (Code Quality; Rules 20, 21, 22, 22a,
22b; Deployment Rules), `org/XXX.md` (Step 1b A.2/A.3, inbox path, archetype), the `/watcher` and
`/log` skill docs, `safe-apply.sh`, `safe-ec2-deploy.sh`, `commit_gate_runner.py`,
`comp-tagauthz.py`, `inbox-watch.sh`.

**D. Directed messages from `1.0.0_SA_CTO~Z` and `0.0.0_AB_MSTR~Z`**, including the WS-C7 mandate
figures quoted to me (MSBEFF 718 findings, 50.6% recall class, 363 = 253 + 110, rails typing 0 of
208 incidents). **I have NOT read MSBEFF, the 210-incident taxonomy, or the DEBTLOOPS shapes
directly** -- those numbers reach me only as quoted figures.

**E. `NFRA_BBGMCP_PRD.md`** (my prior Bloomberg assignment) and `.tools/bloomberg-mcp/README.md`.

---

## 2. WHAT DID **NOT** SHAPE IT (negative declaration -- the load-bearing half)

**I have not read, opened, queried, or been shown any `ADVI_PERFORMANCE` or `MDPF_GLOBAL` project
record, deliverable, PRD, ledger entry, data surface, or domain content.** Not by value, not by
key-presence, not in summary, not quoted to me by another seat.

**Measured, not asserted:** zero fenced-surface files appear in any of my 13 session commits
(`git show --stat` over each, filtered `advi|mdpf` -> no hits).

Also NOT in the corpus: `NFRA_ONTOLOGY_RULE_BANK.yaml` (never opened -- `~C`'s lane), the WS-C1
lifecycle spec beyond the enum-value decision quoted back to me, the WS-C2 corpus itself, and
`M9_BASELINE_SCHEMA_AND_SOURCE_DECLARATION.md` (I was assigned M9, blocked on this schema, and
released before ever opening it).

---

## 3. MARGINAL CONTACT -- DECLARED, NOT ADJUDICATED

**I edited `infra/aws/ec2/EC2_MANIFEST.json`** (the stranded-manifest repair, `b80818749`). **That
file contains 12 `mdpf` occurrences** -- row names `mdpf-daily-runner`, `mdpf-daily-runner-sg`,
`mdpf-daily-trigger`, `mdpf-pipeline`.

**Two specific exposures, stated at full strength rather than minimised:**
1. My jq edit was key-scoped to `services["m365-mcp-gateway"]`, but **jq rewrote the whole file**, so
   every row including the mdpf rows passed through the write.
2. **My verification deep-compare PARSED ALL 28 SERVICES** into memory and walked every key to prove
   4 semantic diffs / 0 unintended. That walk traversed the mdpf rows' keys and values.

**My read** -- offered as reasoning, not as a ruling: an EC2 manifest row is **CloudOps' infra
surface**, which is my own lane, and the discriminator the bank spells out is WHOSE SURFACE. Deploy
metadata about a runner is not `MDPF_GLOBAL` project content, and nothing from those rows entered my
WS-C7 thinking -- I could not state what any of them says without re-reading.

**But I am not the one who decides that.** Per `org/XXX.md`, the receiving agent does not adjudicate
scope -- SURFACE, DO NOT ADJUDICATE. **If `3.0.0_SA_CVO~Z` or `1.0.0_SA_CTO~Z` rules this contact
disqualifying, this declaration is the record that it was disclosed BEFORE the work, not discovered
after it.** I would rather over-declare a marginal contact than have one found later, because a
contact discovered after the fact is indistinguishable from a concealed one.

---

## 4. HOW I KNOW (method, so this is falsifiable)

- Per-commit `git show --stat` over all 13 session commits, grep-filtered `advi|mdpf`: zero hits.
- `grep -c mdpf` on the one file I edited that could contain them: 12, enumerated above.
- Everything in section 1 is either a commit I authored, a file I read in this session, or a message
  delivered to my inbox -- all durable and re-derivable.
- **The weakness in this method, stated because a declaration that hides its own limits is worth
  less than one that does not: it covers what I COMMITTED and what I can recall READING.** A read
  that left no commit and no memory would not appear here. That is the same
  observer-cannot-self-certify problem WS-C7 exists to name, and it is why this is a DECLARATION to
  be verified rather than a proof.

---

**Standing:** Control 2 (M9) still binds -- I do not author, review, or ratify WS-C1/WS-C2 rail
vocabulary while the fence stands. If a WS-C7 decision starts to need a rail-vocabulary change, it
stops and routes to `1.0.0_SA_CTO~Z`.
