# Never-widen ask -- OG-rl-2, the narrow opal-gateway release of the /hx/mail LISTING route (train slot 5)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-01 ~15:1xZ. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-2.hx-mail-listing-release.md`
(A1). Rulings it rests on: PRD v1.4 C7 "Mail listing" + addendum @dabb8e1e9f; `1.0.0_SA_CTO~O` msgs 27843 (cut) and 27852
(artifact-shipped sender table accepted, two read-back conditions); the train ruling (R1, R2 C1-C6); row Z-S32's standing
rule. PHASE A evidence: `deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-2.md`, drained @a47257655c. Build:
`OG-hl-1` complete (drained @9c62463b78; issuer re-grade AC1 12 of 12, AC2 PASS).

**Halves owed:** `1.0.0_SA_CTO~O` (CTO half) and `3.0.0_SA_CVO~O` (second, non-acting half), against THIS file at its
commit. PHASE B re-reads the live ref first (re-cut if moved) and is train slot 5 (MX-r-8 landed e3567ce5f7 at 12:37Z).

## 1. The bytes

Release branch `rel-nfra-oplgtw-hx-mail-listing` (`/c/tmp/og-rel5`), HEAD `0a1d9079c682c640e619612f804257681c5db357`, two
commits on live `e3567ce5f788f45195bec065f4d2fc5a68a38cd3` (host md5 91 of 91 equal; S3 git-ref equal):
- `54d5c219b8`: OG-hl-1's gateway commit `cdd4e5cb08` three-way onto live (both existing files merged clean);
- `0a1d9079c6`: `deploy-to-ec2.sh` -- `MAIL_SENDER_TABLE` read host-side from the shipped `deploy/mail_sender_table.txt`,
  refused (exit 3, no `.env` write, no restart) when missing, empty, blank-only or outside the address charset; the
  deploying-shell `OG_MAIL_SENDER_TABLE` input removed; a `rm -f` of the previous table file before the extract so a
  missing file cannot pass on a stale copy.

Census against live: 5 files, +555/-13 (`app/mail_route.py`, `app/server.py`, `deploy/mail_sender_table.txt`,
`tests/test_mail_listing.py`, `deploy-to-ec2.sh`), 0 outside the gateway directory; `ms_ingest.py` not among them.
Artifact: 95 files, 3 differ from live (`mail_route.py`, `server.py`, the new table file).

## 2. Blast radius -- what the act may touch

| key | before (PHASE A read) | after | rollback |
|---|---|---|---|
| host app files | live `e3567ce5f7`, 91 of 91 by md5 | the 3 named files change | re-deploy `/c/tmp/og-rb5` (94 of 94 equal to live S3) with `DEPLOY_BASE_REF` = the release sha; `OG_MAIL_SENDER_TABLE` from `criterion.py` into the shell only (that template still takes it) |
| host `.env` | 46 keys; `MAIL_SENDER_TABLE` 3 items | 46 keys, same set; `MAIL_SENDER_TABLE` 3 items, now from the shipped file (CTO 27852 condition: count = `criterion.py`'s 3 at the cut) | the same re-deploy |
| **public reach** | `/hx/mail/messages/{id}`, `.../attachments`, `.../attachments/{aid}` | **+ `GET /hx/mail/messages`** (listing): same prefix, ALB rule 35, and the mail bearer as the ONLY edge gate; rows are 5 keys (`message_id`, `receivedDateTime`, `sentDateTime`, `internetMessageId`, `hasAttachments`), never a subject, body, recipient or attachment name; one table sender per request, 31-day window, page_size <= 50, <= 200 Graph pages per request; the page token bound to sender + window and never a Graph URL | re-deploy (the listing unmounts) |
| Graph reads | by-id paths | + `/me/messages` with server-built `$filter`/`$select`/`$orderby`/`$top`, on a separate allowlist tuple used only by the listing handler; GET only, delegated identity unchanged | re-deploy |
| tool list | as read at the BEFORE step (not re-read here) | unchanged: the listing is a headless route, not an MCP tool (ac08 LIVE 60 + OWN 0 in-tree) | -- |
| S3 artifact key | `...-e3567ce5f7.tar.gz` (+ `-latest`) | + `...-0a1d9079c6.tar.gz`; `-latest` moves | the live key stays |
| `EC2_MANIFEST.json` | `deployed_commit` `e3567ce5f7` | the release sha, previous `e3567ce5f7` | revert the manifest commit |

**Not touched, by name:** Terraform, IAM, the ALB, the instance, every secret (none written), `/ms/*`, the by-id mail
and transcripts routes' behaviour, the principal rosters' host-side read, the identity allowlist, the mcportal pin.

**Partial-failure shape (row Z-W15-S17):** the table file ships IN the artifact, so the refusal runs after the extract:
a refusal leaves the new app files on disk with the OLD process and OLD `.env` running; the verify reads it and the
re-deploy of `og-rb5` restores the files.

## 3. The named properties and their writers

**(a) Who can enumerate message ids, and what a row reveals.** N = 2 writers: `match_bearer` (constant time) and the
listing handler's gates (table membership before Graph; per-row own-`from` re-check; the 5-key row builder; the bound
token). Expected branch: `rl2.AC1.sh` reads 9 of 9 (a known row listed with `internetMessageId` equal to the message
route's; off-table 403; empty window 200/0/null; paging without repeats; the transcripts and `/ms` bearers 401; a token
replayed under another sender or window 400; a raw Graph URL token 400). Other branch: any arm fails -> roll back,
ledger ROLLED BACK. Mutation controls at build: row re-check removed -> 3 tests fail; token sender binding removed -> 1.
**Risk left:** the Graph `$filter` shape and `$skiptoken` continuation were tested against stubs only; `rl2.AC1.sh`
(live) is their first real exercise, and a Graph error there is a 502 refusal to the caller (fails closed), caught by
the arms.

**(b) Which senders the mail routes admit.** N = 1 writer after this release: the deploy's host-side read of
`deploy/mail_sender_table.txt` (kept equal to `criterion.py` by `test_sender_table_file_equals_criterion`). Expected: 3
items, equal count to `criterion.py` at the cut (CTO 27852). Other branch: missing/empty -> refused before any `.env`
write (synthetic: missing 3, empty 3, blank-only 3, bad char 3, metacharacters 3; one valid 0; three valid with CRLF 0).

## 4. Act and verify (PHASE B, from the order)

- **Before:** step 7 re-reads live (re-cut if moved); BEFORE reads (tool list, `ENABLED_INTEGRATIONS`, key names only);
  NEVER-2 ledger `nfra-oplgtw-hx-mail-listing-release` committed before the act.
- **Act:** from `/c/tmp/og-rel5`: `DEPLOY_BASE_REF=<live full sha> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15 bash
  infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (no roster or sender
  hand-off).
- **Verify within 90 s:** `/health` 200; shipped md5 = release bytes; tool list unchanged; `ENABLED_INTEGRATIONS` and
  the key set unchanged; `MAIL_SENDER_TABLE` count = 3; `/ms/*` and the by-id `/hx/*` routes as before; then
  `rl2.AC1.sh`. Any failure: roll back, re-verify, close ROLLED BACK. **Criteria:** `rl2.AC1.sh`-`rl2.AC3.sh`.
