"""Run every round-6 check file once at the base and grade its FULL output against the order's own <expect>.

Spine v3.19 L6: a build check FAILS at the base, a bound or control check PASSES there. One line per check; the issuance
commit cites the log this writes to stdout.
"""
import datetime
import glob
import re
import subprocess
import time

ROOT = "org/missions/D5/AMGT/AMGT_CORPUS"
CRITERION_RE = re.compile(
    r'<criterion id="(AC\d)"[^>]*><invocation>(.*?)</invocation><expect>(.*?)</expect></criterion>', re.S
)


def run_check(script):
    try:
        result = subprocess.run(
            ["bash", script], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600
        )
        return result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired as exc:
        return (exc.stdout or "") + (exc.stderr or ""), 124


def main():
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    print("base run at", datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "HEAD", head)
    for order in sorted(glob.glob(ROOT + "/task-orders/AMGT_CORPUS.TO-CRPS-h-*.md")):
        text = open(order, encoding="utf-8").read()
        cell = re.search(r"<owned_cells>(.*?)</owned_cells>", text).group(1)
        for match in CRITERION_RE.finditer(text):
            cid, invocation, expect = match.group(1), match.group(2), match.group(3)
            script = re.search(r"bash (\S+\.sh)", invocation).group(1)
            started = time.time()
            out, rc = run_check(script)
            kept = [line for line in out.splitlines() if "fitz" not in line and "MuPDF" not in line]
            out = "\n".join(kept)
            verdict = "PASS" if re.search(expect, out) else "FAIL"
            last = kept[-1][:140] if kept else "(no output)"
            print("%s %s BASE %s | rc %s | %ds | %s" % (cell, cid, verdict, rc, int(time.time() - started), last))


if __name__ == "__main__":
    main()
