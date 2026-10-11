# The issuer's rendered-read and walk template (round 96)

Added on the CTO's round-95 note 2 (the CVO's walk hygiene): **a read or walk that starts its OWN dev server writes that server's stdout and stderr to a file in the evidence folder**
(`<evidence dir>/devserver.log`), so the next proxy fault is READ, not inferred (round 95's C-S82 reading named this as its deciding source and could not read it).

1. Evidence folder: `deliverables/2.0.0_SA_COO~R1/<round>_prep/` (or the walk's own `tmp/ui-walk/<stamp>/`).
2. Start the dev server as `bun run dev --port 5174 > <evidence dir>/devserver.log 2>&1` (dev builds use port 5174 only; resolve bun via the profile).
3. Keep the log with the evidence and cite its path in the packet; a 5xx the walk records is matched to its `http proxy error` line by path and time.
4. The server-render instrument (`r94_peers_units.cjs`, react-dom/server over the real component) starts no server and needs no log.
