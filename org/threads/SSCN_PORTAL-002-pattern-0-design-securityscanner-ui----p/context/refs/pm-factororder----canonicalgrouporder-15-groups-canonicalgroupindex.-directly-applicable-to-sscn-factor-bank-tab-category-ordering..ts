/**
 * Yang's canonical factor group ordering.
 *
 * Matches the signal DataFrame row order in the alpha PKL.
 * Source of truth: portal/src/pages/PortfolioManagement/utils/factorDescriptions.ts (comment order).
 * Implementation pattern mirrors ECONOMY_ORDER in TradeTab.tsx (line 249).
 */

export const CANONICAL_GROUP_ORDER = [
  'size',
  'efficiency',
  'growth',
  'management',
  'profitability',
  'quality',
  'value',
  'analyst',
  'governance',
  'crowding',
  'insider',
  'short',
  'beta',
  'momentum',
  'technical',
] as const

export type CanonicalGroup = typeof CANONICAL_GROUP_ORDER[number]

export function canonicalGroupIndex(group: string): number {
  const idx = (CANONICAL_GROUP_ORDER as readonly string[]).indexOf(group.toLowerCase())
  return idx === -1 ? CANONICAL_GROUP_ORDER.length : idx
}
