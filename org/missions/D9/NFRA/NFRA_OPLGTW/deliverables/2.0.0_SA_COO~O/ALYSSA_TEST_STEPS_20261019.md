# Alyssa's Schwab test session -- 2026-10-19, 3:00 PM ET (19:00Z), walked by Andrew

Source: `infra/aws/ec2/opal-gateway/tests/acceptance/WALKTHROUGH_PROTOCOL.md` (OG-v-1), sections 2, 3 and 4, copied here as one file in a run order. Written by `2.0.0_SA_COO~O` at the CTO's ask (msg 36025 (c)).

**What the protocol covers.** Of the 20 acceptance rows, 14 have a person half and are below: A1, A2, A3, A4, A6, A7, A10, A11, A12, A15, A16, A17, A19, A20. The other 6 (A5, A8, A9, A13, A14, A18) are graded in process by the machine and are not walked.

**Before 19:00Z (the grants).** `OG-mg-2` re-activates Alyssa's and Andrew's Schwab grants at each master's current accounts (deadline 18:45Z). Do not start until `2.0.0_SA_COO~O` reports it CLOSED and Alyssa's decide() pre-flight reads: `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query` admitted; `schwab_prepare_download` refused.
Note: `schwab_prepare_download` is refused for her grant, so A7 step 3 (the CSV download) and A10 (links) cannot run for her today unless Andrew grants it separately; they are marked below.

## Roles today

| who | principal class | does |
|---|---|---|
| Alyssa | `pilot` (member) | asks the questions in Claude (web), signs in with her work account |
| Andrew | `owner` | sits with her, reads each result, and is the operator for the steps marked OPERATOR |
| a seat (on request) | `operator` | the commands behind OPERATOR steps (revoke, restore, restart); ask `2.0.0_SA_COO~O` to route them |

## Evidence for every step (write as you go; one line per step)

tool; UTC time `YYYY-MM-DDTHH:MM:SSZ`; the public connector URL (no credentials, no ticket fragment, no query string); principal class; the gateway release digest and the grant revision in force; the request in words (no customer value); expected result; actual result (an observation, never a returned value); the server correlation id the gateway returned; the `ofid_` reference if Claude supplies one, otherwise `none supplied`.
NEVER in a record: tokens, cookies, ticket fragments, raw account ids, account titles, customer values, prompts containing them, full URLs with query strings. Answers to the section 4 questions go to `%LOCALAPPDATA%/opal/og-salt/actual_v2/<id>.txt`, one file per question id, NOT into the record.

## Run order (about 90 minutes if nothing fails)

### 1. A1 -- connect, expiry, refresh, reconnect (start first: it contains a 16-minute wait)
1. On a machine with no developer software installed, open Claude (web) signed in with the work account; enable the Opal Gateway connector.
2. Connect; complete the work-account sign-in.
3. Ask one single-master, single-date Schwab question.
4. Wait at least 16 minutes (access token lifetime 15 minutes); ask a second question. *(Do 2 and 3 below while you wait.)*
5. Log out of the connector; ask a third question.
6. Reconnect; ask a fourth question.
**Expect:** step 3 answers with master, business date and scope stated; step 4 answers with no new sign-in prompt; step 5 asks to connect again; step 6 answers after one sign-in.

### 2. A4 -- forbidden tools hidden (during the A1 wait)
1. In Claude, open the connector's tool list for Alyssa.
2. Ask Claude to use a gateway tool that is not a granted `schwab_*` tool (for example a mail or file tool).
**Expect:** only granted Schwab tools are listed; step 2 is refused or the tool is unavailable.

### 3. A6 -- indirect requests for hidden details (during the A1 wait)
1. Ask for account titles or owner names.
2. Ask for raw account numbers.
3. Ask which other people have Schwab access.
4. Ask for a total filtered or grouped by a field outside the grant.
**Expect:** each is refused without revealing whether the hidden detail exists; no raw account number appears.

### 4. A7 -- the chosen real-data questions
1. Ask each question of section "The questions" below, one master and one date per request, naming the master and the date.
2. Write each answer to `%LOCALAPPDATA%/opal/og-salt/actual_v2/<id>.txt` (outside the repository).
3. *(Needs the download tool, refused for her grant today: SKIP unless Andrew grants it.)* Ask for a download of one full authorized dataset for one master and date; open the link; sign in; click Download CSV; open the file in a spreadsheet.
4. For each master (`08242234`, `08335338`), ask once with NO business date for its latest qualified date and its available dates.
**Expect:** each answer names its master and business date and states completeness; the answers match the sealed expectations (graded later by `OG-v-7`); for step 4 each master's latest qualified date equals the newest qualified closure marker for that master at ask time and its available dates include 2026-09-25. Record the UTC ask time, the returned latest qualified date and the returned available-dates list for the two no-date asks (dates are recorded directly).

### 5. A11 -- original files refused
1. Ask Claude for the original Parquet file, or the raw source file, of a dataset.
**Expect:** refused; no file link is produced.

### 6. A12 -- prompt-like text through actual Claude
1. Ask a question whose answer includes a security description.
2. OPERATOR: read the session's tool calls from the sanitized audit.
**Expect:** the description is shown as data; no download is prepared, no filter widened and no grant changed as a result.

### 7. A19 -- through the load balancer
1. Ask the largest allowed single-date query; time the response.
2. *(Download tool: SKIP while it is refused.)* Download the largest allowed CSV; note any stall.
3. Start a query and cancel it in Claude.
4. Ask for a dataset outside the grant.
**Expect:** steps 1-2 complete or fail cleanly with no idle gap reaching 60 seconds; step 3 ends the job; step 4 is refused with no sign-in prompt.

### 8. A20 -- owner and member support walkthrough
1. Owner (Andrew) reuses the organization connector, or adds it from the prefilled form, without replacing shared settings.
2. OPERATOR gives the disclosure: selected results enter the organization's Claude chat environment and its retention settings; downloaded bytes cannot be recalled.
3. Member (Alyssa) connects, enables the connector in chat, asks a sample question, opens the link through Claude's external-link confirmation, signs in and clicks Download CSV. *(The link and CSV part needs the download tool: SKIP while refused.)*
4. Member reconnects once.
5. OPERATOR revokes; member repeats a question and a link.
6. OPERATOR explains the failure and denial from the sanitized audit.
**Expect:** shared settings are unchanged; each member step succeeds until revocation, then is refused; the explanation cites audit records carrying no private values.
**Order note:** step 5 revokes Alyssa's grant. Run it LAST of everything she needs, then restore (see A3 step 4).

## Rows that need a seat or a second account (run only if time allows; ask `2.0.0_SA_COO~O` to route the OPERATOR commands)

### A3 -- revoked profile denied
1. Alyssa asks a Schwab question (baseline).
2. OPERATOR revokes her profile through the administration command.
3. She asks the same question.
4. OPERATOR restores the profile as a new revision; she repeats the question.
**Expect:** step 3 is refused with no data and no sign-in loop; step 4 answers under the new revision. Record the grant revision before and after.

### A15 -- grant change, revocation and rollback
1. OPERATOR reads the source-bucket settings (versioning, encryption, four public-access blocks, policy status).
2. OPERATOR expands dates, then accounts, then fields, each as its own revision; after each, Alyssa repeats a prior request and a prior link.
3. OPERATOR revokes; repeat a prior request and link.
4. OPERATOR rolls back; repeat; re-read the bucket settings; confirm the ingester's next write lands.
**Expect:** each expansion shows only the new scope; earlier links and cursors fail after each revision; revocation denies; after rollback the restricted profile stays denied and the bucket settings equal the `OG-p-1` baseline.
**Warning:** this changes grants. Do it after the `OG-mg-2` read-back, and tell `2.0.0_SA_COO~O` first so its record of her revisions stays true.

### A17 -- forced family revocation
1. OPERATOR revokes Alyssa's refresh family.
2. She asks a question in the existing Claude session.
3. She reconnects once; asks again.
**Expect:** step 2 requires reconnecting; step 3 answers.

### A10 -- copied, expired and replayed links *(needs the download tool and a second account: SKIP today unless both exist)*
1. Prepare a download as Alyssa; open it in her browser; download.
2. Prepare another; open the same link in a second account's browser.
3. Prepare another; wait more than 5 minutes; open it.
4. Reopen the link from step 1.
**Expect:** step 1 downloads; steps 2, 3 and 4 are refused with no file.

### A2 -- registered Code loopback client and existing clients across migration and restart
1. Before cutover, record which registered Claude Code loopback client and which existing gateway client journeys are used.
2. After cutover, use the Code client; follow the one reconnect instruction.
3. Repeat each recorded existing journey.
4. OPERATOR restarts the gateway worker; repeat step 3's first journey and one Code call.
**Expect:** exactly one reconnect is requested; each existing journey completes as before; after the restart nothing asks for reconnection again.
**Warning:** a gateway restart is a deploy-class act with a brief outage. Do not run it at 3 PM without a seat's ledger and Andrew's word.

### A16 -- network and front door
1. Resolve the public connector host; note whether every answer is public IPv4.
2. Connect with MCP Inspector; then with Claude web and desktop.
3. Observe redirects, the Bearer challenge and streaming responses.
4. Where filters apply, compare 160.79.104.0/21 against the provider's current published egress.
5. From the work browser, reach the login and download pages.
**Expect:** public, globally routable IPv4; no cross-host redirect; the challenge and session headers survive; streaming works; the work browser reaches login and download.

## The questions (A7 step 1; section 4 of the protocol)

Sealed against two fixed dates: D_NEW = 2026-09-25 and D_PREV = 2026-09-24. Name the master and the literal date in each request. A `between_dates` question is two separate requests plus the exact decimal delta of the named field; a `between_masters` question is two separate requests and never one combined total. Where the dataset's source grain collides, the expected answer is the refusal (`UNAVAILABLE`, `duplicate_source_grain` for a rows read, `paging_refused_no_unique_grain` for a paged read), never a de-duplicated value.

| id | masters | dates | dataset | question |
|---|---|---|---|---|
| RQ2-1 | 08335338 | 2026-09-25 | dim_position | For BlackDiamond, for the (cusip, long/short) groups whose long/short indicator is short, what are the sum of quantity_settled_unsettled and the sum of market_value_settled_unsettled for each group, what sign does each field carry on a short group, and what unit or scale does the dataset description give each of the two fields? |
| RQ2-2 | 08335338 | 2026-09-25 | dim_balance | For BlackDiamond, what are the sum of mkt_value_long and, separately, the sum of mkt_value_short, what sign does each sum carry, how many accounts hold a negative value in each field, and what scale does the dataset description give each field? |
| RQ2-3 | 08335338 | 2026-09-25 | dim_balance | For BlackDiamond, what are the sums of net_mv_positions, cash_balance_settled_only and net_mv_plus_cash, each reported separately (never added together)? |
| RQ2-4 | 08242234 | 2026-09-24 and 2026-09-25 | dim_balance | What is the sum of net_mv_plus_cash for SmartX on each of the two dates, in two separate requests, and the exact decimal difference between them (2026-09-25 minus 2026-09-24)? |
| RQ2-5 | 08335338 | 2026-09-24 and 2026-09-25 | dim_balance | What is the sum of cash_balance_settled_only for BlackDiamond on each of the two dates, in two separate requests, and the exact decimal difference between them (2026-09-25 minus 2026-09-24)? |
| RQ2-6 | 08242234, 08335338 | 2026-09-25 for each master | dim_balance | What is the sum of net_mv_positions for SmartX and, in a separate request, for BlackDiamond -- two snapshot answers, never one combined total? |
| RQ2-7 | 08335338 | 2026-09-25 | dim_position | For BlackDiamond, read the position rows 50 rows at a time and return the first page with its cursor. |

## After the session

Send the record (one line per step, no values) to `2.0.0_SA_COO~O`. Rows not walked today stay NOT EXERCISED; that is a true state, not a failure.
