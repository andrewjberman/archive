# PLANTED TOMBSTONE -- F6-AC5 CONTROL, complete except `served_source`

This specimen exists to be CAUGHT. It carries six of the seven fields F6-AC5
names and omits `served_source` -- the field that tells a future reader what to
read INSTEAD of the retired artifact, which is the one omission a
"does the file exist and parse" check would sail past. If the parser reports
`MISSING_FIELDS=NONE` here, the real tombstone's PASS is a constant.

```json
{
  "tombstone_version": 1,
  "written_by": "PLANTED -- not a real tombstone",
  "task_order": "PLANTED",
  "authority": [
    "PLANTED: a specimen, not an authority"
  ],
  "archive_keys": [
    "archive/PLANTED/planted_store"
  ],
  "archive_sha256": {
    "archive/PLANTED/planted_store": {
      "sha256_hex": "0000000000000000000000000000000000000000000000000000000000000000",
      "size_bytes": 1
    }
  },
  "manifest": {
    "artifact": "planted_store._build_manifest.json",
    "content": {
      "artifact_claim": "planted"
    }
  },
  "bytes_vs_manifest": "PLANTED: a specimen value so the field is present",
  "builder_last_hash": "0000000000000000000000000000000000000000"
}
```
