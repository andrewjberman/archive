# NFRA_IAMROLES202609.TO-IAM-s-3 -- The COVERAGE vocabulary at PERMISSION grain

`unused` rendered distinctly from `unobservable`, at the grain the claim is made (FWD-7,
manifest row S3). Authored against the instrument IAM-s-1 already landed
(`org/modules/graph/comp_iam_usage.py`'s `permission_ledger` / `_render_permissions` /
`permission-cold` subcommand) -- this file is the RULE-24 RECORD for that vocabulary, not a
second renderer. No code in `comp_iam_usage.py` changes as a result of this cell; the vocabulary
it already emits is exactly the one recorded here.

## 1. The vocabulary, stated

At **PERMISSION grain** (one row per GRANTED action on one role, at assessment time), every
permission renders as exactly one of three values:

| value | means | means-NOT |
|---|---|---|
| `used` | tracked by IAM Access Advisor at ACTION_LEVEL, and accessed within the stated `--lookback` window | "granted and safe to keep" -- it is a usage fact, not a risk verdict |
| `never-used` | tracked by IAM Access Advisor at ACTION_LEVEL, and (a) never accessed at all, or (b) last accessed OUTSIDE the stated lookback | "this permission was examined and found unused" is exactly what this value asserts, no more -- it is never a claim the action was never called at any point in account history, only over the stated window (FWD-2's own phrasing, carried) |
| `unobservable` | this instrument COULD NOT DETERMINE usage for this permission -- Access Advisor's job did not complete, the service has no action-level tracking, the action is absent from the service's tracked-action list, the action token is malformed, or the token is a wildcard (`*`/`svc:*`) not expanded | **NEVER** "clean", "safe", "probably unused" or any other reading that credits an inspection that did not happen |

The literal band name, exactly as `comp_iam_usage.py` emits it, is `unobservable`.

**THE BOUND THAT OUTRANKS EVERYTHING ELSE IN THIS CELL, PRD section 8 row S3 verbatim:** "A GRANT
NOBODY LOOKED AT MUST NEVER RENDER AS A GRANT SHOWN CLEAN. This outranks FWD-1's tidiness." Every
row in the table above is written to hold that line: `unobservable` never collapses into
`never-used`, into `used`, or into silence (an omitted row). `permission_ledger` renders all
three counts on every call, including zero-count bands (`counts: used=%d never-used=%d
unobservable=%d`, unconditionally printed), so a role with only `unobservable` rows still prints
`used=0 never-used=0` rather than omitting the bands nobody hit.

**C-COVERAGE-OVER-COUNT, carried:** a smaller `never-used` figure that states its `unobservable`
count beside it beats a larger, silent one that does not. The vocabulary is the mechanism that
makes that statable -- see section 5's live specimen, where `unobservable` (14) is the LARGEST
band on a real role, the most flattering number to hide and therefore the one this vocabulary
refuses to hide.

## 2. Is `unobservable` a NEW value, a RENAME of `UNKNOWN` at a new grain, or a narrower sibling? -- DECIDED AND RECORDED

**DECISION: `unobservable` is a GRAIN-SHIFTED SIBLING of the existing `UNKNOWN` band, deliberately
given its OWN NAME rather than reusing the string `UNKNOWN` -- not a pure rename, and not an
unrelated new concept.**

Reasoning, against the build ladder (rung 2: the estate already has it) and rule 24 (iv):

- **Same INTENT, different GRAIN.** Role-grain `UNKNOWN` (`comp_debris.classify`, reused verbatim
  by `iam_ledger`) and permission-grain `unobservable` answer the SAME question -- "can this
  instrument say anything about use?" -- at two different grains. `UNKNOWN` is a property of ONE
  ROLE (the whole `RoleLastUsed` read either succeeded or it did not: one verdict, one row).
  `unobservable` is a property of ONE GRANTED PERMISSION within a role's ledger, and a single role
  can carry `used`, `never-used` AND `unobservable` rows simultaneously (the live specimen in
  section 5 does: 6 used, 2 never-used, 14 unobservable, ONE role). Reusing the literal string
  `UNKNOWN` at permission grain would silently violate rule 24(ii) SAME GRAIN -- it would read as
  a role-level verdict bleeding into a permission-level row, and a caller that greps for `UNKNOWN`
  expecting one hit per role would get N hits per role instead, an undocumented grain change under
  an unchanged name.
- **Wider set of causes than role-grain `UNKNOWN`.** Role-grain `UNKNOWN` has exactly one cause in
  `comp_debris.classify`: `hist.get("read")` failed (a metric/RoleLastUsed read error). Permission
  grain `unobservable` covers FIVE distinct causes (`permission_ledger`, in order of the code's own
  checks): malformed action token; wildcard token not expanded; the Access Advisor job itself did
  not complete (`advisor_read_ok is False` -- the role-grain-shaped cause, a whole-read failure);
  the service is entirely absent from Access Advisor's per-role response; the service IS present
  but has no `TrackedActionsLastAccessed` at all; the action IS tracked-capable but this specific
  action is absent from the tracked list. Only the middle cause (advisor job unreadable) is the
  literal grain-shift of role-grain `UNKNOWN`; the other four have NO role-grain analogue at all,
  because they are about what AWS tracks, not about whether OUR READ succeeded. Calling all five
  `UNKNOWN` would flatten "we could not read anything" together with "we read everything correctly
  and AWS itself does not instrument this permission" -- two different epistemic states that both
  currently, correctly, render `unobservable`, but for a reader who needs to know WHICH is true
  each row's `reason` field says so verbatim (e.g. `"access-advisor-job-unreadable (BLIND, not
  unused)"` vs `"service 's3' has no action-level tracking in Access Advisor"`).
- **Not a narrower sibling either**, in the sense of being a strict subset of `UNKNOWN`'s cases:
  it OVERLAPS (the advisor-job-unreadable cause) and also EXTENDS (the four AWS-tracking-shape
  causes) beyond what role-grain `UNKNOWN` could ever mean, since a role can be perfectly readable
  (no `UNKNOWN`) while still carrying `unobservable` permissions.
- **Rung-2 check, explicit:** minting `unobservable` is not "the estate already has this and I
  built a synonym" -- `UNKNOWN` exists at role grain and is REUSED, unmodified, for the ONE cause
  they share in kind (a whole-object read failure: `permission_blind_advisor_job_is_unobservable_
  not_unused` in the self-test is the role-grain-shaped case, just spelled `unobservable` because
  it is reported per-permission-row, not per-role). The remaining four causes have no existing
  estate value to reuse; they are not synonyms of anything, they are new observations about the
  AWS API surface itself.
- **The `blind_is_unknown_NOT_unused` self-test assertion is UNTOUCHED and still green** (section
  4 below): it asserts the ROLE-grain band stays `UNKNOWN`, never `never-used`, for a role whose
  `RoleLastUsed` could not be read. Nothing in this cell's vocabulary record renames, retires or
  reinterprets that assertion or the band it protects.

## 3. Four-postulate record (rule 24) -- THIS vocabulary

- **(i) MECE over a DECLARED domain.** Domain = every GRANTED permission of one role at assessment
  time (`granted_permissions`'s union of Allow-actions across every attached-managed + inline
  policy, read live). MECE, hunted rather than asserted: `permission_ledger` iterates every
  element of that set exactly once (`for perm in granted`) and every branch of its `if/elif`
  chain terminates in one of the three values above -- there is no code path that returns without
  assigning a `status`, and the offline self-test's `permission_denominator_matches_granted_count`
  assertion is the mechanical hunt for an uncovered member: it asserts `len(rows) == len(granted)`,
  i.e. zero permissions fall through unclassified. A malformed token (no `:` in the string) is
  still covered -- it renders `unobservable` with reason `"malformed action token"` rather than
  being dropped from the denominator, which is the uncovered-member case rule 24(i) asks a
  proposal to hunt for and report, not assume away.
- **(ii) SAME GRAIN.** Every value in this vocabulary is a property of ONE GRANTED PERMISSION
  (one `service:Action` string on one role at one assessment time), NONE of a role. This is why
  `unobservable` could not simply reuse the string `UNKNOWN` (section 2): `UNKNOWN` is a role-grain
  value and mixing it in here would violate this exact postulate by letting one row's status speak
  for the whole role.
- **(iii) INTENT COHERENCE.** One axis: what this instrument knows about THIS permission's use,
  and nothing else. The vocabulary does NOT encode risk, blast radius, remediation priority, or
  whether the permission is "dangerous" -- those are separate axes PRD section 8 assigns to other
  cells (S2's posture number, S4's condition axis), and mixing them in here would be an
  intent-coherence violation of exactly the kind rule 24(iii) forbids (one axis, one intent).
- **(iv) STATE COHERENCE -- which values one remedy does NOT move.** Revoking an unused grant (the
  natural remedy `never-used` invites) moves that ONE row from `never-used` toward not-existing;
  it does **not** touch any `unobservable` row on the same role, because `unobservable` is not a
  claim about usage at all -- it is a claim about this instrument's blindness, and blindness is
  fixed by enabling broader Access Advisor coverage or (per `C-ANALYZER-PRICED-FIRST`, HELD) a
  priced instrument, never by revoking a grant. Revoking an `unobservable` permission on the
  strength of this vocabulary alone would be revoking something nobody looked at, which is the
  exact failure PRD section 8's bound forbids one level up (rendering it as clean); STATE
  COHERENCE names that the remedy for `never-used` (revoke, human-gated, out of this cell's scope)
  and the remedy for `unobservable` (widen observability, never revoke on this signal alone) are
  DIFFERENT ACTIONS ON DIFFERENT PLANES, and conflating them is exactly what a reader who cannot
  tell the two bands apart would be at risk of doing -- which is FWD-7's whole ACCEPT sentence,
  restated as a remedy-coherence fact rather than a rendering fact.

## 4. The pre-existing role-grain regression bar -- kept green, not replaced

`blind_is_unknown_NOT_unused` (role grain, `_self_test`) still asserts, unmodified, that a role
whose `RoleLastUsed` could not be read renders band `UNKNOWN` and is excluded from the reap rank
-- it is the ROLE-GRAIN ANCESTOR this cell's permission-grain vocabulary generalizes, per the TO's
own instruction to read it first. Measured on this tree at this cut:

```
$ .tools/comp-iam-usage self-test | grep -c 'blind_is_unknown_NOT_unused'
1
```

19 of 19 self-test assertions PASS on this tree (9 role-grain, including the one above, plus 10
permission-grain), rc=0.

## 5. Word-boundary token census (rule 24 debt, discharged)

Decomposition section 2 recorded this debt explicitly: *"OWED BY IAM-s-3 AT PHASE 1, not run
here -- IAM-s-3 authors the coverage vocabulary (`unused` vs `unobservable` vs the existing
`UNKNOWN` band) and its census must run against the extended tool's own corpus, which does not
exist yet."* The corpus now exists (`IAM-s-1` landed the extension). Run against that corpus,
via the EXPLICIT `.tools/` path so the resolution honours THIS worktree rather than the main
checkout (Z-S3's finding: a bare-name invocation resolves through a `~/bin` forwarder to the
main checkout regardless of caller `$PWD`):

```
$ .tools/comp-find 'unobservable' org/modules/graph --limit 20
comp-find [content] 'unobservable'
  DENOMINATOR: 38 hit(s) across 403 file(s) scanned in scope [corpus=all] | 11 EPHEMERAL-FLOOR, NOT searched | 4 BINARY, NOT searched
  BANDS (true totals, not this page): SURFACED=35 TEST=2 DOC=1
```

**Denominator: 403 file(s) scanned in scope** (`org/modules/graph`, this worktree, `corpus=all`),
**38 hit(s)**, banded SURFACED=35 (the live code: `permission_ledger`, `_render_permissions`, the
`_PERM_LIMITS_BANNER`, docstrings), TEST=2 (`_self_test_permissions`'s own assertions and
comments), DOC=1. Every hit is a WHOLE-VALUE occurrence of the token `unobservable` as a status
string, a docstring reference to that status, or a self-test assertion name -- none is a
fragment/substring hit (CLAUDE.md s.3's WARN-on-fragments trap does not fire here). Positive
control that this run reads the worktree and not the main checkout, discriminated by scope rather
than by an absent file (the file under test, `comp_iam_usage.py`, is already merged to both trees
so a file-presence discriminator would not distinguish them for THIS pathspec): the SAME
invocation by BARE NAME (`comp-find` with no `.tools/` prefix, main-checkout forwarder per Z-S3)
against the SAME pathspec scans 404 file(s) -- one more than the worktree's 403, `.tools/comp-find
--hidden org/modules/graph` shows why: the main checkout carries 175 gitignored files under this
path (1 further searchable, matching the +1), the worktree carries 11 (0 further searchable). The
two counts are close FOR THIS NARROW PATHSPEC because `org/modules/graph` is already merged
between the trees; Z-S3's ~31,000-vs-~55,000 discriminator was measured over the WHOLE repository
tree (no pathspec) and does not reproduce at this directory's scale -- recorded as a filed row
(`NFRA_IAMROLES202609-Z-W1-S3`) rather than silently treated as satisfying that specific numeric
comparison, because the AC2 invocation's own pathspec (correctly, per the decomposition's "the
extended tool's own corpus") narrows the scan far below either reference figure.

**Uncovered-member hunt (rule 24(i), applied to the census itself):** searching for `unobservable`
alone could miss a caller that uses the value without the literal string (e.g. a raw `"status":
"unobservable"` inside a data file rather than code) -- none exists in this corpus: the only
producer of the string is `permission_ledger` in `comp_iam_usage.py`, and the only consumers are
its own `_render_permissions` and the self-test, both in the same file, confirmed by the BANDS
line carrying no HEAD/CONFIG hits (no filename or config file references the token, so there is no
second definition site to reconcile against this one).

## 6. Worked example -- FWD-7's ACCEPT, on a live specimen (feeds AC5)

Live read, same role IAM-s-1 exercised, re-run fresh for this cell:

```
$ .tools/comp-iam-usage permission-cold --role opal-data-refresh-lambda-role --lookback 90
comp-iam-usage permission-cold -- PERMISSION-grain usage for role 'opal-data-refresh-lambda-role' (ADVISORY; NEVER deletes)
  lookback 90 days | granted permissions examined (DENOMINATOR)=22
  counts: used=6 never-used=2 unobservable=14

    never-used     cloudfront:GetInvalidation
    never-used     logs:CreateLogGroup                       last-used=2026-01-19 (234d ago, outside 90d lookback)
    unobservable   dynamodb:DeleteItem                       (service 'dynamodb' has no action-level tracking in Access Advisor)
    unobservable   dynamodb:GetItem                          (service 'dynamodb' has no action-level tracking in Access Advisor)
    unobservable   lambda:InvokeFunction                     (service 'lambda' has no action-level tracking in Access Advisor)
    unobservable   logs:PutLogEvents                         (action not in Access Advisor's tracked-action list for 'logs')
    unobservable   s3:GetObject                              (service 's3' has no action-level tracking in Access Advisor)
    used           cloudfront:CreateInvalidation              last-used=2026-08-01 (39d ago)
    used           logs:CreateLogStream                       last-used=2026-09-04 (5d ago)
```
(full 22-row output: 6 used, 2 never-used, 14 unobservable; denominator line prints all three
counts unconditionally.)

Reading this AS A REVIEWER WHO DID NOT BUILD IT, against FWD-7's ACCEPT sentence verbatim
("Something nobody has looked at never reads as something that was looked at and found clean"):

- **`s3:GetObject`** is granted, and this account's Access Advisor has NO action-level tracking
  for the `s3` service at all -- nobody, and nothing, has looked at whether this permission is
  used. It renders `unobservable`, with the reason stated on the row. It does **not** render
  `never-used` (which would claim an inspection happened and found no use) and does **not** render
  `used`. A reviewer reading this row cannot mistake "we never checked" for "we checked and it's
  clean" -- the two are spelled differently and the row says why.
- **`cloudfront:GetInvalidation`** IS tracked by Access Advisor for this role, and the tracking
  shows no access ever recorded. It renders `never-used` -- an actual inspection happened (a
  completed Access Advisor job, this service present, this action in the tracked list) and it
  found no use. This is the row FWD-7 wants a reviewer to be able to trust AS a clean read,
  distinct from `s3:GetObject` above.
- **14 of 22 permissions (64%) on this real role are `unobservable`, not `never-used`.** If this
  vocabulary collapsed `unobservable` into `never-used` (the BOUND this cell exists to forbid), a
  reviewer would see `never-used=16` and read it as "16 grants, inspected, safe to revoke" --
  PRD section 8's forbidden reading, on the MAJORITY of this role's grants. Rendered correctly,
  the reviewer instead sees `never-used=2, unobservable=14` and knows the instrument's confident
  claim covers only 2 of 22 grants -- a smaller, less flattering number that states what it could
  not see (`C-COVERAGE-OVER-COUNT`), on a real live role rather than a constructed fixture.

## 7. Downstream usability (not built here, recorded so it is checkable)

- **IAM-s-2** (posture number) can build `used + never-used` as its numerator/rollup input and
  must carry `unobservable`'s count and reason-set alongside any headline figure -- the vocabulary
  in section 1 is exactly what makes that separation possible; a posture number that only reads
  `counts["never-used"]` without also surfacing `counts["unobservable"]` beside it would itself be
  the forbidden "grant shown clean" reading, one cell downstream. Not built by this cell; recorded
  as the interface IAM-s-2 must use.
- **IAM-s-9** (re-run harness) reproduces these bands by re-running `permission-cold` against the
  same role and lookback; determinism is exercised in IAM-s-1's own proof (two live runs,
  byte-identical) and nothing in this cell changes that behaviour.
