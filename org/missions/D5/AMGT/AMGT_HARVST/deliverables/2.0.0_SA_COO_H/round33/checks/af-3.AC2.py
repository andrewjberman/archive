"""HVST-af-3 AC2 (issuer, read-only): the FWD-14 depth table over GOLD, with the universe-to-gold key join fixed (Z-S51).

Runs `python -m lib.opal_data_harvest.depth_census` (the cell's module) and grades its printed lines:
- `DENOMINATOR: 89` (the collector universe);
- `MAPPED: <k> of 89` and one `UNMAPPED <universe key> <reason>` line per name not mapped (k + unmapped lines = 89);
- `SOURCE: gold <newest article_security_mention part key>` (the census reads the served gold, not silver);
- `AT 50+: <n> of 89` and `AT 100+: <m> of 89` (Andrew's bar, reported, never re-based).
PASS requires all of these, MAPPED k >= 80, and that the module made no S3 write (it prints `S3 WRITES: 0`).
"""
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()


def main():
    failures = []
    p = subprocess.run([sys.executable, "-m", "lib.opal_data_harvest.depth_census"], cwd=ROOT, capture_output=True,
                       timeout=900)
    out = (p.stdout + p.stderr).decode("utf-8", errors="replace")
    lines = out.splitlines()
    for ln in lines[:12] + ["..."] + lines[-8:]:
        print("  | " + ln)
    den = re.search(r"^DENOMINATOR: (\d+)$", out, re.M)
    mapped = re.search(r"^MAPPED: (\d+) of (\d+)$", out, re.M)
    unmapped = re.findall(r"^UNMAPPED \S+ .+$", out, re.M)
    source = re.search(r"^SOURCE: gold amgt/harvest/gold/article_security_mention/\S+$", out, re.M)
    at50 = re.search(r"^AT 50\+: (\d+) of (\d+)$", out, re.M)
    at100 = re.search(r"^AT 100\+: (\d+) of (\d+)$", out, re.M)
    if p.returncode != 0:
        failures.append("depth_census rc=%d" % p.returncode)
    if not den or den.group(1) != "89":
        failures.append("DENOMINATOR is not 89")
    if not mapped or int(mapped.group(2)) != 89 or int(mapped.group(1)) + len(unmapped) != 89:
        failures.append("MAPPED + UNMAPPED lines do not account for 89")
    elif int(mapped.group(1)) < 80:
        failures.append("only %s of 89 mapped" % mapped.group(1))
    if not source:
        failures.append("the census does not read the served gold mention part")
    if not at50 or not at100:
        failures.append("no AT 50+ / AT 100+ line")
    if "S3 WRITES: 0" not in out:
        failures.append("no 'S3 WRITES: 0' line")
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
