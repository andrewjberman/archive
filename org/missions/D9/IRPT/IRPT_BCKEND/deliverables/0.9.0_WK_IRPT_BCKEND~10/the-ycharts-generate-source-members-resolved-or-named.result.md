# IB-rti-2 result -- 0.9.0_WK_IRPT_BCKEND~10

## Resolution table (arm resolve; full output in ac1_output.txt)
Denominator: declared files[] = 32, live zip members = 31 (`get-function` package, CodeSha256 1L60sG1G9IaF..., LastModified 2026-09-19T14:29:32Z).
The 32-vs-31 difference, by name: declared-not-live = `raw_keys.json` (declared after the live build); live-not-declared = none. Both `firm_registry.json` and `settings.json` ARE in the live zip.

- `settings.json`: tracked source `infra/aws/lambda/investor-reporting/intake/settings.json` (same blob at HEAD and at dc5d119b84). Live bytes = that blob with CRLF (sha256 a05bcea4...). RESOLVED, CRLF-only difference.
- `firm_registry.json`: tracked at `data/firm_registry.json` in commit 1f54e16dfd (git blob 7c483504766345e4c73a7aad355ba9e5ca1e3edc). Live bytes = that blob with CRLF (sha256 cc3f2c63...). The HEAD version of that path is NOT the source (a generated view with an added `_generated` line, sha 5a4c0c3d...). RESOLVED at a historical pin, CRLF-only difference. Row S34's "no blob in history" is false (row W10-S1).

## Branch taken in (b)
The declare branch: two `staged_from` entries added to the `irpt-ycharts-generate` entry (pins 1f54e16dfd and dc5d119b84, sha256 of the LF blob, verified by the builder's own logic). No live bytes were committed as a file. Stated judgment call: both members differ from live by line endings only (git blob is LF, live JSON members were CRLF worktree copies); I treated that as RESOLVED with the difference named, and left whether it meets "byte-identical" to `3.0.0_SA_CVO~B` (R92-AC3).

## Rebuild (arm rebuild; ac2_output.txt), LOCAL only
32 members built; 27 identical; CRLF-only: custodian_key_seam.json, firm_registry.json, settings.json; REBUILT-ONLY: raw_keys.json; **UNEXPLAINED-as-no-behaviour-change: `loaders.py`** -- the entry pins IB-rth-1's 385aff4646 edit, the live zip serves the 39cbad4214 version (sha 49c290f6ac45). Rebuilding and serving that would change served behaviour, so R92-AC2 prints NO token; the order stays open. Nothing uploaded, nothing applied. Row W10-S2.

## Rows
W10-S1 (S34 premise false, CRLF class), W10-S2 (loaders.py content difference), W10-S3 (stale `_staged_from_note` left unedited under the order's bound). Runtime necessity of the members is not decided here (function env `IRPT_FIRM_REGISTRY=/var/task/firm_registry.json`; live zip has no raw_keys.json).
