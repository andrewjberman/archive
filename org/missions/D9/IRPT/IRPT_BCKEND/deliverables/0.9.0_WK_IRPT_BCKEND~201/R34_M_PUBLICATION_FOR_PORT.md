# R34 ~M -- holdings_publication_for (TO-IB-m34-341)

Code: `holdings/snapshot.py` `holdings_publication_for(s3_client=None)` (commit dd546a3c02); test `holdings/tests/test_publication_port.py` (dd546a3c02, 47f9c3b27a).

Criteria, last printed lines:
- IBM34-341-AC1: `OK: holdings_publication_for fences 3 of 3 firms, refuses 5 of 5 bad firms, capture/load_pinned meet the reader` / `IBM34-341-AC1 PASS`
- IBM34-341-AC2: `OK: _scope 223 passed, 67 subtests passed in 3.98s` / `IBM34-341-AC2 PASS` (first run FAILED 4 holdings tests: my test matched PublicationRefused by class and a sibling suite loads a second `publication` module; fixed in 47f9c3b27a, holdings 182 passed)
- IBM34-G-201: `OK: 2 changed path(s), all inside slot ~201's grant` / `IBM34-G-201 PASS`

## S3 read set (code read only, no AWS call)
Bucket: per firm, `opal-data-<firm>` for 49financial, inflection, cottonwood (address builder, product irpt; table `holdings`).
Keys under `irpt/<firm>/platinum/holdings/`:
- `current/manifest.json` (index; read WITHOUT VersionId in begin(); capture only)
- `date=<YYYY-MM-DD>/<revision>.manifest.json` (dated manifest, read with VersionId)
- `date=<YYYY-MM-DD>/<revision>.json` (manifest v1 snapshot body, VersionId)
- `date=<YYYY-MM-DD>/<revision>.header.json` and `<revision>.part%05d.json` (manifest v2, VersionId)
- load_pinned reads the index by the receipt's version_id (VersionId), never the current one.
The gold key (`irpt/<firm>/gold/holdings/...parquet`) is only reference-validated, never fetched.
Actions: s3:GetObject (unversioned on current/manifest.json; with VersionId on the rest). Reads with VersionId: s3:GetObjectVersion is required in addition to s3:GetObject for versioned GETs. No List, no Put.
