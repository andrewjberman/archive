# D4c Phase A — TrueShares holdings fetch path: design, proven parser, and a LANE BLOCKER

**TO:** `D4_ETFPOS.TO-D4c` · **Author:** `0.4.0_DS_ClientPlatform` · **2026-08-19 ~23:30Z**
**Status:** design PROVEN offline, **code not written — the target file is outside my lane.**
**Egress performed: ZERO.** Everything below was derived from bytes already in the repo.

---

## 1. ⛔ THE BLOCKER — the build target is not in the DS lane

COO ruled D4c is *"EXTEND `etfs-netassets-daily`, not write a producer"* and assigned the build to
me. That file is `infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/lambda_function.py`.

**Re-derived against the rule data, not read off the prose:** the longest matching rule for that
path is **`infra/aws/**` → lane `CLOUD_OPS_OR_ETL`** (*"AWS infra (Terraform, IAM, Lambda) — AE
0.5/0.6/0.6.1/0.7 only"*), an **enumerated 11-member lane that does not include
`0.4.0_DS_ClientPlatform`**. There is **no carve-out for `etfs-pipeline`** — I grepped: zero
`etfs` rules in `.owned-paths.yaml`.

**This is a KNOWN, RECURRING CLASS, and `.owned-paths.yaml` documents it against itself.** The
`yang_pipeline` rule (added 2026-08-03) exists for exactly this: *"the Lambda SOURCE dir had NO
rule and fell through to `infra/aws/**` AE-only, so DS's membership grant was inert for source
commits"* — recorded there as **the third record-consistency gap of that day on that family**.
The sibling carve-outs (`inf-*`, `news_*`, `keyword_*`, `v2_portal/*`) are all the same remedy:
a longest-match rule binding the source dir to a `POD*_OR_AE` lane, **DS authors, AE deploys.**

**Why I did not just fix it:** those rules are **grantor-landed under separation of duties** —
the file's own notes are explicit that *the grantee does not self-land its own grant*. Editing
`.owned-paths.yaml` to admit myself is precisely the act SoD exists to prevent. Same line I held
tonight on the `SYSTEM_DEFINITIONS` status field, the L8/L9 dispositions, and COO's criterion-id
re-mint.

**Two clean resolutions, COO's call — I have no preference beyond wanting it explicit:**
- **(a)** Route an `infra/aws/lambda/etfs-pipeline/**` → `POD4_OR_AE` carve-out, grantor-landed
  with SoD, exactly mirroring the four existing precedents. Then I build in place. *Durable, and
  it closes the class for the whole etfs family rather than this one file.*
- **(b)** I hand AE the patch + fixtures below and **AE applies it.** Faster tonight, but it
  leaves the next etfs source change blocked the same way.

---

## 2. The design decision: **DERIVE the sheet id, never hardcode it**

Both TrueShares sheet ids are recoverable **from bytes we already hold** — the fund-page HTML that
`etfs-netassets-daily` downloads every day, captured in-repo from a 2026-08-06 pull:

| fund | sheet id (from the 08-06 capture) |
|---|---|
| DIVZ | `1csUjnC2fHqZQORGBccRy_ew0dgv-jpC_LOKdbjPwI9U` |
| IDVZ | `1H8LXhhQBSbQLK37-y5TPTvJsaeKfE2HVmVcRVpQHKh8` |

**These are the TEST FIXTURE, not the production constant.** The fetch path must parse the id out
of the page it already downloads, at run time. Three reasons, and the third is load-bearing:

1. **No extra request.** The page is already fetched and already persisted to bronze untouched;
   extracting the id is a parse of bytes in hand.
2. **No baked value to drift** — consistent with the derive-don't-hardcode rule.
3. ⚠ **A stale hardcoded id fails in the WORST way.** If TrueShares republishes the sheet, a baked
   id returns either a 404 *or a frozen old sheet that still parses cleanly* — a well-formed-empty
   result that would serve stale holdings while every check reads healthy. **Deriving it makes
   that failure impossible rather than merely detectable.**

---

## 3. The parser, PROVEN OFFLINE with controls (rc=0)

```
=== PARSER TEST vs the CAPTURED 2026-08-06 bronze HTML (zero egress) ===
  DIVZ: PASS  1csUjnC2fHqZQORGBccRy_ew0dgv-jpC_LOKdbjPwI9U
  IDVZ: PASS  1H8LXhhQBSbQLK37-y5TPTvJsaeKfE2HVmVcRVpQHKh8
=== NEGATIVE CONTROLS (the parser must REFUSE, not fall back) ===
  RAISED as required -- page with NO export link
  RAISED as required -- page with TWO distinct links (ambiguous; refusing to guess)
=== HTML-ENTITY CONTROL (the live page carries &amp; not &) ===
  raw '&amp;' form parses: True
RESULT: ALL PASS
```

**`SheetLinkError` RAISES rather than falling back to a baked id** — the refusal *is* the design.
The ambiguity control matters: if the issuer ever links two sheets, guessing which is holdings
would silently serve the wrong fund's composition.

---

## 4. Field mapping — a SECOND SOURCE into an EXISTING shape, not a new plane

`fetch_filepoint()` already normalises the Pathfinder CSV into a `line_items` structure. The
TrueShares sheet header maps onto it field-for-field, so this needs **no second downstream code
path** — build-ladder rung 2 again.

| TrueShares sheet column | existing `line_items` field |
|---|---|
| `Stock Ticker` | `holding_ticker` |
| `CUSIP` | `cusip` |
| `Security Name` | `security_name` |
| `Shares` | `shares` |
| `Price` | `price` |
| `Market Value` | `market_value` |
| `Weightings` | `weight_pct` |
| `Net Assets` | fund-level `net_assets` |

**Not present in the TrueShares sheet:** the Pathfinder `MoneyMarketFlag` that drives `is_cash`.
The cash sleeve is identifiable by security name (`STATE STREET INST U.S. GOVERNMENT MMKT ...`)
but **that is a string-match, and inferring a flag from a name is the exact hazard the model
crosswalk's own docstring warns about** (*map on the id, never the label*). **Recommend: emit
`is_cash=None` for TrueShares rows** — a declared unknown — rather than synthesise it. A consumer
that needs the cash split can be given a ruled rule; silver must not invent one.

Ride the existing `fetch_raw()` control: it persists the **raw response bytes to bronze before
parsing**, so bronze is written from the bytes the parser consumes (Rule 17a holds by construction).

---

## 5. Schedule (D4c-4) — deliverable now, and DISABLED

The TO makes the schedule an acceptance criterion, not a follow-up, and requires it **visible in
Terraform**: *a pipeline whose only trigger is another pipeline's success has no schedule and is a
defect.* `etfs-netassets-daily` already carries `cron(0 22 * * ? *)` in TF, so the holdings fetch
inherits a real schedule rather than needing a new one — **the enable is a flag on an existing
scheduled run, which is why it can be a single reviewable line.**

⛔ **It stays DISABLED until COO relays Andrew's scope word.** No pull has fired from this seat.

---

## 6. Standing residuals

- **D4c-1 / -2 / -3 remain gated on the egress word** (three of five criteria) — see my 231545Z
  scope-fork note; recommendation was to split D4c into a build TO and a serve TO so both halves
  are honestly closeable.
- **`is_cash` for TrueShares rows** needs a ruled answer or stays `None`.
- **The lane blocker in §1** needs COO's routing before any code can land.
