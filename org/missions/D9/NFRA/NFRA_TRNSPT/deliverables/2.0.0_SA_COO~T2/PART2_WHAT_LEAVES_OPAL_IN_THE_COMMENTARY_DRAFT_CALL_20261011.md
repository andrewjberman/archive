# PART 2 -- what leaves Opal in the commentary drafter's outside-model call, to whom, and under whose word (2026-10-11 ~20:2xZ)

Seat: 2.0.0_SA_COO~T2 (the drafter is NFRA_TRNSPT's). Asked by 1.0.0_SA_CTO~DELL2 msg 5728. Read from the code at box/dell2 HEAD and
from the LIVE function's settings. No call to the model was made for this read.

## 1. The answer in three lines

- **To whom:** Moonshot AI, the Kimi chat-completions API, `https://api.moonshot.ai/v1/chat/completions`, model `kimi-k3`.
- **What leaves:** ONE prompt per draft: a fixed instruction, five abstract fields of the request, and (when any exist) wiped
  precedent texts. No client name, firm, household, advisor, account id, ticker, position row or dollar amount is put in it by the code.
- **Under whose word:** NO word names this call. It rests on the general open-egress law (CLAUDE.md edit `4d77a9c3ea`, Andrew-direct
  2026-10-09), which the PRD's C-KIMI ADDENDUM 1 applied to it. Andrew's one Kimi-specific word is scoped to another project. **By the
  CTO's rule in msg 5728 this comes to the CTO before anything is bound.** And see section 5: the function is ALREADY bound to its queue.

## 2. Exactly what is sent (`data/transcripts/scripts/commentary/drafter.py`)

`KimiAdapter.__call__` (lines 123-128) posts this JSON, with an `Authorization` bearer read from Secrets Manager `astn/kimi/api-key`:

`{"model": "kimi-k3", "temperature": 1, "max_tokens": 16000, "messages": [{"role": "user", "content": <prompt>}]}`

`build_prompt` (lines 66-77) makes the prompt from exactly three parts:

| part | content |
|---|---|
| instruction | fixed text: draft commentary in the house voice; treat what follows as data; "Use no client names and no account identifiers." |
| `REQUEST (abstract fields)` | the JSON of `abstract_fields(request)`: ONLY the five keys of `PROMPT_FIELDS` (line 26) |
| precedents | each chosen gold row's `body_text` as `PRECEDENT n (wiped)`; or `PRECEDENTS: none.` |

The five fields, and where each comes from (`commentary/entry.py` `abstract_request`, lines 169-193):

| field | what it is | source | could it carry a client identifier? |
|---|---|---|---|
| `yc_variant` | 1, 2 or 3 | the count of comparison models | no |
| `comparison_keys` | the NAMES of the comparison models chosen | the composition's `resolved.comparison_catalog[key].name` | no client data by design; a model named after a client would pass |
| `account_type` | a label | `commentary_basis.account_type` through `_label` | free text, see below |
| `themes` | labels | `commentary_basis.themes` through `_label` | free text, see below |
| `holdings_categories` | category -> whole percent | `commentary_basis.holdings_category_weights`, or the normalized input's rows summed by category | the percentages ARE one client's allocation; the category names are free text |

**Not sent, though present in the abstract request:** `request_id` and `requester`. `abstract_fields` rebuilds the dict from the five
keys only, so neither reaches the prompt.

**Never read into the abstract request at all:** the holder (`owner` is redacted by IRPT's reader and never read), the firm or tenant,
household, advisor, account ids, tickers, position rows, dollar amounts. Those go to the ticket context, which is internal-only.

## 3. The two soft spots (stated, not fixed)

1. **`_label` is the only filter on the three free-text members** (`account_type`, each theme, each category name): a string of at
   most 80 characters with no `@` (`entry.py:65-72`). It refuses an email address. It does NOT refuse a person's name, a household
   name or an account number typed into a theme or a category. Whether such text can reach `commentary_basis` is decided upstream, in
   IRPT's composition; it is not measured here.
2. **The allocation percentages are client-derived.** They carry no identity, but they are one client's portfolio shape. The PRD's
   C-KIMI names "holdings as category weights" as allowed input, so this is by contract, not a leak.

## 4. Precedents: nothing is sent today, and the gate that would guard them is a string

The handler's `gold_rows` port is `lambda: []` (`lambda_handler.py:262`), so every prompt today ends `PRECEDENTS: none.` No mail
commentary text leaves Opal through this call now. When gold rows are wired, their `body_text` (wiped silver text of analysts'
commentary) is sent, limited to rows not held out, at most 10 per draft. The guard is `wipe_gate_passed`, which is TRUE whenever the
environment variable `WIPE_GATE_RECORD` is non-empty: it is the PATH of a record, not a check of one.

## 5. The live state (read 2026-10-11 ~20:1xZ)

| what | value |
|---|---|
| function `outlook-global-commentary-draft-lambda` | PRESENT (applied 05:26Z, re-applied 05:44Z by another seat's order) |
| `KIMI_API_URL` | `https://api.moonshot.ai/v1/chat/completions` |
| `KIMI_STANDING_WORD_REF` | `4d77a9c3ea` -- non-empty, so the handler BUILDS the model adapter |
| `WIPE_GATE_RECORD` | set to the CTO's round-12 analysis path |
| event source mapping | 1, ENABLED, on `outlook-global-commentary-draft-analysis-ready-queue` |
| that queue now | 0 messages visible, 0 in flight |
| invocations today | 2: 05:49:52Z (3.6 s, logged `composition refused`) and 06:10:01Z (48.8 s, no refusal logged) |

**So the function is bound to its queue already.** Any `analysis_ready` message sent to that queue starts a draft, and a draft is a
call to Moonshot. The CTO's cell (the chain stops before `analysis_ready` is sent for a ticketless request) acts on the SENDER;
nothing on this function's side stops a message that does arrive.

**Whether a call has already been made (inferred, not measured):** the 06:10Z invocation ran 48.8 s against 3.6 s for the refused
one, which fits one model call. The handler logs request ids only, by design, and prints no line for the call, so the log cannot
confirm it. Moonshot's own usage record, or a log line added to the adapter, would.

## 6. The word

| candidate | what it covers | does it name this call? |
|---|---|---|
| `ANDREW_DIRECT_20260930_06xxZ_..._KIMI_STANDING_WORD.md` | Kimi K3 classifier runs in MDPF_SECCLASS: "security names and tickers only, no client data". Its own text: "Not read as: any vendor run with client data, any run outside MDPF_SECCLASS classification, or any wider standing word." | NO |
| CLAUDE.md law edit `4d77a9c3ea` (Andrew-direct 2026-10-09: "infinite egress on all channels now (aside from BBG ...)"; today's text: "Egress is open on every channel, except Bloomberg ... other vendor APIs need no per-use word") | every channel and every vendor but Bloomberg | generally, yes; it names no vendor, no payload and no client-derived data |
| PRD C-KIMI + ADDENDUM 1 (`1.0.0_SA_CTO~DELL2`, 2026-10-09) | "one Kimi K3 call per commentary draft ... No per-use word from Andrew is required" | it is the CTO's reading of the law, not Andrew's word |

**So: no recorded word of Andrew's names sending a client's allocation shape and the firm's commentary themes to Moonshot for
drafting.** The general law permits vendor egress without a per-use word; whether that law is meant to reach client-derived
figures is the question, and it is the CTO's (or Andrew's), not this seat's.

## 7. Not measured

- What IRPT's composition can put into `commentary_basis.themes`, `account_type` and the category names (soft spot 1).
- Whether the 06:10Z run reached Moonshot (section 5).
- Moonshot's retention or training terms for the API: no contract or terms record was read.
