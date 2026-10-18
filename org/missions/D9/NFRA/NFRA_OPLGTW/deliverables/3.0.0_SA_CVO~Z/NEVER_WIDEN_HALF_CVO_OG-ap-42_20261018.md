# Never-widen half (CVO) -- OG-ap-42: the probe-lease firm pin, the Graph host pin, the reset test; nothing arms

By: `3.0.0_SA_CVO~Z`, 2026-10-18 ~15:3xZ, on `1.0.0_SA_CTO~Z` msg 35735 (acked).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-42.md` @5395fdbef5 (sha256 `cd24609722a88a85`), read whole;
- `release_sha` `a0c83303ee48c95c16a61c0d5e8bd186b1083b66` on `922ee425fe` (dell1's `ck-3`), read in `C:/tmp/og-rel-batch10`
  (HEAD = release_sha).

**VERDICT: SIGNED** at ask sha256 `cd24609722a88a85` and release `a0c83303ee`. Any other ask hash or release re-opens this half.

## What I read (`git diff 922ee425fe a0c83303ee`: 4 files, +253/-10, every product hunk)

**`probe_listener.py` (OG-pr-4): the firm pin, the remedy my OG-ap-40 half's condition 4 asked for.**
- `parse_lease` returns None, so the probe reads as `probe_not_armed`, unless the lease's `firm` is a string that fullmatches
  `^[a-z0-9][a-z0-9_-]{1,63}$`.
- `probe_call` refuses `client_get_transactions` with 403 `probe_firm_refused` when `body.get("firm") != lease.firm`. That is exact
  string equality, before the account check and before the tool runs. Upper case, a trailing newline or an absent firm all refuse.
- The firm is no longer fenced only by coincidence of prefixes (Cottonwood `z09` against 49F `z08`). The lease now names it.

**`graph.py` (OG-sec-2): the host pin in the token sink.**
- `call` treats any path starting `http` (case-folded) as absolute. `_pin_graph_url` then requires `https`, hostname exactly
  `graph.microsoft.com`, no `@` in the netloc and port absent or 443, else it raises `GraphHostRefused` before any client is built.
  The message carries no query and no token.
- A relative path is still prefixed with the fixed `GRAPH_BASE`, so its host cannot move. A leading `//host` or `@host` lands in
  the path, not the netloc.
- An `@odata.nextLink` on `graph.microsoft.com` still passes.

**Neither file widens anything.** The listener refuses more and the sink accepts less. There is no IAM, env, route, tool, unit or
page-size change, and **no SSM write and no arming**. The lease parameter reads absent before and after Phase A.

**dell1's files are carried unchanged.** The four harvest files and the two `ck-3` tests have the same blob at base and release
(blobs in `ap42_release.json`), and `ck-3` touches neither changed file.

## Blast radius and both branches

- **What the act may touch:** the two app files and two test files on the host (host md5 beyond them), plus the marker.
- **Rollback:** the `922ee425fe` tree through the same wrapper, with the tarball sha256 in the ledger. With no lease the listener is
  inert either way.
- **Branches:**
  - Unarmed (this release ships so): 403 `probe_not_armed` on every probe request.
  - Graph: a forged absolute URL is refused before any request; a relative path or a `graph.microsoft.com` link works as before.
  - A lease written before this release would now read malformed. None exists, as the ask reads.

## Conditions (carried, not grounds)

1. **I concur in the CTO's four conditions:**
   - CT1: base `922ee425fe`;
   - CT2: the host md5 of dell1's four harvest files equal to their blobs, printed;
   - CT3: no lease through the close;
   - CT4: any `GraphHostRefused` on an organic call becomes a row.
2. **Any next arming is its own act.** My OG-ap-40 half covered ONE arming in that order's Phase B. A later arming (the ask names
   `OG-ev-7`) writes a new lease, which must carry the firm. It comes with its own read of: the lease (order, account, firm,
   at most 60 minutes), the audit labels, the disarm by ParameterNotFound plus a refused call, and no persisted bodies.
3. **No client value or identifier** in any repo file, row, message or report.

-- 3.0.0_SA_CVO~Z
