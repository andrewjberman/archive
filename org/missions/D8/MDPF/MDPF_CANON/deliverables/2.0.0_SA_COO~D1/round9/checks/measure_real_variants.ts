// MDPF_CANON round 9 -- real-data measurement of the Global Trend rows (2.0.0_SA_COO~D1, read-only).
// Run: DATA_DIR=<dir holding global.json, 49financial.json, inflection.json = the newest gold aggregate-aua-timeseries objects> UNROLLED=1 OUT=<file> bun run measure_real_variants.ts
// It imports the page's own pure module from portal/src (the path in T below), builds served and stitch exactly as the page's memos do, and writes Variant 1 and Variant 2 rows.
// UNROLLED=1 reproduces the page as built (CN-p-2 AMENDMENT 2: the stitch no longer rolls Inflection's blends); without it the pre-amendment stitch is reproduced.
import { readFileSync, writeFileSync } from 'node:fs'
const T = 'file:///C:/dev/ajb_workspace/portal/src/'
const { readModelSeries, readGlobalEnterpriseSeries, readGlobalCompleteFrontier } = await import(T + 'lib/pairedProvenanceRead.ts')
const { getCanonicalModelName } = await import(T + 'lib/modelPortfolioColors.ts')
const tg: any = await import(process.env.TG_MODULE ?? (T + 'lib/trendGrouping.ts'))
const { GLOBAL_PRIMARY_LABELS, CUSTOM_MODELS_LABEL, groupCustomModelsSeries, buildGlobalTrendRows, trendModeFor } = tg
const MODEL_ORDER = ['Ultra-Short Term', 'Short Term', 'Intermediate Term', 'Long Term', 'Ultra-Long Term']
const BLEND_ARCHETYPES: Record<string, [string, string]> = { '50/50 ST/INT': ['Short Term', 'Intermediate Term'], '50/50 INT/LT': ['Intermediate Term', 'Long Term'] }
const addNullable = (a: any, b: any) => (a == null && b == null ? null : (a ?? 0) + (b ?? 0))
function roll(byModel: any) {
  const out: any = {}
  for (const [k, s] of Object.entries<any>(byModel)) { if (k in BLEND_ARCHETYPES) continue; out[k] = s.map((p: any) => ({ ...p })) }
  for (const [blend, targets] of Object.entries(BLEND_ARCHETYPES)) {
    const bs = byModel[blend]; if (!bs) continue
    for (const target of targets) {
      const half = (v: any) => (v == null ? null : v / 2)
      if (!out[target]) { out[target] = bs.map((p: any) => ({ period: p.period, aum: half(p.aum) })); continue }
      const idx = new Map(out[target].map((p: any, i: number) => [p.period, i]))
      for (const bp of bs) { const i: any = idx.get(bp.period); if (i === undefined) out[target].push({ period: bp.period, aum: half(bp.aum) }); else out[target][i].aum = addNullable(out[target][i].aum, half(bp.aum)) }
    }
  }
  return out
}
const dir = process.env.DATA_DIR as string
const G = JSON.parse(readFileSync(dir + '/global.json', 'utf8'))
const F = JSON.parse(readFileSync(dir + '/49financial.json', 'utf8'))
const I = JSON.parse(readFileSync(dir + '/inflection.json', 'utf8'))
const ent = readGlobalEnterpriseSeries(G)
const primary: any = {}
for (const k of Object.keys(G.by_model)) {
  if (G.by_model[k].cohort_class === 'sma') continue
  const label = getCanonicalModelName(G.by_model[k].display_name)
  if (GLOBAL_PRIMARY_LABELS.includes(label)) primary[label] = readModelSeries(G, k).map((p: any) => p.value)
}
const served = {
  dates: G.dates, total: ent.map((p: any) => p.totalAua), modelAua: ent.map((p: any) => p.modelAua), primary,
  otherModels: 'other_models' in G.by_model ? readModelSeries(G, 'other_models').map((p: any) => p.value) : null,
  clientSupervised: G.client_supervised_aua ?? null, etfStrategies: G.etf_strategies_aua ?? null, altStrategies: G.alt_strategies_aua ?? null,
  carriedDates: G.carried_dates ?? null,
}
const pts = (d: any, k: string) => readModelSeries(d, k).map((p: any) => ({ period: p.period, aum: p.value }))
const firm49: any = {}
for (const k of Object.keys(F.by_model)) { const e = F.by_model[k]; if (e.cohort_class === 'sma') continue; const l = getCanonicalModelName(e.display_name); if (!GLOBAL_PRIMARY_LABELS.includes(l)) continue; firm49[l] = pts(F, k) }
const ibm: any = {}
for (const k of Object.keys(I.by_model)) { const e = I.by_model[k]; if (e.cohort_class === 'sma') continue; ibm[getCanonicalModelName(e.display_name)] = pts(I, k) }
const inflectionCustom = groupCustomModelsSeries(process.env.UNROLLED ? ibm : roll(ibm), new Set(MODEL_ORDER))[CUSTOM_MODELS_LABEL] ?? []
const stitch = { firm49, inflectionCustom }
const frontier = readGlobalCompleteFrontier(G)
const begins = G.meta?.by_model_fold?.per_model_detail_begins
const mk = (mode: string, st: any) => buildGlobalTrendRows(served, st, mode, begins).filter((r: any) => !frontier || r.period <= frontier)
const infMap = new Map(inflectionCustom.map((p: any) => [p.period, p.aum]))
const diag = G.dates.map((d: string, i: number) => ({ period: d, modelAua: served.modelAua[i], other: served.otherModels?.[i] ?? null, five: GLOBAL_PRIMARY_LABELS.map((l: string) => primary[l]?.[i] ?? null), infl: infMap.has(d) ? infMap.get(d) : 'NOKEY', total: served.total[i] }))
writeFileSync(dir + '/' + (process.env.OUT ?? 'measure_out.json'), JSON.stringify({ frontier, begins, carried: served.carriedDates, v1: mk('variant1', stitch), v2: mk('variant2', null), diag, infl_n: inflectionCustom.length }))
console.log('rows', mk('variant1', stitch).length, 'frontier', frontier)
