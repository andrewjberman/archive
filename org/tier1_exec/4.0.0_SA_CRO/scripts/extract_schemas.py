from __future__ import annotations
import base64
import json
import os
import re
import sys
from urllib.parse import urlparse

SP = sys.argv[1]
HAR_DIR = os.path.join(SP, "har")
OUT = os.path.join(SP, "analysis")

# high-value path regex (normalized-ish, case-insensitive) -> capture full body once
HV = re.compile(r"(performance|allocation|costbasis|income/|capitalmarkets|activitysummary|"
                r"/transactions|alternativeinvestments|portfoliodetailsearch|accountdetailsearch|"
                r"assetdetailsearch|characteristicdetailsearch|issuetypedetailsearch|registrationtype|"
                r"/account-api/account/|/account-api/asset/|relationshipdetailsearch|contactdetailsearch|"
                r"/relationship/request/(v2/)?relationship/z|networth/api/balancesheet|networth/api/account/grid|"
                r"segmentdetailsearch|classdetailsearch|benchmarkdetailsearch|targetdetailsearch|customfields|"
                r"/classification/schema|/classification/segmentdefinition|clientprofile|clientactivity|"
                r"/api/models|/strategies/search|blotter/search|/programs/search|dynamicmodels|firmmaintenance/options|"
                r"billing.*/api/config|insuranceplanning|clientview/api/menu|clientview/api/sitemap|"
                r"monitor/summary|user-api.*/user/|user-api.*/query|globalsettings|report/type/settings/runtime|"
                r"balancesheet|/networth/api/optionslookup|udfs|reconstatus)", re.I)

SKIP_BIG = re.compile(r"report/type/settings$|report/design/$|user/\{?id\}?/avatar|settings/userDetail", re.I)


def decode_body(content):
    txt = content.get('text')
    if txt is None:
        return None
    if content.get('encoding') == 'base64':
        try:
            return base64.b64decode(txt).decode('utf-8', errors='replace')
        except Exception:
            return None
    return txt


def schema(o, depth=0, maxd=5):
    ind = "  " * depth
    if depth > maxd:
        return "..."
    if isinstance(o, dict):
        if not o:
            return "{}"
        parts = []
        for k in list(o.keys())[:60]:
            parts.append(f"{ind}  {k}: {schema(o[k],depth+1,maxd)}")
        return "{\n" + "\n".join(parts) + f"\n{ind}}}"
    if isinstance(o, list):
        if not o:
            return "[]"
        return f"[{len(o)}] " + schema(o[0], depth, maxd)
    if isinstance(o, bool):
        return "bool"
    if isinstance(o, (int, float)):
        return f"num({o})" if depth >= maxd - 1 else "num"
    if isinstance(o, str):
        s = o[:40].replace("\n", " ")
        return f'"{s}"'
    if o is None:
        return "null"
    return type(o).__name__


seen = set()
out = []
for fn in sorted(os.listdir(HAR_DIR)):
    if not fn.endswith('.har'):
        continue
    h = json.load(open(os.path.join(HAR_DIR, fn), encoding='utf-8'))
    for e in h['log']['entries']:
        req = e['request']
        resp = e['response']
        url = req['url']
        u = urlparse(url)
        path = u.path
        if not re.search(r"bdreporting\.com$", u.netloc):
            continue
        full = u.netloc + path
        if not HV.search(full):
            continue
        if SKIP_BIG.search(full):
            continue
        if resp.get('status') != 200:
            continue
        mime = resp.get('content', {}).get('mimeType', '')
        if 'json' not in mime:
            continue
        # normalize key
        npath = re.sub(r'/z\d+', '/z{id}', re.sub(r'/\d+', '/{id}', path))
        npath = re.sub(r'/[0-9a-fA-F-]{20,}', '/{guid}', npath)
        key = f"{req['method']} {u.netloc}{npath}"
        if key in seen:
            continue
        body = decode_body(resp.get('content', {}))
        if not body:
            continue
        try:
            obj = json.loads(body)
        except Exception:
            continue
        seen.add(key)
        post = req.get('postData', {}).get('text')
        try:
            post_obj = json.loads(post) if post else None
        except Exception:
            post_obj = post
        sec = []
        sec.append(f"\n{'='*90}\n{key}   (resp {len(body)} bytes, file={fn})")
        if post_obj is not None:
            sec.append("REQUEST payload:")
            sec.append(schema(post_obj, 0, 4) if isinstance(post_obj, (dict, list)) else str(post_obj)[:800])
        sec.append("RESPONSE schema:")
        sec.append(schema(obj, 0, 5))
        out.append("\n".join(sec))

open(os.path.join(OUT, "schemas.txt"), 'w', encoding='utf-8').write("\n".join(out))
print(f"extracted {len(seen)} high-value endpoint schemas -> analysis/schemas.txt")
print(f"file size: {os.path.getsize(os.path.join(OUT,'schemas.txt'))} bytes")
