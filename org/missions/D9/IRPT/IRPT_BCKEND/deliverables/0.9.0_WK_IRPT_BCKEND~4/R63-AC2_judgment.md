# R63-AC2 JUDGMENT -- IRPT_BCKEND.TO-IB-rtf-6

JUDGMENT criterion, recorded for `3.0.0_SA_CVO`, no verdict. Three sub-questions.

## 1. The two packaging mechanisms -- can they coexist, and which should be the ONLY one?

Two mechanisms package the SAME shared `_authz/enforce.py`/`_authz/served.py` for the SAME
functions today: `infra/aws/lambda/ci/build-and-upload.sh`'s declarative `staged_from`
(`repo_path`/`pin`/`sha256`, resolved by `git show <pin>:<repo_path>`, sha256-verified before a
byte is written -- `build-and-upload.sh:161-201` @`4ee8426c72`) and
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/rte6_package_deploy.py`'s
`resolve()`, which walks `source_dir` first and then a fixed `SHARED_ROOTS` list of live
worktree directories (`rte6_package_deploy.py:40-90` @`7068b14d67`) -- NO pin, NO declared hash,
whatever is on disk at deploy time.

They CANNOT coexist without this exact class recurring every round they both touch the shared
frontier: `rte6_package_deploy.py` has no mechanism to WRITE a pin back to
`lambda-source-map.json` after it deploys, so every edit to `_authz/*` it ships (IB-rtf-2's
inversion, this round) silently stales EVERY `staged_from` pin declared against that file the
moment it runs -- exactly the drift this cell exists to correct, and nothing prevents the NEXT
edit-then-deploy-directly cycle from re-opening it (row `IRPT_BCKEND-W4-S41`'s own mid-flight
collision was one instance of this same shape one level up: a THIRD actor mid-round).

Recommendation: ONE mechanism, the DECLARATIVE one (`build-and-upload.sh`'s `staged_from`) should
be the only path that ever reaches a served Lambda. `rte6_package_deploy.py` is a worker-owned,
undeclared deliverable (`deliverables/0.9.0_WK_IRPT_BCKEND~1/`, not `infra/aws/lambda/ci/`) built
for a round's direct-deploy need; if a direct-resolve path is to remain legitimate estate-wide
tooling rather than a one-round expedient, it needs to WRITE the pin it resolved back to the real
manifest in the SAME act that deploys -- otherwise every direct deploy is a new stale-pin
liability by construction. This is an L4 shape question (which mechanism is canonical, and
whether the other is retired or made pin-writing) -- not this cell's to decide.

## 2. Should a manifest pin be a CONTENT hash rather than a commit?

A commit pin goes stale on every drain of a shared file it names -- measured twice this round
alone: IB-rtf-1 pinned to `c28c728a30`/its predecessors at the cut; IB-rtf-2's very next commit to
the SAME two files staled 13 of those pins immediately (this cell's whole population). A CONTENT
pin (the blob's own sha256, resolved by a content-addressed search of the whole reachable object
graph -- IB-rtf-1's own `content_oid_no_filters()`/`build_oid_index()` instrument,
`battery_ib_rtf_1.py:172-201` @`949dc88099`) cannot go stale in the same way: it either still
resolves to SOME committed blob (possibly at a different path than last time, but the CONTENT is
what is asserted) or the build FAILS LOUDLY the moment the content stops existing anywhere --
never a silent match-the-wrong-vintage. The commit-pin's failure mode is exactly the one this
whole order exists to fix: it stays SYNTACTICALLY valid (the commit exists, the path exists at
that commit) while being SEMANTICALLY wrong (the content it names is not what runs). A content pin
converts that into a loud, structural failure instead of a silent divergence. This order does not
adopt it (BOUNDS: the pin form here is the one `lambda-source-map.json` already declares,
`repo_path`+`pin`+`sha256` where `sha256` is ALREADY the content hash used for verification -- the
schema is half-way there today; the open question is whether `pin` should be DROPPED in favor of
resolving purely by content-address search, or kept as a resolution-speed hint verified against
the content hash as it already is). Recommend: keep both, tighten the BUILD to verify the DECLARED
`sha256` against the pin's blob AND refuse (not silently re-declare) when they disagree, which
`build-and-upload.sh`'s `TMPJS_STAGE` (`:186-193` @`4ee8426c72`) already does today for the pin
itself; the gap is that nothing catches the pin going stale relative to HEAD until a battery like
this one runs it.

## 3. What does `irpt-holdings`'s diverged `enforce.py` mean for FWD-5 today?

Confirmed this run, unchanged from `IRPT_BCKEND-W1-S29`: `irpt-holdings` packages its OWN local
`infra/aws/lambda/investor-reporting/holdings/enforce.py` (tracked at path, no `staged_from`
entry, `resolve()`'s `source_dir`-first check finds it before ever consulting a shared root --
`rte6_package_deploy.py:86-90` @`7068b14d67`), which is a SEPARATE COPY still carrying the
PRE-INVERSION order (`AN UNPROJECTED GRANT IS A REFUSAL`, checked before the empty-set branch --
confirmed present in `HEAD:infra/aws/lambda/investor-reporting/holdings/enforce.py`, this run) and
never sets `census["unprojected_grant"]`. FWD-5 ("the served path's behaviour surviving the next
build") is UNMET for `irpt-holdings` specifically: the next build of every OTHER function in this
population now correctly reproduces the post-inversion, disclosure-bearing behaviour (this cell's
own REAL control, `13 of 13`); the next build of `irpt-holdings` reproduces its OWN pre-fix
behaviour untouched, because nothing in this cell's remedy (a manifest re-pin) can reach a file
that was never declared via the manifest in the first place. This is `IRPT_BCKEND-W1-S29`'s own
finding, re-verified rather than re-argued, and it is NOT this cell's to fix (BOUNDS: "the diverged
`holdings/enforce.py` is rowed, never edited, never pinned"). The CTO's ruling on it (fold
`holdings/enforce.py` onto the shared `_authz` module, or apply the inversion+disclosure fix to
its own fork) determines whether `irpt-holdings` ever reaches FWD-5's bar without a THIRD cell.

No verdict on any of the three; the CVO's read governs.
