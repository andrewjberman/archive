import subprocess
import sys
import tempfile
import pathlib
root = pathlib.Path(subprocess.check_output(["git","rev-parse","--show-toplevel"],text=True).strip())
lib = root/"lib"/"opal_data_harvest"
base = subprocess.check_output(["git","show","%s:lib/opal_data_harvest/run-local.ps1" % subprocess.check_output(["git","merge-base","HEAD","CLOUD"],text=True).strip()],text=True)
tmp = pathlib.Path(tempfile.mkdtemp(prefix="o2_"))
log = tmp/"argv.txt"
stub = tmp/"stub.cmd"
stub.write_bytes(b"@echo off\r\necho %* >> \"" + str(log).encode() + b"\"\r\nexit /b 0\r\n")
basefile = lib/"o2_base_run-local.ps1"
basefile.write_text(base)
def run(script, extra):
    if log.exists():
        log.unlink()
    r = subprocess.run(["powershell.exe","-NoProfile","-ExecutionPolicy","Bypass","-File",str(script),"-Python",str(stub)]+extra,capture_output=True,text=True)
    argv = log.read_text().strip() if log.exists() else ""
    print("script=%s extra=%s rc=%d\n  argv: %s" % (script.name, extra, r.returncode, argv))
    return argv
ok = True
try:
    for extra in ([], ["-AllSecurities","-MaxJobs","2"]):
        a = run(lib/"run-local.ps1", extra)
        need = ["--harvest-grammar"," run ","--new-only"] + (["--all-securities","--max-jobs 2"] if extra else [])
        ok &= all(n in (" "+a+" ") for n in need)
    b = run(basefile, [])
    ok &= ("--harvest-grammar" not in b) and "--new-only" in b
finally:
    basefile.unlink()
print("AC1", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
