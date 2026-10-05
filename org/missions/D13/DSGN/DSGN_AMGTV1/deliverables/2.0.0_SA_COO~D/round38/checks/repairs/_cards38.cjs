/**
 * _cards38.cjs -- the shared instrument of repairs38.cjs, DSGN_AMGTV1 round 38 (issuer 2.0.0_SA_COO~D). NOT a check: it grades
 * nothing by itself. repairs38.cjs (the graders, the planted shapes) and _render38.cjs (the served field census per render) both
 * require it, so the census the renders print and the census the graders read are one table.
 *
 * THE CARD TABLE (CARDS below): every card of the Security Analysis page at base 85e24287, the payload it reads and the SERVED
 *   fields that carry its time and its source. A field is listed by path into that payload ("a.b[].c" walks every array member);
 *   a field whose value is null / '' / absent is NOT served. A card WANTS the footer when at least one time field AND at least one
 *   source field are served (FWD-11); otherwise it prints no footer line (FWD-27).
 *   Fields deliberately NOT read as a source (machine provenance, printed nowhere a reader looks): `*.posture_read.source`,
 *   `*.management_read.source`, `drafting_source`, `read.source` (all "pool"), `identity.crosswalk_source` (an s3 path),
 *   `feed.source` (the producer's table name), `csc_columns.source` (a repo path), `union_universe_source`, `posture.packs.*`.
 * CARD REGIONS in a page render (react-dom/server markup; shared chrome is the loader's stub, data-stub="<export name>"):
 *   (HEAD = the first data-stub="Panel" with no Panel above it that comes before data-stub="TabNavigation".)
 *   K  identity + key-figure row (Security mode): from the start of HEAD to the start of [data-header-brief] (else
 *      [data-timeline-panel], else [data-header-more], else the end of HEAD).
 *   N  recent news: from [data-header-brief] to the start of [data-timeline-panel] (else [data-header-more], else HEAD's end).
 *   T  news timeline + word cloud: from [data-timeline-panel] to the start of [data-header-more] (else HEAD's end).
 *   TAB  the active tab's card: the first data-stub="Panel" after the data-stub="TabNavigation" element (the whole Panel).
 *   W  What changed (Model tab): the section[data-what-changed] (the whole section) -- a card nested inside TAB.
 *   LEAD  the Lead Panel (Universe mode): the whole of HEAD.
 *   A nested card's region is cut out of its parent's for every count below.
 * THE SHARED PIECES, as _render38.cjs stubs them (so a check can see the shared component was USED):
 *   PanelFooter      <div data-check-shared="PanelFooter" data-check-props="<JSON of content/timestamp/dataAsOf/frequency>"> around
 *                    the REAL PanelFooter's markup (src/ui/components/panels/PanelFooter.tsx; its printed text is the real
 *                    formatPanelTimestamp + " | " + content).
 *   SmartPanelFooter <div data-check-shared="SmartPanelFooter" ...> -- it stamps the DATA MANIFEST's time (useDataFreshness), never a
 *                    field this page serves, so it is always a fault here.
 *   PageEnd          <div data-check-shared="PageEnd" data-check-props="{pageName, dataAsOf, ...every other prop handed over}"> around
 *                    the REAL PageEnd markup (its printed date is graded in words, round 39 row S3: endDateFaults).
 * Writes no file; no network, no AWS.
 */
const norm = (s) => String(s === null || s === undefined ? '' : s).replace(/\s+/g, ' ').trim();

// ---- the card table ------------------------------------------------------------------------------------------------------------
const CARDS = {
  K: { name: 'identity + key-figure row', payload: 'overlay', times: ['header_figures[].vintage'], sources: ['header_figures[].source'] },
  N: { name: 'recent news', payload: 'overlay', times: ['feed.items[].published_at', 'feed.items[].published_date', 'feed.window.end_date'], sources: ['feed.items[].publisher'] },
  T: { name: 'news timeline + word cloud', payload: 'timeline', times: ['word_cloud.window.to', 'series[].date', 'markers[].date'], sources: ['source', 'publisher', 'series[].publisher', 'events[].publisher', 'events[].publishers', 'word_cloud.source'] },
  thesis: { name: 'Thesis tab', payload: 'thesis', times: ['generated_at', 'as_of_date', 'drafting_provenance.filing_date'], sources: ['thesis_driver_chart.source', 'drafting_provenance.form'] },
  exec_management: { name: 'Exec Management tab', payload: 'thesis', times: ['management.as_of', 'management.object_as_of', 'management.management_read.as_of'], sources: ['management.roster_source', 'management.officers[].source', 'management.source_form'] },
  peers: { name: 'Peers tab', payload: 'peers', times: ['as_of', 'vintage', 'peer_read.as_of'], sources: ['members[].cap_source', 'subject.source'] },
  model: { name: 'Model tab', payload: 'thesis', times: ['model.generated_at', 'generated_at', 'model.fiscal_year_figures[].vintage', 'model.forecast_figures[].vintage'], sources: ['model.fiscal_year_figures[].source', 'model.forecast_figures[].source'] },
  W: { name: 'What changed (Model tab)', payload: 'compare+thesis', times: ['compare:compared.to_stamp'], sources: ['thesis:header_figures[].source', 'thesis:model.forecast_figures[].source'] },
  posture: { name: 'Posture tab', payload: 'thesis', times: ['posture.as_of', 'posture.posture_read.as_of', 'posture.generation.generated_at'], sources: ['posture.marked'] },
  LEAD_PRICE: { name: 'Lead Panel, Price face', payload: 'rankings', times: ['as_of_date', 'rows[].as_of_date'], sources: ['rows[].source'] },
  LEAD_CHATTER: { name: 'Lead Panel, Chatter face', payload: 'chatter', times: ['as_of', 'window_end'], sources: ['source'] },
};
/** The page's served dates for the end line, by mode (YYYY-MM-DD or a stamp whose day is read). */
const PAGE_TIMES = {
  security: ['overlay:price.as_of_date', 'overlay:breakout_price.as_of_date', 'overlay:axis_reads[].as_of_date', 'overlay:header_figures[].vintage', 'overlay:feed.window.end_date'],
  universe: ['rankings:as_of_date', 'chatter:as_of', 'chatter:window_end'],
};

function pathValues(obj, p) {
  let cur = [obj];
  for (const part of p.split('.')) {
    const arr = part.endsWith('[]');
    const k = arr ? part.slice(0, -2) : part;
    const next = [];
    for (const c of cur) {
      if (!c || typeof c !== 'object') continue;
      const v = c[k];
      if (arr) { if (Array.isArray(v)) next.push(...v); } else next.push(v);
    }
    cur = next;
  }
  return cur.filter((v) => v !== null && v !== undefined && v !== '' && (typeof v === 'string' || typeof v === 'number'));
}
/** Served values of a field list over named payloads: a path "x:a.b" reads payload x, a bare path reads `dflt`. */
function served(list, payloads, dflt) {
  const out = [];
  const by = {};
  for (const spec of list) {
    const i = spec.indexOf(':');
    const [pay, p] = i > 0 && /^[a-z]+$/.test(spec.slice(0, i)) ? [spec.slice(0, i), spec.slice(i + 1)] : [dflt, spec];
    const vals = payloads[pay] ? pathValues(payloads[pay], p) : [];
    if (vals.length) by[spec] = [...new Set(vals.map(String))];
    out.push(...vals.map(String));
  }
  return { values: [...new Set(out)], by };
}
/** {times, sources, timesBy, sourcesBy} for one card over the payloads one render used. */
function cardFields(id, payloads) {
  const c = CARDS[id];
  const dflt = c.payload.split('+')[0];
  const t = served(c.times, payloads, dflt);
  const s = served(c.sources, payloads, dflt);
  return { times: t.values, sources: s.values, timesBy: t.by, sourcesBy: s.by };
}
function pageDates(mode, payloads) {
  return served(PAGE_TIMES[mode], payloads, null);
}

// ---- time equivalence ----------------------------------------------------------------------------------------------------------
/** A served time as {day, ms}: ISO stamps, "YYYY-MM-DDTHHMMZ", compact "YYYYMMDDTHHMMSSZ", or a bare day. */
function timeOf(v) {
  const s = String(v).trim();
  let iso = s;
  let m;
  if ((m = /^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z$/.exec(s))) iso = `${m[1]}-${m[2]}-${m[3]}T${m[4]}:${m[5]}:${m[6]}Z`;
  else if ((m = /^(\d{4}-\d{2}-\d{2})T(\d{2})(\d{2})Z$/.exec(s))) iso = `${m[1]}T${m[2]}:${m[3]}:00Z`;
  const day = (/^(\d{4}-\d{2}-\d{2})/.exec(iso) || [])[1] || null;
  const dayOnly = /^\d{4}-\d{2}-\d{2}$/.test(iso);
  const ms = dayOnly ? null : Date.parse(iso);
  return { day, dayOnly, ms: Number.isFinite(ms) ? ms : null };
}
/** True when the footer's time value is one of the card's served times (same instant, or the same day for a bare day). */
function timeIsServed(v, servedTimes) {
  const f = timeOf(v);
  if (!f.day) return false;
  return servedTimes.some((x) => {
    const t = timeOf(x);
    if (f.dayOnly) return t.day === f.day;
    return t.ms !== null && f.ms !== null ? t.ms === f.ms : false;
  });
}
/** The value PanelFooter formats: `timestamp` when it parses as a Date, else `dataAsOf` (formatPanelTimestamp's own order). */
function effectiveTime(props) {
  const ts = props && props.timestamp;
  if (ts && Number.isFinite(new Date(ts).getTime())) return String(ts);
  return props && props.dataAsOf ? String(props.dataAsOf) : null;
}

// ---- source naming -------------------------------------------------------------------------------------------------------------
const STOP = new Set(['gold', 'daily', 'dapi', 'row', 'des', 'cie', 'the', 'own', 'day', 'view', 'source', 'and', 'for', 'from', 'with', 'boxside', 'pull']);
const DEFAULT_PUBLISHERS = { sa: 'Seeking Alpha', wsj: 'The Wall Street Journal', bbg: 'Bloomberg', barrons: "Barron's", ft: 'Financial Times' };
/** A served source value is a MACHINE CODE when a reader would not read it as words. */
function isMachineCode(code, pubs) {
  const c = String(code);
  return /[_:\/]/.test(c) || /^[a-z]+(?:-[a-z]+)+$/.test(c) || Object.prototype.hasOwnProperty.call(pubs, c.toLowerCase()) || /^[A-Z]{3,}$/.test(c) || /^[a-z]{2,4}$/.test(c);
}
/** The words that NAME a served source value: its publisher name (the page's PUBLISHER_NAMES), its significant tokens, and the
 * value itself when it is not a machine code ("10-K"). */
function sourceNames(code, pubs) {
  const c = String(code);
  const out = [];
  const pub = pubs[c.toLowerCase()];
  if (pub) out.push(pub.toLowerCase().replace(/^the /, ''));
  for (const tok of c.split(/[^A-Za-z0-9]+/)) if (tok.length >= 3 && !/^\d+$/.test(tok) && !STOP.has(tok.toLowerCase()) && !pubs[tok.toLowerCase()]) out.push(tok.toLowerCase());
  if (!isMachineCode(c, pubs)) out.push(c.toLowerCase());
  return [...new Set(out)];
}
const RAW = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b|s3:\/\/|\b[\w.-]+\.json\b|\borg\/missions\//;
/** Faults of one footer's source text against the card's served source values. */
function sourceFaults(text, codes, pubs) {
  const f = [];
  const low = text.toLowerCase();
  for (const code of codes) {
    const names = sourceNames(code, pubs);
    if (!names.some((n) => low.includes(n))) f.push(`does not name the served source "${code}" (would read as one of: ${names.map((n) => `"${n}"`).join(', ') || 'none'})`);
    if (isMachineCode(code, pubs)) {
      const re = /^[a-z]{2,4}$/.test(code) ? new RegExp(`\\b${code}\\b`) : null;
      if (re ? re.test(text) : text.includes(code)) f.push(`prints the served code "${code}" raw`);
    }
  }
  const raw = RAW.exec(text);
  if (raw) f.push(`prints a machine token "${raw[0]}"`);
  return f;
}

// ---- markup tree with document order ---------------------------------------------------------------------------------------------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const decode = (s) => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
function parse(html) {
  const root = { tag: '#root', attrs: {}, children: [], parent: null, i: 0, end: 0 };
  let cur = root;
  let n = 0;
  const all = [root];
  const re = /<!--[\s\S]*?-->|<\/([a-zA-Z][\w:.-]*)\s*>|<([a-zA-Z][\w:.-]*)((?:\s+[^\s=>\/]+(?:="[^"]*")?)*)\s*(\/?)>|([^<]+)/g;
  let m;
  while ((m = re.exec(String(html || ''))) !== null) {
    if (m[1]) { let x = cur; while (x && x.tag !== m[1].toLowerCase()) x = x.parent; if (x && x.parent) cur = x.parent; }
    else if (m[2]) {
      const attrs = {};
      const ar = /([^\s=>\/]+)(?:="([^"]*)")?/g;
      let a;
      while ((a = ar.exec(m[3] || '')) !== null) attrs[a[1]] = a[2] === undefined ? '' : decode(a[2]);
      const node = { tag: m[2].toLowerCase(), attrs, children: [], parent: cur, i: ++n };
      cur.children.push(node);
      all.push(node);
      if (!m[4] && !VOID.has(node.tag)) cur = node;
    } else if (m[5]) { const t = { text: decode(m[5]), parent: cur, i: ++n }; cur.children.push(t); all.push(t); }
  }
  const setEnd = (x) => { x.end = x.i; for (const c of x.children || []) { setEnd(c); if (c.end > x.end) x.end = c.end; } if (x.text !== undefined) x.end = x.i; };
  setEnd(root);
  root.all = all;
  return root;
}
const textOf = (node) => norm(node.text !== undefined ? node.text : (node.children || []).map(textOf).join(' '));
const has = (node, attr, val) => node.attrs && node.attrs[attr] !== undefined && (val === undefined || node.attrs[attr] === val);
const find = (tree, pred) => tree.all.filter((x) => x.tag && pred(x));
const firstOf = (tree, pred, after) => tree.all.find((x) => x.tag && x.i > (after || 0) && pred(x)) || null;
function ancestor(node, pred) { let x = node && node.parent; while (x) { if (x.tag && pred(x)) return x; x = x.parent; } return null; }
const inside = (x, r) => x.i >= r.start && x.i <= r.end;
const inAny = (x, rs) => rs.some((r) => inside(x, r));
function propsOf(node) { try { return JSON.parse(node.attrs['data-check-props'] || '{}'); } catch (e) { return {}; } }

/** The card regions of one page render: [{id, start, end}] (document-order index range, inclusive). */
function cardRegions(tree, mode) {
  const out = [];
  const isPanel = (x) => has(x, 'data-stub', 'Panel');
  const nav = firstOf(tree, (x) => has(x, 'data-stub', 'TabNavigation'));
  const tops = find(tree, (x) => isPanel(x) && !ancestor(x, isPanel));
  const head = tops.find((x) => !nav || x.i < nav.i) || null;
  if (mode === 'security' && head) {
    const within = (pred) => firstOf(tree, (x) => x.i > head.i && x.i <= head.end && pred(x));
    const brief = within((x) => has(x, 'data-header-brief'));
    const tl = within((x) => has(x, 'data-timeline-panel'));
    const more = within((x) => has(x, 'data-header-more'));
    const stop = (...xs) => { const s = xs.filter(Boolean)[0]; return s ? s.i - 1 : head.end; };
    out.push({ id: 'K', start: head.i, end: stop(brief, tl, more) });
    if (brief) out.push({ id: 'N', start: brief.i, end: stop(tl, more) });
    if (tl) out.push({ id: 'T', start: tl.i, end: stop(more) });
  }
  if (mode === 'universe' && head) out.push({ id: 'LEAD', start: head.i, end: head.end });
  if (nav) {
    const tab = tops.find((x) => x.i > nav.end);
    if (tab) out.push({ id: 'TAB', start: tab.i, end: tab.end });
  }
  for (const w of find(tree, (x) => x.tag === 'section' && has(x, 'data-what-changed'))) out.push({ id: 'W', start: w.i, end: w.end });
  return out;
}

const FOOTER_LINE = /\S\s*\|\s*Source:/;
/** Grade one card region. fields = {times, sources}; pubs = the page's publisher names. Returns {footer, printed, faults}. */
function gradeCard(tree, region, all, fields, pubs, label) {
  const nested = all.filter((r) => r !== region && r.start > region.start && r.end <= region.end);
  const mine = (x) => inside(x, region) && !inAny(x, nested);
  const footers = find(tree, (x) => has(x, 'data-check-shared', 'PanelFooter') && mine(x));
  const smart = find(tree, (x) => has(x, 'data-check-shared', 'SmartPanelFooter') && mine(x));
  const sharedSpans = [...footers, ...smart].map((x) => ({ start: x.i, end: x.end }));
  const loose = tree.all.filter((x) => x.text !== undefined && mine(x) && !inAny(x, sharedSpans) && FOOTER_LINE.test(norm(x.text) + ' ' + norm(nextText(tree, x))));
  const wants = fields.times.length > 0 && fields.sources.length > 0;
  const f = [];
  const printed = footers.map(textOf);
  for (const s of smart) f.push(`${label}: SmartPanelFooter stamps the data manifest's time ("${textOf(s).slice(0, 80)}"), not a field this card serves`);
  if (wants) {
    if (footers.length === 0) f.push(`${label}: no shared footer, though the card serves a time (${fields.times.slice(0, 2).join(', ')}) and a source (${fields.sources.join(', ')})`);
    if (footers.length > 1) f.push(`${label}: ${footers.length} shared footers in one card`);
    for (const node of footers) {
      const p = propsOf(node);
      const t = effectiveTime(p);
      const shown = textOf(node);
      if (!t) f.push(`${label}: the footer carries no time ("${shown.slice(0, 80)}")`);
      else if (!timeIsServed(t, fields.times)) f.push(`${label}: the footer's time "${t}" is not a served time of this card (served: ${fields.times.slice(0, 4).join(', ')})`);
      if (!FOOTER_LINE.test(shown)) f.push(`${label}: the footer does not read as "<time> | Source: <source>" ("${shown.slice(0, 100)}")`);
      const m = /^\s*Source:\s*(\S[\s\S]*)$/.exec(String(p.content || ''));
      if (!m) f.push(`${label}: the footer's content does not read "Source: ..." ("${String(p.content || '').slice(0, 80)}")`);
      else for (const x of sourceFaults(m[1], fields.sources, pubs)) f.push(`${label}: the footer ${x} ("${m[1].slice(0, 80)}")`);
    }
    if (footers.length) {
      const last = footers[footers.length - 1];
      const after = tree.all.filter((x) => x.text !== undefined && x.i > last.end && mine(x) && norm(x.text));
      if (after.length) f.push(`${label}: the card does not end in its footer -- "${norm(after.map((x) => x.text).join(' ')).slice(0, 80)}" follows it`);
    }
    if (loose.length) f.push(`${label}: a hand-rolled time | source line outside the shared footer ("${norm(loose[0].text).slice(0, 80)}")`);
  } else {
    if (footers.length) f.push(`${label}: prints a footer ("${printed[0].slice(0, 80)}") though the card serves no ${fields.times.length ? 'source' : 'time'} (FWD-27)`);
    if (loose.length) f.push(`${label}: a time | source placeholder line ("${norm(loose[0].text).slice(0, 80)}") though the card serves no ${fields.times.length ? 'source' : 'time'}`);
  }
  return { footer: footers.length > 0, printed, faults: f };
}
/** The text node after x in document order (a "date | Source" split across two text nodes is one line). */
function nextText(tree, x) {
  for (let k = x.i + 1; k <= x.i + 3 && k < tree.all.length; k += 1) {
    const y = tree.all[k];
    if (y && y.text !== undefined && norm(y.text)) return y.text;
  }
  return '';
}

// ---- the end line's date in words (round 39, row S3) ------------------------------------------------------------------------------
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const ordinal = (n) => { const t = n % 100; if (t >= 11 && t <= 13) return 'th'; return ({ 1: 'st', 2: 'nd', 3: 'rd' })[n % 10] || 'th'; };
/** A YYYY-MM-DD day as the house reads it: "October 2nd, 2026" (computed here, not by the portal's formatter). */
function dayWords(day) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(day || ''));
  if (!m) return null;
  const d = Number(m[3]);
  return `${MONTHS[Number(m[2]) - 1]} ${d}${ordinal(d)}, ${m[1]}`;
}
/** A moment's ET day (YYYY-MM-DD) and ET clock ("3:56p"), from Intl (America/New_York), never from the portal. */
function etParts(ms) {
  const parts = new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', year: 'numeric', month: '2-digit', day: '2-digit', hour: 'numeric', minute: '2-digit', hour12: true }).formatToParts(new Date(ms));
  const get = (t) => (parts.find((x) => x.type === t) || {}).value || '';
  return { day: `${get('year')}-${get('month')}-${get('day')}`, clock: `${get('hour')}:${get('minute')}${get('dayPeriod').toLowerCase().charAt(0)}` };
}
const END_WORDS = /^([A-Z][a-z]+) (\d{1,2})(st|nd|rd|th), (\d{4})(?:, (\d{1,2}:\d{2}[ap]) ET)?$/;
/** Faults of the end line's printed date `words` against the served value(s) it names: the page's `dataAsOf` when handed over,
 * else every served date of the page. The printed DAY must be the day of a named value (a bare day's own day; a moment's ET or
 * UTC day). A printed TIME OF DAY must be the ET clock of a named served MOMENT on that day: after a bare served day, any clock
 * is invented (the shared default's "5:00p ET"). */
function endDateFaults(words, named, label) {
  const m = END_WORDS.exec(words);
  if (!m) return [`${label}: the end line's date "${words}" does not read as a day in words ("October 2nd, 2026") or a served moment in words ("October 2nd, 2026, 3:56p ET")`];
  const mi = MONTHS.indexOf(m[1]);
  const day = mi < 0 ? null : `${m[4]}-${String(mi + 1).padStart(2, '0')}-${String(Number(m[2])).padStart(2, '0')}`;
  const f = [];
  if (!day || dayWords(day) !== `${m[1]} ${m[2]}${m[3]}, ${m[4]}`) f.push(`${label}: the end line's day "${m[1]} ${m[2]}${m[3]}, ${m[4]}" is not a day in the house words (want e.g. "${dayWords(day) || 'October 2nd, 2026'}")`);
  const reads = named.map((v) => { const t = timeOf(v); const et = !t.dayOnly && t.ms !== null ? etParts(t.ms) : null; return { v: String(v), t, et }; }).filter((r) => r.t.day);
  const sameDay = reads.filter((r) => r.t.day === day || (r.et && r.et.day === day));
  if (!sameDay.length) {
    f.push(`${label}: the end line prints the day "${m[1]} ${m[2]}${m[3]}, ${m[4]}" -- not the day of the served value it names (${reads.map((r) => r.v).slice(0, 4).join(', ') || 'none'})`);
    return f;
  }
  if (m[5]) {
    const clock = `${m[5]} ET`;
    const moments = sameDay.filter((r) => r.et);
    if (!moments.length) {
      const bare = sameDay[0].v;
      f.push(`${label}: the end line prints the time of day "${clock}" ("${words}") but the served value it names is the bare day "${bare}" -- an invented clock; a bare served day prints as "${dayWords(bare)}", no time of day`);
    } else if (!moments.some((r) => r.et.clock === m[5] && r.et.day === day)) {
      f.push(`${label}: the end line prints the time of day "${clock}" ("${words}"), which is not the served moment's time (${moments.map((r) => `"${r.v}" = ${r.et.clock} ET on ${r.et.day}`).slice(0, 3).join(', ')})`);
    }
  }
  return f;
}

/** Grade the page end. dates = served page dates ([] = none served); returns {printed, faults}. Round 39 (row S3): the printed
 * text is the REAL PageEnd's own (the marker's children; a marker with no [data-page-end] inside is a fault), and its date is
 * graded in words by endDateFaults -- a bare served day prints with NO time of day. */
function gradePageEnd(tree, dates, label) {
  const f = [];
  const ends = find(tree, (x) => has(x, 'data-check-shared', 'PageEnd'));
  const spans = ends.map((x) => ({ start: x.i, end: x.end }));
  const loose = tree.all.filter((x) => x.text !== undefined && !inAny(x, spans) && /End of Security Analysis/.test(x.text));
  if (ends.length !== 1) f.push(`${label}: the shared PageEnd renders ${ends.length} times (want exactly 1)`);
  if (loose.length) f.push(`${label}: a hand-rolled "End of Security Analysis" line outside the shared PageEnd`);
  const printed = ends.map(textOf);
  for (const node of ends) {
    const p = propsOf(node);
    const text = textOf(node);
    if (p.pageName !== 'Security Analysis') f.push(`${label}: the end line names the page "${p.pageName}"`);
    if (!find(tree, (x) => x.i > node.i && x.i <= node.end && has(x, 'data-page-end')).length) f.push(`${label}: the end line is not the shared PageEnd's own markup (no [data-page-end] inside the marker)`);
    const m = /^End of Security Analysis\.(?: Data as of (.+)\.)?$/.exec(text);
    if (!m) f.push(`${label}: the end line reads "${text.slice(0, 100)}"`);
    else if (!m[1]) { if (dates.length) f.push(`${label}: the end line prints no date though the page serves one (${dates.slice(0, 3).join(', ')})`); }
    else {
      const handed = p.dataAsOf !== undefined && p.dataAsOf !== null && p.dataAsOf !== '';
      if (handed && !timeIsServed(p.dataAsOf, dates)) f.push(`${label}: the end line's date "${p.dataAsOf}" (${m[1]}) is not a served date of the page (served: ${dates.slice(0, 4).join(', ') || 'none'})`);
      else f.push(...endDateFaults(m[1], handed ? [p.dataAsOf] : dates, label));
    }
    const after = tree.all.filter((x) => x.text !== undefined && x.i > node.end && norm(x.text));
    if (after.length) f.push(`${label}: the end line is not at the end -- "${norm(after.map((x) => x.text).join(' ')).slice(0, 80)}" follows it`);
  }
  return { printed, faults: f };
}

module.exports = { CARDS, PAGE_TIMES, cardFields, pageDates, served, pathValues, timeOf, timeIsServed, effectiveTime, sourceNames, sourceFaults, isMachineCode,
  parse, textOf, cardRegions, gradeCard, gradePageEnd, endDateFaults, dayWords, etParts, DEFAULT_PUBLISHERS, norm };
