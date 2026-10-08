# COMM_ASSIST -- registration draft for 1.0.0_SA_CTO's L3 (2.0.0_SA_COO~R, 2026-10-08 ~23:4xZ)

**Asked by:** `1.0.0_SA_CTO` msg 107477, ask (2): "draft the COMM project's registry row and tree (code COMM_ASSIST unless you have
a better name) carrying INBOUND's PRD outcomes, for my L3 registration; until it lands, keep working under NFRA_CTLPLN."
**Macro:** COMM, D9, ratified `0dcb083716` (Andrew-direct ~19:2xZ "2.) Yes agreed."). **This file writes no carrier**: the
tree row, `project.json`, the generated index, the `DIRECTIVES.yaml` members line and the PRD are the CTO's at L3/L4 (CLAUDE.md
rule 27).

## The name

`COMM_ASSIST`, kept. It fits the project grammar `^[A-Z]{4}_[A-Z0-9]{3,18}$`. Census `comp-find 'COMM_ASSIST' --band DEF`,
2026-10-08 ~23:4xZ: 3 hits across 236,720 files [corpus=all], DEF 0 (SURFACED 2, DOC 1: the CTO's message and its copies), no
collision. One project covers what Andrew named for the macro: the Teams and Outlook assistant ("Kimmy"), how it reaches him,
and its queues. No better name.

## Tree (the contract's project folder, `org/standards/PROJECT_TREE.contract.json`)

```
org/missions/D9/COMM/COMM_ASSIST/
  project.json
  STATUS.md
  prd/COMM_ASSIST_PRD.md
  decompositions/
  task-orders/
  deliverables/
  surprise-channel/investigations/INVESTIGATION_v1.md
```

## `project.json`, drafted

```json
{
  "project_code": "COMM_ASSIST",
  "macro_code": "COMM",
  "directive": "D9",
  "fabric": "laptop",
  "placement": "LAPTOP",
  "pipeline": null,
  "status": "active",
  "dep_stage": "EXECUTING",
  "created": "2026-10-08",
  "registered_under_tree": "<the L3 commit's date>",
  "pods": [],
  "related": ["NFRA_CTLPLN", "NFRA_OPLGTW", "NFRA_TRNSPT", "LGIC_NAMING"],
  "name": "Andrew's Teams and Outlook assistant: every message addressed to him reaches his phone, drafted in his voice, answered by text",
  "description": "The LDO-001 assistant (two Lambdas, teams-global-chat-assist-ingress-lambda and -handler-lambda, module ldo_001 of infra/aws/terraform/transcripts) reads Andrew's Teams chats and channel @mentions through the Opal gateway, and his mail from the five firms when its body names him; it texts him each item with a draft written from andrew_voice.md, routes his reply (#1 send, #0 drop, notes to redraft, #dev to open a job), drafts and posts the End of Day update, and counts what was received against what was texted. Nothing goes out in his name without his 1; no mail is sent, only drafted.",
  "brief_ref": "docs/briefs/nfra-ctlpln-seat-roles-and-inbound-work-pipeline-brief-20261007.md@779f5428bc (Parts I, II, III, V; INBOUND's share)",
  "andrew_direct_ref": "org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_184xZ_FIVE_POINTS_KIMMY_EFFICIENCY_ALYSSA_MCPORTAL_OPEN_CALLS_AGGREGATE.md (point 1 and the ~19:2xZ addendum)",
  "prds": ["org/missions/D9/COMM/COMM_ASSIST/prd/COMM_ASSIST_PRD.md"],
  "leads": {"cto": "1.0.0_SA_CTO", "coo": "2.0.0_SA_COO", "cvo": "3.0.0_SA_CVO", "cro": "4.0.0_SA_CRO"},
  "coo_lane": "2.0.0_SA_COO~R",
  "workstreams": null,
  "carried_from": "NFRA_CTLPLN workstream INBOUND, rounds 1-7 (decompositions inbound2..inbound7, orders TO-CT-i-1..13, TO-APPLY-11/19/20); history stays in NFRA_CTLPLN's tree",
  "blocking": null,
  "last_updated": "2026-10-08"
}
```

**Placement:** LAPTOP. D9 is LAPTOP as a whole (DIRECTIVES.yaml, 2026-09-10). The assistant's root and its applier are on the
laptop, and the COO lane `~R` is seated there. Its two inputs on site Z (NFRA_OPLGTW's gateway routes and mail admission) are
dependencies, not placement.

## Outcomes the PRD carries over (cited, not rewritten; the CTO writes the PRD at L4)

| new id | from NFRA_CTLPLN PRD | what it is |
|---|---|---|
| FWD-1 | FWD-20 (v0.17; ACCEPT at v0.17-v0.19) | someone at Opal asks for work in a message; Andrew gets one text with a recommendation; a fresh seat does it; a reviewer grades it; the requester is told. **The thread.** |
| FWD-2 | FWD-26 (v0.19) | anything an agent writes in his name is written from one voice file (`andrew_voice.md`) of his own messages by kind of act |
| FWD-3 (proposed, his words of 2026-10-08 point 1) | none yet: today it is FWD-20's enrichment | **every** Teams message and channel @mention addressed to him reaches his phone, and the received-vs-texted count proves it per day. DONE WHEN: one full day whose count reconciles (texts sent = chat outcomes texted or updated; 0 unexplained; 0 silent refusals). This is the read the CTO set for 2026-10-09 ~22:00Z (msg 107436) |
| FWD-4 (proposed) | C-SEATS clause 9 (v0.18) | his mail from the five firms reaches him by the same text path when the body names "Andrew", client senders flagged. Andrew-direct ~22:5xZ: "No it always has to say andrew in the body text somewhere, otherwise i dont care" (`c0a11edcc8`) |

Contracts carried: C-SEATS clauses 8 (an inbound job is done by a fresh seat briefed from a file; the requester is told), 9 (mail)
and 10 (the voice file). FWD-3 and FWD-4 are proposals: an ENDPOINT is the CTO's and Andrew confirms DONE WHEN (spine L2).

## Write surface (for `.owned-paths.yaml` and the placement check)

- `data/transcripts/scripts/teams_chat/` (the assistant's code) and its tests `data/transcripts/scripts/tests/test_inbound_*.py`,
  `test_teams_chat_*.py`.
- `infra/aws/lambda/teams-chat-assist/` (handlers, build).
- `module.ldo_001` in `infra/aws/terraform/transcripts/chat_assist.tf`. **Overlap, stated:** the root is shared with
  NFRA_TRNSPT (dell2-placed); every COMM apply is targeted at `module.ldo_001` and names the overlap.
- Bucket `opal-data-transcripts`: `teams/transcripts/bronze/chat_messages/`, `.../silver/chat_threads/`,
  `.../state/chat_assist/` (writer declaration `f3170c6f94`).
- **Read, not owned:** `daily_reports/eod/post_format.py`, `VOICE.md` (End of Day shape), `infra/aws/terraform/modules/ldo/`
  (the runtime), `infra/aws/ec2/opal-gateway/app/teams_route.py` (NFRA_OPLGTW's; round 6's routes there ship with its release).

## State at handover

Rounds 6 and 7 are live (21:48Z and 22:32Z), APPLIED and not EXERCISED. Reviewer packet `ac72c4949f`. Open: the 2026-10-09
full-day read; the gateway release (site Z); mail admission (site Z, NFRA_OPLGTW OG-md-1 BUILT AND HELD `15b08fdca1`).
Rows S33 and S34 are disarmed in code and wait on that read.
