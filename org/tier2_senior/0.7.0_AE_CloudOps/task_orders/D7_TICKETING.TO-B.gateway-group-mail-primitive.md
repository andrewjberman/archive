# TO D7_TICKETING.TO-B — the gateway group-mail primitive (LAPTOP, EC2 deploy lane; scope may COLLAPSE on TO-A's on-box read)

<task_order id="D7_TICKETING.TO-B" project="OPAL_TICKETING">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:15Z</issued>
<dated>on TO-A's outputs (the on-box capability read + Andrew's Q3 one-liner reply) — likely 08-20/21; behind your Friday-path rows at your discretion</dated>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "D7_TICKETING" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged -- GO paired; STAGED-ON-TO-A: do not build before the existence check lands (the scope-collapse rule is the point)</status>
<priority>P1-program (D7 is the week's flagship per Andrew -- "water through the pipes") but behind your 49F Friday rows at the seat</priority>
<authority>D7_TICKETING_INTAKE_PRD.md §TO-B at dispatch vintage @36a7fbd70e (CVO verdict + 2 protocol rulings absorbed); Andrew's four ticketing positions (internal-only v1; placement FINAL; 2PM-ET stands; bobby later). CTO gates the deploy.</authority>
</task_order>

## Objective
Extend the opal-gateway app (PRD 4.1) with the DL/group-mail read primitive + identity_scope entry;
deploy via safe-ec2-deploy.sh; behavior-exercise per the R7 ledger pattern (deny + serve + cursor
advance). **THE EXISTENCE CHECK IS TO-A's ON-BOX CAPABILITY READ (protocol §6 fourth form), NOT R8
alone** — the deployed app is not repo-resident, so if it already carries a group-mail read path,
this TO COLLAPSES to expose-and-wire per §6's scope-collapse rule; declare which shape you build in
your first report. Design carries durable OFF-BOX cursor persistence (receipt-vs-tickets derivable;
ticket DDB config item = the natural home, final call at design).

## Acceptance criteria
- TB-1 SHAPE DECLARED: build-vs-collapse decided FROM TO-A's on-box read, cited (never from R8's
  repo proxy alone).
- TB-2 PRIMITIVE LIVE: the read path serves the confirmed DL set (Q3 closure cited), identity_scope
  entry landed, deployed via safe-ec2-deploy.sh under CTO's gate.
- TB-3 BEHAVIOR-EXERCISED per R7: deny (out-of-scope caller) + serve (in-scope) + cursor advance,
  each printed; the cursor persists OFF-BOX and receipt-vs-tickets is derivable after the fact.
- TB-4 proof instance VALID rc=0 positional: ids TB-1,TB-2,TB-3,TB-4. Expected values cite only
  MEASURED/RULED-class run rows per the protocol's run-verdict vocabulary (INFERRED-class rows are
  mechanically ineligible).

<proof_of_spec>
  <expected_criteria>TB-1,TB-2,TB-3,TB-4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D7_TICKETING.TO-B_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No build before TO-A's read (staged-on means staged-on). No alert machinery (the production
  trigger question is TO-C's exit, a SCHEDULE decision). v1 stays internal-only.

## Reporting
COO (cc CTO gate, MSTR for the sitez seam) at shape-declared and at primitive-live. Surprise
channel: one banked line to COO. Session log with Compiler Tools section = deliverable.

---

## ADDENDUM 2026-08-19 ~19:40Z (COO) — TB-1's INPUT HAS LANDED: THE SHAPE IS **REAL BUILD**, NOT COLLAPSE

TO-A's on-box capability read is DONE and ferried from sitez (MSTR bus id 7ab27f01). **This TO does
NOT collapse to expose-and-wire — build it.**

**The grounding (protocol §6 fourth form, APPLIED layer):** SSM on `i-07dccb1615503ac99`, cmd
`912d34e5`, service active. The deployed gateway carries **NO** group/shared-mailbox read path —
`/groups` 0 hits, other-mailbox `users/` 0 hits across 31 deployed `.py` files, **positive-controlled**.
All mail reads are delegated `/me` only. Deployed-currency chain CLOSED: on-box md5 == repo tree ==
`EC2_MANIFEST` @81615fbd3e, and the session's own Graph reads exercised the path.

TB-1 is therefore satisfiable by CITING this read (you do not need to re-derive it) — but say so
explicitly in your first report, per TB-1's wording.

**DL set measured off real partner mailflow:** 49F = `49@opalinvest.com`; Inflection =
`inflection@opalinvest.com`; **Cottonwood = NONE FOUND.** The Cottonwood DL question is inside
Andrew's one-liner, being put to him at the sitez console; answers re-ferry through MSTR. Do not
assume a Cottonwood DL exists.

**TWO SHAPE OPTIONS — Q3's DL-type answer picks between them (do not pick unilaterally):**
- **(a)** DL-membership delivery to the Analyst's OWN consented mailbox — **ZERO new consent**;
  primitive = filtered `/me` read + durable cursor.
- **(b)** group/shared-mailbox read — an **IT admin-consent round-trip**; scope adds carry the
  four-way-pin drift hazard.
Option (a) is materially cheaper and is the likely answer; **wait for the one-liner** before building
the consent-bearing half.

**NEW MEASURED FINDING, ROUTED HERE BECAUSE IT LANDS IN YOUR SCOPE:** the Analyst identity allowlist
currently **DENIES `search_email`** — failing closed, which is correct behavior, not a bug. But
**TO-C's mail-read needs that 4.1 tool allowlisted at TO-B, or an explicit widen decision.** Price it
into your design and name which you are doing; do not silently widen an allowlist as a side effect
of building the primitive.

Cursor persistence stays durable + OFF-BOX as the original TO says.

---

## ADDENDUM 2 — 2026-08-19 ~19:4xZ — **ANDREW-DIRECT: THE INTAKE IDENTITY IS `opalsupport@opalinvest.com`**

**VERBATIM (Andrew, sitez console, said against the D7 one-liner's membership-add proposal):**

> *"We need to either change this email or create a new email to opalsupport@opalinvest.com. Can't
> be broadcasting 'opalbloomberg' externally"*

**Binding:** whatever address joins the partner DLs / fronts the ticketing intake **is**
`opalsupport@opalinvest.com`. This folds into TB-2's shape. Ferried by MSTR (bus id `f97c55bb`),
primary AE as TO-B author, cc COO + CTO.

**MECHANISM — A RECOMMENDATION FROM SITE Z, NOT A RULING. YOU DECIDE (you are the author):**
- **ALIAS (proxy address)** `opalsupport@opalinvest.com` on the **EXISTING** Opal Bloomberg mailbox
  **preserves the zero-new-consent property**: mail to the alias lands in the already-consented
  `/me` mailbox, the Graph primitive is unchanged, and outbound send-as `opalsupport` closes the
  external-visibility hole Andrew named.
- **A SEPARATE NEW MAILBOX BREAKS THE ZERO-CONSENT PATH** — the Analyst's App-2 is delegated `/me`
  on the opalbloomberg account — and forces a consent round-trip. Note how this interacts with
  Addendum 1's option (a)/(b): the alias route keeps you on (a); a new mailbox pushes you toward
  (b)'s admin-consent round-trip. Price that before choosing.

**⚠ THE ALIAS/MAILBOX CREATION IS AN M365 ADMIN ACT — NAME IT AS AN INPUT WITH AN OWNER, DO NOT
ASSUME AN AGENT CAN MINT IT.** Likely Andrew/IT. A TO that silently depends on an identity nobody
has been asked to create is the class where the build finishes and the thing still cannot receive
mail. State the dependency and its owner in your first report.

**Domain note for the record:** `opalinvest.com` **is ours** — Rule 23's caveat is about **SES DKIM
on sends**, not M365 mailboxes/aliases, so this is not a Rule-23 conflict. `opalcapital.com` remains
never-touch (we do not own it).

D9/D6 unaffected by this ruling.

---

## ADDENDUM 3 — 2026-08-19 ~19:41Z — **THE ALIAS MECHANISM IS ASYMMETRIC. INBOUND IS FREE; OUTBOUND IS THE TRAP.**

**Classed INFERRED, with its discharging check named** (COO~Z via MSTR, bus id `0da5cf66`) — treat
it as a prior under test, not a finding. But price it NOW, because the failure mode is late-surfacing.

**The asymmetry:** inbound mail to an `opalsupport@` alias is free — the zero-new-consent property
in Addendum 2 holds. **Outbound does NOT follow.** M365's `SendFromAliasEnabled` **defaults OFF**,
and with it off, **Graph sends present the PRIMARY address (`opalbloomberg@`)** — precisely the
external broadcast Andrew ruled against. **And it would surface only at the first real reply to a
partner** — i.e. after the build reads green, in front of an external counterparty.

**THE DISCHARGING CHECK (one read, IT/Andrew hand):** is `SendFromAliasEnabled` true on this tenant?

**REMEDIES IF IT IS FALSE:**
- **(a)** Enable the flag — tenant-wide setting.
- **(b)** **INVERT primary/alias:** `opalsupport@` becomes PRIMARY, `opalbloomberg@` demoted to
  alias. Same mailbox, same consent, and **presentation is correct BY CONSTRUCTION** rather than by
  a setting someone must keep true. Both site-Z execs prefer this shape. **Cost:** a re-verify of
  BG's identity pins, which key on `opalbloomberg@`.

**Carry the tenant-flag read as a NAMED INPUT in your design either way** — the same discipline as
Addendum 2's admin act. A build that is correct on inbound and wrong on outbound passes every check
you would naturally run.

**Andrew is being asked the refined question at the sitez console now; his answer re-ferries through
MSTR.** Do not pre-commit to (a) or (b) ahead of it.

---

## VINTAGE SUPERSESSION — 2026-08-19 ~19:41Z: **D7 = @fac13ccc3a** (supersedes @36a7fbd70e)
The authority line above cites @36a7fbd70e. **The final absorbed D7 vintage is `@fac13ccc3a`**, which
adds the explicit **#42 ticketing-half acceptance**. Cut/execute against @fac13ccc3a. Everything
already stated in this TO and its addenda stands; the supersession ADDS, it does not retract.
