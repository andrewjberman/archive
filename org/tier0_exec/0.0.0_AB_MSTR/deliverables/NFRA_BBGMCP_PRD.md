# NFRA_BBGMCP — Bloomberg as an MCP surface: tunnel, namespace, endpoint taxonomy

**Status:** DESIGN. Author `0.0.0_AB_MSTR~Z`, 2026-07-30, Andrew-direct at the site-Z terminal.
**Companion:** `NFRA_OPLMCP_PRD.md` (gateway) · `.tools/bloomberg-mcp/README.md` (tunnel provisioning).

> **LOCATION IS DELIBERATE, AND THIS DOC IS NOT YET WHERE IT BELONGS.** It reads as a
> `docs/architecture/NFRA_*` PRD and should eventually live there — but that path is
> `lane=ANY_CTO` under `.owned-paths.yaml` and the pre-commit hook correctly refused an
> `0.0.0_AB_MSTR~Z` commit into it. **Rather than take an audited override to write into
> another lane's territory** — which is the drift the gate exists to prevent — it lands in
> MSTR's own deliverables. **Promotion to `docs/architecture/NFRA_BBGMCP_PRD.md` is a CTO
> action**, and until it happens, cite this path, not that one.

Everything marked **MEASURED** was exercised on this device 2026-07-30. Everything else is
proposal. The distinction is deliberate — an earlier draft of the client's own docstring
asserted a prerequisite that measurement disproved, and that is the failure this section header
exists to prevent.

---

## 1. What is true today (MEASURED)

| Fact | Evidence |
|---|---|
| DAPI serves with the **Terminal GUI closed and the user logged out** | `wintrv` exited, Bloomberg processes 25 -> 1, `bbcomm` held `127.0.0.1:8194`, live data kept flowing (USDCAD ticked 1.4009 -> 1.4011 across the logout) |
| The dependency is **`bbcomm`**, not the GUI, not an interactive login | same test; `bbcomm` PID unchanged throughout |
| DAPI binds **loopback only** | `Get-NetTCPConnection 8194` -> `127.0.0.1`, never `0.0.0.0` |
| **`//blp/emsx` does not exist on this seat** | `openService("//blp/emsx")` -> `False`, `"The request schema or service doesn't exist"` |
| Bulk/BDS fields now work | `INDX_MEMBERS` -> 503 rows; `DVD_HIST` -> 93 rows x 7 cols (`f7bb8abd0`) |

**NOT established, deliberately untested** (Andrew 2026-07-30 — signing in is cheap): whether
`bbcomm` comes up entitled from a **cold boot with no login at all**. *"Survives logout"* and
*"never needs a login"* are different claims and only the first is proven. **Any scheduler built
on this must surface a dead DAPI explicitly rather than assume one.**

> **THE READ-ONLY PROPERTY IS AN ENTITLEMENT FACT, NOT A CODE CONVENTION.** `blp_client` opens
> only `//blp/refdata` by design — but the order/trade service is *not reachable from this seat
> at all*. That is a structural guarantee underneath the design one. **Do not weaken the code
> convention on the strength of it** (a seat's entitlements can change and nothing would tell
> us), but do record that today the blast radius of a client bug is bounded by Bloomberg, not
> only by our own restraint.

---

## 2. Tunnel — already designed; execute, do not redesign

Specified in `.tools/bloomberg-mcp/README.md` §"AWS-native reachability", aligned to
`NFRA_OPLMCP_PRD.md`, which selects **SSM port-forward** as the estate's blessed path and
explicitly rejects Cloudflare/Tailscale.

```
[Terminal] --127.0.0.1:8194--> [blp_client] --> [server.py streamable-http 127.0.0.1:8790]
                                                              ^ SSM port-forward, outbound-registered
[Opal gateway / EC2] --aws ssm start-session--> [this box as mi-... managed instance]
```

**Why the tunnel must terminate locally, and it is not a preference:** DAPI binds `127.0.0.1`.
No VPN, peering, or security-group change can reach it. Something on this box must make the
blpapi call. Every design that forgets this fails at the same place.

**Gates — MEASURED 2026-07-30, re-measured independently by `0.7.0_AE_CloudOps~Z` the same day.
EXECUTION ORDER IS NOT TABLE ORDER; see the two corrections below.**

| # | Gate | State | Order |
|---|---|---|---|
| 1 | AWS creds for this device | **SATISFIED** — `sts get-caller-identity` -> `user/Andrew_Berman`, acct `313476888478`, rc=0 (control: bogus profile errors loudly) | done |
| 4 | IAM role + **`aws_ssm_activation`**, scoped | open — CloudOps | **FIRST** |
| 2 | SSM Agent MSI installed (one-time admin, **Andrew**) | **NOT INSTALLED** | **after 4** |
| 3 | `server.py` `streamable-http` on `:8790` as a service | **NOT LISTENING** | after 2 |
| 5 | Register forwarded endpoint as a gateway backend | open | **after the §3 rename** |

> **CORRECTION 1 — GATE 4 PRECEDES GATE 2, and it is a hard dependency, not a preference.**
> An SSM **hybrid activation is created in AWS first** and emits an activation **code + id**; the
> MSI install then **consumes those as registration inputs**. Working the table order would idle
> Andrew on an admin step that has no inputs yet. Gate 4 first puts the code+id in his hands as
> **one self-contained admin action**. *(Raised by `0.7.0_AE_CloudOps~Z` against this document's
> original ordering; the original table listed 1-5 and implied that sequence.)*
>
> **CORRECTION 2 — GATE 5 MUST FOLLOW THE §3 RENAME.** §6 already sequences *Bloomberg-as-
> IntegrationSpec* after the rename, but gate 5 was written free-standing. **If gate 5 lands
> first, Bloomberg registers under the `m365` namespace and the client-re-registration break is
> paid TWICE** — once for Bloomberg, again for the rename. That is exactly the
> `mcp__m365__bloomberg_reference_data` outcome §3 exists to prevent, **arriving through the
> tunnel half instead of the naming half.** Ordering rename -> gate 5 pays it once.
>
> **Gate 1 was recorded here as "in flight" on the strength of the 07-10 README and was ALREADY
> SATISFIED.** It is the gate that makes gate 4 actionable at all, so a stale "in flight" would
> have read as a blocker on the critical path. *Inheriting a gate state instead of measuring it
> is the same class as every other stale-record finding in this file.*

DAPI **redistribution was cleared by Andrew 2026-07-10** (per that README), so multi-user
exposure is authorized and is not a gate.

---

## 3. Namespace — the gateway is misnamed; the integrations are fine

**FINDING, and it inverts the obvious remedy: YCharts is ALREADY properly split.**
`app/integrations/ycharts/integration.py` is a self-contained `IntegrationSpec` — own id,
`tool_prefix="ycharts_"`, own `secret_id`, `read_only=True`, `min_tier` compartmentalized to the
write-capable roster (Andrew-ruled 2026-07-01), own egress allowlist — registered via
`integrations.register_enabled(mcp, ENABLED_INTEGRATIONS)`, opt-in, defaulting to empty so
shipping integration code does not expose it. **That is the pluggable-backend architecture, and
it already exists.**

**The defect is one line** — `app/tools.py:37`:

```python
mcp = FastMCP("m365-gateway", ...)
```

A multi-vendor gateway wearing a single-vendor name. Tools are correctly prefixed; the *server*
is not, so every integration inherits `m365` as its namespace. `opal_portal` already suffers it.
**Bloomberg would land as `mcp__m365__bloomberg_reference_data`.**

**PROPOSED: rename the server identity to a vendor-neutral `opal-gateway`**, demoting m365 to an
integration alongside ycharts, opal_portal and bloomberg.

- **Do NOT fork a separate ycharts/bloomberg MCP server.** The gateway carries OAuth, guard,
  entitlements, blocklist, ratelimit, revocation, OTP and the `s3://opal-mcp-audit` lake. A
  second server duplicates or forks all of it. **One gateway, many integrations** is right;
  the name is what is wrong.
- **Migration cost, MEASURED:** 10 files reference `mcp__m365__`; **1** references
  `mcp__m365__ycharts_*`. Most of the remainder are historical session logs, which are records
  and **must not be rewritten**. Live surfaces: `.claude/skills/teams-assist/SKILL.md` and the
  gateway's own `audit.py`.
- ~~**Blast radius:** the server name is the client-visible namespace. Every registered client
  needs re-registration; until it happens, tool references break.~~ **STRUCK — FALSE. See the
  correction block below.** The deploy-path discipline still stands: it goes through
  `safe-ec2-deploy.sh` + `EC2_MANIFEST.json`, never an inline edit.

> ### ⛔ CORRECTION (2026-07-30) — THE SERVER RENAME DOES NOT CHANGE THE CLIENT-VISIBLE NAMESPACE
>
> **The struck sentence above is wrong and it was load-bearing** — it sized the whole sequencing
> caution, and Andrew approved a rename on it believing the rename fixed the namespace.
>
> **The client-visible prefix comes from the REGISTRATION KEY, not the server's `FastMCP()` name.**
> The gateway is the estate's only case where the two differ, which makes it the oracle:
>
> | | |
> |---|---|
> | server self-name (`tools.py:37`) | `FastMCP("m365-gateway")` |
> | registration key (`~/.claude.json`) | `m365` |
> | tool names actually held | `mcp__m365__whoami` — matches the **key**, not the name |
>
> **The competing explanation, and it had to be killed** *(raised and closed by
> `0.7.0_AE_CloudOps~Z`; my first proof did not close it)*: that `m365-gateway` is **truncated at
> the hyphen** to `m365`, which would make the server name the source and invert the conclusion.
> **Refuted by hyphen survival** — key `opal-agent-comms` yields `mcp__opal-agent-comms__*`, hyphens
> verbatim. A hyphenated key does not collapse, so `m365` cannot be a truncation. Three keys, three
> exact matches, zero server-name matches, **no surviving alternative.**
>
> **CONSEQUENCES, both directions:**
> 1. The server rename is **harmless** — no client breaks, no sweep needed.
> 2. The server rename is also **cosmetic** — Bloomberg would *still* land as
>    `mcp__m365__bloomberg_reference_data`. **Shipping only that line is a green deploy that changes
>    nothing an agent can see**, i.e. a config-read standing in for a behavioural result.
> 3. **The real fix is the CLIENT KEY** (`m365` -> `opal`).
>
> **TRUE BREAKAGE SURFACE — MEASURED, and far smaller than this document first implied: 2 lines,
> 1 file.** Only full `mcp__m365__` literals break; bare tool names are unchanged by a key move.
> - `teams-assist/SKILL.md:44,47` (`list_chats`, `read_chat_messages`) — **the entire estate-wide set**
> - `tax-pt1` (Alyssa's daily FIS runner): **0** `mcp__`-prefixed refs — uses bare
>   `validate_ssavail_attachment` / `save_email_attachment_to_site`. **UNAFFECTED.** Same for
>   `taxsma-step1`, `tax-pt3`. *An earlier count in this session cited "5 m365-tool refs" in tax-pt1
>   and implied risk; those are bare names and a key change does not touch them.*
>
> **WHO CAN DO IT — a constraint neither the tunnel nor the rename section had stated
> (`0.7.0_AE_CloudOps~Z`): the registration key lives in PER-DEVICE CLIENT CONFIG.** It is **not a
> deploy**. Site Z cannot reach the laptop's or Alyssa's `~/.claude.json`, and on Alyssa's machine it
> is **not ours to change unilaterally**. This moves the work from CloudOps' deploy lane to a
> per-device action requiring the device owner — a different *who*, not just a different *what*.

Owner: **CloudOps.** Sequencing options: (a) server rename + redeploy + client sweep, or (b)
client-side re-registration on one device first to prove the shape, then the fleet.

---

## 4. Endpoint taxonomy — the deterministic paths

**The problem this solves:** an agent that must *guess* a ticker or a field mnemonic will guess
wrong, and Bloomberg's failure mode is quiet — an unknown field is simply absent from the
response, not an error. `reference_data` today omits unknown fields silently
(`blp_client.py`, the `if fd.hasElement(f)` filter). **A hallucinated mnemonic returns a
successful-looking response with a missing key.**

**The cure is Bloomberg's own discovery services, and both are MEASURED reachable on this seat.**

### 4.1 Two-phase contract: DISCOVER -> FETCH

```
DISCOVER  resolve_security("Apple")        -> "AAPL US Equity"      //blp/instruments
          search_fields("dividend yield")  -> ["EQY_DVD_YLD_IND",…]  //blp/apiflds
                              |
FETCH     reference_data / historical_data / intraday_bars           //blp/refdata
          (only ever receives resolved identifiers + validated mnemonics)
```

Discovery calls are cheap, read-only, and make the fetch deterministic. **An agent should never
be the source of a field mnemonic.**

### 4.2 Service map (all MEASURED via `openService`)

| Service | Open? | Use | Status |
|---|---|---|---|
| `//blp/refdata` | **True** | BDP / BDH / BDS / IntradayBar / IntradayTick / BEQS / Portfolio | partly built |
| `//blp/apiflds` | **True** | field discovery + metadata | **PROPOSED — highest value** |
| `//blp/instruments` | **True** | security/curve/govt resolution | **PROPOSED** |
| `//blp/tasvc` | **True** | technical analysis studies | deferred, no demand yet |
| `//blp/mktdata` | **True** | streaming subscriptions | **EXCLUDE — see 4.4** |
| `//blp/emsx` | **False** | order/trade | **NEVER. Not reachable, and never to be opened.** |

### 4.3 Tool roster

**Built (`f7bb8abd0`):** `bloomberg_health`, `bloomberg_reference_data` (BDP **and BDS**),
`bloomberg_historical_data`, `bloomberg_intraday_bars`.

**Proposed, in value order:**

| Tool | Service / request | Why |
|---|---|---|
| `bloomberg_search_fields(query)` | `apiflds` FieldSearch | kills mnemonic guessing — the determinism keystone |
| `bloomberg_field_info(mnemonics)` | `apiflds` FieldInfo | datatype + whether a field is BULK, so callers know the return shape |
| `bloomberg_resolve_security(query)` | `instruments` instrumentList | "Apple" / an ISIN / a CUSIP -> a Bloomberg identifier |
| `bloomberg_portfolio_data(portfolio)` | `refdata` PortfolioDataRequest | PORT holdings — directly serves model-portfolio work |
| `bloomberg_screen(name)` | `refdata` BeqsRequest | run saved EQS screens |
| `bloomberg_intraday_ticks(...)` | `refdata` IntradayTick | the docstring once claimed this existed; it never did |

### 4.4 Deliberate exclusions — stated, not merely absent

- **`//blp/mktdata` streaming.** A subscription is long-lived and push-shaped; MCP tool calls are
  request/response. It would need a different surface (a local collector writing to S3/DynamoDB,
  polled separately). **Excluded by design, not overlooked.**
- **`//blp/emsx` and any order/trade path.** Not reachable today (§1) and must never be opened.
  A gateway-side denylist on the tool prefix is the cheap belt to the code's suspenders.

---

## 5. Operational constraints

- **Session-per-request.** `blp_client` opens and stops a session per call — its own docstring
  calls pooling "a later optimization; correctness first." Correct then; **the tunnel makes it
  due.** Under concurrent gateway callers, a full session handshake per request is the first
  bottleneck.
- **DAPI request limits.** Terminal DAPI carries daily hit and concurrency limits. EC2 fan-out
  can exhaust a limit that a human at a terminal never approaches. **Rate-limit at the gateway,
  where the limiter already exists (`ratelimit.py`), not in the client.**
- **Single point of failure.** One box, one seat. The gateway must report BBG-unavailable
  explicitly — *silence is not a pass.* Prefer a stale-but-labelled answer over an empty one.
- **Attribution.** Calls run under a named human's seat. Anything scheduled or production-facing
  should be a deliberate decision, not a side effect of the tunnel existing.

---

## 6. Gates and ownership

| Item | Owner | State |
|---|---|---|
| Bulk/BDS serializer fix | `0.0.0_AB_MSTR~Z` | **DONE** `f7bb8abd0` |
| MCP committed to git (was untracked) | `0.0.0_AB_MSTR~Z` | **DONE** `f7bb8abd0` |
| SSM Agent MSI + hybrid activation + IAM | **CloudOps** | open (admin once) |
| `server.py` http mode as a service on `:8790` | **CloudOps** | open |
| Gateway rename `m365-gateway` -> `opal-gateway` + client sweep | **CloudOps** | open, **Andrew-approved 2026-07-30** |
| Discovery tools (`search_fields`, `field_info`, `resolve_security`) | unassigned | proposed |
| Bloomberg as a gateway `IntegrationSpec` | unassigned | proposed, follows the rename |
