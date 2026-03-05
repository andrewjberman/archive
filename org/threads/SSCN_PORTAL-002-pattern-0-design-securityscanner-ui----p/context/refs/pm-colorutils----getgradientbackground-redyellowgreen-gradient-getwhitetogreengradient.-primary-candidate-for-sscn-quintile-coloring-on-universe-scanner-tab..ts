/**
 * Gradient color utilities for PortfolioManagement
 *
 * Extracted from PortfolioGrid.tsx so ModelTab and other consumers
 * can reuse the same gradient logic.
 */

/**
 * Get gradient background color based on value relative to min/max
 *
 * Color mapping:
 * - Max value -> Bright green (#10b981)
 * - Zero (0) -> Yellow (#eab308)
 * - Min value -> Bright red (#ef4444)
 *
 * When inverted = true:
 * - Max value -> Bright red (high = bad)
 * - Zero (0) -> Yellow
 * - Min value -> Bright green (low = good)
 */
export function getGradientBackground(value: number, min: number, max: number, inverted = false): string {
  // Handle edge cases
  if (min === max) return 'rgba(234, 179, 8, 0.2)' // Yellow if all same

  // Normalize value to 0-1 range
  let normalized: number

  if (value >= 0) {
    // Positive values: interpolate from yellow (0) to green/red (max)
    if (max <= 0) {
      normalized = 0
    } else {
      normalized = value / max
    }

    const yellow = { r: 234, g: 179, b: 8 }   // #eab308
    const positive = inverted
      ? { r: 239, g: 68, b: 68 }   // #ef4444 (red when inverted — high risk = bad)
      : { r: 16, g: 185, b: 129 }  // #10b981 (green — high alpha = good)

    const r = Math.round(yellow.r + (positive.r - yellow.r) * normalized)
    const g = Math.round(yellow.g + (positive.g - yellow.g) * normalized)
    const b = Math.round(yellow.b + (positive.b - yellow.b) * normalized)

    const opacity = 0.5 + (normalized * 0.35)

    return `rgba(${r}, ${g}, ${b}, ${opacity})`
  } else {
    // Negative values: interpolate from yellow (0) to red/green (min)
    if (min >= 0) {
      normalized = 0
    } else {
      normalized = Math.abs(value / min)
    }

    const yellow = { r: 234, g: 179, b: 8 }   // #eab308
    const negative = inverted
      ? { r: 16, g: 185, b: 129 }  // #10b981 (green when inverted — low risk = good)
      : { r: 239, g: 68, b: 68 }   // #ef4444 (red — negative alpha = bad)

    const r = Math.round(yellow.r + (negative.r - yellow.r) * normalized)
    const g = Math.round(yellow.g + (negative.g - yellow.g) * normalized)
    const b = Math.round(yellow.b + (negative.b - yellow.b) * normalized)

    const opacity = 0.5 + (normalized * 0.35)

    return `rgba(${r}, ${g}, ${b}, ${opacity})`
  }
}

/**
 * Simple white-to-green gradient for non-negative values (Model tab).
 * Maps 0 -> white, max -> green.
 */
export function getWhiteToGreenGradient(value: number, min: number, max: number): string {
  if (max === min) return 'rgba(255, 255, 255, 0.1)'

  const range = max - min
  const normalized = range > 0 ? (value - min) / range : 0
  const clamped = Math.max(0, Math.min(1, normalized))

  // White to green
  const white = { r: 255, g: 255, b: 255 }
  const green = { r: 16, g: 185, b: 129 } // #10b981

  const r = Math.round(white.r + (green.r - white.r) * clamped)
  const g = Math.round(white.g + (green.g - white.g) * clamped)
  const b = Math.round(white.b + (green.b - white.b) * clamped)

  const opacity = 0.15 + (clamped * 0.45)

  return `rgba(${r}, ${g}, ${b}, ${opacity})`
}
