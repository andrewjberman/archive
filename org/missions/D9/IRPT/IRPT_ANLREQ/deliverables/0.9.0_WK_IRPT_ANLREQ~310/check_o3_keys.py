#!/usr/bin/env python3
"""AR419-y-AC3 -- the O3 key check: the five static form models hold exactly the keys of the backend model catalogue.

OPAL_MODELS is read from the portal file (a regex over its `key: '...'` members, so no import and no build). The backend's model
entry keys are read from the template file the backend catalogue loads (comparison_catalog.entries in templates.json, the same
file comparison_catalogue._model_entries reads); every entry there is a model entry. Prints O3-KEYS-OK n=5 only when the two key
sets are equal and n is 5; otherwise O3-KEYS-BAD <diff> and exit 1.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KEY_RE = re.compile(r"key:\s*'([^']+)'")


def workspace_root():
    proc = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=HERE, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=120)
    if proc.returncode != 0:
        print('O3-KEYS-BAD cannot resolve the workspace root: ' + proc.stderr.strip())
        sys.exit(1)
    return proc.stdout.strip()


def portal_keys(root):
    path = os.path.join(root, 'portal', 'src', 'pages', 'TicketCenter', 'opalModels.ts')
    with open(path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    block = text.split('OPAL_MODELS', 1)[1] if 'OPAL_MODELS' in text else ''
    return [k for k in KEY_RE.findall(block)]


def backend_keys(root):
    path = os.path.join(root, 'infra', 'aws', 'lambda', 'investor-reporting', 'ycharts', 'generate', 'templates.json')
    with open(path, 'r', encoding='utf-8') as fh:
        doc = json.load(fh)
    entries = ((doc or {}).get('comparison_catalog') or {}).get('entries')
    if not isinstance(entries, list):
        print('O3-KEYS-BAD comparison_catalog.entries is not a list in templates.json')
        sys.exit(1)
    return [str(e.get('key')) for e in entries if isinstance(e, dict)]


def main():
    root = workspace_root()
    form = portal_keys(root)
    backend = backend_keys(root)
    if len(form) != len(set(form)):
        print('O3-KEYS-BAD the form list repeats a key: %s' % sorted(form))
        sys.exit(1)
    only_form = sorted(set(form) - set(backend))
    only_backend = sorted(set(backend) - set(form))
    if only_form or only_backend or len(form) != 5 or set(form) != set(backend):
        print('O3-KEYS-BAD form-only=%s backend-only=%s form_n=%d backend_n=%d'
              % (only_form, only_backend, len(form), len(set(backend))))
        sys.exit(1)
    print('O3-KEYS-OK n=%d' % len(form))
    sys.exit(0)


if __name__ == '__main__':
    main()
