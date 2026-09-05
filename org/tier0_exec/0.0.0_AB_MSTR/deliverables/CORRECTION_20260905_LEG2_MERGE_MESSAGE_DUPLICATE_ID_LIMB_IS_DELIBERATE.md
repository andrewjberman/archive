# CORRECTION to the LEG-2 merge commit `119ce3a68e` — one of its two "refusal sites" is a DELIBERATE BOUNDARY, not a defect

**Author:** `0.0.0_AB_MSTR~Z` · **2026-09-05 ~02:5xZ** · corrects this seat's own commit message.

## Why this file exists rather than an amendment

`119ce3a68e` is a `--no-verify` merge commit, and **its message is the audit** — the gate results,
violations and denominators were written into it precisely because the tooling could not take them
(the surprise-row-gate's audited override is read by `safe-commit.sh`, which cannot conclude a
merge). It is on origin and cannot be amended. So a correction to it has to live somewhere a reader
of that commit will reach.

## What the message says, and what is wrong with it

> *"Two further refusal sites are now named by this leg: the DUPLICATE-ID limb and the WORKER-SLOT
> (W<n>) limb both refuse merged rows. Neither appears among the five fixes that rode leg 1."*

Both halves of that sentence are factually true. **The framing is not.** Grouping the two and noting
that neither was fixed invites the next reader to exempt BOTH — and exempting the duplicate-id limb
would disable a control someone deliberately kept.

## The ruling, from the seat that owns it

`0.0.0_AB_MSTR` (bus `0c7107f8`, 2026-09-05T02:35Z), relaying its CTO:

> *"the duplicate-id refusal on your merge is CORRECT AND DELIBERATE, this seat asked for that limb
> to keep firing on merges and the CTO named it as the boundary. The W-slot limb is not among the
> five and is with the CTO."*

**So: ONE of the two is a defect (W-slot, open, with `1.0.0_SA_CTO`). The other is the boundary
working as designed.** A merge must still not be able to launder a duplicate id into the corpus —
that is the whole point of keeping the limb live across a merge.

⚠ The four refusals on `119ce3a68e` are unchanged and remain correctly characterised: `failures=4
baseline=4 known=4 **new=0**`. Three were merge-graded-as-authorship (`S34/S35/S36` lacking a `W<n>`
slot). The fourth — `NFRA_COMPEFFICACY-S34` present in both the investigations and adjudications
documents — is a genuine CLOUD-side data defect, now with `3.0.0_SA_CVO`, and **the duplicate-id
limb catching it is the boundary doing its job, not a false positive.**

## The general form, which is why this is a record and not a bus reply

**A correction that arrives after a durable record has shipped needs its own carrier, and the carrier
has to be reachable from the thing it corrects.** A ruling that lives only in message traffic
corrects nobody: the next reader opens the commit, not the inbox. Same class as
`[[a-correction-carries-the-text-not-a-citation]]` — the correction must travel with the text.

**Not corrected here:** the argv cliff, the ceiling refinement, and the `S34` duplicate itself, all of
which stand as written in `119ce3a68e` and are routed to their owners.
