"""Run a canonical headed harvester unchanged, then return its local session.

No cloud parking; never print credential or cookie values. Browser content is not
collected here. FT's flat cookie contract keeps auth provenance in a sidecar.
"""

import hashlib
import json
import pathlib
import subprocess
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parent
NAMES = {"sa": "sa", "ft": "ft", "bbg": "bloomberg"}


class HarvestFailed(RuntimeError):
    pass


def harvest(pub, folder, max_steps=10, trace_hold=False):
    folder = pathlib.Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=False)
    source = SCRIPTS / (NAMES[pub] + "_harvest_session.py")
    copied = folder / source.name
    copied.write_bytes(source.read_bytes())
    source_hash = hashlib.sha256(copied.read_bytes()).hexdigest()
    dependencies = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (
            SCRIPTS / "press_and_hold_lib.py",
            SCRIPTS / "nopecha_hcaptcha_lib.py",
            SCRIPTS / "google_oauth_handler.py",
        )
    }
    driver = folder / "run.py"
    argv = [str(copied), "--max-steps", str(max_steps)]
    if trace_hold and pub in ("sa", "bbg"):
        argv.append("--trace-hold")
    driver.write_text(
        "import runpy, sys\n"
        f"sys.path.insert(0, {str(SCRIPTS)!r})\n"
        f"sys.argv = {argv!r}\n"
        f"runpy.run_path({str(copied)!r}, run_name='__main__')\n",
        encoding="utf-8",
    )
    with (folder / "run.log").open("w", encoding="utf-8") as log:
        proc = subprocess.run([sys.executable, str(driver)], stdout=log, stderr=log)
    bundles = sorted(folder.glob(NAMES[pub] + "_session_*.json"))
    bundle = json.loads(bundles[-1].read_text(encoding="utf-8")) if bundles else None
    if pub == "ft":
        network_ok = "network_auth_corroborated=True" in (folder / "run.log").read_text(
            encoding="utf-8"
        )
    else:
        network_ok = bool(bundle and bundle.get("network_auth_corroborated"))
    evidence = {
        "publisher": pub,
        "source": str(source),
        "source_sha256": source_hash,
        "dependency_sha256": dependencies,
        "exit_code": proc.returncode,
        "bundle_present": bool(bundle),
        "network_auth_corroborated": network_ok,
        "cloud_park": False,
    }
    (folder / "auth-evidence.json").write_text(
        json.dumps(evidence, indent=2), encoding="utf-8"
    )
    print(json.dumps(evidence), flush=True)
    if proc.returncode or not bundle or not network_ok:
        raise HarvestFailed(
            "Canonical harvester did not produce a network-corroborated session"
        )
    return bundle


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("publisher", choices=NAMES)
    parser.add_argument("folder", type=pathlib.Path)
    parser.add_argument("--max-steps", type=int, default=10)
    args = parser.parse_args()
    try:
        harvest(args.publisher, args.folder, args.max_steps)
    except HarvestFailed:
        raise SystemExit(3) from None
