# Owner card -- `sentiment-query-api` stays NOT-JUDGED, EN-s-6-r3 (AMENDMENT 1)

**Author:** `0.9.0_WK_LGIC_ENFORCE~4`. AMENDMENT 1 to `LGIC_ENFORCE.TO-EN-s-6-r3`: "A RAISE whose owner
cannot be measured is NOT minted: write one owner card for it ... and record that name NOT-JUDGED." This
is that card, for the one RAISE this cell's census hits that AMENDMENT 1's declared-source list cannot
resolve.

---

## Card 1 -- `sentiment-query-api` (live API_GW)

**Question for Andrew: who owns the `sentiment-query-api` API Gateway (live, `arn:aws:apigateway:us-east-1::/apis/cxm5b58nme`) and its Lambda, `sentiment_query_api` / `sentiment_query_api-role`?**

**Why it RAISEs:** `grade()` tokenises `sentiment-query-api` to `['sentiment', 'query', 'api']`; `sentiment`
is R1.f -- in no vocabulary (not a `systems.json` key (V1), not a declared `unresolved` token (V2), not a
refused/cadence/scope token (V3)) -- so no registry row can resolve it via the R1.d/e placeholder path
either (that path only fires for a V3 token, and `sentiment` is not one). The only mint AMENDMENT 1 admits
is a NEW `systems.json` row (`key: "sentiment"`), and that mint needs a MEASURED or citably-INFERRED
`owner_directive`.

**Measured, not guessed:**
- `infra/aws/lambda/ci/lambda-source-map.json:882-885` @`c0aa291a17`: the ONLY declared-source carrier
  naming this resource, `"sentiment_query_api": {"source_dir": "infra/aws/lambda/sentiment_query_api",
  "files": ["index.js"]}` -- and unlike every neighbouring entry in the same file (e.g. `opal-news-ai-sentiment`
  :547-556, `opal-news-layer3-curation` :559-570, both carrying `tf_file`/`tf_resource` into
  `infra/aws/terraform/news-pipeline/lambdas.tf`), THIS entry carries no `tf_file` and no `tf_resource` key
  at all -- there is no Terraform resource this source builds.
- `comp-find 'sentiment_query_api' infra/aws/terraform` (this worktree): **0 hit(s) across 586 file(s)
  scanned** (8 binary, not searched) -- no Terraform tree anywhere declares this Lambda or its API Gateway.
  AMENDMENT 1's three declared-source carriers (`lambda-source-map.json` `tf_file`, `EC2_MANIFEST.json`
  `source_path`, "the Terraform tree that declares it") each come up empty except the bare `source_dir`,
  which names where the CODE lives, not who OWNS the deployed resource or which directive it serves.
- `comp-find 'sentiment' org/missions/DIRECTIVES.yaml`: **0 hit(s)** -- no directive's projects line names
  it (the same zero the `news` card already measured for the sibling `news-pipeline` family, R-6/EN-r-5-r3,
  `infra/logic/registry/systems.json` `unresolved[2]`).
- A prior, independent measurement already classifies this exact resource as undeclared drift:
  `org/missions/D12/NFRA/NFRA_REPORT/deliverables/0.9.0_WK_NFRA_REPORT~1/compose_edition.py:243` --
  `"property": "sentiment-query-api (API Gateway, LIVE-no-DECLARED)"` -- and that project's own
  `NFRA_REPORT.TO-RP-s-11` proof (`:63`, `:67`) names it among resources with "No new alarm, monitor, or
  notification" and holds its verdict to lower confidence than a CloudFront read, precisely because it is
  undeclared.
- An IAM role for the same resource, `sentiment_query_api-role`
  (`arn:aws:iam::313476888478:role/sentiment_query_api-role`), is visible only in a LIVE permission census
  (`org/missions/D12/NFRA/NFRA_IAMROLES202609/deliverables/0.9.0_WK_NFRA_IAMROLES202609~8/permission-cold-raw-bundle.json:30983-30985`)
  -- a census artifact, not a declared source; it confirms the resource is real and console/hand-deployed,
  not that it names a directive.

**Why this cell does not write a `systems.json` row for `sentiment`:** AMENDMENT 1's mint standard is "ONLY
where its owner or token is MEASURED from a declared source" -- and every declared-source carrier this cell
can read comes up empty for this token. The one thing that IS measured (`source_dir`) names a path, not an
owner; inventing a directive from the path alone is the exact guess `systems.json`'s `owner_claim` field
exists to refuse (same standard the `astn`/`news`/`trade` cards already applied, R-6 s.3).

**Disposition:** `sentiment-query-api` (live, API_GW) is recorded NOT-JUDGED in
`NOT_JUDGED_S6.r3.json` beside this card -- not graded, not stopped on, per AMENDMENT 1's mechanical
`--not-judged` mechanism. It is NOT added to `systems.json` `unresolved` (that list is EN-r-5's carrier,
scoped to R-6's six tokens by that cell's own task order; this cell's `<paths>` excludes editing
`unresolved`'s membership beyond what AMENDMENT 1 authorizes -- a resources.json/systems.json ROW mint,
which this token does not qualify for). Recovery path: the same one `news`'s card names -- either a
directive claims this resource family (folding it under an existing D<n> mission-tree project, e.g. the
`news-pipeline` owner once `news` itself resolves) or Andrew re-scopes it explicitly; until then it is a
live, undeclared, unowned surface, consistent with the NFRA_REPORT finding already on record.

---

## Card 2 -- `trade-submission-api` (live API_GW)

**Question for Andrew: same question Card 3 of `EN-r-5-r3`'s `OWNER_CARDS.r3.md` already asks for the
`trade` resource family -- this is one more member of it, surfaced by THIS cell's census now that it runs
past `sentiment-query-api`.**

**Why it RAISEs:** `grade()` tokenises `trade-submission-api` to `['trade', 'submission', 'api']`; `trade`
is `systems.json` `unresolved[1]` (a V2 token, declared and MEASURED unresolved by `EN-r-5-r3`,
`infra/logic/registry/systems.json` @`26623a452ff8583d`, this worktree) -- so `_slots()` R1.c raises on it
immediately (a V2 token at the system slot RAISEs by rule; it does not take the R1.d/e placeholder path,
which is V3-only). AMENDMENT 1 admits a mint ONLY where an owner is newly MEASURABLE; `trade`'s owner
question is ALREADY measured-unresolved by `EN-r-5-r3` (same registry commit `23980d3fbe`), so there is no
new mint this cell can make -- re-deriving the same conclusion would not change the registry state.

**Measured, not guessed (confirms the existing card, does not re-derive it):**
- `comp-find 'trade-submission-api' infra/aws/terraform infra/aws/lambda/ci`: **0 hit(s) across 612 file(s)
  scanned** (8 binary, not searched) -- no Terraform tree or lambda-source-map entry declares this
  resource by name; it is undeclared, the same shape as `sentiment-query-api` above and the same class the
  NFRA_REPORT finding already named it under (`compose_edition.py`'s `sentiment-query-api`/
  `trade-submission-api` pair, both `LIVE-no-DECLARED`, `NFRA_REPORT.TO-RP-s-11` proof `:63`/`:67`).
- `EN-r-5-r3`'s own measurement (`OWNER_CARDS.r3.md` Card 3, `infra/logic/registry/systems.json`
  `unresolved[1].why`) already traces `trade`'s 22 (there measured) live resource names to
  `TRSB_LEDGER`/`TRSB_TFIMPT`/`TRSB_PATHFIX`, LEGACY FLAT projects with 0 `DIRECTIVES.yaml` hits and
  SEAT owners only -- `trade-submission-api` is one more resource in that same, already-measured-ownerless
  family; nothing about ITS specific name changes that measurement.

**Disposition:** `trade-submission-api` (live, API_GW) is recorded NOT-JUDGED in `NOT_JUDGED_S6.r3.json`
beside this card, for the same reason Card 1 is: no declared source resolves an owner, and here the
registry ALREADY records that conclusion for the token itself. Recovery path: `EN-r-5-r3`'s Card 3, unchanged.
