# OG-bi-1 -- the one real read

Read-only. Lockfile: `git -C <main repo>/mcportal show a3bff71ffa3f5c73aa0fb7ea1e7386434e233054:bun.lock`
(`services.opal-gateway.mcportal_commit`, EC2_MANIFEST.json; 278 lines; copied to a scratch file, nothing checked out).
Cache: bun's real default, `%USERPROFILE%/.bun/install/cache` (948 top-level entries), read with `os.path.isdir` only.

```
python infra/aws/ec2/opal-gateway/ops/bun_cache_precheck.py <that bun.lock>
77 of 77
exit=0
```

Host as the program read it: win32 / x64. 77 matches the `77 packages installed` of the r27 deploy output.
Missing: none. The 50 entries of other platforms (esbuild, rollup, fsevents, lzma) were excluded by their os/cpu fields,
not by being present. 2 of the 77 are prereleases and were matched by prefix (see BI1_MECHANISM.md).
The first run, before the os/cpu and prerelease rules, read 75 of 127 with 52 listed; those were the rules being absent,
not missing packages.
