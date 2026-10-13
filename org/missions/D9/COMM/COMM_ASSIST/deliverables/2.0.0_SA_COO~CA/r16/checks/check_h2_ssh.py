"""CA-h-2 AC3: this box accepts key logins over SSH, and the administrators key file's fingerprints are listed for comparison with muse's.

Prints:  H2-SSH ok=<True|False> listening=<True|False> keys=<n> fingerprints=<SHA256:...,...> reason=<text>
Read-only: Get-NetTCPConnection on port 22, then ssh-keygen -lf over administrators_authorized_keys. Fingerprints are not secrets;
no key body is printed. It does not prove muse's key is among them: the issuer compares the printed fingerprints with muse's.
"""
import os
import subprocess
import sys

KEYS = os.path.join(os.environ.get("ProgramData", r"C:\ProgramData"), "ssh", "administrators_authorized_keys")


def main():
    listening, fps, why = False, [], ""
    try:
        dev = subprocess.run([sys.executable, "lib/devices.py", "this"], capture_output=True, text=True, timeout=60).stdout.strip()
        if dev != "dell2":
            why = "this box is %r, not dell2 (run from the repository root)" % dev
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command",
                            "(Get-NetTCPConnection -LocalPort 22 -State Listen -ErrorAction Stop | Measure-Object).Count"],
                           capture_output=True, text=True, timeout=60)
        listening = r.returncode == 0 and r.stdout.strip().isdigit() and int(r.stdout.strip()) > 0
        if not listening:
            why = why or "nothing listens on port 22"
        if not os.path.isfile(KEYS):
            why = why or "administrators_authorized_keys not found"
        else:
            k = subprocess.run(["ssh-keygen", "-lf", KEYS], capture_output=True, text=True, timeout=60)
            fps = [ln.split()[1] for ln in (k.stdout or "").splitlines() if len(ln.split()) > 1 and ln.split()[1].startswith("SHA256:")]
            if not fps:
                why = why or "no key fingerprints read (ssh-keygen rc=%s)" % k.returncode
    except Exception as exc:
        why = why or str(exc)[:200]
    print("H2-SSH ok=%s listening=%s keys=%d fingerprints=%s reason=%s" % (not why, listening, len(fps), ",".join(fps) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
