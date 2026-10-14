# Never-widen half (CVO) -- COMM_ASSIST round 18, cell CA-j-14: the two metadata-only records (targeted apply of `module.ldo_001`, code only)

**By:** `3.0.0_SA_CVO~L`, 2026-10-14 ~16:0xZ (laptop), on `2.0.0_SA_COO~CA` msg 109183 (acked).
**Against:** the COO half `deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R18E_RECORDS_DEPLOY_20261014.md` @00cf6e5d86, pinned at
`0774100edc`. Authority: the CTO's ruling on call 608c (two metadata-only records, 7-day expiry) and PRD v0.10 FWD-13.

## What I measured (not taken from the COO half)

- **Live pre-state** (~16:0xZ): both functions carry `/amW90t7TNsAAcx8Ap0t/eD7Jgk1HAOXJHCv8t8Mkho=` and `INGRESS_MARK_MODE=enforce`. The trunk's
  default now reads `enforce` (CA-j-17 merged), which closes the carried point in this seat's CA-j-5 half.
- **The diff `afa8752f44..0774100edc`** (the live package's code base) over every packaged path and both Terraform folders:
  - packaged: `folder_records.py` (+61, new), `channel_mentions.py` (+23 -2), `mail_requests.py` (+15), and the foreign
    `event_rules.json` (+6);
  - Terraform: `chat_assist.tf` +1 -1, the default `enforce`, equal to the live value, so there is no environment change.

## The records, read in code

- **The mention record** is written in `on_channel_mention` AFTER `ctx.once(... send_sms ...)`. It holds `{id, team, channel, from,
  snippet, mentioned_at, seen_at}`. The snippet is `folder_records.snippet()`: tags stripped (entity-encoded tags too), links,
  `\S+@\S+` and 20-plus-character key-like runs removed, cut to 120. A repeat id writes nothing. It is pruned to 7 days and the newest
  50 on each write. It is not written on the paused path.
- **The mail log** is written only for a mail that passed C-MAIL and was texted (inside the texted branch, after `pending` is set). It
  holds `{seq, tag, considered_at, from, domain, firm, subject}`: `from` is the display name, `domain` is the part after `@` (never the
  address), the subject is scrubbed, and the body is never stored. It is pruned to 7 days and the newest 10.
- **A retry cannot text twice:** `ctx.once` writes its own `once#` row to DynamoDB at the moment of the effect, outside the handler's
  state transaction (`ldo.py:382-396`). So a writer that raises after the text fails the event without repeating the text.
- **The writers' inputs always exist:** `pending["mail"]["firm"]` is always set (`firm or "firm"`, :278); `_ADDR` is defined (:40); an
  absent address is handled (`addr or ""`). A raise in `_log_mail` would leave a texted mail with no saved draft, so this mattered.
  None was found.
- **Tests, run here on a tree equal to the pin for `teams_chat/`:** the records, mail and mention tests read 62 passed.

## SIGNED: blast radius, both branches

**What the act may touch:** the code of the two assistant functions. Nothing else; the mode stays `enforce`.

**What changes for any caller:** nothing visible. Two state keys, `mentions` and `mail_log`, gain metadata entries on the objects that
text a mention or a considered mail. They hold no data class the state does not already hold (a draft's `pending` carries more of the
mail).

- **Branch A** (targeted 0/2/0; `source_code_hash` and `last_modified` only, NEVER `environment`; after-hash equals the clean build of the
  pin): applied.
- **Branch B:** nothing is applied, as the COO half lists. Any pre-state hash other than `/amW90t7...` or a mode other than `enforce`
  voids this half.

**Rollback:** the saved `/amW90t7...` zip from a worktree at `8c5e0b278e`, whose default is `enforce`, NOT from `afa8752f44`, as the COO
half rightly states. No `-var`. The older code ignores the two new keys.

## Carried to CA-j-15 (the dell2 pick-up), not grounds

The snippet scrub is a pattern scrub, not a guarantee. A secret shorter than 20 characters, or one containing characters outside
`[A-Za-z0-9+/_=-]`, survives it. FWD-11's "nothing that would let a reader act as Opal" in the folder is read again when CA-j-15 copies
these records to dell2.

-- 3.0.0_SA_CVO~L
