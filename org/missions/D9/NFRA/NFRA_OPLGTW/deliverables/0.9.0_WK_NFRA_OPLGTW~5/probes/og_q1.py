"""OGQ1-AC13 probe (NFRA_OPLGTW, cell OG-q-1, worker 0.9.0_WK_NFRA_OPLGTW~5).

Usage: python og_q1.py AC13

Reads the host Python version from OG-p-1's BASELINE.json (OGP1-AC2 measurement.python_version) and the exact
PyArrow and DuckDB pins from infra/aws/ec2/opal-gateway/requirements.txt. For each pin it runs

    pip download --only-binary=:all: --no-deps --platform manylinux2014_aarch64 --python-version <host> <pin>

into <workspace>/.scratch/og_q1_ac13/<package>/ (emptied first), then checks that exactly one wheel for that exact
version landed and that its tags name the host's CPython (or abi3/py3) and aarch64. Prints one line per pin, then
`VERDICT: PASS-OGQ1-AC13` or `VERDICT: FAIL-OGQ1-AC13 <reason>`.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[8]
BASELINE = ROOT / "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/BASELINE.json"
REQUIREMENTS = ROOT / "infra/aws/ec2/opal-gateway/requirements.txt"
OUT = ROOT / ".scratch" / "og_q1_ac13"
PLATFORM = "manylinux2014_aarch64"
PACKAGES = ("pyarrow", "duckdb")
PIP_TIMEOUT_SECONDS = 50


def verdict_fail(reason):
    print(f"VERDICT: FAIL-OGQ1-AC13 {reason}")
    return 1


def read_pins():
    pins = {}
    problems = []
    lines = REQUIREMENTS.read_text(encoding="utf-8").splitlines()
    for name in PACKAGES:
        found = []
        for raw in lines:
            line = raw.split("#", 1)[0].strip()
            match = re.match(r"([A-Za-z0-9_.\-]+)", line)
            if match and match.group(1).lower().replace("_", "-") == name:
                found.append(line)
        if len(found) != 1:
            problems.append(f"{name}: {len(found)} requirement lines (want 1)")
            continue
        exact = re.fullmatch(rf"{name}==([0-9][0-9A-Za-z.]*)", found[0].replace(" ", ""), flags=re.IGNORECASE)
        if not exact:
            problems.append(f"{name}: not an exact == pin ({found[0]!r})")
            continue
        pins[name] = exact.group(1)
    return pins, problems


def ac13():
    if not REQUIREMENTS.is_file() or not BASELINE.is_file():
        return verdict_fail(f"workspace root not resolved: {ROOT}")
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    version_text = str(baseline["OGP1-AC2"]["measurement"]["python_version"]).strip()
    match = re.fullmatch(r"Python (\d+)\.(\d+)\.\d+", version_text)
    if not match:
        return verdict_fail(f"host python version unreadable: {version_text!r}")
    host = f"{match.group(1)}.{match.group(2)}"
    cp_tag = f"cp{match.group(1)}{match.group(2)}"
    print(f"host python (BASELINE.json OGP1-AC2 python_version): {version_text} -> --python-version {host}")

    pins, problems = read_pins()
    print(f"pins read from {REQUIREMENTS.relative_to(ROOT).as_posix()}: {pins}")
    if problems:
        return verdict_fail("; ".join(problems))

    failures = []
    resolved = 0
    for name in PACKAGES:
        version = pins[name]
        dest = OUT / name
        shutil.rmtree(dest, ignore_errors=True)
        dest.mkdir(parents=True)
        cmd = [
            sys.executable, "-m", "pip", "download",
            "--only-binary=:all:", "--no-deps",
            "--platform", PLATFORM, "--python-version", host,
            "-d", str(dest), f"{name}=={version}",
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=PIP_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            failures.append(f"{name}=={version}: pip download timed out after {PIP_TIMEOUT_SECONDS}s")
            print(f"{name}=={version}: pip TIMEOUT")
            continue
        wheels = sorted(p.name for p in dest.glob("*.whl"))
        print(f"{name}=={version}: pip rc={proc.returncode} wheels={wheels}")
        if proc.returncode != 0:
            tail = [ln for ln in proc.stderr.splitlines() if ln.strip()][-1:] or ["(no stderr)"]
            print(f"  pip stderr tail: {tail[0]}")
            failures.append(f"{name}=={version}: pip rc={proc.returncode}")
            continue
        if len(wheels) != 1:
            failures.append(f"{name}=={version}: {len(wheels)} wheels downloaded (want 1)")
            continue
        parts = wheels[0][: -len(".whl")].split("-")
        if len(parts) < 5 or parts[0].lower() != name or parts[1] != version:
            failures.append(f"{name}=={version}: unexpected wheel name {wheels[0]}")
            continue
        python_tags, abi_tags, platform_tags = parts[-3].split("."), parts[-2].split("."), parts[-1].split(".")
        python_ok = cp_tag in python_tags or "py3" in python_tags or "abi3" in abi_tags
        platform_ok = any("aarch64" in tag and "linux" in tag for tag in platform_tags)
        print(f"  python tags {python_tags} abi {abi_tags} platform {platform_tags} -> python_ok={python_ok} "
              f"aarch64_ok={platform_ok}")
        if not (python_ok and platform_ok):
            failures.append(f"{name}=={version}: wheel tags do not match {cp_tag}/linux aarch64")
            continue
        resolved += 1

    print(f"resolved {resolved} of {len(PACKAGES)} pins for {PLATFORM} on Python {host}")
    if failures:
        return verdict_fail("; ".join(failures))
    print("VERDICT: PASS-OGQ1-AC13")
    return 0


def main(argv):
    if len(argv) != 2 or argv[1] != "AC13":
        print("usage: og_q1.py AC13")
        return 2
    return ac13()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
