# ETFS_RIVALS task order -- `RIV-gw-1` -- ROUND 12 (ENRICHMENT): THE GATEWAY SERVES THE DAY'S AUDIT PAGE AT /rivalfunds/YYYY-MM-DD/audit

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D5/ETFS/ETFS_RIVALS/decompositions/ETFS_RIVALS_DECOMP.md</decomp_doc>
<owned_cells>RIV-gw-1</owned_cells>
</decomp_ref>
<issued_to>0.9.0_WK_ETFS_RIVALS~2</issued_to>
<issued_by>2.0.0_SA_COO~RV</issued_by>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule, cron or trigger is added or moved by this cell
comp-iam: DECLARED-NOT-APPLICABLE the gateway's read policy already grants GetObject on the page prefix `<key_prefix>*` (gen_rivalfunds_location.policy_doc); the new object sits under it; no grant changes
comp-adversary: DECLARED-NOT-APPLICABLE the validator-context composer profiles RETURNED work for the L8/L9 packet; at the cut nothing is returned, and the issuer's evidence context is this order's check file
</preflight>

**Project:** ETFS_RIVALS (D5/ETFS, fabric site-z) -- *rivalfunds*: a daily research page on rival active ETFs, published to S3 by the package `data/etfs/scripts/rivalfunds/` and served signed-in by the opal-gateway (Starlette app under `infra/aws/ec2/opal-gateway/app/`) at `mcp.opalinvest.dev/rivalfunds`. **Round 12** (narrowed, on Andrew's word that every ticker mention links to its modal): the page's audit trail moves to its own dated object `audit.html` beside the day's `index.html`; this cell lets the gateway serve it. Nothing in round 12 deploys, merges or releases the gateway from a worker. Work ONLY in the worktree your spawn line names; every path below is relative to that root.

## 1. YOUR CELL (inlined verbatim from the decomposition)

### `RIV-gw-1` -- the gateway serves the day's audit page (row Z-S47)
- Measured 2026-10-06: `infra/aws/ec2/opal-gateway/app/rivalfunds_view.py` serves only `<key_prefix>date=<day>/index.html`
  (`object_key`, `_PAGE_NAME`); server.py:1112-1115 mounts `/rivalfunds`, `/rivalfunds/`, `/rivalfunds/archive`,
  `/rivalfunds/{day}`. The read policy (`gen_rivalfunds_location.py` `policy_doc`) already grants GetObject on
  `<key_prefix>*`, so an object beside index.html needs no new grant.
- Interface: `audit_key(day)` = `<key_prefix>date=<day>/audit.html` from the generated location (never typed) and the handler
  `rivalfunds_audit(request)`: no viewer 401; a bad date 400; a missing object 404 naming the day's audit page with a link to
  the day's page; otherwise the bytes with `_HEADERS`, under the same 2 MB cap and TTL cache as the page. The server.py Route
  line is the issuer's hookup at the merge.
- **Organic trigger:** a signed-in viewer following the main page's audit link.

## 2. WHAT YOU NEED TO KNOW (measured at the cut, base CLOUD 8f1c1a9e6e)

- The check file's docstring is the exact interface it reads: read `org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round12/checks/gw-1.AC1.py` before you build.
- Follow `rivalfunds_day` / `_serve_day` (rivalfunds_view.py ~154-196): the same `_viewer` identity read, `valid_day`, `_cached` + `_fetch_capped`, `_OverCap` -> 502, NoSuchKey -> 404, other S3 errors -> 502, `audit.log_call(email, "rivalfunds_view", {...}, ...)` on each outcome (add `"route": "audit"`). Prefer generalising `_serve_day` over a copy.
- Do NOT edit `server.py` (a shared file): name the one Route line you need in your report, exactly as it should read, placed BEFORE `Route("/rivalfunds/{day}", ...)`.
- Unit tests live in `infra/aws/ec2/opal-gateway/app/tests/test_rivalfunds_view.py` (S3 and the viewer stubbed, a Starlette app built in the test); add the audit route's cases there. Run from `infra/aws/ec2/opal-gateway`: `python -m pytest app/tests/test_rivalfunds_view.py -q` (0 failed).

## 3. SURFACES AND BOUNDS

You READ (never edit): `lib/`, the rest of `infra/aws/ec2/opal-gateway/` (incl. `server.py`, `gen_rivalfunds_location.py`, `rivalfunds_location.json`), `data/etfs/scripts/rivalfunds/` (another chain owns the renderer), the round-12 check folder `org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round12/checks/`, and the decomposition `org/missions/D5/ETFS/ETFS_RIVALS/decompositions/ETFS_RIVALS_DECOMP.md`.

You WRITE only the `<paths>` below (plus `deliverables/0.9.0_WK_ETFS_RIVALS~2/`). NEVER: any S3 read or write, any deploy or gateway release, any Terraform, any change to the IAM policy or location files. A check you cannot satisfy without leaving your `<paths>` is a surprise row in the investigation file (`surfaced_at` = `date -u +%FT%TZ` at filing), never an edit outside them.

<paths>
infra/aws/ec2/opal-gateway/app/rivalfunds_view.py
infra/aws/ec2/opal-gateway/app/tests/test_rivalfunds_view.py
org/missions/D5/ETFS/ETFS_RIVALS/surprise-channel/investigations/INVESTIGATION_v1.Z.md
</paths>

## 4. PROOF OF SPEC (each invocation LITERAL, run from your worktree root)

- **AC1** -- GET /rivalfunds/2026-10-06/audit serves the stored audit.html under the view's headers; no viewer 401, bad date 400, missing 404; control: /rivalfunds/2026-10-06 still serves index.html (`org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round12/checks/gw-1.AC1.py`)

<proof_of_spec>
  <criterion id="AC1" cell_refs="RIV-gw-1"><invocation>python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round12/checks/gw-1.AC1.py</invocation><expect>AC1 RESULT: PASS 0 failures</expect></criterion>
</proof_of_spec>

## 5. WHEN YOU ARE DONE

Write the instance at `org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~2/ETFS_RIVALS.TO-RIV-gw-1.gateway-serves-audit-page.proof_of_spec.json` with `to_id` `ETFS_RIVALS.TO-RIV-gw-1.gateway-serves-audit-page`. Report once: the criterion's verdict line with the output above it; files written; the gateway test file's final line; rows filed (id + one line); the exact server.py Route line the issuer adds at the merge. Leave the `<status>` flip to the issuer.

<!-- ===================== RECORD FACE -- does NOT travel to the worker ===================== -->

**ISSUER NOTES (L5/L6, 2.0.0_SA_COO~RV):** ROUND_ANALYSIS.round10.md ADDENDUM 3 @8f1c1a9e6e item 2 (route B); Andrew-direct record @05c469e083; decomposition round 12 v1.0 (narrowed). Chain `~2`, slot `~2`, position 1 of 1. Check dry-run at base CLOUD 8f1c1a9e6e: gw-1.AC1 FAIL (2; control (c) PASS) as expected. Bounds: the gateway release that carries this route is an issuer act under its own never-widen pair (the gateway release path of NFRA_OPLGTW, last release rel-nfra-oplgtw-r20 @2c27f3a795); it lands BEFORE the publisher's split page.

<risk>SERVED</risk>
<worker_class>worker-light</worker_class>
<status>pending</status>
<round>12</round>
<slot>~2</slot>
<fabric>site-z</fabric>
