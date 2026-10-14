"""Assemble IB196-1_closure_record.json from the scratch measurements (no network, no AWS).

The closure is read by ast from the pin working tree core file; the traced files come from the three trace runs;
the import proof comes from import_proof.json (per-member detail dropped from the tracked record).
"""
import ast
import json
from pathlib import Path

SCR = Path("C:/dev/_scratch385")
WT = Path("C:/dev/wk-IRPT_BCKEND-385")
OUT = WT / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~385/IB196-1_closure_record.json"
MISSING = "data/assets/scripts/silver/opal_unidentified.py"
FIRMS = ["49financial", "cottonwood", "inflection"]

src = Path("C:/dev/wk-ib540-pin/.tools/safe_deploy_core.py").read_text(encoding="utf-8")
closure = None
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_IRPT_HOLDINGS_CLOSURE" for t in node.targets):
        closure = [e.value for e in node.value.elts if isinstance(e, ast.Constant)]
assert closure and len(closure) == len(set(closure)) == 46, len(closure or [])

traces = {f: json.loads((SCR / ("trace_%s.json" % f)).read_text(encoding="utf-8")) for f in FIRMS}
traced = set()
for f in FIRMS:
    traced |= set(traces[f]["traced"])
missing = sorted(traced - set(closure))
extra = sorted(set(closure) - traced)
assert missing == [] and extra == [], (missing, extra)

old = json.loads((SCR / "old/members.json").read_text(encoding="utf-8"))
new = json.loads((SCR / "new/members.json").read_text(encoding="utf-8"))
delta_added, delta_changed, delta_removed = set(), set(), set()
for f in FIRMS:
    om, nm = old[f]["members"], new[f]["members"]
    delta_added |= set(nm) - set(om)
    delta_removed |= set(om) - set(nm)
    delta_changed |= {k for k in set(om) & set(nm) if om[k] != nm[k]}
index_changed = sorted(delta_changed & {"SHA256SUMS"})
closure_changed = sorted(delta_changed - {"SHA256SUMS"})
assert sorted(delta_added) == [MISSING] and closure_changed == [] and not delta_removed, (delta_added, closure_changed, delta_removed)
added_sha = new["49financial"]["members"][MISSING]

ip = json.loads((SCR / "import_proof.json").read_text(encoding="utf-8"))
import_proof = {}
for f in FIRMS:
    rec = ip[f]
    import_proof[f] = {
        "python_flags": rec["python_flags"],
        "members_imported": rec["members_imported"],
        "import_errors": rec["import_errors"],
        "bundle_tree_members": rec["bundle_tree_members"],
    }

record = {
    "base_commit": "0d7cf141bdcf50b3681cae14401eb14f13f48f83",
    "base_pin": "49467335d288d5c0012fe339c4cafcb74bd43fb5",
    "new_pin": None,
    "new_pin_status": "NOT CREATED. The pin commit on branch pin-ib-pr-540 was refused at commit time by the TO issuance gate (surprise row IRPT_BCKEND-D2-W385-S1). The edited core file is uncommitted in the pin worktree, blob a09879f2f8d223a71b58889ec0283e1cc1878541. Every measurement below was taken from that uncommitted working tree, whose only difference from the old pin is the two-line closure edit.",
    "new_core_blob": "a09879f2f8d223a71b58889ec0283e1cc1878541",
    "import_proof": import_proof,
    "closure_vs_trace": {
        "traced_files": sorted(traced),
        "missing": missing,
        "extra": [],
    },
    "bundle_delta": {
        "members_added": [MISSING],
        "members_changed": closure_changed,
        "members_removed": sorted(delta_removed),
        "generated_index_changed": index_changed,
        "added_member_sha256": added_sha,
        "per_firm_members": {f: {"old": len(old[f]["members"]), "new": len(new[f]["members"])} for f in FIRMS},
        "payload_sha256_identical_across_firms": len({new[f]["payload_sha256"] for f in FIRMS}) == 1,
    },
    "notes": [
        "base_commit is the worktree HEAD before this worker's first commit (0d7cf141bd); new_pin is null because the pin commit was refused (IRPT_BCKEND-D2-W385-S1), so AC1 to AC3 cannot pass on this record and no check was edited.",
        "Bundles: core.find_bundle and core.build_bundle_payload were called from each tree's own .tools (WORKSPACE is the tree), no upload. Old pin from a detached worktree at 49467335d2; new from the pin worktree's uncommitted core edit. Member counts: old 46 closure plus SHA256SUMS = 46 entries, new 47 (46 closure plus SHA256SUMS); the three firm payloads are byte-identical in each tree.",
        "bundle_delta: the one added member is data/assets/scripts/silver/opal_unidentified.py. Over the 46 closure members no member is changed or removed (45 unchanged members have identical sha256). SHA256SUMS, the generated index, changes by exactly one added line (the sha256 of the added member); it is reported as generated_index_changed and not counted as a closure change (IRPT_BCKEND-D2-W385-S2).",
        "import_proof: for each firm, every .py closure member (34) was imported in its own python -I -c process; the sys.path given to the process is every directory holding a closure .py member plus the tree's lib directory; each module counted as imported only when its __file__ resolves to the member path inside that firm's extracted tree. Zero import errors per firm. The 12 non-.py closure members (json and schema files) are data, not imported.",
        "bundle_tree_members counts every file in the extracted tree except __pycache__ directories (which the -I interpreter writes) = 46 closure members plus SHA256SUMS = 47.",
        "closure_vs_trace: each firm ran one real read-only build, holdings_snapshot.build_snapshot with VersionedInputs over a boto3 S3 client wrapped to pass only get_, list_ and head_ (refused operations: none). Traced files are the union of files opened under the tree (open audit hook) and module files in sys.modules, excluding __pycache__ and SHA256SUMS. The union is the closure exactly: missing empty, and extra empty (every closure member was touched by at least one of the three runs).",
        "Build counts per firm (not identifiers): 49financial 22 S3 get calls, cottonwood 20, inflection 20; node counts 156504, 17966 and 36702 (inflection matches the issuer's earlier 36,702). The read-only S3 wrapper refused no operation.",
        "Not read or not done: no bundle was minted, uploaded, applied, signed or invoked; no packet was signed; no row was written in any other file than this worker's own investigation channel; no client identifier, holding name, position value or account id is in this record. Producer-created service clients (other than the S3 client passed in) are not wrapped by this harness and were not separately measured.",
        "The trace and build stderr (which name securities) stayed in scratch and are not quoted here.",
        "rows_written counts table or warehouse rows written to any store and is 0. The two surprise-channel rows (IRPT_BCKEND-D2-W385-S1 and S2) are investigation rows in the project channel file, not table rows.",
    ],
    "functions_invoked": 0,
    "sign_ins_made": 0,
    "aws_writes_made": 0,
    "rows_written": 0,
    "figures_written": 0,
    "vendor_requests_sent": 0,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="utf-8")
print("WROTE", OUT, "closure", len(closure), "traced", len(traced), "missing", missing, "extra", extra)
