from __future__ import annotations
import base64
import hashlib
import json
import os
import re
import sys
from collections import Counter
from urllib.parse import urlparse, parse_qsl

SP = sys.argv[1]
HAR_DIR = os.path.join(SP, "har")
OUT = os.path.join(SP, "analysis")
BODIES = os.path.join(OUT, "bodies")
os.makedirs(BODIES, exist_ok=True)

BD_HOST_RE = re.compile(r"(^|\.)bdreporting\.com$")
NOISE_HOSTS = ("pendo.io","helpscout.net","signalr.net","cloudfront.net","google","doubleclick",
               "gstatic","googleapis","segment","launchdarkly","sentry","datadog","newrelic")

def is_bd(host): 
    return bool(BD_HOST_RE.search(host))

def norm_path(p):
    parts = p.split('/')
    out = []
    for seg in parts:
        if re.fullmatch(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', seg):
            out.append('{guid}')
        elif re.fullmatch(r'\d+', seg):
            out.append('{id}')
        elif re.fullmatch(r'[0-9a-fA-F]{16,}', seg):
            out.append('{hex}')
        else:
            out.append(seg)
    return '/'.join(out)

def decode_body(content):
    txt = content.get('text')
    if txt is None:
        return None
    if content.get('encoding') == 'base64':
        try:
            raw = base64.b64decode(txt)
            return raw.decode('utf-8', errors='replace')
        except Exception:
            return None
    return txt

catalog = {}   # key -> record
files_summary = []

for fn in sorted(os.listdir(HAR_DIR)):
    if not fn.endswith('.har'): 
        continue
    path = os.path.join(HAR_DIR, fn)
    with open(path, 'r', encoding='utf-8') as fh:
        h = json.load(fh)
    log = h['log']
    pagemap = {p['id']: p.get('title','') for p in log.get('pages', [])}
    ents = log['entries']
    rt_counter = Counter()
    host_counter = Counter()
    bd_api = 0
    for i, e in enumerate(ents):
        req = e['request']
        resp = e['response']
        url = req['url']
        u = urlparse(url)
        host = u.netloc
        rt = e.get('_resourceType','?')
        rt_counter[rt]+=1
        host_counter[host]+=1
        if any(n in host for n in NOISE_HOSTS): 
            continue
        if not is_bd(host):
            continue
        method = req['method']
        content = resp.get('content',{})
        mime = content.get('mimeType','')
        is_api = rt in ('xhr','fetch') or 'json' in mime
        if not is_api:
            continue
        if method == 'OPTIONS' or rt == 'preflight':
            continue
        bd_api += 1
        npath = norm_path(u.path)
        key = f"{method} {host}{npath}"
        qkeys = sorted({k for k,_ in parse_qsl(u.query)})
        page = pagemap.get(e.get('pageref',''), '')
        rec = catalog.get(key)
        if rec is None:
            rec = {"key":key,"method":method,"host":host,"path":npath,
                   "count":0,"statuses":Counter(),"query_keys":set(),
                   "pages":set(),"files":set(),"sample":None,"resp_sizes":[]}
            catalog[key]=rec
        rec["count"]+=1
        rec["statuses"][resp.get('status')]+=1
        rec["query_keys"].update(qkeys)
        if page:
            rec["pages"].add(page)
        rec["files"].add(fn)
        rec["resp_sizes"].append(content.get('size',0) or resp.get('bodySize',0))
        # capture a sample body for a successful JSON response
        if rec["sample"] is None and resp.get('status')==200 and 'json' in mime:
            body = decode_body(content)
            postdata = req.get('postData',{}).get('text')
            slug = hashlib.md5(key.encode()).hexdigest()[:12]
            sample = {"key":key,"url":url,"status":200,
                      "req_query":dict(parse_qsl(u.query)),
                      "req_post":postdata[:4000] if postdata else None,
                      "resp_body":(body[:30000] if body else None),
                      "resp_full_len":(len(body) if body else 0)}
            with open(os.path.join(BODIES, f"{slug}.json"),'w',encoding='utf-8') as bf:
                json.dump(sample, bf, indent=1)
            rec["sample"]=slug
    files_summary.append({"file":fn,"entries":len(ents),"bd_api_calls":bd_api,
                          "pages":list(pagemap.values()),
                          "resourceTypes":dict(rt_counter),
                          "top_hosts":host_counter.most_common(12)})
    print(f"{fn}: {len(ents)} entries, {bd_api} BD-API calls, {len(pagemap)} pages")

# serialize catalog
cat_out = []
for k,r in sorted(catalog.items()):
    sizes = r["resp_sizes"]
    cat_out.append({
        "key":r["key"],"method":r["method"],"host":r["host"],"path":r["path"],
        "count":r["count"],"statuses":dict(r["statuses"]),
        "query_keys":sorted(r["query_keys"]),
        "pages":sorted(r["pages"]),"files":sorted(r["files"]),
        "max_resp_size":max(sizes) if sizes else 0,
        "sample":r["sample"],
    })
with open(os.path.join(OUT,"endpoint_catalog.json"),'w',encoding='utf-8') as f:
    json.dump(cat_out, f, indent=1)
with open(os.path.join(OUT,"files_summary.json"),'w',encoding='utf-8') as f:
    json.dump(files_summary, f, indent=1)

print("\n=== TOTALS ===")
print("unique BD API endpoints:", len(cat_out))
print("catalog ->", os.path.join(OUT,"endpoint_catalog.json"))
