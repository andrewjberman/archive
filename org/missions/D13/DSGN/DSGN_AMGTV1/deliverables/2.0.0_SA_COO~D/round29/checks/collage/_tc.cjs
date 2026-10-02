/**
 * _tc.cjs -- DSGN_AMGTV1 round 29, AV-zg-4 helper (issuer 2.0.0_SA_COO~D): renders the Topic Cloud the SAME way at capture time
 * (round29/fixtures/collage/r29c.build.cjs, run on BASE dcdc89b1) and at grade time (tone.cjs), so its render can be compared
 * byte for byte before and after the getSentimentColor extraction.
 *
 * @visx/wordcloud is replaced by a deterministic stand-in: word i is placed at a fixed grid point and the component's own
 * children function draws it (so every fill attribute comes from TopicCloud's own getSentimentColor call). @visx/text is the
 * installed package. Not a check: it prints nothing and grades nothing.
 */
module.exports = function renderTopicCloud(L, keywords) {
  const React = L.React;
  L.stubSource('@visx/wordcloud', {
    __esModule: true,
    Wordcloud: (p) => {
      const cloud = p.words.map((w, i) => ({
        text: w.text,
        x: (i % 5) * 30 - 60,
        y: Math.floor(i / 5) * 20 - 40,
        rotate: typeof p.rotate === 'function' ? p.rotate(w) : 0,
        size: typeof p.fontSize === 'function' ? p.fontSize(w) : p.fontSize,
        font: p.font,
        weight: p.fontWeight,
      }));
      return React.createElement(React.Fragment, null, p.children(cloud));
    },
  });
  const m = L.source('src/components/market-performance/TopicCloud.tsx');
  return L.render(m.TopicCloud, { keywords, onKeywordClick: () => {} });
};
