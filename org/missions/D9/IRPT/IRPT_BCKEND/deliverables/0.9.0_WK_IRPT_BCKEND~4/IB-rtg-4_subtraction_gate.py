import json
import os
import subprocess

REPO = r"C:\tmp\wk-irpt-7-4-apply"
TF = os.path.join(REPO, ".tools", "terraform.exe")
SCRATCH = os.path.join(REPO, ".scratch")
TF_ROOT = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting")

ROOTS = ["api", "core", "directory", "export", "holdings", "intake", "narrative", "ops",
         "performance", "ycharts"]

# subtraction set: (i) plan's top-level .timestamp; (ii) S3 data-source version_id/last_modified
# wherever they appear in prior_state/relevant_attributes.
SUBTRACT_TOP = {"timestamp"}


def strip_volatile(obj, path=()):
    """Return (kept_paths_removed_count) after stripping the subtraction set IN PLACE conceptually;
    here we just count what WOULD be subtracted, without mutating, by walking prior_state trees for
    aws_s3_object data sources."""
    pass


def resource_changes_after_subtraction(planfile, root_dir):
    out = subprocess.run([TF, "-chdir=" + root_dir, "show", "-json", planfile],
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=REPO, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("terraform show failed rc=%d stderr=%s" % (out.returncode, out.stderr[:500]))
    j = json.loads(out.stdout)
    top_timestamp = j.get("timestamp")
    rcs = j.get("resource_changes") or []
    entries_compared = len(rcs)
    subtracted_paths = 0
    kept = []
    for rc in rcs:
        actions = rc["change"]["actions"]
        if actions == ["no-op"]:
            continue
        # subtract version_id/last_modified from S3 data-source entries (aws_s3_object)
        is_s3_object_ds = (rc.get("type") == "aws_s3_object" and rc.get("mode") == "data")
        entry = {
            "address": rc["address"],
            "type": rc.get("type"),
            "actions": actions,
            "before": (rc["change"].get("before") or {}),
            "after": (rc["change"].get("after") or {}),
        }
        if is_s3_object_ds:
            for side in ("before", "after"):
                for f in ("version_id", "last_modified"):
                    if f in entry[side]:
                        del entry[side][f]
                        subtracted_paths += 1
        kept.append(entry)
    return {
        "top_timestamp_subtracted": bool(top_timestamp),
        "entries_compared": entries_compared,
        "substantive_changes": kept,
        "subtracted_paths_this_root": subtracted_paths,
    }


def main():
    total_entries = 0
    total_subtracted = 1  # count the top-level .timestamp field itself, subtracted once per root read... see below
    total_subtracted = 0
    report = {}
    for root in ROOTS:
        pf = os.path.abspath(os.path.join(SCRATCH, "ib_rtg_4_%s.tfplan" % root))
        root_dir = os.path.join(TF_ROOT, root)
        r = resource_changes_after_subtraction(pf, root_dir)
        # top .timestamp subtraction counts as 1 path per root (it is always present in a fresh plan)
        r["subtracted_paths_this_root"] += (1 if r["top_timestamp_subtracted"] else 0)
        total_entries += r["entries_compared"]
        total_subtracted += r["subtracted_paths_this_root"]
        report[root] = r
        print("=" * 100)
        print("ROOT:", root)
        print("  entries_compared (resource_changes, whole):", r["entries_compared"])
        print("  paths subtracted this root (timestamp + s3-object version_id/last_modified):",
              r["subtracted_paths_this_root"])
        print("  substantive (non-no-op) changes after subtraction: %d" % len(r["substantive_changes"]))
        for c in r["substantive_changes"]:
            b_hash = c["before"].get("source_code_hash")
            a_hash = c["after"].get("source_code_hash")
            print("    %-70s actions=%s" % (c["address"], c["actions"]))
            if b_hash is not None or a_hash is not None:
                print("        source_code_hash: %s -> %s" % (b_hash, a_hash))
            # print any OTHER changed top-level keys besides source_code_hash/s3_object_version/handler
            other_keys = set()
            for k in c["before"]:
                if c["before"].get(k) != c["after"].get(k):
                    other_keys.add(k)
            for k in c["after"]:
                if c["before"].get(k) != c["after"].get(k):
                    other_keys.add(k)
            allowed = {"source_code_hash", "s3_object_version", "handler", "last_modified",
                       "policy", "id", "name", "tags", "tags_all"}
            unexpected = sorted(k for k in other_keys if k not in allowed)
            if unexpected:
                print("        OTHER CHANGED KEYS (not in the allow-list, needs manual review): %s" % unexpected)

    print()
    print("=" * 100)
    print("DENOMINATOR: entries compared across all %d roots = %d; paths subtracted = %d"
          % (len(ROOTS), total_entries, total_subtracted))

    with open(os.path.join(SCRATCH, "subtraction_gate_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, default=str)


if __name__ == "__main__":
    main()
