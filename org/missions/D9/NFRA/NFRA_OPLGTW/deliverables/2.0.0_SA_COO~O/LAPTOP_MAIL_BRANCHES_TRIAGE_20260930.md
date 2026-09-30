# NFRA_OPLGTW order 4 -- triage of the four laptop gateway mail-tool scratch branches (2026-09-30)

**For:** `2.0.0_SA_COO~O` / `1.0.0_SA_CTO~O`. **Input:** relay
`org/tier0_exec/0.0.0_AB_MSTR~Z/deliverables/RELAY_20260930_1454Z_LAPTOP_CTO_103268_NFRA_TRNSPT_GATEWAY_ORDERS.md`
(order 4 = three Mail.Read tools: attachment `$value` download; a filtered paged list on sender, received, has-attachment
and nextLink; `ccRecipients`, `internetMessageId`, `conversationId` and `sentDateTime` in `read_email`'s `$select`).
**Status:** read-only triage, NOT committed. No branch was merged, checked out or cherry-picked.

## Method (what each number was read from)

- CLOUD HEAD = `5897445325` (`git rev-parse HEAD`, branch CLOUD). The branches were fetched into `refs/remotes/origin/<name>`.
- Merge-base: `git merge-base CLOUD <tip>`. Diffstat: `git diff --stat <merge-base> <tip>`.
- Conflicts: `git merge-tree --write-tree --name-only` (3-way merge against HEAD), plus a cherry-pick simulation
  (`--merge-base=<tip>^`). Both gave the same file lists.
- Content equality: the `+`/`-` lines of each `tools.py` diff were compared, int vs f2+f1+f3 in file order.
- Tests: each merged tree was exported with `git archive` to the session scratchpad. The one count conflict was resolved
  there only, and pytest ran against it. Nothing was written to the repo tree.
- Every test mocks `graph.call` and `_run`. No test calls live Graph. The risk class of these results is LOCAL only.

## Shared facts (all 4 branches)

| Item | Finding |
|---|---|
| Commits per branch over merge-base | 1 of 1 on each branch. The author is `0.0.0_AB_MSTR` under an audited override; the message says "preservation commit" |
| LD-0613 "Progress 40" hunk | Present on 4 of 4 branches with identical content (blob `0025bd03dc`, +8 lines). It conflicts with CLOUD's LD-0613 (HEAD blob `814300a36c`) on 4 of 4. Drop it on adoption |
| Capability on CLOUD HEAD, by content | `read_email` `$select` on HEAD = `subject,from,toRecipients,receivedDateTime,body` (`app/tools.py:220`). None of the 5 new fields is present. `list_email_filtered`: 0 hits in HEAD `app/`. `inspect_email_attachment`: 0 hits. HEAD's mail tools are `list_recent_email`, `search_email`, `read_email`, `list_email_attachments`, `save_email_attachment_to_site`, `send_email`, `reply_email` and `validate_ssavail_attachment`. **None of the three capabilities exists on CLOUD** |
| Competing work on this device | Mail-tool edits in the 2 live OPLGTW worktrees (`C:/tmp/wk-oplgtw-12`, `C:/tmp/og-rel2`): 0 of 2 carry them. `og-rel2` holds release `rel-nfra-oplgtw-tier-auth`, which touches `tools.py`. A deploy of adopted code must follow or re-base on that release |
| `identity_tool_allowlist.txt` | Touched by 0 of 4 branches. The file has 19 lines and 1 data row (`opalbloomberg@... opal_data_refresh_upload client=...`) |
| `app/identity_scope.py` (`_SEED`) | Touched by 0 of 4 branches. The one scoped identity has 12 seeded tools and no mail tool, so the new tools are DENIED to it by default (deny-by-default, `identity_scope.py:11`) |
| Graph scopes / Mail.Read | Touched by 0 of 4 branches. `Mail.Read` is already in the full-tier scopes (`app/config.py:64`) and the read-tier scopes (`:100`). Every new call is a `/me/messages...` GET under the caller's own delegated token |
| Routes, server.py, token_broker, Terraform, requirements | Touched by 0 of 4 branches. There is no new route and no headless or static-bearer path (those are orders 2 and 5, which none of these branches implements) |
| Who can call the new tools | They are added to `destructive_ops.SAFE_TOOLS` (read class, `write_class=None`) and `data_entitlement.NATIVE_TOOLS` (class `legacy`). Unprofiled, unscoped principals get them at every tier. A restricted (Schwab-profile) principal is denied them like every legacy tool (`data_entitlement.py:374-377`). A scoped identity is denied them by default |
| Egress | No new host. The Graph `$value` attachment fetch already exists on HEAD (`tools.py:252`, `:489`) |
| Dependency | f3 imports `pypdf` lazily. `pypdf` is in 0 of 1 requirements files (`infra/aws/ec2/opal-gateway/requirements.txt`). Without it the tool returns `parse_error: "pypdf not installed"`. Whether pypdf is on the box is UNREAD. The commit message says vendored `.whl` files in `wt-gw-f1` were not committed |
| Test baseline in the export | `test_entitlement_admin.py` ac01-ac07: 7 of 9 ERROR identically on HEAD and on all 4 trees, because the export lacks `org/standards/NFRA_OPLGTW_CONTRACT.json`. This comes from the export's scope, not from the branches. Below, "ac08" is the test that counts tools |

## gw-f1-read-email-fields

| Field | Value |
|---|---|
| Tip | `5ec089b9a1` |
| Merge-base with CLOUD | `c4019eacd2` (CLOUD is 2475 commits ahead of it) |
| Files (3) | `app/tools.py`, `tests/test_read_email_fields.py` (new), `org/tier0/ledger/LD-0613.md` |
| +/- | +64 / -2 over 3 files. Gateway only: +58 / -2 over 2 files |
| What it does | Widens `read_email`'s `$select` from 5 to 11 fields: adds `ccRecipients`, `bccRecipients`, `internetMessageId`, `conversationId`, `hasAttachments` and `sentDateTime`, and updates the docstring. This covers the 4 of 4 fields order 4 names, plus 2 more |
| Tests in diff | Yes: 1 file, 1 test (asserts all 11 fields plus method and path). On the merged tree it gives 1 of 1 passed. Tool count unchanged, so ac08 is not affected |
| Overlap with CLOUD | None. HEAD's `$select` has 5 fields |
| Conflicts vs HEAD | 1 of 3 files: `LD-0613.md` only. The gateway files merge clean (2 of 2) |
| Auth / allowlist touch | None. Same tool and same Graph call, more fields from the caller's own mailbox. `bccRecipients` is populated only on the sender's own copy |
| Same code in int? | Yes. int's `tools.py` carries this hunk identically (see int). int does NOT carry `test_read_email_fields.py` |
| **Recommendation** | **SUPERSEDE** by gw-mail-tools-int for the code. Take `tests/test_read_email_fields.py` from this tip into the int adoption |

## gw-f2-email-filtered

| Field | Value |
|---|---|
| Tip | `15ef03f0bc` |
| Merge-base with CLOUD | `c4019eacd2` (CLOUD +2475) |
| Files (6) | `app/tools.py`, `app/destructive_ops.py`, `app/data_entitlement.py`, `tests/test_entitlement_admin.py`, `tests/test_list_email_filtered.py` (new), `LD-0613.md` |
| +/- | +202 / -3 over 6 files. Gateway only: +194 / -3 over 5 files |
| What it does | Adds the new tool `list_email_filtered(senders, received_from, received_to, has_attachments, top, page_token)`. It filters exact sender addresses (OR-ed), received date bounds (`ge`/`lt`, ISO8601; a date-only value is normalised to `T00:00:00Z`) and has-attachments, with `$orderby receivedDateTime desc` only when a date bound is present. `top` is clamped to 1-250. The Graph nextLink is reduced to an opaque base64 `$skiptoken`/`$skip` page token; the URL itself is never returned or accepted. Inputs are regex-validated before any Graph call, and single quotes in addresses are escaped. Registered in SAFE_TOOLS and NATIVE_TOOLS |
| Tests in diff | Yes: 1 file, 11 tests (filter build, no orderby without a date, 6 injection/invalid cases, paging round-trip, top cap, registration). On the merged tree: 11 of 11 passed; ac08 passed after the count was set to 54 |
| Overlap with CLOUD | None. HEAD's `list_recent_email` filters only `since_iso`/unread; `search_email` is fuzzy `$search` |
| Conflicts vs HEAD | 2 of 6 files: `tests/test_entitlement_admin.py` (the hard tool count: HEAD 53, branch 52) and `LD-0613.md`. The resolved value is 54 |
| Auth / allowlist touch | None to the allowlist, scopes or routes. It widens the SAFE read set by 1 tool for unprofiled principals (own mailbox, Mail.Read) |
| Adopting f2 and f3 separately | Cherry-picking f3 on top of f2 conflicts in `app/data_entitlement.py` (the NATIVE_TOOLS lines are adjacent) and in `LD-0613.md`. int already resolves this |
| **Recommendation** | **SUPERSEDE** by gw-mail-tools-int for the code. Take `tests/test_list_email_filtered.py` from this tip into the int adoption |

## gw-f3-inspect-attachment

| Field | Value |
|---|---|
| Tip | `6c61ac531b` |
| Merge-base with CLOUD | `c4019eacd2` (CLOUD +2475) |
| Files (5) | `app/tools.py`, `app/destructive_ops.py`, `app/data_entitlement.py`, `tests/test_inspect_email_attachment.py` (new), `LD-0613.md` |
| +/- | +195 / -1 over 5 files. Gateway only: +187 / -1 over 4 files |
| What it does | Adds the new tool `inspect_email_attachment(message_id, attachment_id, max_bytes=5_000_000)`. It fetches attachment metadata, then `$value` SERVER-SIDE, and returns name, contentType, isInline, bytes, sha256, the first 8 bytes as hex and, for a `%PDF` file, page count, 5 info fields and at most 1500 characters of page-1 text. It refuses above `max_bytes` (from metadata before the fetch, or after it) and errors on item/reference attachments. It never returns the attachment bytes. Registered in SAFE_TOOLS and NATIVE_TOOLS |
| Tests in diff | Yes: 1 file, 7 tests. On the merged tree: 7 of 7 passed with local pypdf 6.16.2. **ac08 FAILS on f3 alone (`assert 54 == 53`)**: the branch does not bump the hard tool count |
| Overlap with CLOUD | Partial mechanism only. `save_email_attachment_to_site` (`tools.py:236`) and `validate_ssavail_attachment` (`:471`) already do the same `$value` fetch; neither returns a hash, magic bytes or PDF facts. The capability itself is absent |
| Conflicts vs HEAD | 1 of 5 files: `LD-0613.md`. It is textually clean, but ac08 needs a count edit (53 -> 54) |
| Fit to order 4 | Order 4 says "attachment `$value` download". f3 is an INSPECT and delivers no bytes to the caller. If order 4 means bytes returned to the caller over MCP, that is a new content-egress path with an output limit. f3 does not serve it, and it would be a PRD-addendum item (allowlist and auth boundary). As written, f3 is read-only facts plus 1500 characters of text |
| Auth / allowlist touch | None to the allowlist, scopes or routes. It widens the SAFE read set by 1 tool. First-page text (at most 1500 characters) is attachment content reaching the caller from the caller's own mailbox |
| **Recommendation** | **SUPERSEDE** by gw-mail-tools-int for the code. Take `tests/test_inspect_email_attachment.py` from this tip. The literal "download" clause stays open and NEEDS-ADDENDUM only if a byte-returning tool is wanted |

## gw-mail-tools-int

| Field | Value |
|---|---|
| Tip | `6a7b9e78fa` |
| Merge-base with CLOUD | `2ab90bf162` (CLOUD +1000). `app/tools.py` at the merge-base has the same blob as HEAD (`ed86df2605`), so there is no drift in the main file |
| Files (5) | `app/tools.py`, `app/destructive_ops.py`, `app/data_entitlement.py`, `tests/test_entitlement_admin.py`, `LD-0613.md` |
| +/- | +171 / -7 over 5 files. Gateway only: +163 / -7 over 4 files |
| What it does | Combines all three changes. The commit message says "f2+f3", but by content `tools.py` also carries f1's `read_email` `$select` hunk |
| Equal to f1+f2+f3 by content? | `tools.py`: 141 of 141 changed lines are identical to f2+f1+f3 concatenated (diff empty). `destructive_ops.py`: 3 of 3 changed lines are identical to f2 plus f3. `data_entitlement.py`: the NATIVE_TOOLS set is identical (the same 2 names added) and the line wrap differs. `test_entitlement_admin.py`: the count is 54 (based on 52), which differs from f2's 53 |
| Tests in diff | **No new test file (0 of 3).** The only test change is the ac08 count, 52 -> 54. With the 3 f-branch test files placed in the merged tree: 1 of 1 + 11 of 11 + 7 of 7 passed, `test_attachment_tools.py` 5 of 5, and ac08 passed at 55 |
| Overlap with CLOUD | None (see shared facts) |
| Conflicts vs HEAD | 2 of 5 files: `tests/test_entitlement_admin.py` (HEAD 53 after MX-q-3's `gateway_query_catalog`; branch 54; correct value **55**) and `LD-0613.md`. `data_entitlement.py` merges clean with HEAD's `dim_transaction` and `gateway_query_catalog` additions |
| Auth / allowlist touch | None to `identity_tool_allowlist.txt`, `identity_scope.py`, scopes, routes or egress. The SAFE/NATIVE read set grows by 2 tools, and `read_email` returns 6 more fields |
| **Recommendation** | **ADOPT**: cherry-pick `6a7b9e78fa` minus the LD-0613 hunk, set the ac08 count to 55 with a comment naming both tools, and add the 3 test files from the f1/f2/f3 tips. This covers order 4's `$select` clause and filtered-list clause. The attachment clause is covered as an inspect only (see f3). No PRD addendum is needed for this adoption, because it touches no allowlist and no auth boundary. The headless mail route (order 5) is where that boundary lives |

## Summary

| Branch | Verdict | Why |
|---|---|---|
| gw-mail-tools-int `6a7b9e78fa` | ADOPT (cherry-pick minus LD-0613; count 55; plus 3 test files) | It is f1+f2+f3 by content, with the one f2/f3 conflict already resolved, and the capability is absent on CLOUD |
| gw-f1-read-email-fields `5ec089b9a1` | SUPERSEDE (take its test file) | Its code is carried identically in int |
| gw-f2-email-filtered `15ef03f0bc` | SUPERSEDE (take its test file) | Its code is carried identically in int, and applying it separately with f3 conflicts |
| gw-f3-inspect-attachment `6c61ac531b` | SUPERSEDE (take its test file) | Its code is carried identically in int. Alone it fails ac08 (54 vs 53). A byte-returning `$value` download is not built; that would be NEEDS-ADDENDUM |
