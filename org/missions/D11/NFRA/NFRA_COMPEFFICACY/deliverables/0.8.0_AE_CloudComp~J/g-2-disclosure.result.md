# G-2 disclosure — measure-first evidence

Measured by `0.8.0_AE_CloudComp~J` before any G-2 source edit, 2026-09-03.

## Real default runs

`comp-trace gold:A_00.accounts_dimension` returned its existing, distinct trace-cache
provenance: `cache: ...graph.json built_at=2026-09-03T11:48:41Z (age 5.9h)` and
`universe: head-pinned TRACE graph, 2302 nodes / 3044 edges`. It has no Kuzu `VINTAGE:`
answer line and no `--json` vintage field.

`comp-blast gold:A_00.accounts_dimension` was issued with no `--force`. Its then-current
auto path rebuilt after reporting `BEHIND Nessie HEAD`; the completed real answer printed the
raw provenance block, including `DB: kuzu_nessie_db (27226 nodes / 58606 edges)` and
`built: 2026-09-03T17:58:13.785385+00:00 (age: 0.0h)`, followed by a 179-node blast radius.
It did not print the required one-line `VINTAGE:` disclosure at answer grain.

## One carrier, read-only source citations

The DB-own provenance carrier is `_provenance.format_provenance_header` at
`infra/aws/globgrph/_provenance.py:560-622`: it reads the manifest `built_at`, node and edge
counts, computes age once with `_age_hours`, and renders the existing `built:` line. The
stale served label is sourced by that same header at `:570-589`; the seam writes its label via
`_canonical._incremental_or_serve_stale` at `infra/aws/globgrph/_canonical.py:559-607`.
Both `comp-blast` and `comp-trace` currently render in `org/modules/graph/cli.py` (`cmd_blast`
and `cmd_trace`); no engine, loader, CLI, fallback sink, provenance, or rebuild-seam bytes
were changed for this measurement.

**State:** measure-first complete; disclosure rendering and battery remain pending.
