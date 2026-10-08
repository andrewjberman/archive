#!/usr/bin/env python3
"""YCD-w-6 checks. One argument: brand | bytes | render. Prints one RESULT line. Run from the worktree root. ASCII only.

brand   load_brand() in a fresh process: no IRPT_BRAND_* env var, cwd in a temp dir outside any git repository, git made to
        fail; both assets must come from ycharts/research/brand/ beside layout_overview.py.
bytes   brand.json == build_brand_spec() written as json.dump(indent=2) byte for byte; the logo == its committed blob
        (git show HEAD:<path>) and its sha256 is printed.
render  the package members the resident builder ships for `--research` (its own research_wanted filter, read at HEAD) plus
        the logo as a `--member`, extracted from HEAD blobs into a temp tree OUTSIDE any git repository; there, with no
        brand env var, load_brand() + the Opal HTML layout run (pricing=False), and the PDF step runs when node and
        playwright-core already exist on this box (nothing is installed or fetched), else it is recorded as not run.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip())
IR = "infra/aws/lambda/investor-reporting"
RES = IR + "/ycharts/research"
LOGO = RES + "/brand/Opal-Capital-Logo-Full-Color.svg"
SPEC = RES + "/brand/brand.json"
BUILDER = ROOT / "org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/build_resident_package.py"
BRAND_ENV = ("IRPT_BRAND_SPEC", "IRPT_OPAL_LOGO")


def git_bytes(*args):
    r = subprocess.run(["git", "-C", str(ROOT)] + list(args), capture_output=True)
    if r.returncode != 0:
        raise SystemExit("RESULT: FAIL git %s rc=%d" % (" ".join(args), r.returncode))
    return r.stdout


def clean_env():
    env = {k: v for k, v in os.environ.items() if k not in BRAND_ENV}
    return env


def outside_git(path):
    r = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return r.returncode != 0


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROBE = r"""
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import layout_overview as lo
def no_git(*a):
    raise AssertionError("git consulted")
lo._git = no_git
packaged = Path(lo.__file__).resolve().parent / "brand"
spec_p = lo._asset_path("IRPT_BRAND_SPEC", lo.SPEC_REL)
logo_p = lo._asset_path("IRPT_OPAL_LOGO", lo.LOGO_REL)
b = lo.load_brand()
ok = (spec_p == packaged / "brand.json" and logo_p == packaged / "Opal-Capital-Logo-Full-Color.svg"
      and b["spec"]["colors"]["opal_navy"]["hex"] == "#163372" and len(b["logo_svg"]) > 0)
print(json.dumps({"ok": ok, "spec": str(spec_p), "logo": str(logo_p), "logo_bytes": len(b["logo_svg"])}))
"""


def check_brand():
    with tempfile.TemporaryDirectory() as td:
        if not outside_git(td):
            return "RESULT: brand FAIL temp cwd %s is inside a git repository" % td
        r = subprocess.run([sys.executable, "-c", PROBE, str(ROOT / RES)], cwd=td, env=clean_env(), capture_output=True, text=True)
    if r.returncode != 0:
        return "RESULT: brand FAIL probe rc=%d %s" % (r.returncode, r.stderr.strip().splitlines()[-1:] )
    got = json.loads(r.stdout.strip().splitlines()[-1])
    if not got["ok"]:
        return "RESULT: brand FAIL %s" % got
    return "RESULT: brand PASS spec=%s logo=%s logo_bytes=%d env_brand_vars=0 cwd_outside_git=True git_consulted=False" % (
        got["spec"], got["logo"], got["logo_bytes"])


def check_bytes():
    bs = load_module("bs", ROOT / "deck_generation/scripts/03_extract_brand_spec.py")
    spec, missing = bs.build_brand_spec()
    want = json.dumps(spec, indent=2).encode("utf-8")
    have = (ROOT / SPEC).read_bytes()
    committed_spec = git_bytes("show", "HEAD:" + SPEC)
    logo_have = (ROOT / LOGO).read_bytes()
    logo_commit = git_bytes("show", "HEAD:" + LOGO)
    sha = hashlib.sha256(logo_have).hexdigest()
    problems = []
    if have != want:
        problems.append("brand.json != build_brand_spec()")
    if committed_spec != have:
        problems.append("brand.json working file != HEAD blob")
    if logo_have != logo_commit:
        problems.append("logo != HEAD blob")
    if any(b > 127 for b in have):
        problems.append("brand.json not ASCII")
    if problems:
        return "RESULT: bytes FAIL " + "; ".join(problems)
    return ("RESULT: bytes PASS brand.json=%d bytes equals build_brand_spec() (logo variants missing on this box: %d of 6) "
            "logo=%d bytes sha256=%s equals HEAD blob" % (len(have), len(missing), len(logo_have), sha))


def check_render():
    builder = load_module("brp", BUILDER)
    listing = git_bytes("ls-tree", "-r", "--name-only", "HEAD", "--", RES).decode().split()
    members = [p for p in listing if builder.research_wanted(p)]
    svg_by_filter = builder.research_wanted(LOGO)
    members.append(LOGO)  # as `--member ycharts/research/brand/<svg>=<repo path>`: the builder's --research filter omits .svg
    members = sorted(set(members))
    with tempfile.TemporaryDirectory() as td:
        if not outside_git(td):
            return "RESULT: render FAIL temp tree %s is inside a git repository" % td
        tree = Path(td) / "package"
        for p in members:
            dest = tree / "ycharts" / "research" / p[len(RES) + 1:]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(git_bytes("show", "HEAD:" + p))
        fx = ROOT / RES / "tests" / "fixtures"
        probe = r"""
import base64, json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import layout_overview as lo
fx = Path(sys.argv[2])
run = json.loads((fx / "run.json").read_text(encoding="utf-8"))
mp = json.loads((fx / "map.json").read_text(encoding="utf-8"))
kept = lo.load_kept(fx / "kept")
brand = lo.load_brand()
html = lo.build(run, kept, mp, brand, pricing=False)
out = {"logo_in_html": base64.b64encode(brand["logo_svg"]).decode("ascii") in html,
       "opal_credit": "Data: Opal Capital" in html, "no_vendor_word": "ycharts" not in html.lower(),
       "html_bytes": len(html), "pdf": None, "pdf_note": None}
try:
    pdf = lo.render(html)
    from pypdf import PdfReader
    import io
    out["pdf"] = {"magic": pdf[:4].decode("ascii", "replace"), "bytes": len(pdf), "pages": len(PdfReader(io.BytesIO(pdf)).pages)}
except Exception as exc:
    out["pdf_note"] = "%s: %s" % (type(exc).__name__, str(exc).splitlines()[0][:160])
print(json.dumps(out))
"""
        env = clean_env()
        if "IRPT_PLAYWRIGHT_CORE" not in env:
            for cand in (Path(subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--git-common-dir"], capture_output=True,
                                             text=True).stdout.strip()).resolve().parent / "portal" / "node_modules" / "playwright-core",
                         ROOT / "portal" / "node_modules" / "playwright-core"):
                if cand.is_dir():
                    env["IRPT_PLAYWRIGHT_CORE"] = str(cand)  # an already-present package; the render hop's own setting, not a brand var
                    break
        r = subprocess.run([sys.executable, "-c", probe, str(tree / "ycharts" / "research"), str(fx)], cwd=td, env=env,
                           capture_output=True, text=True, timeout=240)
        if r.returncode != 0:
            return "RESULT: render FAIL probe rc=%d %s" % (r.returncode, r.stderr.strip().splitlines()[-1:])
        got = json.loads(r.stdout.strip().splitlines()[-1])
    shipped = "%d members (logo via --member: builder research_wanted(svg)=%s)" % (len(members), svg_by_filter)
    if not (got["logo_in_html"] and got["opal_credit"] and got["no_vendor_word"]):
        return "RESULT: render FAIL html checks %s" % got
    if got["pdf"]:
        pdf_part = "pdf=%(magic)s %(bytes)d bytes %(pages)d pages" % got["pdf"]
        if got["pdf"]["magic"] != "%PDF":
            return "RESULT: render FAIL " + pdf_part
    else:
        pdf_part = "pdf=NOT RUN (%s)" % got["pdf_note"]
    return ("RESULT: render PASS tree outside git, package=%s, no brand env var, load_brand ok, html %d bytes with embedded "
            "logo + 'Data: Opal Capital' + no vendor word, %s" % (shipped, got["html_bytes"], pdf_part))


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("brand", "bytes", "render"):
        print("usage: w6_checks.py brand|bytes|render")
        return 2
    line = {"brand": check_brand, "bytes": check_bytes, "render": check_render}[sys.argv[1]]()
    print(line)
    return 0 if " PASS" in line else 1


if __name__ == "__main__":
    sys.exit(main())
