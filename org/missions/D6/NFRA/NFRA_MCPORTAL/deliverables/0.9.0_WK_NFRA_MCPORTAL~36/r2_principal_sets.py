"""MP-pf-6 comparator: the principals the Scan of the grant store returns, against the principals in the grant
writer's own change history. Python 3.9, standard library only.

compare(scan_set, history_set) returns the counts and the verdict. Two empty sets are NOT evidence of equality:
`vacuous` is true when both are empty and `equal` is then false.

CLI: python r2_principal_sets.py --from-read <file> --out r2_run.json
  <file> is the stdout of the issuer's read step (pf6.run.sh): one line `ssm command=<id> status=<s>` and, when the
  read worked, one line `R2 {json}`. The output file holds the counts and the verdict only, never a raw set.
"""
import argparse
import json
import sys


def compare(scan_set, history_set):
    scan = set(scan_set)
    history = set(history_set)
    only_scan = scan - history
    only_history = history - scan
    vacuous = not scan and not history
    equal = (not only_scan) and (not only_history) and (not vacuous)
    return {
        "scan_n": len(scan),
        "history_n": len(history),
        "only_scan_n": len(only_scan),
        "only_history_n": len(only_history),
        "equal": equal,
        "vacuous": vacuous,
    }


def _parse_read(text):
    """Return (ssm_command, ssm_status, r2_dict_or_None, error_line_or_None)."""
    ssm_command = None
    ssm_status = "NONE"
    r2 = None
    last_line = None
    no_r2_line = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        last_line = line
        if line.startswith("ssm command="):
            parts = line.split()
            for part in parts:
                if part.startswith("command="):
                    ssm_command = part[len("command="):]
                elif part.startswith("status="):
                    ssm_status = part[len("status="):]
        elif line.startswith("R2 "):
            if r2 is None:
                r2 = json.loads(line[len("R2 "):])
        elif line.startswith("no R2 line"):
            no_r2_line = line
    if r2 is not None:
        return ssm_command, ssm_status, r2, None
    error = no_r2_line if no_r2_line is not None else (last_line or "empty read output")
    return ssm_command, ssm_status, None, error


def main(argv=None):
    ap = argparse.ArgumentParser(description="MP-pf-6 principal-set comparator")
    ap.add_argument("--from-read", required=True, help="stdout of pf6.run.sh")
    ap.add_argument("--out", required=True, help="run file to write (r2_run.json)")
    args = ap.parse_args(argv)

    with open(args.from_read, encoding="utf-8") as fh:
        text = fh.read()
    ssm_command, ssm_status, r2, error = _parse_read(text)

    if r2 is None:
        out = {"ssm_status": ssm_status, "ssm_command": ssm_command, "error": error}
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2)
            fh.write("\n")
        print("ERROR: no R2 line; wrote %s" % args.out)
        return 2

    cmp_result = compare(r2.get("scan_set") or [], r2.get("history_set") or [])
    out = {
        "ssm_status": ssm_status,
        "ssm_command": ssm_command,
        "scan_n": r2.get("scan_n"),
        "history_n": r2.get("history_n"),
        "history_items": r2.get("history_items"),
        "history_pages": r2.get("history_pages"),
        "history_unparsed_items": r2.get("history_unparsed_items"),
        "only_scan_n": cmp_result["only_scan_n"],
        "only_history_n": cmp_result["only_history_n"],
        "equal": cmp_result["equal"],
        "vacuous": cmp_result["vacuous"],
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print("OK: wrote %s equal=%s only_scan_n=%s only_history_n=%s vacuous=%s"
          % (args.out, out["equal"], out["only_scan_n"], out["only_history_n"], out["vacuous"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
