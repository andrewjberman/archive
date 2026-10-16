# ANDREW_DIRECT 2026-10-16 ~03:3xZ-03:4xZ -- /fideles skill: the fabric mails muse; dell1 MSTR owns the watcher

Channel: the laptop `2.0.0_SA_COO~CA` terminal. Recorded by 2.0.0_SA_COO~CA, same turn.

## His words, VERBATIM

First (~03:3xZ):

> i want to create a skill called /fideles. the premise is that the fabric is andrew@fideles.capital, it uses gmail mcp to
> email andrew@goldengate.dev (which is muse), this is a clean communication channel, as I own both emails. The question then
> becomes what agent runs the /fideles watcher so that there is no race condition in response.

Then, answering 2.0.0_SA_COO~CA's recommendation of one dedicated MSTR lane (~03:4xZ):

> Dell1 MSTR should do it. we use DELL1 as the primary operator for muse. If Dell1 is down, Dell2 takes it. Both dells should
> maintain the muse folder on their box.

## What it settles

1. A skill `/fideles` is created. The fabric's mailbox is `andrew@fideles.capital`; muse's mailbox is `andrew@goldengate.dev`;
   the transport is the Gmail MCP connector. Andrew owns both mailboxes.
2. The ONE reader of the fabric's mailbox (the `/fideles` watcher) is `0.0.0_AB_MSTR~DELL1`. When dell1 is down,
   `0.0.0_AB_MSTR~DELL2` takes it. Never both at once.
3. dell1 is the primary operator box for muse.
4. BOTH dells keep the muse folder on their own box (today the folder `muse-reader` lives on dell2 only).

## Who acts

- 2.0.0_SA_COO~CA drafts the skill file `.claude/skills/fideles/SKILL.md` (this turn).
- Item 4 changes the dell1 and dell2 seats' work (the COMM_ASSIST reader folder). Surfaced to `1.0.0_SA_CTO` by one line naming
  this record; this seat does not adjudicate its scope.
