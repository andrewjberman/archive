# YCD-b-16: the three items the binding's PART 1 left unread, read

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~21:0xZ. Round-16 analysis @1dd909d19d section 3 item 2: "each as a read by the seat
that can make it without a new grant". All three were readable by this seat with its existing read access: two live
`get` reads of one resource each, and one code read. No write, no call to any route, no token used.

## 1. Are the two queue policies applied? YES, both (measured, 21:01Z)

`get-queue-attributes` with `Policy`, one queue per call:

| queue | applied statement | matches the Terraform text |
|---|---|---|
| `outlook-global-commentary-draft-analysis-ready-queue` | Sid `TheResidentSendsAnalysisReady`, Allow, principal `role/irpt-ycharts-runner-role`, action `sqs:SendMessage`, no condition | yes (`transcripts/commentary.tf` lines 139-144) |
| `outlook-global-commentary-draft-commentary-ready-queue` | Sid `TheResidentConsumesCommentaryReady`, Allow, the same principal, actions `sqs:ReceiveMessage`, `sqs:DeleteMessage`, `sqs:GetQueueAttributes`, no condition | yes (lines 176-181) |

Each queue: retention 345,600 s, visibility 1,800 s, redrive to its own dead-letter queue at `maxReceiveCount` 3. So the
resident's role can send to the first and receive and delete on the second, by the queues' own policies. The role's own
policy has no statement for either (PART 1); a same-account queue policy naming the role is what grants it. **Not shown: a
send or a receive by that role.** dell2's agent identity is refused `iam:SimulatePrincipalPolicy`, so the proof by simulate
is the laptop's if the CTO wants it in PART 2; the policy text itself is now measured.

## 2. Which API base passes the authorizer's origin gate? The portal's front door; NOT the gateway's direct address (code)

`infra/aws/users/lambda/portal-authorizer/originVerify.mjs`, `isOriginVerified` (the file's last function): a request is
verified only if it carries the header `x-opal-origin-verify` equal to the current or the previous slot of the secret
`opal/auth/origin-verify`; with no such header it returns false, and the handler denies BEFORE it looks at the token
(`index.mjs` lines 340-350). That header is added by the portal's front door (the distribution), not by a caller. So:

- **`https://opalinvest.dev` (the front door): passes**, the header being added on the way in. Corroborated once: the
  drafter's mint was exercised on 2026-10-09 against host `https://opalinvest.dev` and its arms were answered by the ticket
  service (`org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/tckt_f10/F10-M_arms_result.json`, `host`).
- **The gateway's direct address (`https://7k3ed8px20.execute-api.us-east-1.amazonaws.com`): refused**, by this code, for
  any caller that does not itself hold the origin secret.

**So the packager's `api_base` is `https://opalinvest.dev`.** NOT measured: a refusal at the direct address (I called
nothing), and that the deployed authorizer carries this gate (this is the repo's file).

## 3. The drafter's live settings (measured, 21:01Z; key names, presence, and the three non-secret values)

`outlook-global-commentary-draft-lambda`: State Active, `CodeSha256` `AI4UQD0ME+AB...`, last modified 2026-10-11T05:44:45Z.
One event source mapping, **Enabled**, batch 1, on the analysis-ready queue.

| setting | state |
|---|---|
| `KIMI_STANDING_WORD_REF` | set: `4d77a9c3ea` (so the vendor-word gate is OPEN: the drafter does call the model) |
| `WIPE_GATE_RECORD` | set (92 characters; value not read) |
| `KIMI_API_URL` | `https://api.moonshot.ai/v1/chat/completions` |
| `COMPOSITION_READ_FUNCTION`, `DRAFT_STORE_FUNCTION` | `irpt-commentary-composition-read-lambda`, `irpt-commentary-draft-store-lambda` |
| `COMMENTARY_READY_QUEUE_URL` | set (103 characters, the length of the commentary-ready queue's URL) |
| `TICKET_TOKEN_SECRET_ID` | set (29 characters; a secret NAME, not read) |
| `TICKET_API_BASE` | **`https://7k3ed8px20.execute-api.us-east-1.amazonaws.com`, the gateway's DIRECT address** |

So both of the drafter's own gates are open on the live function: with the resident bound, an `analysis_ready` message
does reach a model call. That is what the ticket and commentary conditions in the worker are for.

## 4. A finding outside the three (row filed)

**The drafter's live `TICKET_API_BASE` is the gateway's direct address, which the origin gate refuses (section 2).** On the
queue path the drafter does not post to the ticket service (it stops at `draft_stored`), so nothing fails today. But the
day the drafter is switched to the ticket's draft route (CTO msg 5830 names that switch as pending), its posts would be
denied at the authorizer before its token is read, unless the base is changed to the front door. It is NFRA_TRNSPT's
setting and TCKT_VNEXT's route; this seat changes neither.

## 5. What PART 2 can now say, and what it still cannot

Can: both queue policies are applied as written; `api_base` is the front door; the drafter's two gates are open and its
model endpoint is named. Cannot yet: anything exercised (no message has travelled the chain on a product path); the simulate
proof of the role's access; the closed-list check on the drafter (not applied); the submission and acceptance half of
`commentary_requested` (not built).
