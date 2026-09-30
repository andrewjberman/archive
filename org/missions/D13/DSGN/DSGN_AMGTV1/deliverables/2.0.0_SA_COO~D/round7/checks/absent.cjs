/**
 * absent.cjs -- DSGN_AMGTV1 round 7, AV-s-1: A NO-CALL POSTURE IS A DESIGNED EMPTY STATE, NEVER THE SERVED REASON (round-6
 * analysis ruling 1; FWD-11).
 *
 * Usage (repo root): node <this file>
 * The served 992 HK /thesis (round7/fixtures/thesisBundle.992_HK_Equity.json, captured at the cut from the deployed scoped API)
 * carries posture {status: SERVED, verdict: "absent", comparable: null} whose `reason` is the producer's own prose: a file name
 * (model_block_992_HK_Equity.json), a project code (AMGT-s-1) and ruling ids (F2/G-24). That text is the POSITIVE CONTROL: it
 * must never reach visible text. One ISSUER VARIANT (labelled below) is built in memory: the same bundle with posture
 * {status: "ABSENT"} and a planted machine reason, because no served fixture carries an ABSENT posture.
 * The page shows the designed empty state "No call on this name yet" plus ONE plain reason class taken from the served STATUS
 * only, carried on `data-posture-reason-class`:
 *   not-drafted   -- status ABSENT (no posture drafted for this name)
 *   no-comparable -- status SERVED, verdict "absent", comparable null (no comparable company could be matched)
 *   no-call-made  -- status SERVED, verdict "absent", comparable present (the evidence did not support a call)
 * The served reason stays on the element's attribute (`data-posture-reason`), never in visible text.
 * Arms:
 *   1  the Posture tab (tabs/PostureTab.tsx) on 992 HK (no-comparable) and on the ABSENT variant (not-drafted): visible text
 *      carries "No call on this name yet", the reason-class attribute reads the expected class, no fragment of the served /
 *      planted reason and no "ABSENT" word is visible, and data-posture-reason still carries the served reason
 *   2  the header's one posture line -- SecurityOverlay.tsx IdentityHeader (the live one) AND LeadPanel.tsx's exported
 *      PostureHeaderLine (the copy the page harnesses read) -- on the same two postures: the same four conditions
 *   3  the control: a served CALL (VLO, verdict better) still renders its verdict word (BETTER) and sentence on the tab and
 *      in the header, and no no-call wording appears there
 * Prints one line per arm and "NO-CALL POSTURE IN WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const hk = L.fixture('thesisBundle.992_HK_Equity.json');
const hkOv = L.fixture('overlay.992_HK_Equity.json');
const vlo = L.fixture('thesisBundle.VLO_US_Equity.json');
const vloOv = L.fixture('overlay.VLO_US_Equity.json');
const served = hk.posture || {};
// ISSUER VARIANT (not served): an ABSENT posture carrying a planted machine reason.
const PLANT = 'no landed model_block_ZZ_US_Equity.json (AMGT-zz-9 record, F9/G-99) -- PLANTED_REASON_TOKEN';
const absentPosture = { status: 'ABSENT', security_key: '992_HK_Equity', reason: PLANT };
const hkAbsent = clone(hk);
hkAbsent.posture = absentPosture;
const hkOvAbsent = clone(hkOv);
hkOvAbsent.posture = absentPosture;

const bundles = { '992_HK_Equity': hk, 'ZZ_ABSENT': hkAbsent, VLO_US_Equity: vlo };
L.hookState.impl = { useThesisBundle: (k) => bundles[k], usePeerSet: () => undefined, useManagement: () => undefined };
L.stubSource('src/pages/SecurityAnalysis/components/TimelinePanel.tsx', { TimelinePanel: () => null });

const NO_CALL = /No call on this name yet/;
// fragments of each reason that must never be visible: every 18-character window of the reason, plus its code shapes
const fragments = (r) => {
  const s = String(r || '');
  const out = [];
  for (let i = 0; i + 18 <= s.length; i += 6) out.push(s.slice(i, i + 18));
  return out;
};
const CODE_SHAPES = /model_block|\.json\b|AMGT-[a-z]+-\d|\bF\d+\/G-\d+|PLANTED_REASON_TOKEN|\bABSENT\b/;
const leak = (text, reason) => {
  const f = fragments(reason).find((x) => text.includes(x));
  if (f) return 'reason fragment "' + f + '"';
  const m = text.match(CODE_SHAPES);
  return m ? 'code shape "' + m[0] + '"' : null;
};
const attr = (html, name) => ((new RegExp(name + '="([^"]*)"')).exec(html) || [])[1];
const unesc = (s) => String(s || '').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const safe = (f) => { try { return f(); } catch (e) { return 'RENDER FAILED ' + String(e.message).split('\n')[0]; } };
function judge(where, html, reason, cls) {
  const text = L.textOf(html);
  const l = leak(text, reason);
  const c = attr(html, 'data-posture-reason-class');
  const kept = unesc(attr(html, 'data-posture-reason')) === String(reason);
  const ok = !/^RENDER FAILED/.test(html) && NO_CALL.test(text) && c === cls && !l && kept;
  return { where, ok, detail: `${where}: no-call words ${NO_CALL.test(text)}, class ${c || 'none'} (want ${cls}), leak ${l || 'none'}, reason on attribute ${kept}` };
}

const tab = () => L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx').PostureTab;
const ov = () => L.source('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx');
const lp = () => L.source('src/pages/SecurityAnalysis/components/LeadPanel.tsx');

// ---- arm 1: the Posture tab ---------------------------------------------------------------------------------------------
const a1c = [
  judge('tab 992 HK', safe(() => L.render(tab(), { securityKey: '992_HK_Equity' })), served.reason, 'no-comparable'),
  judge('tab ABSENT variant', safe(() => L.render(tab(), { securityKey: 'ZZ_ABSENT' })), PLANT, 'not-drafted'),
];
// ---- arm 2: the header's posture line, both copies ---------------------------------------------------------------------
const header = (bundle) => safe(() => { const m = ov(); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle, onBack: () => {}, onRefresh: () => {} }); });
const lpLine = (posture, bundle) => safe(() => L.render(lp().PostureHeaderLine, { posture, subjectIdentity: bundle.identity }));
const a2c = [
  judge('header 992 HK', header(hkOv), served.reason, 'no-comparable'),
  judge('header ABSENT variant', header(hkOvAbsent), PLANT, 'not-drafted'),
  judge('LeadPanel line 992 HK', lpLine(hkOv.posture || served, hkOv), (hkOv.posture || served).reason, 'no-comparable'),
  judge('LeadPanel line ABSENT variant', lpLine(absentPosture, hkOvAbsent), PLANT, 'not-drafted'),
];
// ---- arm 3: the control -- a served call is unchanged ------------------------------------------------------------------
const vloTab = L.textOf(safe(() => L.render(tab(), { securityKey: 'VLO_US_Equity' })));
const vloHead = L.textOf(header(vloOv));
const a3 = /\bBETTER\b/.test(vloTab) && /BETTER pick/.test(vloHead) && !NO_CALL.test(vloTab) && !NO_CALL.test(vloHead);
const a3d = `VLO tab BETTER ${/\bBETTER\b/.test(vloTab)}, header "BETTER pick" ${/BETTER pick/.test(vloHead)}, no-call wording absent ${!NO_CALL.test(vloTab) && !NO_CALL.test(vloHead)}`;

const arms = [
  ['the Posture tab shows the designed no-call state, never the served reason', a1c.every((c) => c.ok), a1c.map((c) => c.detail).join(' | ')],
  ['the header posture line (live + exported copy) does the same', a2c.every((c) => c.ok), a2c.map((c) => c.detail).join(' | ')],
  ['control: a served call (VLO, better) is unchanged', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`NO-CALL POSTURE IN WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
