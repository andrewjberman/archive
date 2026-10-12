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
