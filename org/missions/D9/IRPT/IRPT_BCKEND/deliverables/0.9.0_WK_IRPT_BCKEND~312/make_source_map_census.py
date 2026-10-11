"""IB-pr-456 source-map census (ASCII). From the worktree root:
    python <this file> <out_json> [<map_ref>]
Parses the WHOLE map at <map_ref> (default HEAD), counts every function entry, and places each as packaging or not
packaging any of the three changed members, by files[] (resolved to the repo path the member is packaged from), by
staged_from (repo_path equal to a member, or a directory that contains one) and by source_dir (the entry's source_dir
IS or CONTAINS a member's directory, with a files[] name that resolves to it). A looser name-only hit (a files[] basename
equal to a member's basename that does NOT resolve to the member's repo path) is recorded separately as name_only_not_the_member."""
import json
import subprocess
import sys

OUT = sys.argv[1]
REF = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
G = "infra/aws/lambda/investor-reporting/ycharts/generate/"
MEMBERS = {"submission.py": G + "submission.py", "acceptance.py": G + "acceptance.py",
           "AnalysisSubmissionRequest.schema.json": "docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json"}
raw = subprocess.run(["git", "show", REF + ":infra/aws/lambda/ci/lambda-source-map.json"], capture_output=True, check=True).stdout.decode("utf-8")
fns = json.loads(raw)["functions"]
rows, hits = [], []
for name, e in fns.items():
    sd = (e.get("source_dir") or "").strip("/")
    files = e.get("files") or []
    staged = e.get("staged_from") or []
    by_files, by_staged, by_sd, name_only = [], [], [], []
    packaged_as = {s["packaged_as"]: s["repo_path"] for s in staged}
    for s in staged:
        for k, p in MEMBERS.items():
            if s["repo_path"] == p or p.startswith(s["repo_path"].rstrip("/") + "/"):
                by_staged.append({"member": k, "packaged_as": s["packaged_as"], "pin": s["pin"][:10]})
    for f in files:
        resolved = packaged_as.get(f) or (sd + "/" + f if sd else f)
        for k, p in MEMBERS.items():
            if resolved == p:
                by_files.append({"member": k, "files_entry": f, "resolved_repo_path_is_member": True})
            elif f.split("/")[-1] == k and resolved != p:
                name_only.append({"member": k, "files_entry": f, "resolves_to": resolved})
    for k, p in MEMBERS.items():
        pd = p.rsplit("/", 1)[0]
        if sd and (sd == pd or pd.startswith(sd + "/")):
            by_sd.append({"member": k, "source_dir": sd, "kind": "source_dir_is_member_dir" if sd == pd else "source_dir_contains_member_dir"})
    packages = sorted({x["member"] for x in by_files} | {x["member"] for x in by_staged})
    row = {"function": name, "source_dir": sd, "packages": packages}
    if by_files:
        row["by_files"] = by_files
    if by_staged:
        row["by_staged_from"] = by_staged
    if by_sd:
        row["by_source_dir"] = by_sd
    if name_only:
        row["name_only_not_the_member"] = name_only
    if packages:
        hits.append(row)
    elif by_sd or name_only:
        rows.append(row)
doc = {"map_ref": REF, "entries_scanned": len(fns), "entries_packaging_a_changed_member": len(hits),
       "members": MEMBERS, "functions_packaging": hits, "near_misses_not_packaging": rows}
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(doc, indent=1) + "\n")
print("scanned=%d packaging=%d near_misses=%d" % (len(fns), len(hits), len(rows)))
for h in hits:
    print(h["function"], h["packages"], "files" if h.get("by_files") else "", "staged" if h.get("by_staged_from") else "", "sd" if h.get("by_source_dir") else "")
for r in rows:
    print("NEAR", r["function"], r["source_dir"], [x["member"] for x in r.get("by_source_dir", [])], r.get("name_only_not_the_member", [])[:2])
