# BI3_MARK -- what marks a finished bun cache entry (OG-bi-3)

Read-only, with Python os.listdir / open, on the real cache (948 root names: 721 entry directories, 227 `*.npm` files).

- bun's own record of a finished entry: NONE readable without bun. The cache root has no index or dotfile. The 227
  `*.npm` files are bun's npm MANIFEST cache (header `bun-npm-manifest-cache-v0.0.7`, binary), one per package name; they
  describe the registry's metadata, not whether an extracted entry is complete. Entry directories hold only the
  package's own files (for example gensync: index.js, index.js.flow, LICENSE, package.json, README.md, test; react:
  cjs, index.js, package.json, ...). No completion marker file is inside them.
- Mark relied on (the order's second candidate): the entry directory is non-empty AND holds a `package.json` that parses
  as a JSON object with string `name` and `version` equal to the lockfile entry's name and EXACT version string.
  Reason words: absent (no directory), empty (directory with nothing in it), no-manifest (no / unparseable / name-or-version
  not a string), version-mismatch (parses but names another name or version).
- Prerelease: bun's directory name carries a hash of the tag that is not reproduced; every `<x.y.z>-<hash>@@@1` directory
  is a candidate and the entry passes only if one's package.json carries the exact version. This closes OG-bi-1's
  prefix weakness (a different prerelease of the same x.y.z no longer passes).

## What it proves and does not prove

- Proves: an empty or manifest-less folder, or one holding another version, is not counted as cached.
- Does NOT prove: that the other files in the entry are present or uncorrupted (a partial extraction that kept
  package.json passes, and package.json is not necessarily the first file bun writes); and not that `bun install` will not
  fetch for some other reason (see BI3_METADATA.md).

## Integrity value

The lockfile's `sha512-...` is the hash of the registry TARBALL. The cache holds the extracted tree, no tarball and no
stored hash that I found, so the integrity value is NOT checkable against anything in the cache. Not checked.
