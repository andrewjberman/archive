/**
 * sidebar.cjs -- DSGN_AMGTV1 round 9, AV-p-4: THE SECURITY ANALYSIS ICON SITS IN THE TOOLS SECTION, DIRECTLY BENEATH SECURITY
 * SCANNER (Andrew-direct 2026-09-30 ~03:1xZ to 2.0.0_SA_COO~D, verbatim: "the Security Analysis icon in the portal sidebar is in
 * the wrong location. It is a tool, so it shoudl actually sit beneath the Security Scanner icon in the tools section.").
 *
 * Usage (repo root): node <this file>
 * Reads portal/src/App.tsx NAV_SECTIONS (the sidebar's one source) as text. At base the entry sits in the 'analysis' section
 * between Philosophy and Positioning.
 * Arms:
 *   1  exactly ONE '/security-analysis' entry in NAV_SECTIONS, and it is in the section with id 'tools'
 *   2  it is the item directly after '/security-scanner' in that section; every other item of both sections keeps its order
 *   3  the entry keeps its label, icon and gate ("Security Analysis", LayoutGrid, requiresDev: true, requiresAdmin: true), and
 *      both routes keep their ProtectedRoute requireDev requireAdmin
 * Prints each section's paths, one line per arm and "SECURITY ANALYSIS UNDER TOOLS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const file = path.join(process.cwd(), 'portal/src/App.tsx');
const text = fs.readFileSync(file, 'utf8');
const start = text.indexOf('NAV_SECTIONS');
const end = text.indexOf('const NAV_ICONS', start);
const nav = start >= 0 && end > start ? text.slice(start, end) : '';
const sections = [];
for (const m of nav.matchAll(/id:\s*'([^']+)'/g)) sections.push({ id: m[1], at: m.index });
const secOf = (at) => { let s = null; for (const x of sections) if (x.at < at) s = x.id; return s; };
const items = [...nav.matchAll(/\{\s*path:\s*'([^']+)'[^}]*\}/g)].map((m) => ({ path: m[1], body: m[0], section: secOf(m.index) }));
const paths = (id) => items.filter((i) => i.section === id).map((i) => i.path);
for (const s of sections) console.log(`SECTION ${s.id}: ${JSON.stringify(paths(s.id))}`);

const BASE_ANALYSIS = ['/philosophy', '/positioning', '/attribution', '/factor-tilts', '/valuations', '/correlations', '/macro'];
const BASE_TOOLS = ['/security-scanner', '/portfolio-management', '/trade-submission', '/ticket-center'];
const sa = items.filter((i) => i.path === '/security-analysis');
const a1 = sa.length === 1 && sa[0].section === 'tools';
const tools = paths('tools');
const at = tools.indexOf('/security-analysis');
const a2 = at > 0 && tools[at - 1] === '/security-scanner'
  && JSON.stringify(tools.filter((p) => p !== '/security-analysis')) === JSON.stringify(BASE_TOOLS)
  && JSON.stringify(paths('analysis')) === JSON.stringify(BASE_ANALYSIS);
const b = sa[0] ? sa[0].body : '';
const routes = [...text.matchAll(/<Route path="\/security-analysis[^"]*" element=\{<ProtectedRoute requireDev requireAdmin><SecurityAnalysis \/><\/ProtectedRoute>\} \/>/g)].length;
const a3 = /label:\s*'Security Analysis'/.test(b) && /icon:\s*LayoutGrid/.test(b) && /requiresDev:\s*true/.test(b) && /requiresAdmin:\s*true/.test(b) && routes === 2;
const arms = [
  ['one Security Analysis entry, in Tools', a1, `${sa.length} entry(ies); section ${sa.map((i) => i.section).join(',') || 'none'}`],
  ['directly beneath Security Scanner; every other item keeps its order', a2, `tools ${JSON.stringify(tools)}`],
  ['label, icon and gate kept; both routes gated', a3, `entry "${b.replace(/\s+/g, ' ')}"; gated routes ${routes}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`SECURITY ANALYSIS UNDER TOOLS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
