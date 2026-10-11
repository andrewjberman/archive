# Release 1 REVISION 6 -- reached `ArtifactRepository.get` sites on the built irpt-status zip (answer to CTO msg 4066)

Author `2.0.0_SA_COO~Y2`, 2026-10-11 ~04:3xZ. Zip: this seat's BUILD_ONLY build, CodeSha256 `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=`.
Line numbers are the zip's own members. Every statement below is a READ of the zip's bytes; nothing was imported or run.
The promote is HELD: hold sent to `0.7.0_AE_CloudOps~DELL2` at 04:31Z; its msg 4069 answers NOT PROMOTED (live still `t6OJTCcm`; the artifact is
uploaded as version `hRe7.zty9CYey5GkmjHlETbeZkKsD.3O`, which nothing points at).

## The number asked for

**4 call sites of `ArtifactRepository.get` / `.head` are reached from the 7 routes. NONE passes a family as a literal, because the method takes no
family argument at all.** `repository.py:453` is `get(self, principal, artifact_id, *, data_firm=None)`; `:484` is `head(...)`, which calls `get`.
The family is read from the STORED row (`repository.py:466-467`, `ref = item["ref"]`, then `_allow(..., read_family=ref.get("family"))`).
So by the half's A4 wording every one of the 4 is non-literal, and this file is the file-and-line the CTO asked for.

Denominator: 753 `.get(` / `.head(` call sites in the 434 reached functions (of 559). 35 have the two-positional shape; none of those 35 has an
artifact repository as receiver (they are dict, index, acceptance and store reads). The 4 below were found by receiver text (`artifacts.get`,
`artifacts.head`) over every top-level member; a fifth textual match, `enforce.py:817 self.artifacts.get(object_id)`, is a one-argument read of
the Enforcer's own `artifacts` mapping (`enforce.py:325`, default `{}`), not the repository.

## The 4 sites, and what binds the family at each

| site | in | what the family is bound to BEFORE the call | what is checked AFTER |
|---|---|---|---|
| `owned_requests.py:194` `self.artifacts.head(principal, ref.get("artifact_id"), ...)` | `OwnedRequestReader._materialize` | `ref` comes from `_validate`, which refuses unless `ref.get("family") == "REQUEST_COMPOSITION"` (`:187`, a literal) | the returned stored ref must EQUAL `ref` or `COMPOSITION_REFERENCE_CHANGED` |
| `owned_requests.py:202` `self.artifacts.get(...)` | `OwnedRequestReader._selected_client` | the same `_validate` (`:201`) | `saved.get("ref") != ref` refuses (`:203`) |
| `owned_requests.py:246` `self.artifacts.get(...)` | `OwnedRequestReader.read` | the same `_validate` (`:243`) | `saved.get("ref") != ref` refuses (`:247`) |
| `prospect_dates.py:245` `self.requests.artifacts.get(self.principal, ref["artifact_id"], ...)` | `RetainedProspectDates._artifact(ref, family)` | `ref.get("family") != family` refuses (`:238`) | `saved.get("ref") != ref` refuses (`:247`) |

Callers of `_artifact` in the zip, with the `family` each passes (denominator 7 call sites, all in `prospect_dates.py` and `owned_report.py`):
`"REQUEST_COMPOSITION"` (`prospect_dates.py:253`, `owned_report.py:296`), `"NORMALIZED_PORTFOLIO"` (`prospect_dates.py:269`,
`owned_report.py:309`), `"ORIGINAL_HOLDINGS"` (`prospect_dates.py:295`), `"ORIGINAL_CSV"` (`prospect_dates.py:299`), and ONE variable,
`owned_report.py:331`, where `family = "ORIGINAL_HOLDINGS" if template else "ORIGINAL_CSV"` on the line above (`:330`).

So at each of the 4 sites the stored family must equal one of four literals -- `REQUEST_COMPOSITION`, `NORMALIZED_PORTFOLIO`,
`ORIGINAL_HOLDINGS`, `ORIGINAL_CSV` -- or the read refuses. `ANALYSIS_COMMENTARY` is none of them, and the string appears in the zip only in
`repository.py` (the two tables and their comments).

## One more path the CTO should see: the packager wiring in `resident_installed.py`

`resident_installed.py:283-302` `make_packager` passes the artifact repository to `opal_packager.live_read_artifact(artifacts)` (`:300`), and
`build_resident_runtime` (`:305-388`) calls it (`:386`). That is the `svc-irpt-packager` reader A1 names.
- `opal_packager` is NOT a member of this zip (0 members match `packager`); `make_packager` imports it inside the function (`:293`).
- Nothing in the zip calls `make_packager` or `build_resident_runtime` except `resident_installed.py` itself; `status_installed.py:130` imports
  only `make_authorize` from it. Its own header (`:3`) says its entry is `ycharts/generate/resident_main.py`, which is not in this zip either.
- `reach_read.py` marks `resident_installed` functions as reached (11) only because its edges are by name; that is the over-approximation, and the
  two functions above are in that set. The `get_ac` limb did not count them, because no `.get(` call sits in them.

## What is NOT measured

- That a principal on these routes is never a service subject (`is_service_principal`): that is `served.py` admission, not read here.
- Dynamic dispatch (`getattr` with a computed name), and anything a route does on real rows: ABSENT != EXERCISED-AGAINST.
