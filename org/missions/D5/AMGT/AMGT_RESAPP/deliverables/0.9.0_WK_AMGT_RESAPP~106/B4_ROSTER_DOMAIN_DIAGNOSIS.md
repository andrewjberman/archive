# B4 Roster / Domain Diagnosis -- `AMGT-rk-106` (round 27)

Read-only diagnosis, no code change, 0 S3 writes (proven at AC3). All measurements run against live
`opal-data-harvest` under the seat's existing read credentials (`get_object`/`list_objects_v2` only).
Code cited at HEAD `40f01c2b08` (worktree `C:/tmp/wk-amgt-27-106`, branch `wk-amgt-27-106`); `git diff
--stat d3ba12c64b HEAD -- lib/research/management/roster.py lib/research/management/enrich.py
lib/research/api/scoped_amgt.py lib/research/harvest/lusha.py` returns nothing, so every line number
below is identical to the task order's own pointers, measured at `d3ba12c64b`.

Security under diagnosis: `6861_JP_Equity` (Keyence Corp).

---

## Q-a1: which source serves 6861's officers on Exec Management today

**Route traced, live:**
1. `read_management(security_key, identity)` -- `lib/research/api/scoped_amgt.py:2507` @40f01c2b08 --
   resolves identity, then calls `read_pool_object(MANAGEMENT_PREFIX, key)` at
   `lib/research/api/scoped_amgt.py:2536` @40f01c2b08, `MANAGEMENT_PREFIX = "management/v1/"` at
   `lib/research/api/scoped_amgt.py:171` @40f01c2b08. Pool bucket `opal-data-harvest`
   (`lib/research/coverage/pool_reader.py:72` @40f01c2b08, `POOL_BUCKET` default).
2. Served object (GET, read-only): `s3://opal-data-harvest/management/v1/6861_JP_Equity/2026-09-19.json`
   -- exactly the one object the task order names, confirmed still the only served object (it is the
   one `read_management` reads for `security_key="6861_JP_Equity"`).
3. `officers = list(document.get("officers") or [])` -- non-empty (1), so `read_management` does NOT
   take the `ZERO_OFFICERS` branch (`lib/research/api/scoped_amgt.py:2557-2574` @40f01c2b08); it falls
   through to `_roster_source(document, officers)` at `lib/research/api/scoped_amgt.py:2575` @40f01c2b08,
   which reads the object's OWN `roster_source` field first (`lib/research/api/scoped_amgt.py:2487-2496`
   @40f01c2b08).
4. **The served object's own field: `roster_source = "BLOOMBERG_FALLBACK"`.** This routes
   `read_management` into the `BLOOMBERG_FALLBACK` block (`lib/research/api/scoped_amgt.py:2577-2620`
   @40f01c2b08): `management_status = POOL_SERVED`, `source_item = "Bloomberg COMPANY_EXEC_OFFICERS
   (fallback: no RESOLVED filing roster)"`, `source_key` built from `fallback.raw_key =
   "raw/bloomberg/6861_JP_Equity/20260921T162534Z/exec_officers.json"`, no pool tenure comparison
   (Bloomberg carries no role start).
5. The object's own `roster_status = "UNRESOLVED-SOURCE"` and `roster_reason = "The Japanese annual
   securities report (Yuho) was found, but its officer section is empty, so no officers could be read
   from the filing."` -- i.e. the object itself records that its FILING roster never resolved; the
   Bloomberg fallback is what is actually served.

**Served officer COUNT and source field value (read-only GET of the served object):**
- `officer_count = 1`
- `roster_source = "BLOOMBERG_FALLBACK"`
- `roster_status = "UNRESOLVED-SOURCE"`
- Officer's own `source` field on the roster row = `"bloomberg"` (1 of 1 officers).
- No officer name, contact field or personal URL is printed here (count and roles/fields only, per
  bounds).

**ANSWER (Q-a1):** Today Exec Management serves 6861's officers from the **Bloomberg
`COMPANY_EXEC_OFFICERS` fallback** (`roster_source = BLOOMBERG_FALLBACK`), NOT the filing roster and
NOT the served object's own filing-roster branch -- the served object's `roster_status` is itself
`UNRESOLVED-SOURCE` for the filing half; the object is served ONLY because `read_management`'s
`BLOOMBERG_FALLBACK` branch (`:2577-2620`) exists precisely to serve a roster when the filing side did
not resolve. Officer count served: 1.

---

## Q-a2: why `load_source_object` + `build_roster` return 0 for 6861

Run exactly as `lib/research/harvest/lusha.py::_cli` does (`lib/research/harvest/lusha.py:234-236`
@40f01c2b08: `roster.load_source_object(security_key)` then `roster.build_roster(source_object, as_of,
label)`), read-only, no Lusha call, no write, against live `opal-data-harvest`:

```
source_object_present True
source_label      silver:filing_source:6861_JP_Equity:doc-1defdb68a7ffd3b7
roster_status      UNRESOLVED-SOURCE
roster_reason      The Japanese annual securities report (Yuho) was found, but its officer section is
                    empty, so no officers could be read from the filing.
officer_count      0
diagnostics        {'candidates': 0, 'rejected': []}
```

**Exact branch of `derive_roster` taken:** `lib/research/management/roster.py:1211-1217` @40f01c2b08 --
`load_source_object` returns a SILVER row (status `RESOLVED`), so the `not source_object` branch
(`:1201-1205`) and the `status != "RESOLVED"` branch (`:1208-1210`) are both skipped. `section =
source_object.get("officer_section") or {}` at `:1211`; the live object's `officer_section` field is
`None` (confirmed by direct read: `officer_section = null`), so `section` is `{}` and `section.get("text")`
is `None`; `if not (section.get("text") or "").strip():` at `:1213` is TRUE, so `:1214-1217` returns
`roster_reason = "The %s was found, but its officer section is empty, so no officers could be read from
the filing." % _filing_label(source_object)` with `officer_count = 0`. This is the EXACT text observed
above.

**Why `officer_section` is `None` on this RESOLVED object -- upstream cause, not a `roster.py` defect:**
the winning document came from the `company-site` battery route (step 4), which the winner-assembly code
sets to `officer_section: None` BY CONSTRUCTION on every company-site win
(`lib/research/filings/battery.py:1182` @40f01c2b08: `"excerpt": None, "sections": result["family"].get
("sections"), "officer_section": None,`) -- the company-site route does not extract an officer section at
all; only later EDGAR-form parsing paths populate `officer_section`. So the object is genuinely
`RESOLVED` (a real filing was found and verified) but carries no officer section for `derive_roster` to
read, independent of anything `roster.py` or `lusha._cli` do.

**Does the previous claim, "its filing source resolved to an issuer-site document", hold?**
**YES.** Live read of `_silver_rows_for_security` / `hstore.silver_latest` by vendor, denominator printed:
- vendor `sec`: 13 rows total in the `filing_source` silver table; **0** match `security_key ==
  "6861_JP_Equity"`.
- vendor `issuer-site`: 1 row total in the `filing_source` silver table; **1** matches
  `security_key == "6861_JP_Equity"` -- `{"security_key": "6861_JP_Equity", "accession":
  "doc-1defdb68a7ffd3b7", "status": "RESOLVED", "bronze_key":
  "filings/v1/6861_JP_Equity/doc-1defdb68a7ffd3b7.source.json", "url":
  "https://www.keyence.co.jp/pdf/AnnualSecuritiesReport_202606_ja.pdf"}`.
- Denominator of filing_source silver rows read for 6861 across BOTH vendors: **14 rows read, 1
  matching** (13 `sec` + 1 `issuer-site`).
- `filing_identity = {"key": "https://www.keyence.co.jp/pdf/AnnualSecuritiesReport_202606_ja.pdf",
  "route": "company-site", "source": "battery", "step": 4}` -- `company-site` routes to vendor
  `issuer-site` (`lib/research/harvest/filings.py:58-63` @40f01c2b08, `_BATTERY_ROUTE_TO_VENDOR`).

So the claim holds exactly: 6861's filing source IS a RESOLVED issuer-site document (the Keyence Yuho
PDF), it is just one whose `officer_section` the winning route never populates -- distinct from an
UNRESOLVED source, and distinct from a resolved filing whose officer section was searched and found
empty.

**A second, older object exists and is NOT what `load_source_object` reads today:** a
`filing_attempt/.../UNRESOLVED-SOURCE.json` state marker is still live at
`amgt/harvest/state/filing_attempt/security_key=6861_JP_Equity/UNRESOLVED-SOURCE.json`
(`retrieved_at = 2026-09-19T06:20:51Z`) -- but `load_source_object` only reads this marker when NO silver
row exists (`lib/research/management/roster.py:1145-1146,1151` @40f01c2b08: `if rows: ... return`; the
state-marker branch is `:1151-1164`). Since the issuer-site silver row now exists (written later, at
`retrieved_at = 2026-09-19T08:32:27Z`, per the RESOLVED object's own `retrieved_at`), the earlier
UNRESOLVED-SOURCE marker is superseded and simply never read by this path -- it is a stale leftover of
an earlier, failed run (its own `reason`: step 4 "crawl bound reached (seeds=['https://www.keyence.co.jp/']
pages_visited=40 (cap 40) candidates_tried=0 queue_remaining=407) before a candidate passed ... --
resumable"), never overwritten because the state-marker write is a conditional put
(`lib/research/harvest/filings.py:239-247` @40f01c2b08, never-overwrite).

**ANSWER (Q-a2):** `load_source_object` + `build_roster` return 0 officers for 6861 because the
RESOLVED issuer-site filing object (`doc-1defdb68a7ffd3b7`, the Keyence Yuho PDF) carries
`officer_section = None` -- a direct consequence of the `company-site` battery route never populating
`officer_section` on a win (`battery.py:1182`) -- which `derive_roster`'s `:1213-1217` branch converts
into `roster_status = UNRESOLVED-SOURCE`, `officer_count = 0`, with the reason string observed above. The
filing source itself IS resolved (an issuer-site document); the roster is not.

---

## Q-b: where a company domain should come from for a name with no `domains.json` entry

**Denominator, by subtraction: every field carrying a URL or a host, across every object read for 6861,**
across 6 named objects (crosswalk record, filing_attempt state marker, the ONE filing_source silver row,
the served management object, `domains.json`, and the crosswalk record's `model_key`/`identity`
sub-block -- no separate "model" S3 tier exists in `opal-data-harvest`'s 21 top-level prefixes, none
named `model/`; the crosswalk record's `model_key` field is the closest analogue and is read explicitly
below):

```
OBJECT crosswalk.record_for                              url_occurrences 0
OBJECT filing_attempt.state_marker(.../UNRESOLVED-SOURCE.json)  url_occurrences 4
   https://filings.xbrl.org/api/entities/529900M7PQBS7A89DZ11/filings
   https://www.keyence.co.jp/            (x2, incl. one embedded in a nested-JSON evidence string)
OBJECT filing_source.silver_row(silver:filing_source:6861_JP_Equity:doc-1defdb68a7ffd3b7)  url_occurrences 11
   https://filings.xbrl.org/api/entities/529900M7PQBS7A89DZ11/filings
   https://www.keyence.co.jp
   https://www.keyence.co.jp/
   https://www.keyence.co.jp/pdf/AnnualSecuritiesReport_202606_ja.pdf
OBJECT served_management(management/v1/6861_JP_Equity/2026-09-19.json)  url_occurrences 4
   https://www.globaldata.com/company-profile/keyence-corp/executives/
   https://www.marketscreener.com/news/keyence-corporation-announces-president-changes-...
   https://www.theglobeandmail.com/investing/markets/stocks/KYCCF/pressreleases/...
OBJECT domains.json                                       url_occurrences 0
OBJECT crosswalk.record.model_block(model_key+identity)   url_occurrences 0
TOTAL_URL_OCCURRENCES_ACROSS_ALL_OBJECTS  19  (distinct hosts: 4 -- keyence.co.jp,
   filings.xbrl.org, globaldata.com, marketscreener.com, theglobeandmail.com -- 5 distinct hosts)
```

**Candidates, by host (excluding the two pure-news-article hosts, which name no company site):**

| Value | Who wrote it | Verified or seed/display | Existing reader |
|---|---|---|---|
| `www.keyence.co.jp` (`verified_site.host`, on the RESOLVED issuer-site filing object) | `lib/research/filings/battery.py:1162-1165` @40f01c2b08 -- the company-site route's win branch, guarded by RULED item 3 (never an exchange host) | **VERIFIED** -- `source: "winning-document-host"`, `evidence: "legal name 'Keyence Corp' matched on the cover; LEI absent from the document"` | `enrich.verified_domain_for(source_object)` -- `lib/research/management/enrich.py:166-174` @40f01c2b08, already called at `enrich.py:653` and `enrich.py:1000` @40f01c2b08 -- but ONLY to gate whether the CEO SERP search runs, NEVER fed into `domain_for`'s Lusha-facing `company_domain` |
| `https://www.keyence.co.jp/` (`battery.attempts[3].key`, the company-site route's SEED) | `lib/research/filings/battery.py` (the seed list passed into the company-site crawl step, same run) | SEED only (the crawl's starting URL, not itself a verification) | not read by any function directly; it is consumed only as the crawl's input and happens to match the verified host above |
| `filings.xbrl.org/api/entities/...` (`battery.attempts[2].url`, esef-lei route) | `lib/research/filings/battery.py`, esef-lei step | Neither -- this is the XBRL FILING REGISTRY's own API host (a lookup endpoint), not the issuer's site; the LEI resolved but the route did not win | not read as a domain candidate anywhere |
| `www.globaldata.com` (`ceo_public_profile.url`) | the CEO SERP path (`ceo_search.py` / `enrich.py`'s CEO-bio flow) | Display/citation value for the CEO bio; a THIRD-PARTY research site, not Keyence's own domain | read as `ceo_public_profile.url` (a citation for the CEO fact), never as a company domain |
| `www.marketscreener.com`, `www.theglobeandmail.com` (news article URLs inside `ceo_profile.search`) | the CEO SERP path | Neither -- third-party news articles surfaced by the CEO search, not a company site | not read as domain candidates by any function |
| (absent) `domains.json["6861_JP_Equity"]` | n/a -- no row exists (5 names declared total: `BABA_US_Equity, BA_US_Equity, COST_US_Equity, HD_US_Equity, SAP_GY_Equity`; 6861 is not one) | n/a | `enrich.domain_for(security_key)` -- `lib/research/management/enrich.py:140-148` @40f01c2b08 -- the ONLY function `lusha._cli` / `harvest_company` uses for the Lusha-facing company domain, and it reads ONLY this table |

**ANSWER (Q-b):** the one candidate that is both VERIFIED (not a guess, not a third-party site, not a
mere seed) and already produced by the estate's own resolution pipeline is `verified_site.host =
"www.keyence.co.jp"` on the RESOLVED issuer-site filing object, written at
`lib/research/filings/battery.py:1162-1165` and already read by `enrich.verified_domain_for`
(`enrich.py:166-174`) -- just not for Lusha's `company_domain`. Recommended rule for a later code cell:
**when `domains.json` carries no entry for a security_key, `domain_for` (or its Lusha-facing caller) may
fall back to `enrich.verified_domain_for(source_object)` read off the SAME `load_source_object` result
`lusha._cli` already loads for the roster -- and ONLY that field, never `ceo_public_profile.url`, never a
battery seed/attempt URL, never the XBRL registry host.** This satisfies the `domain_for` docstring's own
hazard ("a guessed domain enriches the wrong company"): `verified_site` is explicitly a MEASURED,
name-matched value (RULED item 3, battery.py), not a guess, and is already the one field
`verified_domain_for` exists to serve for the CEO-bio use case -- extending its Lusha use is a reuse of an
existing verified field, not a new guess.

---

## What the next round would cut (at most 3 code cells)

1. **Wire `domain_for` (or a new fallback wrapper) to fall back to `enrich.verified_domain_for` when
   `domains.json` has no entry, for the Lusha-facing `company_domain` only** -- files:
   `lib/research/management/enrich.py` (the `domain_for` function and its two call sites at `:643` and
   the CLI re-derive mode near `:1000`), `lib/research/harvest/lusha.py` (`_cli`'s `enrich.domain_for`
   call at `:238`).
2. **Decide and implement whether a `company-site` battery win should ALSO attempt an officer-section
   extraction** (today `battery.py:1182` hard-sets `officer_section: None` on every company-site win,
   which is the root cause of Q-a2's 0-officer roster for every name whose filing resolves via
   company-site rather than EDGAR) -- file: `lib/research/filings/battery.py` (the company-site win
   assembly, `:1140-1184`).
3. **Decide whether the stale `filing_attempt/UNRESOLVED-SOURCE.json` marker should be cleaned up (or at
   least excluded from any future "which names are still unresolved" census) once a later silver row
   RESOLVES the same security_key** -- files: `lib/research/harvest/filings.py`
   (`state_put_filing_attempt`, `:239-`), `lib/research/management/roster.py` (`load_source_object`'s
   silver-first precedence, `:1116-1164`, which already makes this marker inert for the roster path but
   leaves it live for anything else that reads `filing_attempt/` directly).
