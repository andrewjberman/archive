# W7 — SharePoint reach + registry

**Author:** `4.0.0_SA_CRO~Z` · started 2026-08-12 ~1825Z · site Z
**Authorization:** Andrew-direct ~1702Z @`f09cbd13ef` Part 2; routed to this seat by `1.0.0_SA_CTO~Z`
182248Z (within-program reassignment from a saturated `0.5.0_AE_OpalETL~Z`).
**Scope:** READ-ONLY. No writes, no uploads, no site mutations. `upload_text_to_site` and
`save_email_attachment_to_site` are out of scope for this wave.

> **METHOD:** rung 2 first — the reach already partly exists, so **verify and register what is there
> rather than build a client.** Every registered capability is backed by an **EXERCISED** call, not a
> config read. Every count states what it is out of and what the instrument is blind to. The
> call-shape rule carries across from W8: *a `search_site_files` iterated wide enough is an
> enumeration; a `read_document` loop across a library is a harvest.*

---

## 1. IDENTITY — the reach is a PERSON'S, and that governs everything below

`whoami` (EXERCISED) -> **`Andrew Berman`, `Andrew@opalinvest.com`.**

The gateway is OAuth'd as **a named human**, not a service principal.

⛔ **THE CONSEQUENCE, AND IT IS THE MOST IMPORTANT LINE IN THIS REGISTRY: every "not found" from
these tools is indistinguishable from "exists but Andrew cannot see it."** There is no permission
error to catch — an inaccessible site simply does not appear in the result set, cleanly. **So no
absence claim in this registry is a claim about the TENANT; it is a claim about Andrew's view of
the tenant**, and it is labelled that way throughout.

Second consequence: **every call attributes to Andrew.** Anything scheduled or production-facing on
this surface should be a deliberate decision rather than a side effect of the reach existing.

---

## 2. SITE ENUMERATION — and the name query is SHORT BY 9

| Instrument | Call | Sites returned |
|---|---|---|
| A | `find_sharepoint_site("Opal")` | **6** |
| B | `find_sharepoint_site("*")` | **15** |

**B - A = 9 sites that a plausible, well-formed "Opal" query never surfaces**, including substantive
ones: **`Shared`** (description "Shared", **lastModified 2026-07-13** — recent), **`ExternallyShared`**,
**`allcompany`** ("the default group for everyone in the network"), `smarshteamsarchive` (Teams
archiving), the tenant root Communication site, two `avanan_inline_{incoming,outgoing}` (mail
security), and two `contentstorage` sites (Designer / a GUID-named backing store).

> ⚠ **THIS IS THE SAME CLASS W8 SPENT THE DAY ON, and it is live on the FIRST enumeration act of W7.**
> A name-scoped query returns a **clean, confident, well-formed subset that reads as the whole.** It
> does not error. Had I registered off query A — the natural query for an estate called Opal — the
> registry would have been **40% short and internally consistent.**

⛔ **AND `"*"` IS NOT PROVEN CLOSED EITHER.** It is *another query*, not an enumeration primitive.
Known exclusions by construction: personal OneDrive sites, and **any site Andrew cannot access**
(§1). **15 is a FLOOR, not a total.** No claim in this document treats it as a denominator of the
tenant.

---

## 3. CAPABILITY REGISTRY — what is reachable, each EXERCISED

| Capability | Tool | State | Evidence |
|---|---|---|---|
| Identity | `whoami` | **EXERCISED** | returned Andrew Berman / Andrew@opalinvest.com |
| Site discovery | `find_sharepoint_site` | **EXERCISED** | 6 vs 15 across two queries (§2) |
| Library discovery | `list_site_drives` | **EXERCISED** | 3 sites probed, 1 library each (§4) |
| File listing | `list_site_files` | **EXERCISED** | 49Financial root -> 3 folders with `childCount` + `size` |
| Content search | `search_site_files` | **NOT EXERCISED** | deliberately deferred — see §6 |
| Document read | `read_site_file` / `read_document` | **NOT EXERCISED** | deferred — a read is content egress, sized separately |
| Workbook read | `read_site_workbook` | **NOT EXERCISED** | deferred |
| File profiling | `profile_site_file` | **NOT EXERCISED** | deferred |
| Writes | `upload_text_to_site`, `save_email_attachment_to_site` | **OUT OF SCOPE** | read-only wave (Andrew: *"readonly by the way"*) |

**Registered as reachable: 4 of 8 read-side capabilities exercised.** The other 4 are **NOT claimed
as working** — they are named, unexercised, and deferred. *An unexercised tool in a registry is a
promise, not a capability.*

---

## 4. LIBRARY COVERAGE — a real limitation, honestly unexercised

`list_site_drives`'s own contract states the `list_site_files` / `read_site_*` tools reach **the
DEFAULT library only**; other libraries need a drive-scoped call.

**Probed 3 of 15 sites** (`49Financial`, `Shared`, `OpalOCIO`): **each returned exactly ONE library
("Documents", `driveType: documentLibrary`).**

**So the limitation is REAL IN THE TOOL and UNEXERCISED ON WHAT I TESTED.** On these three sites
default-library-only costs nothing, because default is all there is. **12 of 15 sites are untested
and a multi-library site would be silently under-read** — the tools would return the default
library's contents cleanly, with no signal that others exist. *This is the shape to watch, not a
defect I have observed.*

---

## 5. DOCUMENT UNIVERSE — bounded WITHOUT recursing, deliberately

`list_site_files` returns `folder.childCount` and `size` per entry, so a **bound** is obtainable
without walking the tree. `49Financial` root: 3 folders, `childCount` 4 / 3 / 1, `size` 31.9 MB /
36.7 MB / 3.4 MB.

**This is the whole reason not to recurse.** A depth-first walk to "get the document count" is
precisely the harvest the call-shape rule forbids, and **the metadata already carries the bound.**
Per-site bounds will be collected the same way — one listing per site, never a walk.

---

## 6. WHY `search_site_files` IS DEFERRED RATHER THAN EXERCISED

Search is the tool most likely to be reached for and **most likely to become an enumeration.** One
call is cheap; the failure mode is iterating it across sites and terms until it has effectively
dumped a library index. There is **no published quota on this surface that I know of** — which is a
reason for more discipline, not less, since there is no meter to warn us.

It will be exercised in increment 2 with a **declared query set and a declared stop**, not
opportunistically.

---

## 7. UNVERIFIED PREMISES — named, not carried as fact

| # | Premise | Status |
|---|---|---|
| 1 | The 15-site list is the tenant's site set | **FALSE AS STATED — it is Andrew's visible set, and a FLOOR.** Personal sites and permission-invisible sites are excluded by construction |
| 2 | Sites carry one library each | **UNVERIFIED beyond 3 of 15.** True where tested; the tool's default-library limit would hide the rest silently |
| 3 | `"*"` enumerates all sites | **UNVERIFIED.** It is a query, not an enumeration primitive |
| 4 | The 4 unexercised read tools work | **UNVERIFIED — not claimed.** Named in §3 as unexercised |
| 5 | No quota governs this surface | **UNKNOWN, not established.** Absence of a published limit is not absence of a limit |

---

## 8. INCREMENT 1 COVERAGE

| Axis | Enumerated | Of | Instrument | Confidence |
|---|---|---|---|---|
| Identity | 1 | 1 | `whoami`, exercised | high |
| Sites | 15 | **UNKNOWN** | `find_sharepoint_site("*")` | **floor only** |
| Libraries | 3 sites probed | 15 | `list_site_drives`, exercised | high for the 3 |
| Read capabilities | 4 exercised | 8 | direct calls | high |
| Document universe | 1 site bounded | 15 | listing metadata, no recursion | high for the 1 |

*Increment 1 ends here. Read-only throughout; no writes, no content reads, no recursion.*
