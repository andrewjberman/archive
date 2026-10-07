# BI3_METADATA -- does a frozen install with every entry cached contact the registry?

Answer: UNDETERMINED.

Read: the manifest-cache files in the cache root (227 `*.npm`, header `bun-npm-manifest-cache-v0.0.7`, mtimes 2026-09-01
to 2026-10-06) and `bun install --help` (bun 1.3.14). The `*.npm` files are a binary format that carries registry URLs
and (apparently) timestamps, but no documentation on this box says whether `--frozen-lockfile` consults them or revalidates
them when every extracted entry is cached; `--help` lists `--no-cache` ("Ignore manifest cache entirely") and nothing about
an offline mode or about when the registry is contacted. Deciding it from the binary format would be a guess about bun
internals; observing it needs a run with a network observer, which is barred. No read decides it.
