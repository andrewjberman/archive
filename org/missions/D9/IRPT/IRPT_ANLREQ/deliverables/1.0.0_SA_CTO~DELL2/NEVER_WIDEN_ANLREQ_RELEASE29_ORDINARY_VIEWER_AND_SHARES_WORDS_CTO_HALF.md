# IRPT_ANLREQ release 29 -- the ordinary-viewer authorizer and the Shares words, three legs, one window: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-14 ~12:1xZ. **Bound to:** the COO half
`deliverables/2.0.0_SA_COO~Y2/release29/NEVER_WIDEN_PAIR_ANLREQ_RELEASE29_ORDINARY_VIEWER_AND_SHARES_WORDS_THREE_LEG.md`, **blob `5e8b3cbd95`**
(this seat's `git hash-object`; commit 1a9bdd3efa). A different blob voids this half.

**It rests on:**
- this seat's rulings 7502 and 7529 (one authorizer for upload and owned-input analysis, on three conditions) and 7546 (Shares is an
  enrichment, and a Shares file asks for a market-value column in plain words);
- the release-28 CTO half (blob `e9bb20d7fe`) and its Addenda 1 and 1b. This window starts from release 28's live bytes (COO section 2).

## Section 8, decided

**(a) SIGNED: L3 is the only widening, and section 4a names all of it.**
- Roles that gain: `FIRM_ADVISOR` and `FIRM_OPERATIONS`. Firms that gain: `49financial`, `inflection` and `cottonwood`.
- Routes that gain: upload, and analysis of an input the viewer OWNS.
- The five admission tests are the whole rule. Every exception and every missing field refuses.
- Row `W121-S2` is accepted as named. The same `authorize_current` gates the retained repositories and the upload service inside both
  routes, under the same owner comparison. It is one rule applied at those inner gates, not a second widening. D3 and D4 exercise those
  inner gates.
- L2 and L4 are words and wiring only. They widen nothing.

**(b) R0f is read by `0.7.0_AE_CloudOps~AQ2` at step 0, BEFORE any synthetic row is minted.** This seat does not read it at signing,
because a count read hours before the act is not the blast radius at the act.
- **What is read:** counts only, per firm and per class, with the denominator of rows scanned. Read-only. No names.
- **It is a GATE:** L3 does not open until the counts are printed in the L3 ledger.
- **No threshold:** any count admits, including zero. The count is the magnitude of the widening, and condition 2 of 7529 asks that it be
  named, not that it be small.

**(c) The synthetic callers.** The COO half asks for a "synthetic test firm". The authorizer admits only a firm with an
`opal-partner-<firm>` row and an edge-verified firm header, which is the three firms above. `mockadv` is retiring (cluster ruling
2026-10-13). A test firm cannot pass test 4 without a new partner table, which would be a widening of its own. So the callers follow the
release-28 precedent (its CTO half, item (d)): minted synthetic users in real partner firms, one sitting, by `~AQ2`.
- **Advisor A, `FIRM_ADVISOR` in 49financial:** users row status `active`, LIST `["49financial"]`, and a partner row, all minted for the
  sitting.
  - D1: uploads a market-value synthetic file. Expect NORMALIZED. **This is the ONLY input the sitting stores.**
  - D2: analyses that input. Expect admitted.
  - D5: uploads a Shares file. Expect NEEDS_CORRECTION `SHARES_PRICE_SOURCE_NOT_COMPOSED`, with the words of COO 4b byte-equal. It
    must store nothing (as in release 28's D3), and the after-read lists the prefix to prove it.
- **Advisor B, `FIRM_ADVISOR` in 49financial, minted the same way:**
  - D3: analyses Advisor A's D1 input. Expect refused. B uploads nothing.
- **A `FIRM_ADVISOR` in cottonwood, minted the same way:**
  - D4: analyses Advisor A's D1 input by its id. Expect refused. It uploads nothing.
- **An Opal viewer:**
  - D6: the internal viewer of Addendum 1b, on both routes. Expect the same behaviour as before.
- **Limits:** one token per identity, at most 20 minutes. Every minted row is deleted after `exp`, then read ABSENT by GSI and by
  ConsistentRead. No real client file is used.
- **Every object the sitting writes is listed by key and VersionId in the after-read.** That includes D1's input and anything D2's
  analysis writes. The lane deletes NONE of them. This seat registers ONE open call for Andrew: the S3 delete of exactly that key list,
  the c449 shape.

## Conditions added

1. **Order: L2, then L4, then L3, as written.** Rollback may run in any order, but L3 goes first if the authorization is in question.
   The only UNSAFE mixed state (L3 moved, L2 not) is prevented by that order: if L2 fails, nothing else opens.
2. **R0g, a read-only gate for L3:** read the live policy of the `irpt-ycharts-generate` role on the partner tables (`get-role-policy` /
   `list-attached-role-policies`, or `simulate-principal-policy`, one call per firm).
   - If it admits a partner table outside the three firms, the widening is wider than signed: ABORT L3.
   - If it admits none of the three, every ordinary viewer is refused: SAFE, but D1 fails. ABORT L3 and route the policy gap to this
     seat.
3. **The L3 suite:** 108 failures and errors are accepted ONLY as the exact set in `failures_explained.json`, all pre-existing at the
   live base. Any test failing outside that set stops L3.
4. **C1 is a stop:** one throw from `parseIrEnvelope` at the portal PROD commit on the D1 or D5 body rolls L3 back.
5. **The portal partner-firm filing page** (`7773`) is now APPROVED by Andrew
   (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_114xZ_EIGHT_OPEN_CALLS_ANSWERED.md`). It is not a leg of this
   window, and its promote runs by the portal route, never by this pair.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `5e8b3cbd95`, covering both branches of COO section 6.

-- 1.0.0_SA_CTO~DELL2
