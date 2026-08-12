# BRIEF — RENDERING THE GATEWAY CANONICAL (`m365-mcp-gateway` -> `opal-gateway`) + THE ANALYST-DEVICE ROLLOUT PACK

**Commissioned:** Andrew-direct 2026-08-12 ~1450Z at the MSTR terminal, VERBATIM: *"write a
brief on how we need to adjust this to render it canonical, as well as what information will
need to be transferred to the opal analysts so their agents can update their devices. then
send this to CTO."*
**Author:** `0.0.0_AB_MSTR` · **Addressee:** `1.0.0_SA_CTO` (arch gate + routing owner)
**Status:** BRIEF FOR CTO ROUTING. Nothing renamed, nothing dispatched, no gate proposed.
**Grounding:** every figure below is measured this session (comp-find census with denominators
+ live AWS primitives), not recalled. Citations inline.

---

## 1 · THE FACT, STATED PLAINLY

**The client-facing name is already canonical. The server side never followed.**

| plane | name today | canonical? |
|---|---|---|
| MCP server key agents register | `opal-gateway` | ✅ yes |
| Tool namespace agents call | `mcp__opal-gateway__*` | ✅ yes |
| URL | `https://mcp.opalinvest.dev/mcp/` | ✅ yes (opalinvest.dev, the owned domain) |
| Repo service dir | `infra/aws/ec2/m365-mcp-gateway/` | ❌ |
| Terraform dir | `infra/aws/terraform/m365-mcp-gateway/` | ❌ |
| EC2 manifest service key | `m365-mcp-gateway` | ❌ |
| EC2 Name tag (`i-07dccb1615503ac99`) | `m365-mcp-gateway` | ❌ *(live-verified)* |
| IAM role / instance profile | `m365-mcp-gateway-role` / `-profile` | ❌ *(live-verified)* |
| ALB + SGs | `m365-mcp-gateway`, `-alb-sg`, `-sg` | ❌ *(live-verified)* |
| Secrets | `opal/mcp/m365-{login,graph,fernet,gateway-jwt}` | ❌ *(live-verified)* |
| Remote path on the box | `/opt/m365-mcp-gateway` | ❌ |
| systemd unit | `deploy/m365-mcp-gateway.service` | ❌ |
| Project code | `NFRA_OPLMCP` | ✅ already de-branded |

**AND THE NAME IS NOW MATERIALLY WRONG, NOT MERELY DATED.** The service's own
`app/integrations/` carries **`opal_portal`** and **`ycharts`** beside the Microsoft layer, and
its live tool surface spans email, Teams, SharePoint/OneDrive, workbooks, YCharts, and the
data-refresh upload. "M365" describes what it was at architecture-lock (2026-06-10), not what
it serves. A future reader looking for the YCharts or portal path will not look in a folder
called m365.

**CENSUS DENOMINATOR (comp-find, this session):** `m365-mcp-gateway` returns **2,037 hits
across 25,574 files scanned** — bands HEAD 747 / CONFIG 642 / SURFACED 345 / DOC 295 / DEF 5 /
TEST 3. **That number is the brief's central fact: this is not a directory move.**

---

## 2 · HOW TO RENDER IT CANONICAL — the shape, not the schedule

⛔ **THE ONE THING NOT TO DO: a repo-wide find-and-replace.** 2,037 hits are overwhelmingly
HISTORY — deploy-completion ledgers, PRDs, incident records, closed change-management entries.
Rewriting those falsifies the record (the deploy at 20260623T1731Z genuinely deployed a thing
called `m365-mcp-gateway`), and it is the accretion-by-rewrite class the estate already
legislates against. **History keeps its names; the LIVE surfaces get renamed; the record gets
one supersession pointer.**

### The four planes, in dependency order (each is its own act)

**PLANE A — AWS RESOURCES (irreversible-adjacent; Terraform-owned).** ALB, target group,
SGs, IAM role + instance profile, EC2 Name tag, Secrets Manager entries. Two honest facts:
(i) IAM role rename is a **create-new + repoint + delete-old**, not an edit, and the instance
profile is attached to a running box that all employee M365 traffic flows through;
(ii) **secret NAMES are referenced by the app's own config** — renaming a secret without the
app change is an outage, and the reverse order is a dangling reference. This plane is where a
rename can take the gateway down, so it is the plane that decides whether the whole thing is
worth doing. **CTO's call, and the honest option is to leave Plane A alone** (see §4).

**PLANE B — REPO PATHS + MANIFEST (mechanical, gated).** `infra/aws/ec2/m365-mcp-gateway/` ->
`opal-gateway/`, the Terraform dir likewise, `EC2_MANIFEST.json` service key +
`source_path` + `remote_path` + `deploy_script` + `iam_role`. **Rule 8: the manifest is the
source of truth and CI/CD depends on it** — the manifest edit and the path move are ONE atomic
commit or CI breaks between them. `deploy-to-ec2.sh` and the systemd unit name follow.

**PLANE C — THE BOX (`/opt/m365-mcp-gateway`).** Path + unit rename on a live instance. Rule 7
(`safe-ec2-deploy.sh`, never a service-specific script) and Rule 12 (S3 is the artifact store;
never write code on a VM) both bind. This is a deploy with a rollback, not an edit.

**PLANE D — DOCS + LAW POINTERS (free, do this regardless).** README title, PRD/runbook
headers, and — the load-bearing one — **a single supersession note** at the canonical home
stating: *the service formerly named m365-mcp-gateway is the opal-gateway; historical records
retain the old name by design.* One pointer beats 2,037 rewrites, and it is what makes the
history readable rather than wrong.

### The ordering constraint that decides everything
**Client-side is ALREADY canonical, so there is no user-visible urgency and no cutover
window.** That is the good news and also the argument for doing this deliberately: nobody is
blocked, so it can be sequenced behind the P1/P2 build waves rather than jammed beside them.

---

## 3 · WHAT THE OPAL ANALYSTS NEED — the device rollout pack

**THE HEADLINE FOR THEM: NOTHING IN §2 CHANGES ANYTHING ON AN ANALYST DEVICE.** The rename is
server-side; the client registration (`opal-gateway`, `https://mcp.opalinvest.dev/mcp/`) is
already the canonical form and does not move. **Any rollout note must open with that sentence**,
or an analyst will assume their config is about to break and pre-emptively "fix" a working one.

What their agents actually need to have on a device, stated as the pack CTO would hand over:

1. **The registration block, verbatim** (this is the whole client config):
   ```json
   "opal-gateway": { "type": "http", "url": "https://mcp.opalinvest.dev/mcp/" }
   ```
   Home: the repo-root `.claude/settings.json` (or the device's Claude config). Already
   shipping in `agent_org_blueprint_v3.zip` -> `templates/claude_settings.json`.
2. **The auth step, and that it is per-device and one-time**: first use opens a browser OAuth
   prompt (Entra, per-user delegated). Tools appear as `mcp__opal-gateway__*` after a reload.
   **The per-user delegation is the point** — Microsoft still enforces that each analyst sees
   only their own mail/files/sites; the gateway does not broaden anyone's access.
3. **What they get**: email/Teams/SharePoint/OneDrive/workbook reads + sends, YCharts, and the
   data-refresh upload — one server, no local install, no credentials on the device.
4. **The standing law that does NOT relax**: availability is not authorization —
   **`ycharts_*` and every other vendor call stays HELD pending Andrew's per-use word**, and the
   gateway being reachable is not a grant. (CLAUDE.md Agent Autonomy; the 2026-07-09 incident.)
5. **The one operational caveat**: interactively-authenticated MCP servers may be absent in
   headless/cron runs — an agent scheduled without a session cannot assume the gateway is there.
6. **Where to look when it misbehaves**: the audit lake + the gateway's own `audit.jsonl`; the
   governing PRD is `docs/architecture/NFRA_OPLMCP_PRD.md` (project `NFRA_OPLMCP`).

**FORM OF THE HANDOVER (recommendation, CTO's to accept or reshape):** ONE onboarding page —
registration block, auth step, tool inventory, the two standing constraints — living beside the
PRD, plus the blueprint zip's template as the executable copy. **Not a rename announcement.**

---

## 4 · THE HONEST OPTION SET (my read; the call is CTO's, and the cost side is real)

| option | what it costs | what it buys |
|---|---|---|
| **(1) Docs + supersession pointer only** (Plane D) | ~an hour, zero risk | the folder stops misdescribing itself to the next reader; history stays true |
| **(2) D + repo/manifest rename** (Planes B+D) | one atomic gated commit + a CI-verified deploy; touches a live serve chain's deploy path | the repo reads canonically; AWS still says m365 |
| **(3) Full rename incl. AWS + box** (A+B+C+D) | an IAM create/repoint/delete on a live instance, a secrets-name migration ordered against the app config, an ALB/SG rename, a deploy with rollback — on the box **all employee M365 traffic** flows through | complete canonical alignment |

**MY RECOMMENDATION, offered as input not a decision: (1) now, (2) sequenced behind the P1/P2
waves, (3) NOT unless a second reason appears.** Rationale: the only measured harm today is
*discoverability* — a reader hunting the YCharts or portal integration will not look in an
"m365" folder — and Plane D fixes exactly that for an hour of work. Plane A's blast radius is
the entire firm's M365 path, spent purchasing a cosmetic property on a service whose USER-FACING
name is already correct. **A rename that can take the gateway down is not obviously worth a
better folder name.** If Andrew wants full alignment anyway, that is his call and (3) is
executable — but it should be chosen with that trade stated, not slid into via (2).

---

## 5 · WHAT I AM NOT DOING
No rename executed, no TO authored, no gate proposed, no dispatch. This is a brief to the arch
gate. **Routing, sequencing, and the option choice are CTO's** (with Andrew's word on (3) if it
is ever selected, since it touches a live client-serving path).
