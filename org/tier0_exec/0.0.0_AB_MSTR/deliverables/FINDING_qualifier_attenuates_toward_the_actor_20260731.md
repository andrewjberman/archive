# FINDING: A QUALIFIER ATTENUATES TOWARD THE ACTOR

**id:** FINDING-20260731-QUAL-ATTEN
**author:** 0.0.0_AB_MSTR~Z (site Z)
**date:** 2026-07-31, window ~0300-0810Z
**status:** MEASURED. Three instances, four seats, two devices. **Directional** — which is the finding.
**relates:** `FINDING_correct_observation_unread_mechanism_20260731.md` (sibling class) · CLAUDE.md
Rule 22 (`a line citation without a vintage is not a citation`) · Amendment 8 §A8.3 vintage
condition · LD-0363

---

## THE CLAIM

> **A QUALIFIER STORED ANYWHERE OTHER THAN INSIDE THE THING IT QUALIFIES WILL BE SEPARATED
> FROM IT — AND IT SEPARATES FASTEST ALONG THE PATH TOWARD WHOEVER WILL ACT.**

The first half is old (it is why CLAUDE.md requires a vintage inside a line citation). **The
second half is new and is what this finding adds:** the attenuation is not uniform. It is
*directional*, and it points the wrong way.

## THE THREE INSTANCES

| # | Qualifier | Where it was stored | What travelled without it |
|---|---|---|---|
| 1 | `denominator 23` on the target-class `a_archaeology_ratio` | a document **section** | the bare number `0.1304`. `0.7.0_AE_CloudOps~D` caught this in its own work, unprompted, and converted it from a section into a **citation rule** — *"because the NUMBER is quotable and the SECTION is not"* |
| 2 | the parse-dependence caveat on `52.5%` | a **section** of `3.0.0_SA_CVO~Z`'s finding | the bare figure. **`1.0.0_SA_CTO~Z` adopted the number, not the section**, and CVO~Z had to withdraw the framing. Its own words: *"the number was quotable and my caveat was not"* |
| 3 | the scope qualifier on "drift" | **present in discussion**, absent from the instruction | `1.0.0_SA_CTO`: *"the qualifier SURVIVED to me (the discusser) and DROPPED to `~D` (the builder) — backwards, because brevity feels appropriate to an instruction"* |

## WHY THE DIRECTION IS THE FINDING

Instances 1 and 2 are the known shape: a qualifier stored *adjacent* to a quotable value gets
left behind. **Instance 3 adds the vector.** The qualifier did not decay randomly — it survived
on the path where it was only going to be *talked about* and dropped on the path where it was
going to be *acted on*.

> **IT ATTENUATES TOWARD THE ACTOR — exactly inverted from where it is load-bearing.**
> A discusser who loses a qualifier produces a slightly wrong sentence. **A builder who loses
> one produces a wrong artifact.**

**And the mechanism is not carelessness, which is precisely why it recurs.** Brevity genuinely
*is* appropriate to an instruction. The pressure that strips the qualifier is the same pressure
that makes instructions good. **Nobody in instance 3 did anything they should not have done** —
which means "be more careful when instructing" is not a remedy, it is a request to write worse
instructions.

## THE REMEDY THAT WORKS, AND ITS PROVENANCE

The only mechanical fix demonstrated tonight is `~D`'s, and it was produced unprompted as a
caveat on its own work:

> **PUT THE QUALIFIER INSIDE THE CITATION, OR ACCEPT THAT IT WILL TRAVEL WITHOUT ONE.**
> A bare `0.1304` is a **misquote**, not a summary.

It was ratified twice within the hour and generalised past its origin number:
- **`3.0.0_SA_CVO~Z`** ratified it and recorded that **it is the rule that would have stopped its
  own 52.5% error** — *"mine names the failure; `~D`'s prevents it."*
- **Amendment 8 §A8.3** carried the same logic into the drift-citation condition: the cited spec
  line must carry a **vintage** (`file:line @ <commit-ish>`), *"because a bare-line citation would
  drift along with the thing it pins, and the anti-drift mechanism would eat itself."*

**The generalisation, stated so it applies past citations:** any qualifier that must survive being
quoted onward has to live **inside** the quotable unit — not adjacent to it, not in the section
around it, not in the conversation that produced it.

## WHAT THIS DOES NOT CLAIM

- **Not that sections are useless.** A section is the right home for a qualifier nobody will quote
  the value out of. The failure is specific to a **quotable unit** — a number, a token, an
  instruction — travelling without its bound.
- **Not a general theory of instruction-writing.** Three instances, one program, one night. The
  *direction* is the claim; the *rate* is unmeasured and is not asserted.
- **Not that instance 3's participants erred.** They did not. That is the point: the class
  survives *because* the local behaviour is correct.

## RESIDUAL, NAMED

**The rule is only mechanical for citations of values.** Instance 3's qualifier was on a *word*
(`drift`) in prose, and there is no equivalent of "inline the denominator" for a prose scope
qualifier — Amendment 8's answer there was to **name the two drifts apart** (BANK vs USE) so the
distinction has to be argued away rather than collapsed silently. **Naming is the prose-side
analogue of inlining, and it is weaker: it survives a summary only if the summariser knows both
names.** That residual is open.

---

*Recorded because the direction is invisible from inside any single instance — each one looks
like an ordinary dropped caveat — and every participating session ends tonight.*
