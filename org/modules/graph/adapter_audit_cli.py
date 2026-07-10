#!/usr/bin/env python3
"""adapter_audit_cli.py -- comp-adapter-audit backend: portal adapter field-threading audit.

PURPOSE (ratified by Andrew 2026-07-10; both failures are SILENT -- nothing errors):
  1. Catch silent data loss between the served S3 artifact and the screen: gold emits a
     field into the live JSON, the adapter never threads it into its output.
  2. Catch the TS type drifting from the real envelope. `apiRequest<T>` is an unchecked
     cast, so the compiler blesses `raw.x` reading `undefined` forever.

VERDICT DISCIPLINE (the whole point of the 2026-07-10 repair):
  An audit has THREE distinct non-OK outcomes, and collapsing them is how this tool lied:
    NO_S3_SOURCE    the adapter has no static artifact (it calls a Lambda). The audit
                    DOES NOT APPLY. This is not a failure and not a pass.
    FETCH_FAILED    an S3 source was derived but the object could not be read.
    TYPE_UNRESOLVED the raw input type could not be resolved (or is ambiguous), so the
                    typed side of the comparison is empty.
  In every one of those, `verified` is false and there are ZERO findings. A zero-finding
  UNVERIFIED run MUST NOT be readable as a clean audit -- not on the terminal, and not in
  the manifest, which `.tools/portal-hooks/d1_adapter_threading_gate.py` parses to render
  a portal pre-push verdict.

MANIFEST WRITE IS LOAD-BEARING -- DO NOT MAKE IT OPT-IN.
  The D-1 gate calls this CLI and then reads `<adapter>.yaml` from _ADAPTER_AUDIT_DIR. If
  the manifest is absent the gate cannot render a verdict and degrades to WARN forever.
  Use `--manifest-dir` to redirect the write for a read-only exercise; never remove it.

SYMMETRY: comparing against an empty set manufactures findings. That hazard exists in
THREE places, and each is guarded below:
  (a) s3_raw_fields empty   -> every typed field looks "missing from S3"
  (b) raw_type_fields empty -> every S3 field looks like SCHEMA-DRIFT   [was unguarded]
  (c) nested_typed unresolved (a named type we did not resolve) -> every nested S3 key
      looks like NESTED-SCHEMA-DRIFT                                    [was unguarded]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent
_WORKSPACE = _THIS_DIR.parent.parent.parent
_PORTAL_SRC = _WORKSPACE / 'portal' / 'src'
_ADAPTER_AUDIT_DIR = _WORKSPACE / 'org' / 'modules' / 'graph' / 'adapter-audit'

_ENDPOINT_FILES = [
    _PORTAL_SRC / 'api' / 'endpoints' / 'advisor-intelligence.ts',
    _PORTAL_SRC / 'api' / 'endpoints' / 'portfolio.ts',
]

PLATINUM_S3_ROOT = 's3://opal-data-inf/platinum'

# Verification statuses. Only OK admits findings.
OK = 'OK'
NO_S3_SOURCE = 'NO_S3_SOURCE'
FETCH_FAILED = 'FETCH_FAILED'
TYPE_UNRESOLVED = 'TYPE_UNRESOLVED'

# Exit codes follow the fabric CANNOT-EVALUATE convention:
#   0 = audited (PASS or WARN)   1 = FAIL (--severity error) / adapter not found
#   2 = could not evaluate (UNVERIFIED / NOT-APPLICABLE) -- neither pass nor fail
RC_OK, RC_FAIL, RC_CANNOT_EVALUATE = 0, 1, 2


# -------- Helpers --------

def _rel(path_str: str) -> str:
    try:
        return str(Path(path_str).relative_to(_WORKSPACE))
    except ValueError:
        return path_str


def _brace_block(src: str, open_idx: int) -> str:
    """Return the text between the `{` at open_idx and its matching `}`."""
    depth = 0
    for i in range(open_idx, len(src)):
        if src[i] == '{':
            depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0:
                return src[open_idx + 1:i]
    return src[open_idx + 1:]


def _find_adapter_source(adapter_name: str) -> tuple[Path | None, str]:
    """Find the TypeScript file + function body for an adapter function."""
    search_files = list(_ENDPOINT_FILES)
    ep_dir = _PORTAL_SRC / 'api' / 'endpoints'
    if ep_dir.exists():
        for f in sorted(ep_dir.glob('*.ts')):
            if f not in search_files:
                search_files.append(f)

    for ts_file in search_files:
        if not ts_file.exists():
            continue
        src = ts_file.read_text(encoding='utf-8', errors='ignore')
        lines = src.splitlines()
        fn_start = None
        for i, line in enumerate(lines):
            if re.search(rf'(async\s+function|function)\s+{re.escape(adapter_name)}\s*\(', line):
                fn_start = i
                break
        if fn_start is None:
            for i, line in enumerate(lines):
                if re.search(rf'\b{re.escape(adapter_name)}\s*=', line):
                    fn_start = i
                    break
        if fn_start is None:
            continue

        # Brace counting. NOTE 2026-07-10: this was reported (D3) as over-running the
        # function because it counts braces inside strings/comments. EXERCISED AND
        # REFUTED on all five live targets -- it returns the exact function extent
        # (getPlatinumFirmDashboard = lines 448..502 = 55). The wrong raw-type came
        # from _extract_raw_type_name, not from here. Left as-is deliberately.
        body_lines = []
        depth = 0
        started = False
        for line in lines[fn_start:]:
            opens = line.count('{')
            closes = line.count('}')
            body_lines.append(line)
            if opens > 0 and not started:
                started = True
            if started:
                depth += opens - closes
                if depth <= 0:
                    break

        return ts_file, '\n'.join(body_lines)

    return None, ''


# -------- Type resolution (D4: resolve across imported files; D2: name what we used) --------

def _import_corpus(ts_file: Path) -> list[tuple[Path, str]]:
    """[(path, src)] for ts_file plus every relative module it imports.

    D4: interfaces frequently live in `_shared/types.ts`, not the endpoints file.
    Searching only `ts_file` yielded `Typed fields: 0`, which then tripped guard (b).
    """
    corpus: list[tuple[Path, str]] = []
    try:
        src = ts_file.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return corpus
    corpus.append((ts_file, src))

    # `@/x` is the portal's src-root alias; advisor-intelligence.ts imports EVERY type via
    # `} from '@/pages/AdvisorIntelligence/_shared/types'`. A relative-only regex resolved
    # zero modules and reproduced `Typed fields: 0` -- D4 wearing a different mask.
    for m in re.finditer(r"""from\s+['"]([^'"]+)['"]""", src):
        spec = m.group(1)
        if spec.startswith('.'):
            base = (ts_file.parent / spec).resolve()
        elif spec.startswith('@/'):
            base = (_PORTAL_SRC / spec[2:]).resolve()
        else:
            continue  # package import
        for cand in (base.with_suffix('.ts'), base.with_suffix('.tsx'),
                     base / 'index.ts', base / 'index.tsx', base):
            if cand.is_file():
                try:
                    corpus.append((cand, cand.read_text(encoding='utf-8', errors='ignore')))
                except OSError:
                    pass
                break
    return corpus


def _find_type_body(corpus: list[tuple[Path, str]], name: str,
                    _seen: set[str] | None = None) -> tuple[str | None, Path | None]:
    """Locate `interface name {...}` / `type name = {...}`, following `type name = Other`."""
    _seen = _seen or set()
    if name in _seen or not name:
        return None, None
    _seen.add(name)
    esc = re.escape(name)

    for path, src in corpus:
        m = re.search(r'(?:export\s+)?interface\s+' + esc + r'\b[^{]*\{', src)
        if m:
            return _brace_block(src, m.end() - 1), path
        m = re.search(r'(?:export\s+)?type\s+' + esc + r'\s*=\s*\{', src)
        if m:
            return _brace_block(src, m.end() - 1), path

    # alias: `type X = Y` (one hop, cycle-guarded)
    for path, src in corpus:
        m = re.search(r'(?:export\s+)?type\s+' + esc + r'\s*=\s*(\w+)\s*$', src, re.MULTILINE)
        if m:
            return _find_type_body(corpus, m.group(1), _seen)
    return None, None


def _top_level_members(body: str) -> dict[str, str]:
    """{field: declared_type_text} for the top level of an interface body."""
    members: dict[str, str] = {}
    depth = 0
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith('//') or s.startswith('*') or s.startswith('/*'):
            continue
        if depth == 0:
            m = re.match(r'(\w+)\??\s*:\s*(.+?)\s*$', s)
            if m:
                members[m.group(1)] = m.group(2).rstrip(',;')
        depth += s.count('{') - s.count('}')
    return members


def _resolve_type_fields(corpus: list[tuple[Path, str]], type_name: str
                         ) -> tuple[dict[str, list[str] | None], Path | None]:
    """{top_field: [nested] | None}. None == nested shape UNRESOLVED (do not compare).

    Guard (c): a field declared as a *named* type we could not resolve must never be
    compared against the live nested keys -- that manufactures NESTED-SCHEMA-DRIFT for
    every key, which is guard (b)'s bug one level down.
    """
    body, where = _find_type_body(corpus, type_name)
    if body is None:
        return {}, None

    out: dict[str, list[str] | None] = {}
    for field, decl in _top_level_members(body).items():
        if decl.startswith('{'):
            idx = body.find(decl)
            inline = _brace_block(body, body.index('{', idx)) if idx >= 0 else ''
            out[field] = list(_top_level_members(inline))
            continue
        base = re.sub(r'\[\]$', '', decl.split('|')[0].strip()).strip()
        if re.fullmatch(r'\w+', base) and base[:1].isupper():
            nested_body, _ = _find_type_body(corpus, base)
            out[field] = list(_top_level_members(nested_body)) if nested_body is not None else None
        else:
            out[field] = None if base and base[:1].isupper() else []
    return out, where


def _extract_raw_type_name(function_body: str) -> tuple[str, str]:
    """(type_name, how). '' means UNRESOLVED -- and that is an honest answer.

    D3: the old code took the FIRST `apiRequest<...>` anywhere in the body. For
    getPlatinumFirmDashboard that is a NESTED sub-fetch inside a Promise.all
    (`FeeEfficiencyResponse`), while the adapter's own envelope arrives via a bare
    `fetch()` + `JSON.parse` and is cast at `return stub as PlatinumFirmDashboard`.
    """
    has_bare_fetch = re.search(r'(?<!api)\bfetch\s*\(', function_body) is not None
    parsed = re.search(r'const\s+(\w+)\s*=\s*JSON\.parse', function_body)
    if has_bare_fetch and parsed:
        m = re.search(r'return\s+' + re.escape(parsed.group(1)) + r'\s+as\s+(\w+)', function_body)
        if m:
            return m.group(1), 'return-cast of the JSON.parse envelope'
        return '', 'bare fetch() envelope with no `as <Type>` cast'

    all_types = list(dict.fromkeys(re.findall(r'apiRequest<(\w+)>', function_body)))
    # A multi-fetch adapter (getPlatinumClientDetailStatic merges 4 artifacts) has a
    # PRIMARY envelope and N sub-fetches. Refusing to audit it at all was a regression:
    # the pre-fix tool produced a correct clean audit there. Take the primary, and say
    # how many others exist rather than pretending they were audited.
    primary = re.search(r'(?:const\s+\w+\s*=\s*await|return\s+await|return)\s+apiRequest<(\w+)>',
                        function_body)
    if primary:
        extra = len(all_types) - 1
        return primary.group(1), ('apiRequest<T> (sole call)' if extra <= 0
                                  else f'primary apiRequest<T>; {extra} sub-fetch type(s) NOT audited')
    if all_types:
        extra = len(all_types) - 1
        return all_types[0], ('apiRequest<T> (sole call)' if extra <= 0
                              else f'first of {len(all_types)} apiRequest<T>; {extra} NOT audited')

    m = re.search(r'as\s+(\w+Raw\w*)', function_body)
    if m:
        return m.group(1), 'as <...Raw> cast'
    return '', 'no apiRequest<T>, no raw cast'


# -------- S3 --------

def _sample_id(segment: str) -> str | None:
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'awscli', 's3', 'ls', f'{PLATINUM_S3_ROOT}/{segment}/'],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return None
        ids = sorted(
            line.split()[-1].rstrip('/')
            for line in result.stdout.splitlines() if 'PRE' in line
        )
        return ids[0] if ids else None
    except Exception:
        return None


def _derive_s3_target(function_body: str, raw_type_name: str) -> str | None:
    m = re.search(r'apiRequest<' + re.escape(raw_type_name) + r'>\s*\(\s*`([^`]+)`',
                  function_body) if raw_type_name else None
    url = m.group(1) if m else ''
    ctx = url
    for vm in re.finditer(r'\$\{(\w+)\}', url):
        bm = re.search(r'\b' + re.escape(vm.group(1)) + r'\s*=\s*`([^`]+)`', function_body)
        if bm:
            ctx += ' ' + bm.group(1)
    for scope in (ctx, function_body):
        for seg in ('clients', 'advisors'):
            if re.search(r'/' + seg + r'/', scope):
                sid = _sample_id(seg)
                return f'{PLATINUM_S3_ROOT}/{seg}/{sid}/' if sid else None
        if re.search(r'/firm/', scope):
            return f'{PLATINUM_S3_ROOT}/firm/'
    return None


def _artifact_name(function_body: str, raw_type_name: str) -> str | None:
    m = re.search(r'apiRequest<' + re.escape(raw_type_name) + r'>\s*\(\s*`([^`]+)`',
                  function_body) if raw_type_name else None
    search_space = m.group(1) if m else function_body
    am = (re.search(r'/(\w+\.json)', search_space)
          or re.search(r'`([\w./${}-]*\b\w+\.json)`', search_space)
          or re.search(r'"([^"]*\b\w+\.json)"', search_space))
    return am.group(1).split('/')[-1] if am else None


def _fetch_s3_raw_fields(function_body: str, raw_type_name: str
                         ) -> tuple[dict[str, list[str]], str, str, str]:
    """(fields, status, s3_uri, vintage).

    D11: `artifact_name is None` means the adapter has NO static artifact -- it calls a
    Lambda. That is NO_S3_SOURCE, not a failed fetch. The old code printed "S3 fetch
    failed" for a fetch it never attempted, which manufactured three false hypotheses
    (creds / empty listing / bad regex) during the 2026-07-10 hand-audit.
    """
    artifact = _artifact_name(function_body, raw_type_name)
    if not artifact:
        return {}, NO_S3_SOURCE, '', ''

    prefix = _derive_s3_target(function_body, raw_type_name)
    if not prefix:
        return {}, FETCH_FAILED, '', ''

    uri = f'{prefix}{artifact}'
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'awscli', 's3', 'cp', uri, '-'],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0 or not result.stdout:
            return {}, FETCH_FAILED, uri, ''
        data = json.loads(result.stdout)
        if not isinstance(data, dict):
            return {}, FETCH_FAILED, uri, ''
    except Exception:
        return {}, FETCH_FAILED, uri, ''

    # D12: a finding without a vintage is not reproducible. The live envelope was
    # observed changing shape mid-session (17 -> 16 top-level keys, 2026-07-10T14:53Z).
    vintage = str(data.get('generated_at') or data.get('data_as_of') or '')

    top: dict[str, list[str]] = {}
    for k, v in data.items():
        if isinstance(v, dict):
            top[k] = list(v.keys())
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            top[k] = list(v[0].keys())
        else:
            top[k] = []
    return top, OK, uri, vintage


# -------- Threading --------

def _raw_identifier(function_body: str) -> str | None:
    """The identifier holding the raw envelope.

    Name-agnostic on purpose (D7): the old predicate hard-coded the literal 'raw'. Nor can
    we assume an `await apiRequest<>` assignment -- getPlatinumAdvisorSummaryStaticInflection
    binds its envelope with `const raw = bookResult.value` off a Promise.allSettled. So:
    prefer the explicit forms, else pick the declared const with the most property accesses.
    """
    m = (re.search(r'const\s+(\w+)\s*=\s*await\s+apiRequest<', function_body)
         or re.search(r'const\s+(\w+)\s*=\s*JSON\.parse', function_body))
    if m:
        return m.group(1)

    best, best_n = None, 0
    for name in dict.fromkeys(re.findall(r'const\s+(\w+)\s*=', function_body)):
        n = len(re.findall(r'\b' + re.escape(name) + r'\s*\.\s*\w+', function_body))
        n += len(re.findall(r'\(\s*' + re.escape(name) + r'\s+as\s+\w+\s*\)\s*\.\s*\w+', function_body))
        if n > best_n:
            best, best_n = name, n
    return best


def _threaded_fields(function_body: str, raw_var: str | None) -> tuple[set[str], bool, bool]:
    """(threaded, passthrough_all, conditional_passthrough).

    D7: `has_spread` tested `'raw' in function_body` while the variable is named `stub`.
    That predicate is decided by a VARIABLE NAME. Exercised 2026-07-10: renaming
    stub->raw flips has_spread False->True and SUPPRESSES three true findings. The tool's
    only true positives were contingent on an identifier.
    U2: in SPLIT mode the return object is rebuilt field-by-field, so NOT-THREADED IS
    meaningful there. `if (!stub.split) return stub` is a CONDITIONAL passthrough; the
    live firm envelope carries `split: true`, so the mapped path is the one that runs.
    """
    if not raw_var:
        return set(), False, False
    rv = re.escape(raw_var)

    if re.search(r'\.\.\.\s*' + rv + r'\b', function_body):
        return set(), True, False

    uncond = False
    cond = False
    for line in function_body.splitlines():
        if re.search(r'\breturn\s+' + rv + r'\b', line):
            if re.match(r'\s*if\s*\(', line.strip()) or re.search(r'\bif\s*\(.*\breturn\s+' + rv, line):
                cond = True
            else:
                uncond = True
    if uncond:
        return set(), True, False

    # `raw.x`, and the cast form `(raw as any).x` the Inflection adapters use.
    threaded = set(re.findall(r'\b' + rv + r'\s*\.\s*(\w+)', function_body))
    threaded |= set(re.findall(r'\(\s*' + rv + r'\s+as\s+\w+\s*\)\s*\.\s*(\w+)', function_body))
    # Top-level keys of the returned object literal. `[^}]*` cannot cross a nested brace
    # and truncated the key set at the first `}` -- which read as "nothing is threaded".
    for m in re.finditer(r'return\s*\{', function_body):
        threaded |= set(_top_level_members(_brace_block(function_body, m.end() - 1)))
    return threaded, False, cond


def _audit_field_threading(raw_type_fields: dict[str, list[str] | None],
                           s3_raw_fields: dict[str, list[str]],
                           function_body: str,
                           raw_type_name: str) -> list[dict]:
    findings: list[dict] = []
    all_typed = set(raw_type_fields)
    all_s3 = set(s3_raw_fields)

    raw_var = _raw_identifier(function_body)
    threaded, passthrough_all, conditional_passthrough = _threaded_fields(function_body, raw_var)

    # D2: name the type ACTUALLY consulted, not f'{adapter_name}Raw' (a string that
    # resolved to nothing -- `getPlatinumFirmDashboardRaw` has 0 occurrences portal-wide).
    for field in sorted(all_s3 - all_typed):
        findings.append({
            'field': field,
            'status': 'SCHEMA-DRIFT',
            'detail': f'In S3 actual envelope but NOT in typed interface {raw_type_name}; type is stale',
            'severity': 'WARN',
        })

    for field in sorted(all_typed - all_s3):
        findings.append({
            'field': field,
            'status': 'TYPE-ONLY',
            'detail': f'Declared in {raw_type_name} but NOT in S3 actual envelope; may be historical or never emitted',
            'severity': 'INFO',
        })

    for field in sorted(all_s3):
        if not passthrough_all and field not in threaded:
            note = ''
            if conditional_passthrough:
                note = (' (a conditional whole-object return exists, but the mapped path '
                        'omits this field; the live envelope determines which path runs)')
            findings.append({
                'field': field,
                'status': 'NOT-THREADED',
                'detail': f'In S3 raw envelope but not threaded into the adapter output{note}',
                'severity': 'WARN',
            })
            continue

        nested_typed = raw_type_fields.get(field)
        if nested_typed is None:
            continue  # guard (c): unresolved named type -- absence of knowledge, not drift
        for nf in sorted(set(s3_raw_fields.get(field, [])) - set(nested_typed)):
            findings.append({
                'field': f'{field}.{nf}',
                'status': 'NESTED-SCHEMA-DRIFT',
                'detail': 'Nested field in S3 raw envelope but not in typed interface; may be silently dropped',
                'severity': 'WARN',
            })

    # FALLBACK-ORDER is the D-1 gate's ONLY BLOCK class. Semantics unchanged deliberately:
    # changing it would arm or disarm a portal pre-push block. (Its `book`/`summary`
    # hardcoding is reported to CTO, not fixed here.)
    fallback_expr = ''
    for _line in function_body.splitlines():
        if '??' in _line and 'book' in _line and 'summary' in _line:
            fallback_expr = _line.strip()
            break
    if fallback_expr and '.book' in fallback_expr and 'summary' in fallback_expr:
        book_pos = fallback_expr.find('.book')
        summary_pos = (fallback_expr.find('.summary') if '.summary' in fallback_expr
                       else fallback_expr.find('summary'))
        headline_pos = fallback_expr.find('.headline') if '.headline' in fallback_expr else -1
        has_spread = '...' in fallback_expr
        inverted = book_pos < summary_pos
        findings.append({
            'field': '_fallback_chain',
            'status': 'FALLBACK-ORDER' if inverted else 'FALLBACK-ORDER-OK',
            'detail': (
                f'Fallback chain: .book@{book_pos} ?? .summary@{summary_pos}'
                + (f' ?? .headline@{headline_pos}' if headline_pos >= 0 else '')
                + (' - book FIRST loses historical_quarters (summary-only field)'
                   if inverted and not has_spread else
                   ' - summary FIRST + spread preserves all fields' if has_spread else
                   ' - check historical_quarters threading')
            ),
            'severity': 'WARN' if inverted and not has_spread else 'INFO',
        })

    return findings


# -------- Manifest --------

def _write_manifest(directory: Path, adapter_name: str, ts_file: Path, raw_type_name: str,
                    type_source: Path | None, status: str, reason: str, s3_uri: str,
                    vintage: str, raw_type_fields: dict, s3_raw_fields: dict,
                    findings: list[dict]) -> Path:
    verified = status == OK
    warns = [f for f in findings if f['severity'] == 'WARN']

    lines = [
        f'adapter_fn: {adapter_name}',
        f'source_file: {_rel(str(ts_file))}',
        f'raw_type: {raw_type_name or "UNRESOLVED"}',
        f'raw_type_source: {_rel(str(type_source)) if type_source else "UNRESOLVED"}',
        # D5: the manifest must be unmistakable to a reader who sees ONLY the yaml.
        f'verified: {"true" if verified else "false"}',
        f'verification_status: {status}',
    ]
    if not verified:
        lines.append(f'unverified_reason: {reason!r}')
    lines += [
        f's3_uri: {s3_uri or "NONE"}',
        f's3_artifact_vintage: {vintage or "UNKNOWN"}',   # D12
        f'typed_field_count: {len(raw_type_fields) if verified else "null"}',
        f's3_field_count: {len(s3_raw_fields) if verified else "null"}',
        f'total_findings: {len(findings) if verified else "null"}',
        f'warn_count: {len(warns) if verified else "null"}',
        'findings:',
    ]
    for f in findings:
        lines.append(f'  - field: {f["field"]}')
        lines.append(f'    status: {f["status"]}')
        lines.append(f'    severity: {f["severity"]}')
        lines.append(f'    detail: {repr(f["detail"][:150])}')

    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f'{adapter_name}.yaml'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return path


# -------- Command --------

def cmd_audit(args: argparse.Namespace) -> int:
    adapter_name = args.adapter_fn
    severity_filter = getattr(args, 'severity', None)
    manifest_dir = Path(getattr(args, 'manifest_dir', None) or _ADAPTER_AUDIT_DIR)

    print(f'COMP-ADAPTER-AUDIT: {adapter_name}')

    ts_file, function_body = _find_adapter_source(adapter_name)
    if not ts_file:
        print(f'  ERROR: adapter function {adapter_name!r} not found in endpoint files')
        print('\nERROR: comp-adapter-audit could not locate the adapter')
        return RC_FAIL
    print(f'  Source: {_rel(str(ts_file))}')
    print(f'  Function body: {len(function_body.splitlines())} lines')

    raw_type_name, how = _extract_raw_type_name(function_body)
    print(f'  Raw input type: {raw_type_name or "UNRESOLVED"}  [{how}]')

    corpus = _import_corpus(ts_file)
    raw_type_fields, type_source = _resolve_type_fields(corpus, raw_type_name) if raw_type_name else ({}, None)
    print(f'  Typed fields: {len(raw_type_fields)} top-level in {raw_type_name or "UNRESOLVED"}'
          f'{f" (from {_rel(str(type_source))})" if type_source else ""}')

    print('  Fetching S3 raw envelope...')
    s3_raw_fields, status, s3_uri, vintage = _fetch_s3_raw_fields(function_body, raw_type_name)

    if status == OK and not raw_type_fields:
        status = TYPE_UNRESOLVED

    reason = {
        NO_S3_SOURCE: ('adapter has NO static S3 artifact -- it fetches from a Lambda '
                       'endpoint. The S3-envelope threading audit DOES NOT APPLY.'),
        FETCH_FAILED: f'an S3 source was derived ({s3_uri or "prefix undeterminable"}) but could not be read.',
        TYPE_UNRESOLVED: f'the raw input type could not be resolved ({how}); the typed side is empty.',
        OK: '',
    }[status]

    if status == OK:
        print(f'  S3 raw fields: {len(s3_raw_fields)} top-level keys  [{s3_uri} @ {vintage or "UNKNOWN"}]')
        findings = _audit_field_threading(raw_type_fields, s3_raw_fields, function_body, raw_type_name)
        print(f'\n  Field threading audit ({len(findings)} finding(s)):\n')
        if not findings:
            print('  PASS: all S3 fields are typed and threaded through adapter')
        else:
            rank = {'WARN': 0, 'INFO': 1}
            for f in sorted(findings, key=lambda f: (rank.get(f['severity'], 2), f['field'])):
                if severity_filter == 'error' and f['severity'] != 'WARN':
                    continue
                print(f'  {f["status"]:<22}  {f["severity"]:<5}  {f["field"]}')
                print(f'  {"":22}  {"":5}  {f["detail"][:110]}')
    else:
        findings = []
        label = 'NOT-APPLICABLE' if status == NO_S3_SOURCE else 'UNVERIFIED'
        print(f'\n  {label}: {status} -- threading audit SKIPPED')
        print(f'    {reason}')
        print('    This is NOT a pass and NOT a set of real findings. Zero findings here')
        print('    means the comparison never ran, not that the adapter is clean.')

    warns = [f for f in findings if f['severity'] == 'WARN']
    drifts = [f for f in findings if 'SCHEMA-DRIFT' in f['status'] or 'NOT-THREADED' in f['status']]
    if status == OK:
        print(f'\n  Summary: {len(warns)} WARN(s), {len(drifts)} threading/drift issue(s)')

    path = _write_manifest(manifest_dir, adapter_name, ts_file, raw_type_name, type_source,
                           status, reason, s3_uri, vintage, raw_type_fields, s3_raw_fields, findings)
    print(f'\n  Manifest: {_rel(str(path))}  (verified: {"true" if status == OK else "false"})')

    # D6: the success token is bound to the AUDIT, not to the absence of a severity filter.
    # 15 WARNs must never print PASS; an unaudited adapter must never print PASS.
    if status != OK:
        print(f'\n{"NOT-APPLICABLE" if status == NO_S3_SOURCE else "UNVERIFIED"}: '
              f'comp-adapter-audit could not evaluate {adapter_name} ({status})')
        return RC_CANNOT_EVALUATE
    if severity_filter == 'error' and warns:
        print(f'\nFAIL: comp-adapter-audit complete -- {len(warns)} WARN(s)')
        return RC_FAIL
    if warns:
        print(f'\nWARN: comp-adapter-audit complete -- {len(warns)} WARN(s), 0 blocking')
        return RC_OK
    print('\nPASS: comp-adapter-audit complete -- 0 WARN(s)')
    return RC_OK


def main() -> int:
    parser = argparse.ArgumentParser(
        prog='comp-adapter-audit',
        description='Portal adapter function field-threading audit',
    )
    parser.add_argument('adapter_fn', help='Adapter function name (e.g. getPlatinumFirmDashboard)')
    parser.add_argument('--severity', choices=['warn', 'error'], default=None,
                        help='Filter findings by severity; error exits 1 on any WARN')
    parser.add_argument('--manifest-dir', default=None,
                        help='Write the manifest here instead of org/modules/graph/adapter-audit/ '
                             '(for read-only exercise; the D-1 gate reads the default dir)')
    return cmd_audit(parser.parse_args())


if __name__ == '__main__':
    sys.exit(main())
