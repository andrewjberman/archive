
// ---------------------------------------------------------------------------------------------------------------------
// CN-p-2 (PRD v2.19 to v2.21): the Global AUA Trend over full history. REFERENCE IMPLEMENTATION (scratch; the worker writes
// its own to the same exported interface). Pure; imports nothing. FIELD-READ LAW: every group is a served field or ONE served
// difference (Custom Models); the total is read, never recomposed. ABSENT IS NOT ZERO. Roll FORWARD only, and only on a date
// the producer lists in carried_dates.
// ---------------------------------------------------------------------------------------------------------------------

export const GLOBAL_PRIMARY_LABELS = ['Ultra-Short Term', 'Short Term', 'Intermediate Term', 'Long Term', 'Ultra-Long Term'] as const
export const MODELS_BAND_LABEL = 'Models'
export const SUPPRESSED_FOOTNOTE = 'models held at one firm are in the total and not broken out'
export const CARRIED_LEGEND_LABEL = 'Carried forward (last known value)'

export type TrendMode = 'variant1' | 'variant2'

/** Variant 1 (single-firm history stitched read-side) for an INTERNAL session only; every other session draws Variant 2. */
export const trendModeFor = (internal: boolean): TrendMode => (internal === true ? 'variant1' : 'variant2')

type Num = number | null

export interface GlobalTrendServed {
  dates: ReadonlyArray<string>
  total: ReadonlyArray<Num>
  modelAua: ReadonlyArray<Num>
  primary: Readonly<Record<string, ReadonlyArray<Num>>>
  otherModels: ReadonlyArray<Num> | null
  clientSupervised: ReadonlyArray<Num> | null
  etfStrategies: ReadonlyArray<Num> | null
  altStrategies: ReadonlyArray<Num> | null
  carriedDates: ReadonlyArray<string> | null
}

export interface GlobalTrendStitch {
  firm49: Readonly<Record<string, ReadonlyArray<{ period: string; aum: Num }>>>
  inflectionCustom: ReadonlyArray<{ period: string; aum: Num }>
}

export interface GlobalTrendRow {
  period: string
  total: Num
  models: Record<string, Num>
  custom: Num
  modelsBand: Num
  clientSupervised: Num
  etfStrategies: Num
  altStrategies: Num
  customSuppressed: boolean
  carried: string[]
}

const finiteOrNull = (v: unknown): Num => (typeof v === 'number' && Number.isFinite(v) ? v : null)
const readAt = (arr: ReadonlyArray<Num> | null | undefined, i: number): Num => finiteOrNull(arr?.[i])
const indexByPeriod = (pts: ReadonlyArray<{ period: string; aum: Num }> | undefined): Map<string, Num> => {
  const m = new Map<string, Num>()
  for (const p of pts ?? []) m.set(p.period, finiteOrNull(p.aum))
  return m
}

/** modelAua minus the present primary lines, to cents; null when either side is absent or the remainder is under half a cent. */
const customByDifference = (modelAua: Num, five: ReadonlyArray<Num>): Num => {
  const lines = sumPresent(five)
  if (modelAua === null || lines === null) return null
  const d = toCents(modelAua - lines)
  return Math.abs(d) < 0.005 ? null : d
}

export function buildGlobalTrendRows(
  served: GlobalTrendServed,
  stitch: GlobalTrendStitch | null | undefined,
  mode: TrendMode,
  detailBegins: string | null | undefined
): GlobalTrendRow[] {
  const stitchOn = mode === 'variant1' && stitch !== null && stitch !== undefined
  const firm49: Record<string, Map<string, Num>> = {}
  if (stitchOn) for (const label of GLOBAL_PRIMARY_LABELS) firm49[label] = indexByPeriod(stitch!.firm49[label])
  const infCustom = stitchOn ? indexByPeriod(stitch!.inflectionCustom) : new Map<string, Num>()
  const carriedSet = new Set(served.carriedDates ?? [])
  const lastKnown: Record<string, Num> = {}
  return served.dates.map((period, i) => {
    const pre = typeof detailBegins === 'string' && period < detailBegins
    const v: Record<string, Num> = { total: readAt(served.total, i) }
    const five: Num[] = []
    for (const label of GLOBAL_PRIMARY_LABELS) {
      const x = pre ? (stitchOn ? (firm49[label].get(period) ?? null) : null) : readAt(served.primary[label], i)
      v[label] = x
      if (!pre) five.push(x)
    }
    const modelAua = readAt(served.modelAua, i)
    v[MODELS_BAND_LABEL] = mode === 'variant2' && pre ? modelAua : null
    let custom: Num = null
    let suppressed = false
    if (!pre) {
      const diff = customByDifference(modelAua, five)
      if (readAt(served.otherModels, i) !== null) custom = diff
      else if (stitchOn) custom = infCustom.get(period) ?? null
      else if (mode === 'variant2' && diff !== null) suppressed = true
    }
    v[CUSTOM_MODELS_LABEL] = custom
    v['Client Supervised'] = readAt(served.clientSupervised, i)
    v['ETF Strategies'] = readAt(served.etfStrategies, i)
    v['ALT Strategies'] = readAt(served.altStrategies, i)
    const carried: string[] = []
    for (const key of Object.keys(v)) {
      if (v[key] === null && carriedSet.has(period) && lastKnown[key] !== undefined && lastKnown[key] !== null) {
        v[key] = lastKnown[key]
        carried.push(key)
      }
      if (v[key] !== null) lastKnown[key] = v[key]
    }
    const models: Record<string, Num> = {}
    for (const label of GLOBAL_PRIMARY_LABELS) models[label] = v[label]
    return {
      period,
      total: v.total,
      models,
      custom: v[CUSTOM_MODELS_LABEL],
      modelsBand: v[MODELS_BAND_LABEL],
      clientSupervised: v['Client Supervised'],
      etfStrategies: v['ETF Strategies'],
      altStrategies: v['ALT Strategies'],
      customSuppressed: suppressed,
      carried,
    }
  })
}

/** The footnote Variant 2 states where Custom is suppressed; null for Variant 1 and when no row is suppressed. */
export function globalTrendFootnote(rows: ReadonlyArray<GlobalTrendRow>, mode: TrendMode): string | null {
  if (mode !== 'variant2') return null
  return rows.some((r) => r.customSuppressed) ? SUPPRESSED_FOOTNOTE : null
}

/** The boundary note: Variant 2 only. Variant 1 draws the earlier dates, so it states nothing. */
export function trendDetailNoteFor(mode: TrendMode, begins: string | null | undefined, firstPeriod: string | null | undefined): string | null {
  return mode === 'variant2' ? trendDetailNote(begins, firstPeriod) : null
}

/** The point class a plotted point carries: the estimate wins, then carried, else whatever the page derived. */
export function trendPointClass(existing: string | undefined, carriedKeys: ReadonlyArray<string>): string | undefined {
  if (existing === 'interpolated_estimate') return existing
  return carriedKeys.length > 0 ? 'carried' : existing
}

/** The tooltip label of a series on a hovered row; a carried value says so. `carried` is the row's key list or its '|' join. */
export function carriedTooltipLabel(label: string, carried: ReadonlyArray<string> | string | null | undefined): string {
  const keys = typeof carried === 'string' ? (carried === '' ? [] : carried.split('|')) : (carried ?? [])
  return keys.includes(label) ? `${label} (carried)` : label
}

/** The two composition steps of the Global total (spec: footnote them, they are not drawing errors). Internal sessions only: it names two partner firms. */
export function compositionFootnote(mode: TrendMode): string | null {
  return mode === 'variant1'
    ? "Composition: Inflection's models enter the Total on May 15, 2026; Cottonwood enters on May 28, 2026 (estimated until July 20, 2026)."
    : null
}
