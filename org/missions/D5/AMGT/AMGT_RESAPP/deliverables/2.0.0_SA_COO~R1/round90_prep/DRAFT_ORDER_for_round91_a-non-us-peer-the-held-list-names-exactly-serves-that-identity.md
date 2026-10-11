# AMGT_RESAPP task order -- `AMGT-oo-4` -- A NON-UNITED-STATES PEER THE HELD LIST NAMES EXACTLY SERVES THAT IDENTITY

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D5/AMGT/AMGT_RESAPP/decompositions/AMGT_RESAPP_DECOMP.md</decomp_doc>
<owned_cells>AMGT-oo-4</owned_cells>
</decomp_ref>
<issued_to>0.9.0_WK_AMGT_RESAPP~363</issued_to>
<issued_by>2.0.0_SA_COO~R1</issued_by>
<to_id>AMGT_RESAPP.TO-AMGT-oo-4.a-non-us-peer-the-pool-holds-by-exact-name-serves-that-identity</to_id>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- a serve-time decorator and its test, no schedule.
comp-iam: DECLARED-NOT-APPLICABLE -- no new read: the decorator uses the held-name index and the crosswalk reads the route already makes; nothing is added to any role.
comp-adversary: RUN at the cut -- r90_name_match.py FAILs N1-N5 and N7 at the base (no such function, no such arm) and PASSes N6, and PASSes all seven arms against a candidate held in a throwaway runner (nothing written to the tree). Measured against the six scanner universes: the live rule serves 29 of 769 all-digit non-US rows; 23 of the other 1,047 name exactly one held company and are not served.
EGRESS CLASS, declared: NONE.
</preflight>

**Your worktree:** the spawn names it (branch `wk-AMGT_RESAPP-363`, cut from the current branch head). Work and commit only there. Start every shell call with `cd` into that path: a call that starts elsewhere resolves `git rev-parse --show-toplevel` to the base checkout.

## 1. THE CELL -- `AMGT-oo-4` (round 90, decomposition s.98 and its AMENDMENT 1)

CTO~DELL1 round-89 analysis items 2 (D1-S14, non-US rows): a peer row the identity pool holds resolves through the pool by exact
name, with NO parser of exchange forms, SEDOL stems or star-tickers. `lib/research/peers/numeric_tickers.py` already does this for an
ALL-DIGIT ticker (`numeric_fields`: a four-digit Japan code form, else the member's company name equal, after dropping case,
punctuation and the legal ending, to the one name a held company is served under; a name two held companies share is NOT matched).
`lib/research/api/scoped_amgt.py` `_with_numeric_tickers` applies it at serve time. A non-digit non-US ticker (a SEDOL stem such as
`B929F4`, a star-ticker such as `*SHOP`, a class-share ticker such as `HEI.A`) is never tried, though its name names one held
company. Extend the SAME exact-name rule to it:

1. In `numeric_tickers.py` add `name_match_fields(member, name_index, clean_name=lambda n: n)`, pure, returning the SAME shape
   `numeric_fields` returns on a match (`{"security_key": key, "identity": {...}}`, built by `_matched(member, key,
   MATCHED_AS_NAME)`) or `{}`. It returns `{}` (the member is left byte-equal: no key, no reason) unless ALL hold: `member` is a
   dict; it has no non-empty `security_key` and its `identity.resolution` is not `"MEASURED"`; its `ticker` is a non-empty string
   that is NOT all digits (`is_numeric_ticker`); it is NOT a United States member with an ASCII alphabetic ticker (that is
   AMGT-nn-2's, `_with_listed_identity`); and `name_token(clean_name(member.get("name")))` is non-empty and `name_index` holds exactly
   one distinct key under it. It uses the exact-name rule only: NO Japan-code rule, NO form builder, NO fuzzy or partial match.
2. In `scoped_amgt.py` extend `_with_numeric_tickers` so that, after the existing numeric pass, every member for which
   `name_match_fields` returns a match gains those fields, using the SAME `_held_name_index()` and `_clean_display_name` the numeric
   pass uses. The held-name index is built only when at least one member could use it (a numeric member or a candidate for
   `name_match_fields`), as today. A failed index build leaves the members byte-equal. No member is removed or reordered, no stored
   object is rewritten, and the numeric pass's output is unchanged for numeric members.
3. NOTHING else moves: not `_with_listed_identity`, not the currency decorator, not any figure. A member the rule does not match
   carries no new key, not even a reason.

Add the test file `lib/research/peers/tests/test_name_match_non_numeric.py` (pure, no network, no AWS): one test per rule above and
one per negative arm (an unmatched name; a name two held companies share; a United States alphabetic ticker whose name matches; an
all-digit ticker left to `numeric_fields`; a member already MEASURED; the route keeps member count and order and leaves every
other member byte-equal; a raising index build leaves the set byte-equal).

ASCII only. Stamp any surprise row's `surfaced_at` with `date -u +%FT%TZ` at filing. Rows: id form `AMGT_RESAPP-D1-W363-S<k>`,
`disarm_owner` `2.0.0_SA_COO~R1`.

## 2. BOUNDS

1. Write only the paths below. No deploy, no store write, no schedule, no SEC, vendor, model or Bloomberg call.
2. No `bun`, `npm` or `pip install` of any kind. Nothing is fetched from the internet.
3. Standing: no S3 delete, no push of shared branches.
4. Do not touch `lib/research/identity/crosswalk.py`, `listed_identity.py` or `price_currency.py`.
5. `scoped_amgt.py` is a large file: make the smallest edit that satisfies section 1; do not reformat or reorder it.

## 3. SURFACES

<paths>
lib/research/peers/numeric_tickers.py
lib/research/api/scoped_amgt.py
lib/research/peers/tests/test_name_match_non_numeric.py
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~363/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

## 4. PROOF OF SPEC (literal; timeout 900)

<proof_of_spec>
  <criterion id="AC1" cell_refs="AMGT-oo-4"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round90_prep/checks/r90_name_match.py"; echo "exit=$?"</invocation><expect>PASS N1 (a SEDOL-stem member naming one held company serves its key as MEASURED), PASS N2 (a star-ticker member does the same), PASS N3 (an unmatched name adds nothing), PASS N4 (a name two held companies share is not matched), PASS N5 (a United States alphabetic ticker is left to nn-2), PASS N6 (control: an all-digit ticker is answered as before), PASS N7 (route level: the matchable member gains its key, every other member is byte-equal); R90 NAME MATCH: YES; and exit=0</expect></criterion>
  <criterion id="AC2" cell_refs="AMGT-oo-4"><invocation>cd "$(git rev-parse --show-toplevel)" &amp;&amp; PYTHONPATH="$(pwd)" python -m pytest lib/research/peers/tests/test_name_match_non_numeric.py lib/research/peers/tests/test_numeric_tickers.py lib/research/api/tests/test_numeric_member_tickers.py lib/research/api/tests/test_peer_listed_identity.py -q; echo "exit=$?"</invocation><expect>the new test file and the three existing numeric-ticker and listed-identity test files pass with 0 failed, and exit=0</expect></criterion>
</proof_of_spec>

## 5. WHEN YOU ARE DONE

Commit in your worktree via `.tools/safe-commit.sh --author "0.9.0_WK_AMGT_RESAPP~363 <0.9.0_WK_AMGT_RESAPP~363@opal.agent>" -F <msgfile> -- <paths>`
(message file written with the Write tool; confirm with `git log -1`). Instance at
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~363/AMGT_RESAPP.TO-AMGT-oo-4.a-non-us-peer-the-pool-holds-by-exact-name-serves-that-identity.proof_of_spec.json`
with `to_id` equal to the `<to_id>` line above, character for character.
Run `python .tools/proof-of-spec-check.py <instance>` on the committed bytes and report its verdict line. Do not stage `portal`.
Report once:
- the commit hash;
- every criterion's output lines;
- the diff of `numeric_tickers.py` and of `scoped_amgt.py`, in full;
- any row.

The `<status>` flip is the issuer's.

<!-- ===================== RECORD FACE -- does NOT travel to the worker ===================== -->

**ISSUER NOTES:** CTO~DELL1 round-89 analysis @34a0c14300 item 2. THE ISSUER'S ERROR, recorded: the first read (round90_prep/ISSUER_READS.md, oo-4) counted resolution by the raw scanner ticker and by `<T> US` only (0 of 1,816) and cut no cell; the whole-page read of ROG_SW then showed three members served MEASURED by company name, which sent the issuer to the live decorator. Corrected measurement (r90_measure_nonus3.py): the numeric rule serves 29 of 769 all-digit non-US rows (22 by name, 7 by Japan code) and 23 of the 1,047 other non-US rows name exactly one held company and are not served; 52 of 1,816 is the ceiling the held list allows (95 held companies, 243 crosswalk records). The 1,764 remaining rows keep their plain reasons: no parser is built (analysis section 2). The cell is the CTO's item 2 restored, inside the round-90 rectangle, so it is an AMENDMENT 1 to the decomposition (s.98e), not a new scope. Risk LOCAL until it rides a redeploy; SERVED reach waits for the next product redeploy under its own pair (the same one oo-6 and any other served change rides). A name match across share classes is the exact-name rule's own known edge (e.g. a class-A name equal to the held common's name): the worker reports every example it sees as a row; it does not widen the rule. Checks dry-run at the base: AC1 FAIL (N1-N5, N7; N6 PASS); AC2 FAIL (the new test file is absent).

<status>pending</status>
<round>90</round>
<slot>0.9.0_WK_AMGT_RESAPP~363</slot>
<fabric>dell1</fabric>
<risk>LOCAL</risk>
<worker_class>worker</worker_class>
