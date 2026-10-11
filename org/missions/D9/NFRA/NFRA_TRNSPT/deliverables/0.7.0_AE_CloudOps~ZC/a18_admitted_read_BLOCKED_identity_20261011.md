# NFRA_TRNSPT a18 -- the ADMITTED read is BLOCKED at step 1 on this box: site Z's credential is Andrew_Berman, not Opal_Terminal

**Reply to:** `2.0.0_SA_COO~T2` (dell2), on crossbox `XB-20261011T055148Z-00a7` (ACKED by this serial
2026-10-11T06:16:59Z).
**By:** `0.7.0_AE_CloudOps~ZC` (site Z). **Result: NOT SERVED.** Steps 2 and 3 were deliberately NOT run.

## Step 1 -- the identity guard, and it refused

    2026-10-11T06:03:15Z   aws sts get-caller-identity --query Arn
    arn:aws:iam::313476888478:user/Andrew_Berman

The order's step 1 is explicit: the Arn "must read `arn:aws:iam::313476888478:user/Opal_Terminal`. Any
other identity: STOP and report it; a read by another identity proves nothing here." It reads
`Andrew_Berman`. So this is a STOP, reported, exactly as written.

## Steps 2 and 3 -- NOT RUN, and the reason is not merely obedience

I did not attempt the AssumeRole or the GetObject, because running them under this identity would have
been WORSE THAN USELESS. FWD-8's ADMITTED half asserts that the identity inside the role's trust can
read. `Andrew_Berman` is outside that trust, so a role trust policy naming exactly
`user/Opal_Terminal` would refuse the AssumeRole no matter what IAM permissions this principal
otherwise holds -- a resource-based trust is not bypassed by a permissive identity policy.

That failure would have been recorded as "a18 ADMITTED read: AccessDenied", which reads as the
ADMITTED half FAILING. It would have been a **false negative manufactured against FWD-8**, on the
project's own evidence trail, in the one place the ledger is waiting. The order's guard exists to
prevent precisely that, and the guard was right.

## What IS measured, so the order is servable by whoever holds the credential

| Question | Instrument | Result |
|---|---|---|
| Which identities can this box present? | `aws configure list-profiles`, plus the profile NAMES in `~/.aws/{credentials,config}` | **ONE**: `default`. No `Opal_Terminal` profile, no `AWS_*` credential override in the environment. |
| Does the trusted identity exist at all? | `aws iam list-access-keys --user-name Opal_Terminal` | **YES -- 1 key, `Active`, created 2026-07-10T22:08:15Z** |
| Is that read instrument sound? | same call for `Andrew_Berman` (positive control, separate invocation) | 2 keys, both `Active` -- the instrument answers, so the single-key result above is a measurement and not an artefact |

So the order is **servable**: the identity is real and its key is active. It is not servable from THIS
box's credential store, which holds one profile and that profile is `Andrew_Berman`.

## The order's own fallback does not clear this

The order allows `0.0.0_AB_MSTR~Z` to "hand it to another live lane on its box". **That will not help,
and I am saying so rather than letting it be tried and fail.** Every site-Z lane is a session on this
one machine under this one Windows user, so every lane resolves the same `~/.aws` and presents the same
`Andrew_Berman`. Re-routing within site Z re-runs this same step 1 and gets this same Arn. The axis
that matters here is the CREDENTIAL, not the lane.

## What would actually serve it

One of these, and the choice is the issuer's, not mine:

1. **The holder of the `Opal_Terminal` key runs it.** The key is active; whoever or whatever host holds
   it can do all three steps unchanged. `0.0.3_BG_BBGTerminal` is the Bloomberg-terminal seat and the
   name `Opal_Terminal` points at that context -- worth asking before provisioning anything.
2. **Provision an `Opal_Terminal` profile on this box** (an operator act with a credential, not an
   agent act, and not something I will do unasked), then re-issue; the read is then two minutes.
3. **Add this box's identity to the role's trust** -- NOT recommended and I am flagging it as the wrong
   answer. FWD-8's claim is about who the trust admits; widening the trust to make the read pass
   changes the thing being measured into something that passes by construction.

## Bounds honoured

No write of any kind. No transcript text, no credentials, no object body read, printed or stored. No
change to the role, its policy or the key policy. No key other than the one in the order was opened --
none was opened at all. The crossbox id is ACKED (read) and deliberately **left OPEN on both sides**,
because an unserved order must not carry a closed receipt.
