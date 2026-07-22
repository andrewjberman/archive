# comp-iam: should the tool key off LIVE state instead of Terraform? — grounding for Andrew's proposed flip

**Author:** `0.8.0_AE_CloudComp` · **Date:** 2026-07-22 · **For:** Andrew (direct)
**Question asked (verbatim):**

> "Is the basis for the lack of research identification here is because its keying off of terraforms
> and when we're in a state of building many new resources the terraforms for those items simply dont
> exist yet? If that is the case, I think we should flip the mechanism of the tool, which is probably
> the more logical use case anyway. Instead of keying off terraform resources as primary, it keys off
> the real state as primary, which should all be discoverable via kuzu anyway."

**Verdict: FLIP IS RIGHT — but the dominant mechanism is NOT the one in the hypothesis, and the
argument for flipping is STRONGER than the one proposed.** Both claims tested rather than accepted.

---

## 1. The hypothesis, measured

"The terraform for new resources simply doesn't exist yet."

Of 35 live roles comp-iam reported as not-in-Terraform (47 raw, minus 12 AWS service-linked classified
on the structured `/aws-service-role/` ARN path):

| bucket | n | meaning |
|---|---|---|
| mentioned in a `.tf`, not parsed by comp-iam | 7 | parser defect — the flip does NOT fix these |
| no literal mention in any of 383 `.tf` files | 28 | *appeared* to confirm the hypothesis |

**THE 28 WAS MY OWN INSTRUMENT ERROR AND I RETRACT IT.** A literal substring scan cannot find an
identifier that Terraform CONSTRUCTS:

```
infra/aws/terraform/opal-assets/silver.tf:295     name = "opal-assets-silver-${each.key}-role"
infra/aws/terraform/modules/served-guard/main.tf:24  name = "opal-${var.firm}-served-guard"
```

All six `opal-assets-silver-*` roles and all three `opal-*-served-guard` roles ARE declared in
Terraform. There are **102** interpolated `name =` assignments in `infra/**.tf`, so this is systemic
for any literal-name matching. **kuzu classified them `DECLARED` and was right; my grep said
"no Terraform" and was wrong.** I ran a literal matcher against dynamically-constructed identifiers
and read absence as absence — the same shape as every other false-clean catalogued today.

## 2. The REAL mechanism, and it is more fundamental

comp-iam holds **`opal-assets-silver-${each.key}-role`** in its parsed role table — the template
string, verbatim, as a role name. One template row against six real live roles.

> **TERRAFORM SOURCE IS A TEMPLATE, NOT A FACT. Names, ARNs and ids are resolved at APPLY time.**
> comp-iam's DESIRED↔APPLIED join is exact string equality on `RoleName` (CVO brief §2 #3).
> **So any resource whose identity is COMPUTED is unjoinable BY CONSTRUCTION.**

That is not a coverage gap more parsing fixes. It is the wrong plane holding the wrong kind of object:
a template cannot be joined to an instance by name, because the template does not have a name.
It also explains CVO's brief §7 head-to-head observation — comp-iam printing `${aws_instance.astn.id}`
where live resolves `i-059405dfefcb4b44a`. Same defect, resource axis instead of role axis.

**Why the hypothesis still lands:** it is right in EFFECT for new construction — a `for_each` fleet is
exactly what recent building produces, and those are precisely the unjoinable ones. It is wrong in
CAUSE: the Terraform exists. It just does not contain resolvable identities.

## 3. "Discoverable via kuzu anyway" — VERIFIED TRUE, with three bounds

`comp-kuzu`, DB `kuzu_nessie_db`, built 2026-07-22T16:54:58Z:

| check | result |
|---|---|
| live IAM in the graph? | YES — 193 `IAM_ROLE` + 441 `IAM_POLICY` `CloudNode`s |
| resolved identities? | YES — real names/ARNs (`arn:aws:s3:::opal-data-inf`, `drift_class LIVE-INCREMENTAL`) |
| coverage vs live account (205) | 193 present, **0 phantoms** (nothing in kuzu that is not live) |
| **already computes the set-difference?** | **YES — `drift_class`: `DECLARED` 173 / `LIVE-no-DECLARED` 20** |
| gets the interpolated ones right? | YES — the exact cases comp-iam and my grep both got wrong |

**kuzu is already doing live-primary drift detection. comp-iam is re-deriving a worse version of a
computation the graph already performs correctly.** The flip is less "build a new mechanism" than
"stop ignoring the one that exists."

**BOUNDS — stated so the flip is not oversold:**
1. **12 live roles absent from kuzu** — all `AWSServiceRoleFor*` (AWS-managed, service-linked). They
   are the population you would exclude anyway, but "kuzu is complete" is false; it is complete for
   the *governable* population. A flip must state that denominator, not inherit it silently.
2. **kuzu has a vintage** (nodes last-write 4.2h; DB built 1.9h). The same vintage-honesty discipline
   built into the census this session applies to kuzu. **Good news: `comp-kuzu` already prints a
   provenance header with per-table vintage — the flip inherits vintage honesty rather than needing it
   rebuilt.**
3. **kuzu is a DETECTOR, not an AUTHORIZATION ORACLE.** It holds nodes and a drift class; it does not
   evaluate Deny, boundaries, conditions or SCPs. The brief's Plane-2/Plane-3 separation must survive
   the flip intact: `simulate-principal-policy` stays the only allow/deny authority (Rule 22a).
   A live-primary index makes the detector honest; it does not make it an oracle.

## 4. What the flip changes, concretely

- **PRIMARY becomes the live population** (kuzu index, census for statement-level depth). Terraform
  becomes the *overlay* answering "is this governed by IaC?", which is the question it can actually
  answer — a template is fine evidence of INTENT and useless as evidence of IDENTITY.
- **The unjoinable class disappears** rather than being reported as drift: a `for_each` fleet resolves
  to six live roles that all trace to one declaration, instead of six false "ungoverned" findings plus
  one TF row matching nothing.
- **Andrew's third gap closes properly**: the set-difference finally runs against the real population
  instead of an enumerated subset. That is what makes MISSING distinguishable from ABSENT.
- **The 7 parser-gap roles remain a genuine comp-iam defect** and are NOT fixed by the flip. Named so
  the flip is not credited with them.

## 5. Residual / not claimed

- Whether kuzu carries statement-level grants (action-level drift) at sufficient depth to replace the
  census for `reconcile`'s action comparison — **NOT verified**. `IAM_POLICY` nodes exist (441); their
  contents were not inspected. Until checked, the census remains the statement source and kuzu the
  identity/population index.
- What kuzu's `DECLARED` is computed AGAINST (which declaration source the derive reads) — **NOT
  determined**. It is demonstrably not a literal `.tf` name scan, since it resolves interpolated names.
  That mechanism should be read before the flip depends on it.
- The 12 service-linked absences: whether deliberate exclusion or ingestion gap — **NOT determined**.
