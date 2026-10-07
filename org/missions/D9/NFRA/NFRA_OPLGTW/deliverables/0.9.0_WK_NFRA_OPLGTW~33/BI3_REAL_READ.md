# BI3_REAL_READ -- the new pre-check against the real lockfile and the real cache

Lockfile: `git -C <main repo>/mcportal show a3bff71ffa3f5c73aa0fb7ea1e7386434e233054:bun.lock`
(`services.opal-gateway.mcportal_commit` of infra/aws/ec2/EC2_MANIFEST.json). Cache: bun's default
(`pc.default_cache()`), read only. Command: `python infra/aws/ec2/opal-gateway/ops/bun_cache_precheck.py <lock>`.

Output: `77 of 77`, exit 0. Entries reported missing: NONE (0). Equal to the first cell's `77 of 77` (BI1_REAL_READ.md).
Every one of the 77 entries has a non-empty directory with a package.json naming the exact name and version.
