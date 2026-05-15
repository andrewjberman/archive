#!/usr/bin/env python3
"""adapter_audit_cli.py — comp-adapter-audit backend: portal adapter field-threading audit."""
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

# Known adapter endpoints file locations (searched in order)
_ENDPOINT_FILES = [
    _PORTAL_SRC / 'api' / 'endpoints' / 'advisor-intelligence.ts',
    _PORTAL_SRC / 'api' / 'endpoints' / 'portfolio.ts',
]

# -------- Helpers --------

def _rel(path_str: str) -> str:
    try:
        return str(Path(path_str).relative_to(_WORKSPACE))
    except ValueError:
        return path_str


def _find_adapter_source(adapter_name: str) -> tuple[Path | None, str]:
    """Find the TypeScript file + function body for an adapter function.

    Returns (file_path, function_body_text) or (None, '').
    """
    search_files = list(_ENDPOINT_FILES)
    # Also scan all endpoint files
    ep_dir = _PORTAL_SRC / 'api' / 'endpoints'
    if ep_dir.exists():
        for f in sorted(ep_dir.glob('*.ts')):
            if f not in search_files:
                search_files.append(f)

    for ts_file in search_files:
        if not ts_file.exists():
            continue
        src = ts_file.read_text(encoding='utf-8', errors='ignore')
        # Match async function <name>( ... ) { ... }
        # Use a simple line-based approach to find function start
        lines = src.splitlines()
        fn_start = None
        for i, line in enumerate(lines):
            if re.search(rf'(async\s+function|function)\s+{re.escape(adapter_name)}\s*\(', line):
                fn_start = i
                break
        if fn_start is None:
            # Try arrow function / const assignment
            for i, line in enumerate(lines):
                if re.search(rf'\b{re.escape(adapter_name)}\s*=', line):
                    fn_start = i
                    break
        if fn_start is None:
            continue

        # Find the function body by brace counting
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
                if depth <= 0 and started:
                    break

        return ts_file, '\n'.join(body_lines)

    return None, ''


def _extract_raw_type_name(function_body: str) -> str:
    """Extract the raw input type name from the function body (apiRequest<TypeName>)."""
    m = re.search(r'apiRequest<(\w+)>', function_body)
    if m:
        return m.group(1)
    m = re.search(r'as\s+(\w+Raw\w*)', function_body)
    if m:
        return m.group(1)
    return ''


def _extract_type_fields_from_interface(ts_src: str, type_name: str) -> dict[str, list[str]]:
    """Extract field names from a TypeScript interface/type definition.

    Returns {top_field: [nested_field, ...]} for nested objects.
    """
    m = re.search(r'interface\s+' + re.escape(type_name) + r'\s*\{([\s\S]*?)\n\}', ts_src)
    if not m:
        return {}
    body = m.group(1)
    fields: dict[str, list[str]] = {}
    current_top = None
    depth = 0
    nested_lines: list[str] = []

    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('//') or stripped.startswith('*'):
            continue
        opens = stripped.count('{')
        closes = stripped.count('}')
        if depth == 0:
            fm = re.match(r'(\w+)\??:', stripped)
            if fm:
                current_top = fm.group(1)
                fields[current_top] = []
                nested_lines = []
        elif depth > 0:
            # inside a nested block
            fm = re.match(r'(\w+)\??:', stripped)
            if fm and current_top:
                fields[current_top].append(fm.group(1))
        depth += opens - closes

    return fields


def _fetch_s3_raw_fields(adapter_name: str, function_body: str) -> dict[str, list[str]]:
    """Fetch actual S3 raw envelope for the adapter's data source.

    Returns {top_field: [nested_field, ...]} from the live JSON.
    """
    # Extract S3 path from the function body
    s3_patterns = [
        r'`\$\{[^}]+\}/advisors/\$\{[^}]+\}/(\w+\.json)`',
        r'"([^"]+\.json)"',
        r'PLATINUM_BASE\}/advisors/\$\{[^}]+\}/(\w+\.json)',
    ]
    artifact_name = 'book.json'  # default for advisor adapter
    for pat in s3_patterns:
        m = re.search(pat, function_body)
        if m:
            artifact_name = m.group(1)
            break

    # Determine which S3 prefix to use
    # For advisor-intelligence adapters, use a known advisor path
    s3_prefixes = [
        's3://opal-data-inf/platinum/advisors/inflection_wealth_management/',
        's3://opal-data-inf/platinum/advisors/peter_lee/',
    ]

    for prefix in s3_prefixes:
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'awscli', 's3', 'cp', f'{prefix}{artifact_name}', '-'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                if isinstance(data, dict):
                    top_fields: dict[str, list[str]] = {}
                    for k, v in data.items():
                        nested: list[str] = []
                        if isinstance(v, dict):
                            nested = list(v.keys())
                        elif isinstance(v, list) and v and isinstance(v[0], dict):
                            nested = list(v[0].keys())
                        top_fields[k] = nested
                    return top_fields
        except Exception:
            continue
    return {}


def _audit_field_threading(
    raw_type_fields: dict[str, list[str]],
    s3_raw_fields: dict[str, list[str]],
    function_body: str,
    adapter_name: str,
) -> list[dict]:
    """Compare raw type fields, S3 actual fields, and function body references.

    Returns list of audit findings per field.
    """
    findings: list[dict] = []

    # All fields from the typed raw interface
    all_typed = set(raw_type_fields.keys())
    # All fields actually in S3
    all_s3 = set(s3_raw_fields.keys())
    # All top-level raw field references in function body (raw.X, (raw as any).X)
    referenced = set()
    for m in re.finditer(r'(?:raw|headline|composition|billing|clients?)\s*\.\s*(\w+)', function_body):
        referenced.add(m.group(1))
    # Also check spread patterns
    has_spread = '...' in function_body and 'raw' in function_body

    # Fields in S3 but NOT in typed interface = schema drift (type is stale)
    for field in sorted(all_s3 - all_typed):
        findings.append({
            'field': field,
            'status': 'SCHEMA-DRIFT',
            'detail': f'In S3 actual envelope but NOT in typed interface {adapter_name}Raw; type is stale',
            'severity': 'WARN',
        })

    # Fields in typed interface but NOT in S3 = possibly removed or never emitted
    for field in sorted(all_typed - all_s3):
        findings.append({
            'field': field,
            'status': 'TYPE-ONLY',
            'detail': f'Declared in typed interface but NOT in S3 actual envelope; may be historical or never emitted',
            'severity': 'INFO',
        })

    # Fields in S3 but not explicitly referenced in the adapter body
    for field in sorted(all_s3):
        is_ref = field in referenced or any(field in line for line in function_body.splitlines())
        if not is_ref and not has_spread:
            findings.append({
                'field': field,
                'status': 'NOT-THREADED',
                'detail': f'In S3 raw envelope but adapter body has no explicit reference; silently dropped',
                'severity': 'WARN',
            })
        elif is_ref:
            # Check nested fields
            nested_s3 = s3_raw_fields.get(field, [])
            nested_typed = raw_type_fields.get(field, [])
            for nf in sorted(set(nested_s3) - set(nested_typed)):
                findings.append({
                    'field': f'{field}.{nf}',
                    'status': 'NESTED-SCHEMA-DRIFT',
                    'detail': f'Nested field in S3 raw envelope but not in typed interface; may be silently dropped',
                    'severity': 'WARN',
                })

    # Look for inverted fallback patterns (order matters)
    # Use line-by-line scan to capture full ?? chain (regex non-greedy truncates on inner parens)
    fallback_expr = ''
    for _line in function_body.splitlines():
        if '??' in _line and 'book' in _line and 'summary' in _line:
            fallback_expr = _line.strip()
            break
    if fallback_expr:
        # Check if a narrower field comes before a broader field
        # Use .book / .summary / .headline to find field ACCESSES not variable names
        if '.book' in fallback_expr and ('.summary' in fallback_expr or 'summary' in fallback_expr):
            book_pos = fallback_expr.find('.book')
            summary_pos = fallback_expr.find('.summary') if '.summary' in fallback_expr else fallback_expr.find('summary')
            headline_pos = fallback_expr.find('.headline') if '.headline' in fallback_expr else -1
            has_spread = '...' in fallback_expr
            findings.append({
                'field': '_fallback_chain',
                'status': 'FALLBACK-ORDER' if book_pos < summary_pos else 'FALLBACK-ORDER-OK',
                'detail': (
                    f'Fallback chain: .book@{book_pos} ?? .summary@{summary_pos}'
                    + (f' ?? .headline@{headline_pos}' if headline_pos >= 0 else '')
                    + (' — book FIRST loses historical_quarters (summary-only field)' if book_pos < summary_pos and not has_spread else
                       ' — summary FIRST + spread preserves all fields' if has_spread else
                       ' — check historical_quarters threading')
                ),
                'severity': 'WARN' if book_pos < summary_pos and not has_spread else 'INFO',
            })

    return findings


def cmd_audit(args: argparse.Namespace) -> int:
    adapter_name = args.adapter_fn
    severity_filter = getattr(args, 'severity', None)

    print(f'COMP-ADAPTER-AUDIT: {adapter_name}')

    # Phase 1: Find adapter source
    ts_file, function_body = _find_adapter_source(adapter_name)
    if not ts_file:
        print(f'  ERROR: adapter function {adapter_name!r} not found in endpoint files')
        return 1
    print(f'  Source: {_rel(str(ts_file))}')
    print(f'  Function body: {len(function_body.splitlines())} lines')

    # Phase 2: Extract raw type name
    raw_type_name = _extract_raw_type_name(function_body)
    if not raw_type_name:
        print(f'  WARN: could not detect raw input type from function body')
        raw_type_name = 'Unknown'
    print(f'  Raw input type: {raw_type_name}')

    # Phase 3: Extract typed fields from interface definition
    ts_src = ts_file.read_text(encoding='utf-8', errors='ignore')
    raw_type_fields = _extract_type_fields_from_interface(ts_src, raw_type_name)
    print(f'  Typed fields: {len(raw_type_fields)} top-level fields in {raw_type_name}')

    # Phase 4: Fetch S3 raw envelope
    print(f'  Fetching S3 raw envelope...')
    s3_raw_fields = _fetch_s3_raw_fields(adapter_name, function_body)
    if s3_raw_fields:
        print(f'  S3 raw fields: {len(s3_raw_fields)} top-level keys')
    else:
        print(f'  WARN: S3 fetch failed or returned no data; skipping live schema check')

    # Phase 5: Threading audit
    findings = _audit_field_threading(raw_type_fields, s3_raw_fields, function_body, adapter_name)

    # Print results
    print(f'\n  Field threading audit ({len(findings)} finding(s)):\n')
    if not findings:
        print('  PASS: all S3 fields are typed and threaded through adapter')
    else:
        severity_rank = {'WARN': 0, 'INFO': 1}
        findings_sorted = sorted(findings, key=lambda f: (severity_rank.get(f['severity'], 2), f['field']))

        print(f'  {"STATUS":<22}  {"SEV":<5}  FIELD / DETAIL')
        print(f'  {"-"*22}  {"-"*5}  {"-"*60}')
        for f in findings_sorted:
            if severity_filter == 'error' and f['severity'] != 'WARN':
                continue
            print(f'  {f["status"]:<22}  {f["severity"]:<5}  {f["field"]}')
            print(f'  {"":22}  {"":5}  {f["detail"][:100]}')

    # Count severities
    warns = [f for f in findings if f['severity'] == 'WARN']
    schema_drifts = [f for f in findings if 'SCHEMA-DRIFT' in f['status'] or 'NOT-THREADED' in f['status']]
    print(f'\n  Summary: {len(warns)} WARN(s), {len(schema_drifts)} threading/drift issue(s)')

    # Write manifest
    _ADAPTER_AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = _ADAPTER_AUDIT_DIR / f'{adapter_name}.yaml'
    yaml_lines = [
        f'adapter_fn: {adapter_name}',
        f'source_file: {_rel(str(ts_file))}',
        f'raw_type: {raw_type_name}',
        f'typed_field_count: {len(raw_type_fields)}',
        f's3_field_count: {len(s3_raw_fields)}',
        f'total_findings: {len(findings)}',
        f'warn_count: {len(warns)}',
        f'findings:',
    ]
    for f in findings:
        yaml_lines.append(f'  - field: {f["field"]}')
        yaml_lines.append(f'    status: {f["status"]}')
        yaml_lines.append(f'    severity: {f["severity"]}')
        yaml_lines.append(f'    detail: {repr(f["detail"][:150])}')
    manifest_path.write_text('\n'.join(yaml_lines) + '\n', encoding='utf-8')
    print(f'\n  Manifest: {_rel(str(manifest_path))}')

    exit_code = 1 if (severity_filter == 'error' and warns) else 0
    status = 'FAIL' if exit_code else 'PASS'
    print(f'\n{status}: comp-adapter-audit complete')
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(
        prog='comp-adapter-audit',
        description='Portal adapter function field-threading audit'
    )
    parser.add_argument('adapter_fn', help='Adapter function name (e.g. getPlatinumAdvisorSummaryStaticInflection)')
    parser.add_argument('--severity', choices=['warn', 'error'], default=None,
                        help='Filter findings by severity; error exits 1 on any WARN')

    args = parser.parse_args()
    return cmd_audit(args)


if __name__ == '__main__':
    sys.exit(main())
