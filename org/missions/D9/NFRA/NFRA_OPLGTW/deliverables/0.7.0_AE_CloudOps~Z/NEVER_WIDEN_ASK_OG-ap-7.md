# Never-widen ask -- OG-ap-7: the NFRA_CTLPLN CT-i-11 `/hx/teams/*` channel-read release

By: `0.7.0_AE_CloudOps~Z`, 2026-10-11. Halves owed: `1.0.0_SA_CTO~Z` (the gateway's CTO) and
`2.0.0_SA_COO~O` (the issuer). The laptop CTO's ruling @de13ed0e00 term 2 states no laptop half is
owed; its Addendum 1 @4f285abe22 extends consent to the build tip `4d722ff458`.

- **Base (the live ref):** `c3af8687e44a1e641259b37f992033ae02cdce3d`
- **Release:** `28ba9532b648061cecafe426836d3e96af4529cd` on `rel-nfra-oplgtw-cti11`, worktree
  `C:/tmp/og-rel-cti11`. Never merged into `box/sitez`.
- **Nothing is deployed.** B1 is re-cut, prove and ask.

## 0. The live ref is established by CONTENT, not by a label

One SSM read of the host's shipped files against `c3af8687e4`'s blobs: **`MD5 listed 106 identical
106 mismatch 0 []`**. The host therefore runs exactly that commit's shipped bytes. The generating
method was controlled first -- it reproduced this seat's own OG-ap-6 base list **104 of 104** at
`2a5966dfbd` -- so an eol or `.gitattributes` shift since that order would have been caught rather
than silently moving every hash.

**Host superset, every extra named** (step 1): **7** files, all under `dashboard/` --
`index.html`, the 2 assets `index.html` references (`index-BTe-mgyF.css`, `index-CKTlb93s.js`), and
**4 orphans** (`index-BP6X9XJd.js`, `index-BqfQgt7G.css`, `index-CrZMj-00.js`,
`index-a6wjv_wv.css`). The set is UNCHANGED from this seat's OG-ap-6 read-back, so the mcportal
bundle has not moved since. The orphans are row `NFRA_OPLGTW-Z-S82`, already adopted into OG-ap-6's
step 8 by its AMENDMENT 1.

## 1. The diff, by file

| file | +/- | what |
|---|---|---|
| `app/server.py` | +4 / -0 | three `Route(...)` registrations, and nothing else |
| `app/teams_route.py` | +70 / -5 | the three route constants and their endpoints |
| `tests/test_teams_route.py` | +151 / -4 | CT-i-11's own tests |

Three files, 0 paths outside `infra/aws/ec2/opal-gateway/`. `ap7.AC1` reads
`patch-id built=37fa4995232e release=37fa4995232e equal=yes`, which reproduces the issuer's
recorded positive control exactly.

**"Ships as built" verified per file, by content.** The order's own command is a HUNK apply onto
the live ref, not a whole-file take, so the phrase means CT-i-11's hunks ship as built:

- `app/teams_route.py` -- sha256 **EQUAL** to the tree at `4d722ff458`
- `tests/test_teams_route.py` -- sha256 **EQUAL** to the tree at `4d722ff458`
- `app/server.py` -- **DIFFERS** from `4d722ff458`, and that is CORRECT: `server.py` moved on trunk
  between the build and the live ref, so taking the build's whole file would have REVERTED unrelated
  trunk work in it. What matters is the delta against the LIVE ref, and it is exactly CT-i-11's own
  hunk: **4 insertions, 0 deletions**, the four added `Route(...)` lines byte-identical to CT-i-11's
  `server.py` hunk. Nothing else rode in. Negative control: `app/tools.py`, which CT-i-11 does not
  touch, reads EQUAL to the live ref.

CT-i-11's suite in the release tree: **21 passed**.

## 2. Blast radius: the `/hx/teams/*` routes only

`PREFIX = "/hx/teams"`, so all three new routes sit under it. Exactly three GET routes are added and
nothing is removed or re-pointed:

| new route | Graph path it reads |
|---|---|
| `GET /hx/teams/teams` | `/me/joinedTeams` |
| `GET /hx/teams/teams/{team_id}/channels` | `/teams/{team_id}/channels` |
| `GET /hx/teams/channels/{team_id}/{channel_id}/messages` | `/teams/{id}/channels/{id}/messages` (`$expand=replies`) |

The four routes that file already served are untouched: `/hx/teams/me`, `/hx/teams/chats`,
`/hx/teams/chats/{chat_id}/messages`, and the existing replies route. Counted in `server.py`'s route
list: **51 -> 54**, exactly +3.

No role, policy, bearer, secret, schedule, alarm or monitor changes. No IAM change: the order's
preflight declares `comp-iam` NOT-APPLICABLE and this is code only.

## 3. The Graph scopes -- and the one conditional I resolved on the host

The scope analysis is `0.9.0_WK_NFRA_CTLPLN~39`'s
`org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/0.9.0_WK_NFRA_CTLPLN~39/CHANNEL_READ_SCOPES_MEASURED.md`.
Needed by the three paths: **`Team.ReadBasic.All`**, **`Channel.ReadBasic.All`**,
**`ChannelMessage.Read.All`**.

That document is careful about what it could not read, and it left ONE conditional open: it is a
file-only read, and `graph_scope_map.CALLER_GRAPH_SCOPES["teams_route"]` does NOT list
`Team.ReadBasic.All` or `Channel.ReadBasic.All`. **If** `MS_INGEST_IDENTITY` were a SCOPED identity,
`token_broker` line 223 would cut the request to the overlay's union and those two scopes would drop
out, so the two list routes would ask for a token without them and Graph would refuse.

**This seat has host access, so the conditional is now measured rather than carried.** One
read-only SSM run importing the installed app's own `config` and `identity_scope`
(`ap7_scope_filter_read.py`, output `ap7_scope_filter_read.out`, no secret printed):

```
consent_scopes_is_None   True
identity_is_in_overlay   False
overlay_entries          0
GRAPH_SCOPES             17 scopes, incl. Team.ReadBasic.All, Channel.ReadBasic.All, ChannelMessage.Read.All
READ_ONLY_GRAPH_SCOPES    8 scopes, incl. all three of the above
VERDICT  UNSCOPED identity: consent_scopes returns None, line 223 cuts nothing, so all three
         needed scopes survive in the request.
```

So the W39-S1 hazard **does not bite**: the identity is unscoped, the overlay is empty, and both
effective lists -- read live from the service's own config, which also confirms no host environment
override is in play -- carry every needed scope. **No consent is changed and no scope list is
edited by this release.**

**What this does NOT establish, named rather than left implied.** Two causes of a non-200 remain
unread, and neither is a widening:

1. **Tenant consent.** Whether the tenant has actually consented those delegated permissions for the
   app registration is not read here; `config.py`'s comment is a past claim, not today's consent.
2. **The cached token's vintage.** A refresh token for `MS_INGEST_IDENTITY` minted before the Teams
   scopes were consented would return `NeedsLogin`, which these routes surface as **409**.

Either would answer 403 or 409, not widen anything -- which is the issuer's own framing. They are
the live-grade risk to term 3's 200, and they are why the grade is a real call and not a desk read.

## 4. Both branches of a call

- **ADMITTED.** A GET with a valid identity on an allowlisted Graph path returns the Graph page as
  JSON. Paging is bounded: the page size is validated (`invalid_page_size`), the continuation token
  must match a strict shape (`invalid_page_token`), and a `nextLink` is refused unless it is a string
  that continues the requested path (`nextLink does not continue the requested path`). So a
  server-supplied link cannot redirect the reader to another Graph path.
- **REFUSED.** Every refusal is RETURNED to the caller and nothing is alerted -- the file says so at
  its head, and there is no SNS, alarm or notification anywhere in the change: no identity -> **401**
  with `WWW-Authenticate: Bearer`; route not configured -> **503**; a verb or non-allowlisted Graph
  path -> `PathRefused`; a malformed page size, token or body -> a `_Bad` refusal; a token that needs
  re-login -> **409**. A missing scope would surface as Graph's own 403. **No branch writes
  anything** -- all three routes are GET and read-only.

## 5. Triggers, relative to the live base read at the act

Not Phase A constants; each is measured against `before` on the live base at the deploy:

| trigger | expected |
|---|---|
| shipped md5 | equals the RELEASE list (106 of 106) |
| MCP tool list | **UNCHANGED**, name for name -- this release adds no tool |
| `.env` key names | **UNCHANGED** -- this release adds no env key |
| every `.env` value digest | unchanged |
| routes | **+3**, exactly the three named in section 2, none removed |
| `/health` | 200, service active |
| `dashboard/` | unchanged, including the 4 orphans |
| served grade (term 3) | `GET /hx/teams/teams` **200** where it is **404** today |

Any trigger firing: redeploy the base and file an ARMED row naming `2.0.0_SA_COO~O`.

## 6. Rollback

**Redeploy `c3af8687e44a1e641259b37f992033ae02cdce3d`** -- one act, through the same
`safe-ec2-deploy.sh` path with `DEPLOY_BASE_REF` set to the release sha. Nothing else is needed:
this release adds no grant, no env key, no tool and no schedule, so there is nothing else to undo,
and because it writes no object there is no data to delete. The routes simply return to 404.

## 7. Decisions asked of the halves

1. Accept the re-cut: CT-i-11's hunks on the live ref, with `server.py` being live + exactly the four
   `Route(...)` lines rather than the build's whole file (section 1).
2. Accept the blast radius as the three `/hx/teams/*` GET routes only, routes 51 -> 54 (section 2).
3. Accept that no scope list or consent is changed, that the scope-filter hazard is measured not to
   bite, and that a 403 from tenant consent or a 409 from a stale cached token remain possible at the
   live grade and are not widenings (section 3).

## Half -- `1.0.0_SA_CTO~Z`

(sign / refuse + date)

## Half -- `2.0.0_SA_COO~O`

(sign / refuse + date)
