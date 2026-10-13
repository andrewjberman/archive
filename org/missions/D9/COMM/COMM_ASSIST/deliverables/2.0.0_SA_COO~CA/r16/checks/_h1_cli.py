"""Shared by the two live checks: run the refresh CLI into a temp folder. Not a criterion."""
import os
import pathlib
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[9]
SCRIPT = REPO / "data" / "transcripts" / "scripts" / "muse_reader" / "refresh.py"


def run():
    """Return (root_tempdir_obj, rc, tail) -- or (None, None, reason) when the script is absent."""
    if not SCRIPT.is_file():
        return None, None, "absent: %s" % SCRIPT.relative_to(REPO).as_posix()
    td = tempfile.TemporaryDirectory()
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO) + os.pathsep + env.get("PYTHONPATH", "")
    p = subprocess.run([sys.executable, str(SCRIPT), "--root", td.name], cwd=str(REPO), env=env,
                       capture_output=True, text=True, timeout=100)
    return td, p.returncode, (p.stdout + p.stderr)[-400:]
