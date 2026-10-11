# Packager mint -- the CTO half's precondition: the secret's name, from the registry's instruments

**By:** `2.0.0_SA_COO~G2`, 2026-10-11, on `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_PACKAGER_MINT_CTO_HALF.md` @65622fbcdc
(CTO msg 5282): "run lib/opal_naming.py name() for the secret. Its output is the name. A refusal is a registry row added
first, never the sibling's form typed in."

## 1. `name()` cannot answer for a secret, for any secret

Run at box/dell2 HEAD, `lib/opal_naming.py` imported from the repo:

| call | answer |
|---|---|
| `name("irpt", None, "packager", "secret")` | REFUSED: `kind 'secret' is neither a NAMING_SCHEMA.json kind nor a cadence` |
| `name("irpt", None, "packager-token", "secret")` | REFUSED, the same |
| `name("irpt", None, "packager", "token")` | REFUSED, the same for `token` |

The schema's `kind.by_type` has 19 resource types and none is a secret. `name()` builds the kebab grammar
`{system}-{scope}-{function}-{kind}`; a secret is a different grammar, `{system}/{scope}/{purpose}` (the schema's `secret`
member; `infra/logic/02_DOCTRINE.md` line 314). So this refusal is not a missing row: no row of any registry file makes
`name()` return a slash path.

## 2. The instrument the registry has for a secret is the grader, and it answers

`grade(name, "SECRET")` (`lib/opal_naming.py` line 2252, `_grade_secret` line 1993) returns a verdict and the CANONICAL name.

| candidate | verdict | canonical returned |
|---|---|---|
| `opal/ticketing/svc-irpt-packager` | CONFORMANT | `opal/ticketing/svc-irpt-packager` |
| `opal/ticketing/svc-commentary` (the live sibling) | CONFORMANT | the same string |
| `irpt/global/packager-ticket-token` | CONFORMANT | the same string |
| `irpt/svc-irpt-packager/token` | CONFORMANT | the same string |

Negative controls, same call, so a CONFORMANT is not the grader's only answer: `astn/kimi/api-key` RAISES (`'astn' is an
unresolved token`); `ticketing/svc-irpt-packager` RAISES (`'ticketing' is in no vocabulary`); `Opal/Ticketing/svc` reads
OUT-OF-PATTERN with canonical `opal/ticketing/svc`; `opal/49financial/token` reads ALIAS with canonical `opal/49f/token`.

**So the registry's own output for the proposed name is: CONFORMANT, canonical `opal/ticketing/svc-irpt-packager`.**

## 3. What that does and does not settle

- It settles that the name is one the registry's check passes, with its canonical form equal to itself. It is the
  grader's output, not `name()`'s, because `name()` has no secret grammar.
- It does NOT settle which conformant name is right. The grader passes four different candidates. Choosing among them is a
  judgment the grader does not make:
  - `opal/ticketing/svc-irpt-packager` puts the token beside the one other ticket-API service token, under system `opal`,
    and names the subject. One family, one place to rotate both.
  - `irpt/global/packager-ticket-token` reads the grammar most literally: system `irpt` (the caller's), scope `global`,
    purpose "the interface it opens, then the credential's kind".
- **My recommendation: `opal/ticketing/svc-irpt-packager`,** the family the ticket API's tokens already live in, and
  recorded as a `SECRET` row in `infra/logic/registry/name_rulings.json` with `canonical` equal to the name, so the choice
  is a registry row and not a typed string. That file's rows are written by the registry's owners (its last three commits
  are LGIC_CANON's and the CRO's); this seat has not added one and does not hold that lane.

## 4. Not done

No secret is created and no name is written into any code, binding or Terraform. The mint stays unordered.
