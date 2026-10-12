# Ownership-map reads, legacy vs canonical (0.7.0_AE_CloudOps~FB1; COO msgs 4416, 4430, 4433)

## 15:00Z
LEGACY    s3://opal-data-bd/platinum/49financial/ownership_map.json | VersionId FcsnGhU7Rt280E9rmDacateI5WiK8S28 | LastModified 2026-10-12T05:22:13Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
CANONICAL s3://opal-data-49financial/advi/49financial/platinum/49financial/ownership_map.json | VersionId HXMgugyoEpzWQF_6VFAt.MMOklh53bK2 | LastModified 2026-10-12T07:29:12Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
read at 2026-10-12T15:00:04Z (target 2026-10-12T15:00:00Z): ownership maps byte-equal: True | legacy and canonical VersionIds printed above
RESULT: EQUAL

## 16:00Z
LEGACY    s3://opal-data-bd/platinum/49financial/ownership_map.json | VersionId FcsnGhU7Rt280E9rmDacateI5WiK8S28 | LastModified 2026-10-12T05:22:13Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
CANONICAL s3://opal-data-49financial/advi/49financial/platinum/49financial/ownership_map.json | VersionId HXMgugyoEpzWQF_6VFAt.MMOklh53bK2 | LastModified 2026-10-12T07:29:12Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
read at 2026-10-12T16:00:09Z (target 2026-10-12T16:00:00Z): ownership maps byte-equal: True | legacy and canonical VersionIds printed above
RESULT: EQUAL

## 16:16Z (with the closing reads)
LEGACY    s3://opal-data-bd/platinum/49financial/ownership_map.json | VersionId FcsnGhU7Rt280E9rmDacateI5WiK8S28 | LastModified 2026-10-12T05:22:13Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
CANONICAL s3://opal-data-49financial/advi/49financial/platinum/49financial/ownership_map.json | VersionId HXMgugyoEpzWQF_6VFAt.MMOklh53bK2 | LastModified 2026-10-12T07:29:12Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
read at 2026-10-12T16:16:08Z (target 2026-10-12T00:00:00Z): ownership maps byte-equal: True | legacy and canonical VersionIds printed above
RESULT: EQUAL

# Hours 17Z to 21Z, appended 2026-10-12T21:02Z (0.7.0_AE_CloudOps~FB1; COO msg 4508 added the validator log read)

Every ownership-map read below is EQUAL: legacy VersionId `FcsnGhU7Rt280E9rmDacateI5WiK8S28`, canonical `HXMgugyoEpzWQF_6VFAt.MMOklh53bK2`, 474,841 bytes, one sha256; neither VersionId moved.

## 17:00Z
```
LEGACY    s3://opal-data-bd/platinum/49financial/ownership_map.json | VersionId FcsnGhU7Rt280E9rmDacateI5WiK8S28 | LastModified 2026-10-12T05:22:13Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
CANONICAL s3://opal-data-49financial/advi/49financial/platinum/49financial/ownership_map.json | VersionId HXMgugyoEpzWQF_6VFAt.MMOklh53bK2 | LastModified 2026-10-12T07:29:12Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
read at 2026-10-12T17:00:14Z (target 2026-10-12T17:00:00Z): ownership maps byte-equal: True | legacy and canonical VersionIds printed above
RESULT: EQUAL

validator read at 17:00:45Z (window since 15:15:10Z): log groups found 7 across edge regions; events per region {'eu-central-1': 0, 'eu-west-1': 0, 'eu-west-2': 0, 'us-east-1': 0, 'us-east-2': 129, 'us-west-1': 0, 'us-west-2': 0}
  invocations by function Version: {'23': 27} | v23 lines: 27
  Auth OK lines: 27 | by path class: {'platinum/firm': 25, 'other': 2}
  denial markers: 0 | fetch_failed: 0
  first /platinum/accounts/ or /books/relationship/ request line: NONE YET
```

## 18:00Z
```
LEGACY    s3://opal-data-bd/platinum/49financial/ownership_map.json | VersionId FcsnGhU7Rt280E9rmDacateI5WiK8S28 | LastModified 2026-10-12T05:22:13Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
CANONICAL s3://opal-data-49financial/advi/49financial/platinum/49financial/ownership_map.json | VersionId HXMgugyoEpzWQF_6VFAt.MMOklh53bK2 | LastModified 2026-10-12T07:29:12Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
read at 2026-10-12T18:00:15Z (target 2026-10-12T18:00:00Z): ownership maps byte-equal: True | legacy and canonical VersionIds printed above
RESULT: EQUAL

validator read at 18:00:33Z (window since 15:15:10Z): log groups found 7 across edge regions; events per region {'eu-central-1': 0, 'eu-west-1': 0, 'eu-west-2': 0, 'us-east-1': 617, 'us-east-2': 311, 'us-west-1': 0, 'us-west-2': 0}
  invocations by function Version: {'23': 216} | v23 lines: 216
  Auth OK lines: 216 | by path class: {'platinum/firm': 137, 'other': 79}
  denial markers: 0 | fetch_failed: 0
  first /platinum/accounts/ or /books/relationship/ request line: NONE YET
```

## 19:00Z
```
LEGACY    s3://opal-data-bd/platinum/49financial/ownership_map.json | VersionId FcsnGhU7Rt280E9rmDacateI5WiK8S28 | LastModified 2026-10-12T05:22:13Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
CANONICAL s3://opal-data-49financial/advi/49financial/platinum/49financial/ownership_map.json | VersionId HXMgugyoEpzWQF_6VFAt.MMOklh53bK2 | LastModified 2026-10-12T07:29:12Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
read at 2026-10-12T19:00:03Z (target 2026-10-12T19:00:00Z): ownership maps byte-equal: True | legacy and canonical VersionIds printed above
RESULT: EQUAL

validator read at 19:00:37Z (window since 15:15:10Z): log groups found 7 across edge regions; events per region {'eu-central-1': 0, 'eu-west-1': 0, 'eu-west-2': 0, 'us-east-1': 998, 'us-east-2': 506, 'us-west-1': 0, 'us-west-2': 0}
  invocations by function Version: {'23': 349} | v23 lines: 349
  Auth OK lines: 349 | by path class: {'platinum/firm': 224, 'other': 125}
  denial markers: 0 | fetch_failed: 0
  first /platinum/accounts/ or /books/relationship/ request line: NONE YET
```

## 20:00Z
```
LEGACY    s3://opal-data-bd/platinum/49financial/ownership_map.json | VersionId FcsnGhU7Rt280E9rmDacateI5WiK8S28 | LastModified 2026-10-12T05:22:13Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
CANONICAL s3://opal-data-49financial/advi/49financial/platinum/49financial/ownership_map.json | VersionId HXMgugyoEpzWQF_6VFAt.MMOklh53bK2 | LastModified 2026-10-12T07:29:12Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
read at 2026-10-12T20:00:08Z (target 2026-10-12T20:00:00Z): ownership maps byte-equal: True | legacy and canonical VersionIds printed above
RESULT: EQUAL

validator read at 20:00:40Z (window since 15:15:10Z): log groups found 7 across edge regions; events per region {'eu-central-1': 16, 'eu-west-1': 0, 'eu-west-2': 0, 'us-east-1': 1464, 'us-east-2': 909, 'us-west-1': 0, 'us-west-2': 0}
  invocations by function Version: {'23': 559} | v23 lines: 559
  Auth OK lines: 554 | by path class: {'platinum/firm': 324, 'other': 230}
  denial markers: 0 | fetch_failed: 0
  first /platinum/accounts/ or /books/relationship/ request line: NONE YET
```

## 21:00Z
```
LEGACY    s3://opal-data-bd/platinum/49financial/ownership_map.json | VersionId FcsnGhU7Rt280E9rmDacateI5WiK8S28 | LastModified 2026-10-12T05:22:13Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
CANONICAL s3://opal-data-49financial/advi/49financial/platinum/49financial/ownership_map.json | VersionId HXMgugyoEpzWQF_6VFAt.MMOklh53bK2 | LastModified 2026-10-12T07:29:12Z | 474841 bytes | sha256 6367f1ed6a6633dd74c12c92915531d5103b30fef6063968693acd4a8b20fad2
read at 2026-10-12T21:00:07Z (target 2026-10-12T21:00:00Z): ownership maps byte-equal: True | legacy and canonical VersionIds printed above
RESULT: EQUAL

validator read at 21:00:43Z (window since 15:15:10Z): log groups found 7 across edge regions; events per region {'eu-central-1': 16, 'eu-west-1': 0, 'eu-west-2': 0, 'us-east-1': 1572, 'us-east-2': 1143, 'us-west-1': 0, 'us-west-2': 0}
  invocations by function Version: {'23': 635} | v23 lines: 635
  Auth OK lines: 630 | by path class: {'platinum/firm': 390, 'other': 240}
  denial markers: 0 | fetch_failed: 0
  first /platinum/accounts/ or /books/relationship/ request line: NONE YET
```

## Notes
- The validator reads count log lines of the `auth-validator-edge` groups in the edge regions since 15:15:10Z (counts only; the lines name other
  firms' users and are not copied). Version 23 throughout; 0 denial markers and 0 `fetch_failed` at every read; the first request line on a
  `/platinum/accounts/` or `/books/relationship/` path had NOT appeared by 21:00:43Z (the labelled residual of `0.7.0_AE_CloudOps~FBL`'s L6).
- Invocations 635 against 630 `Auth OK` lines at 21Z: the five without an `Auth OK` line emitted no other application line (a scan of every
  non-lifecycle, non-`Auth OK` line in the window returned 0).
- The first read of the series (16:57:56Z) read 27 invocations, 0 denial markers, 0 `fetch_failed`.
