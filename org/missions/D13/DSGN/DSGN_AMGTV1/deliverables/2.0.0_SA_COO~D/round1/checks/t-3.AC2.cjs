/**
 * AV-t-3 AC2 -- EACH THESIS CARD'S WINDOW CARRIES ITS SENTENCES, THEIR PASSAGES, EACH CITATION'S
 * DOCUMENT IN WORDS, AND (RECOMMENDATION) WHOSE VIEW IT IS.
 *
 * Input: Valero's served Thesis bundle (as AC1). Renders the named export `ThesisCardDetail` of
 * portal/src/pages/SecurityAnalysis/components/ThesisCards.tsx -- the body the card's window
 * shows -- with props { sectionId, bundle }.
 *
 * Arms, all must hold:
 *   A  per section (investment_thesis, risks, recommendation): the count of data-drafted-sentence
 *      equals the served sentence count, the count of data-thesis-passage equals the served evidence
 *      count, and every served passage's opening 40 characters appear in the visible text.
 *   B  per section: the count of data-citation-document equals the served evidence count, and each
 *      one's visible text names the document in words -- it contains "10-K" and "2026-02-25"
 *      (the bundle's drafting_provenance form and filing_date) and no run of 15 or more digits.
 *   C  recommendation: an element carries data-recommendation-author="machine-draft", and the
 *      window's visible text says, in plain words, that the research team's own position is not
 *      there (it contains "research team").
 *   D  an evidence record whose accession is NOT the provenance accession still gets a citation in
 *      words (non-empty, no run of 15 or more digits) and is not labelled with the 10-K's date.
 */
const L = require('./_load.cjs');

const vlo = L.fixture('thesisBundle.VLO_US_Equity.json');
let ThesisCardDetail;
try {
  ({ ThesisCardDetail } = L.source('src/pages/SecurityAnalysis/components/ThesisCards.tsx'));
} catch (e) {
  console.log('LOAD FAIL components/ThesisCards.tsx :: ' + String(e && e.message).split('\n')[0]);
}
const SECTIONS = ['investment_thesis', 'risks', 'recommendation'];
const sec = (b, id) => (b.drafted_sections || []).find((s) => s.section_id === id);
const renderDetail = (id, b) => (typeof ThesisCardDetail === 'function' ? L.render(ThesisCardDetail, { sectionId: id, bundle: b }) : '');
const inners = (html, attr) => {
  const out = [];
  let from = 0;
  for (;;) {
    const at = html.indexOf(attr + '="', from);
    if (at < 0) break;
    out.push(L.textOf(L.innerOf(html.slice(html.lastIndexOf('<', at)), attr) || ''));
    from = at + 1;
  }
  return out;
};

const results = [];
const htmls = {};
for (const id of SECTIONS) {
  const s = sec(vlo, id);
  const ev = s.sentences.flatMap((x) => x.evidence || []);
  const html = renderDetail(id, vlo);
  htmls[id] = html;
  const text = L.textOf(html);
  const nS = L.attrValues(html, 'data-drafted-sentence').length;
  const nP = L.attrValues(html, 'data-thesis-passage').length;
  const missing = ev.filter((e) => !text.includes(L.textOf(e.passage).slice(0, 40))).length;
  results.push([`A ${id} sentences and passages`, html.length > 0 && nS === s.sentences.length && nP === ev.length && missing === 0, `sentences=${nS}/${s.sentences.length} passages=${nP}/${ev.length} passage_text_missing=${missing}`]);
  const cites = inners(html, 'data-citation-document');
  const bad = cites.filter((t) => !t.includes('10-K') || !t.includes('2026-02-25') || /\d{15,}/.test(t));
  results.push([`B ${id} citations name the document`, cites.length === ev.length && bad.length === 0, `citations=${cites.length}/${ev.length} not_in_words=${bad.length}`]);
}
{
  const html = htmls.recommendation || '';
  const author = L.attrValues(html, 'data-recommendation-author').map((a) => a.value);
  const ok = author.includes('machine-draft') && /research team/i.test(L.textOf(html));
  results.push(['C recommendation says whose view it is', ok, `author=[${author.join(',')}] names_research_team=${/research team/i.test(L.textOf(html))}`]);
}
{
  const b = JSON.parse(JSON.stringify(vlo));
  const s = sec(b, 'risks');
  s.sentences[0].evidence[0].source = { ...(s.sentences[0].evidence[0].source || {}), accession: '000999999926000001' };
  const html = renderDetail('risks', b);
  const cites = inners(html, 'data-citation-document');
  const first = cites[0] || '';
  const ok = first.length > 0 && !/\d{15,}/.test(first) && !first.includes('2026-02-25');
  results.push(['D a citation from another document is still in words', ok, `first="${first.slice(0, 80)}"`]);
}

let pass = 0;
for (const [name, ok, detail] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${detail}`);
  if (ok) pass += 1;
}
console.log(`THESIS CARD WINDOWS: ${pass} of ${results.length} arms`);
process.exit(pass === results.length ? 0 : 1);
