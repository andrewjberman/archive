"""OG-rl-14 Phase B: scan the whole deploy output (read-only) for (1) the build log's download/fetch lines between `building mcportal` and the build's end, (2) the host pip step's counts.
usage: python r28c_scan_deploy.py <deploy.out> <cache_before.out> <cache_after.out> <cache_count_raw.json> <RL14_BUN_CACHE.json out> <host_pip.json out>
Prints the spans and counts it measured; judges nothing."""
import json
import re
import sys

dep, cb, ca, cc, out_bun, out_pip = sys.argv[1:7]
raw = open(dep, encoding="utf-8", errors="replace").read()
ansi = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
lines = [ansi.sub("", ln).replace("\r", "\n") for ln in raw.split("\n")]
lines = [x for ln in lines for x in ln.split("\n")]
print("deploy output lines (ANSI stripped, CR split):", len(lines))

i0 = next((i for i, ln in enumerate(lines) if "building mcportal" in ln), None)
print("line index of 'building mcportal':", i0)
# the build's end: the vite 'built in' line (or the line that reports the dist copy), whichever is first after the start
i1 = None
if i0 is not None:
    for i in range(i0, len(lines)):
        if re.search(r"\bbuilt in\b", lines[i]):
            i1 = i
            break
print("line index of the build's end ('built in'):", i1)
span = lines[i0:(i1 + 1 if i1 is not None else len(lines))] if i0 is not None else []
# after the build: lines up to the `INFO:` that follows the build, to show nothing else downloads before the upload
pat = re.compile(r"download|fetch|GET http|https?://|resolving|registry|npmjs|manifest for|saved lockfile|Extracted|\bcurl\b|wget", re.I)
hits = [ln.strip() for ln in span if pat.search(ln)]
print("build span lines:", len(span), " download/fetch pattern hits:", len(hits))
for h in hits:
    print("  HIT:", h[:200])
print("--- build span, first 12 and last 12 lines (for the record) ---")
for ln in span[:12]:
    print("  |", ln[:160])
print("  ...")
for ln in span[-12:]:
    print("  |", ln[:160])

# host pip step
ia = sum(1 for ln in lines if re.search(r"already satisfied", ln, re.I))
ic = [ln.strip() for ln in lines if re.match(r"\s*Collecting\b", ln)]
idl = [ln.strip() for ln in lines if re.match(r"\s*Downloading\b", ln)]
ic_any = [ln.strip() for ln in lines if re.search(r"\bCollecting\b", ln)]
idl_any = [ln.strip() for ln in lines if re.search(r"\bDownloading\b", ln)]
print("host pip: already satisfied lines=%d  Collecting lines (anchored)=%d (anywhere)=%d  Downloading lines (anchored)=%d (anywhere)=%d" % (ia, len(ic), len(ic_any), len(idl), len(idl_any)))
for x in ic_any + idl_any:
    print("  PIP LINE:", x[:200])
# the pip block context
pi = [i for i, ln in enumerate(lines) if "pip install" in ln or "Requirement already satisfied" in ln]
print("pip-related line indexes: first", pi[:1], "last", pi[-1:], "count", len(pi))

sz_b = json.loads(open(cb, encoding="utf-8").read().split("R28C_CACHE_SIZE ", 1)[1])
sz_a = json.loads(open(ca, encoding="utf-8").read().split("R28C_CACHE_SIZE ", 1)[1])
cnt = json.load(open(cc, encoding="utf-8"))
doc = {"deploy_started_utc": cnt["deploy_started_utc"], "entries_counted": cnt["entries_counted"], "entries_touched_since_start": cnt["entries_touched_since_start"],
       "bytes_before": sz_b["bytes"], "bytes_after": sz_a["bytes"], "files_before": sz_b["files"], "files_after": sz_a["files"],
       "build_log_download_lines": {"count": len(hits), "lines": hits},
       "basis": cnt["basis"], "size_basis": "every file of bun's install cache to full depth (os.walk, lstat st_size); read at " + sz_b["read_at"] + " (immediately before the deploy command) and " + sz_a["read_at"] + " (right after it returned)",
       "build_span": {"from": "line containing 'building mcportal'", "to": "line containing 'built in'", "lines": len(span)}}
json.dump(doc, open(out_bun, "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
pipdoc = {"already_satisfied": ia, "Collecting": len(ic_any), "Downloading": len(idl_any), "collecting_or_downloading_package_names": [x[:120] for x in ic_any + idl_any]}
json.dump(pipdoc, open(out_pip, "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
print("wrote", out_bun, out_pip)
print(json.dumps(doc, sort_keys=True)[:700])
