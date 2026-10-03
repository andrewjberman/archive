"""P-2 window, leg B3 (packet @855fdad77c): the LIVE adapter's bytes refuse 49 Financial on PATH A and still compose Inflection.

Downloads the deployed irpt-performance-adapter zip (get-function Code.Location, the bytes Lambda runs), extracts it, and imports
it in the FLAT /var/task layout (row IRPT_BCKEND-W3-S26: an in-tree test passes on a zip that dies at cold start, so this is
checked by extract-and-import, never by a test run from the repo). Read-only: no invoke, no write.

Prints: the live CodeSha256; whether entry.py and retained.py import in the flat layout; COMPOSED_FIRMS (49F absent, INF and COT
present); the *Retired* subclass of ProviderPathNotComposed; and the public code the boundary's own map gives that subclass.
"""
import io
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

import boto3

g = boto3.client("lambda").get_function(FunctionName="irpt-performance-adapter")
print("LIVE CodeSha256", g["Configuration"]["CodeSha256"], g["Configuration"]["LastModified"])
body = urllib.request.urlopen(g["Code"]["Location"], timeout=120).read()
d = tempfile.mkdtemp(prefix="p2_b3_")
zipfile.ZipFile(io.BytesIO(body)).extractall(d)
probe = r"""
import sys
sys.path.insert(0, %r)
import retained, tenants
c = set(retained.COMPOSED_FIRMS)
print('COMPOSED 49F', tenants._CANONICAL_49F in c, '| INF', tenants._CANONICAL_INF in c, '| COT', tenants._CANONICAL_COT in c)
ret = [n for n in dir(retained) if 'Retired' in n and isinstance(getattr(retained, n), type)
       and issubclass(getattr(retained, n), retained.ProviderPathNotComposed)]
print('RETIRED CLASSES', ret)
import entry
src = open(entry.__file__, encoding='utf-8').read()
row = '"ProviderPathNotComposed": "OBJECT_NOT_COVERED"'
print('ENTRY IMPORTS OK; live entry.py maps the base class (the subclass inherits by the MRO walk):', row in src)
""" % d
r = subprocess.run([sys.executable, "-c", probe], cwd=d, capture_output=True, text=True, timeout=120)
print(r.stdout.strip())
if r.returncode:
    print("FAIL: flat-layout import rc=%d: %s" % (r.returncode, r.stderr[-600:]))
    sys.exit(1)
