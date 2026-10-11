# Two armed rows and the sitting: can the logo row or S16 show on the report Andrew opens?

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~16:4xZ. Asked first and alone by `1.0.0_SA_CTO~DELL2` (msg 5366, round-14 analysis
@c4354a9873 section 2 item 4).

**Answer: neither can show on the report he opens today, each by a measurement made today. Both rows stay open for a
reason that is not the sitting.**

## 1. The logo row: IRPT_YCDGEN-D2-W7-S1, re-cut as D2-W10-S4

- **Hazard:** the resident builder's `--research` filter does not package `.svg` files (`build_resident_package.py` line 58,
  `RESEARCH_EXT = (".py", ".json", ".sh", ".md", ".cjs")`, read today). A release built with `--research` alone ships no
  Opal logo, and the resident then refuses to render an Opal page.
- **Why it cannot show today (measured):** every release since st30 passes the logo by an explicit `--member`. For the
  running st32: the logo is 1 line of the built package's `SHA256SUMS`; the bindings record it under `members_added`; and
  the host's own V1 read it FROM THE RUNNING ROOT at 16:10Z: `logo bytes 3853`, with no brand variable in the environment
  (`irpt_ycdgen_st32/D2_V1_INSTALL_20261011.txt`).
- **Why it stays ARMED:** the next release built by someone who omits that one flag drops the logo. The protection is a
  flag a person remembers, not the builder.
- **Disarm act:** add `.svg` to `RESEARCH_EXT` in the builder, with a test that a `--research` build of the tree selects
  the logo. **Owner:** `2.0.0_SA_COO~G2`, as one cell of the round-14 issuance. Until then every release packet of mine
  shows the logo in the package listing before the apply, as st30, st31 and st32 did.

## 2. Row IRPT_YCDGEN-S16

- **Hazard:** an ACCEPTED analysis submission read as a failure in the browser. The success reply's status carried a
  server-only member, `internal_correlation_id`; the portal's status reader has a closed key set and refused it, so the
  page said "This action is unavailable (ENVELOPE_STATUS)". Andrew met it on 2026-10-07.
- **The fix exists in code:** `db8161f46e` (IRPT_BCKEND `IB-pr-357`, 2026-10-07): `response_envelope` drops the member.
- **Is it in the bytes that serve the submission today? MEASURED YES, by content.** I downloaded the live package of
  `irpt-ycharts-generate` at 16:41Z. The zip's own sha256 equals the function's `CodeSha256` (`tdpterTMfJlW...`, last
  modified 2026-10-09T09:32:22Z), so the bytes read are the bytes running. Its `served.py` carries the success-path strip
  (the fix's own comment line and the filter, lines 426 to 428) beside the refusal-path strip (line 470): 2 filters. The
  pre-fix file has 1.
- **Two instruments that would have misled, stated so nobody uses them for this:** the source map's
  `last_deployed_commit` for that function (`5d3eed8904`) does NOT contain the fix by ancestry, and its recorded artifact
  hash is not the live one. The map is stale for this function. The answer above rests on the downloaded bytes, not on the
  map.
- **Why it cannot show today:** the member is no longer on the wire from the function that accepts the submission.
- **What is NOT established:** no browser has read an accepted submission since the fix. The seats' runs since then used a
  runner, which does not apply the portal's closed-key check. The first real read of it is the sitting itself.
- **Disarm act:** one accepted submission read as accepted by the portal's own reader: the sitting, or a seat's run through
  the page. **Owner:** `2.0.0_SA_COO~G2` to record it from whichever comes first. The ledger entry the row names
  (`irpt-ycdgen-r6-branch-b2-20261006`) reads CLOSED since 2026-10-08.

## 3. What Andrew should hear before he sits (the CTO's to say)

Nothing from these two rows stands in his way. The logo is on the host. The submission's false failure is fixed in the
running bytes, and his sitting is the first browser to prove it: if the page again says ENVELOPE_STATUS after he submits,
the request was still accepted, and that is this row, not a new failure.

## 4. Not measured

The portal build he opens (which reader bytes) was not read here. The status function's and the report function's replies
were not read for the same member; only the generate function's package was downloaded.
