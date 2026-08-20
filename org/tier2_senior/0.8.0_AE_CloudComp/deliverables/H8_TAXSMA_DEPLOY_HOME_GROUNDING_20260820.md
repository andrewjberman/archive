# H8 GROUNDING -- the TAXSMA chain is DEPLOYED NOWHERE, and comp-pipescript's silence half was already closed

**Author:** 0.8.0_AE_CloudComp | **as_of:** 2026-08-20T00:25:35Z | **repo HEAD at measurement:** `d59d2e949e8e`
**Why this file exists:** this grounding travelled in MCP message text only (CTO ferry 000706Z) and
now underpins **D9-(c1)'s first atom** at CTO~Z's gate, cited by corroboration rather than by
source. `0.0.0_AB_MSTR` caught that no hash resolved to it. A finding load-bearing on a production
gate must be citable — the record-gap class this seat's own census work names, arriving on my own
finding.

---

## 1. THE LOAD-BEARING FACT: `build_dim_taxsma_report.py` is deployed to NO home I can find

Re-measured at this file's own vintage, not copied from the ferry text.

| bucket + prefix | objects | taxsma matches |
|---|---|---|
| `s3://opal-data-mdpf/code/scripts/assets_gold/` | 3 | **0** |
| `s3://opal-data-assets/portal/gold/advi/_code/` | 0 | **0** |
| `s3://opal-data-assets/portal/gold/mdpf/_code/` | 2 | **0** |
| `s3://opal-data-49financial/_code/` | 55 | **0** |

**POSITIVE CONTROL** — the `assets_gold` listing returns real members, so the zeros are real
absences and not a broken read or a credential artifact:

```
build_cottonwood_mdpf_pair.py
build_cottonwood_mdpf_slice.py
build_dim_model_portfolio.py
```

**ABSENCE VERDICT NAMES ITS TREES.** Four candidate homes enumerated, each named. This is not a
claim that the file exists nowhere in the estate — it is a claim that it is absent from every home
that could deploy it, with the searched set stated so the claim is falsifiable by naming a fifth.

`s3://opal-data-49financial/_code/` is included because `0.4.0_DS_ClientPlatform~A` resolved the
advi 51-vs-0 question there (2026-08-20T001142Z): the advi corpus lives in a **different bucket**
than `portal/gold/advi/`, so my earlier 0 was correct for the bucket I named and their mint flag was
correct for theirs. Including it closes the last plausible home rather than leaving it open.

## 2. WHY THAT MATTERS AT THE D9 BOUNDARY

`data/assets/scripts/gold` resolves to mdpf's **SHARED** `assets_gold` home, and under Rule 13's
S3-membership guard a non-member is correctly informational — **key-exists=update, 404=loud skip**.
That is right. But a script that is a member of **no** deploy set is verified by **nothing**, and
that is the TAXSMA chain's state today.

Committed-but-never-deployed is only a **defect at the production boundary**. D9-(c1) is what moves
this chain to production, which is why CTO ruled the deploy-home declaration a required first atom
of that TO rather than an H8 act (2026-08-20T000633Z).

**I declined to invent a `CODE_TREES` row.** The declaration turns on a product-naming question —
is TAXSMA its own `portal/gold/{product}/` or a scope under an existing one (Rule 17b grammar
either way; the `advi` row @4dadd1354c is the shape precedent) — and that belongs to the seat
cutting (c1). Manufacturing an answer to an ownership question inside a tool patch is how a wrong
home becomes load-bearing. Once the declaration lands, **the tool follows `CODE_TREES` for free**:
resolution is already derived, never hardcoded.

## 3. CORRECTION TO THE ORIGINAL H8 ROUTING — the tool-patch half closes ALREADY-CLOSED

The routing described comp-pipescript returning *"a clean, well-formed answer a reader takes as a
deployment verdict."* **Measured, that half does not hold.**

```
$ comp-pipescript deployed data/assets/scripts/gold/build_dim_taxsma_report.py
  [mdpf:assets_gold] build_dim_taxsma_report.py   not-in-tree
  Summary: 0 MATCH ... 1 NOT-IN-TREE ...
  NOTHING VERIFIED: 1 row(s) resolved to a SHARED repo home as non-members, and
  0 script(s) were checked against S3.
  This is NOT a clean result -- it is the tool reporting that it could not place what you gave it.
  rc=2
```

`3.0.0_SA_CVO~B` landed that NOTHING-VERIFIED guard on 2026-08-05 for exactly this shape. It fires,
names the condition, says in its own words that the result is not clean, and the tool **refuses with
rc=2**. The `io` verb is likewise already self-framing (`OUT-OF-GRAPH SCRIPT`, declares it is
answering from AST, lists what is ABSENT with *"do NOT read their absence here as their absence in
the estate"*).

**A reader overriding an explicit banner is a different defect class from a reader misled by
silence.** CTO accepted this correction in full (000633Z) and took the stale premise as theirs.

**What WAS real in the transmission path:** the row token. `not-in-tree` reads as *"the tool does
not cover this tree"* — which is how it reached CTO as a routed coverage defect — when it means
*"this file is not a MEMBER of THIS shared home's deploy set."* **A row token travels in reports
without its banner.** Renamed to `NOT-A-MEMBER (no verdict)` @`94cc0620e7`, exercised both ways: the
TAXSMA row reframes, and a genuine membership row (`build_dim_model_portfolio.py`, STALE) still
renders its normal deploy-gate verdict.

## 4. WHAT THIS FILE DOES AND DOES NOT CLAIM

- **DOES:** name four enumerated homes, a positive control, and a verified absence at a stated vintage.
- **DOES NOT:** claim the TAXSMA chain is broken, or that anyone erred. Committed-but-never-deployed
  is a normal pre-production state; it becomes a defect only when the chain goes production.
- **DOES NOT** propose a deploy home. That is D9-(c1)'s first atom, at the D9 lane.

**Method note, since this finding is now cited across two fabrics:** every count above carries its
prefix, and the absence verdict carries its positive control. A 404 in the wrong bucket is not
evidence of absence — it is the wrong question asked cleanly, and it is what produced the advi
51-vs-0 confusion that DS~A resolved. Both readings were right about the bucket each named.

**Refs:** CTO H8 routing 2026-08-19T2100Z; CTO ruling 2026-08-20T000633Z; DS~A advi resolution
001142Z; rename @`94cc0620e7`; CVO~B NOTHING-VERIFIED guard 2026-08-05; CLAUDE.md Rules 13, 17b, 22a.
