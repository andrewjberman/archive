'use strict';
const fs = require('fs');
const fx = JSON.parse(fs.readFileSync('.scratch/v6_fixtures_postB1.json', 'utf8'));
const ORDER = ['fixed_income', 'equity', 'structured', 'commodities', 'alternatives'];
const LABEL = { fixed_income: 'Fixed Income', equity: 'Equity', structured: 'Structured', commodities: 'Commodities', alternatives: 'Alternatives' };

function table(title, portfolios, renderedRows) {
  console.log('== ' + title + ' ==');
  const books = Object.keys(portfolios);
  console.log(['CLASS'.padEnd(14), ...books.map(b => b.padStart(9))].join(''));
  const sums = books.map(() => 0);
  for (const k of ORDER) {
    const cells = books.map((b, i) => {
      const a = portfolios[b].allocation || {};
      const v = (a[k] || 0) + (k === 'fixed_income' ? (a.cash || 0) : 0);
      sums[i] += v;
      return v.toFixed(2).padStart(9);
    });
    console.log([LABEL[k].padEnd(14), ...cells].join(''));
  }
  console.log(['SUBTOTAL SUM'.padEnd(14), ...sums.map(s => s.toFixed(2).padStart(9))].join(''));
  console.log(['|SUM-100|'.padEnd(14), ...sums.map(s => Math.abs(s - 100).toFixed(3).padStart(9))].join(''));
  console.log(['hedge(served)'.padEnd(14), ...books.map(b => String((portfolios[b].allocation || {}).hedge ?? 'absent').padStart(9))].join(''));
  console.log('WITHIN 0.1 OF TOTAL: ' + (sums.every(s => Math.abs(s - 100) <= 0.1) ? 'YES (' + sums.length + ' of ' + sums.length + ')' : 'NO'));
  console.log('RENDERED (read from the PNG): ' + renderedRows);
  console.log('');
}
const models = fx['/api/general/positioning/positioning_data.json'];
table('MODELS (served json/positioning/positioning_data.json @OuevyO7kCIJdEqzGlJWd.z.8S8pqiXJk)', models.portfolios,
  'FI 100 / 82.60 / 32.80 / 12.70 / 8.10 ; EQ 0 / 17.40 / 67.20 / 87.30 / 91.90 ; STRUCT 0 x5 ; COMM 0 x5 ; ALT 0 x5');
const etfs = fx['/api/general/etfs/positioning_data.json'];
table('ETFS (served platinum/etfs/positioning_data.json @MkASX8obEltFZpHHzNa81cuAVXKf7wR2)', etfs.portfolios,
  'FI 0.62 / 0.95 / 0.09 / 0.63 ; EQ 99.38 / 99.05 / 99.90 / 99.36 ; STRUCT 0 x4 ; COMM 0 x4 ; ALT 0 x4');
console.log('SERVED ALLOCATION KEY SET (models, per book): ' +
  JSON.stringify([...new Set(Object.values(models.portfolios).map(p => Object.keys(p.allocation).join(',')))]));
console.log('SERVED ALLOCATION KEY SET (etfs, per book):   ' +
  JSON.stringify([...new Set(Object.values(etfs.portfolios).map(p => Object.keys(p.allocation || {}).join(',')))]));
