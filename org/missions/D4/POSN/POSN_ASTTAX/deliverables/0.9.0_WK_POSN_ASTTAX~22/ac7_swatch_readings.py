"""POSN_ASTTAX.TO-V5-1 / V5-AC7 -- READINGS ONLY, NO VERDICT.

V5-AC7 is judgment="true" and is graded by 3.0.0_SA_CVO~Z at L9. This script records
NUMBERS so the grader is not handed an adjective:

  * the silver canvas resolved from portal/CLAUDE.md's own colour law (HSL 222 24% 81%),
  * WCAG 2.x contrast of yellow500 and amber500 against that canvas,
  * CIE76 dE(Lab) between yellow500 and amber500, with two CONTROL pairs so the number
    can be read: an IDENTICAL pair (dE must be 0) and a pair nobody disputes is distinct
    (blue500 vs orange500).

It offers no verdict and no threshold of its own. Run: python <this file>
"""
import math

CANVAS_HSL = (222.0, 0.24, 0.81)   # portal/CLAUDE.md:13-14, "--palette-silver, 222 24% 81%"

SWATCHES = {
    'yellow500 (Commodities, this order)': '#eab308',
    'amber500  (Cash, pre-existing)':      '#f59e0b',
    'pink500   (Structured, this order)':  '#ec4899',
    'green500  (Fixed Income)':            '#10b981',
    'blue500   (Equity)':                  '#3b82f6',
    'orange500 (Alternatives)':            '#f97316',
}


def hsl_to_rgb(h, s, lum):
    c = (1 - abs(2 * lum - 1)) * s
    x = c * (1 - abs(((h / 60.0) % 2) - 1))
    m = lum - c / 2
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return tuple(int(round((v + m) * 255)) for v in (r, g, b))


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rel_lum(rgb):
    def ch(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def rgb_to_lab(rgb):
    def ch(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.00000
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1.0 / 3) if t > 0.008856 else (7.787 * t + 16.0 / 116)
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def de76(a, b):
    la, lb = rgb_to_lab(a), rgb_to_lab(b)
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(la, lb)))


canvas = hsl_to_rgb(*CANVAS_HSL)
print('SILVER CANVAS, resolved from portal/CLAUDE.md:13-14 (HSL 222 24%% 81%%) -> rgb%s  #%02x%02x%02x'
      % (canvas, canvas[0], canvas[1], canvas[2]))
print('  (the law states the same value as "approx rgb(195,202,218)"; this derivation gives %s)' % (canvas,))
print('')
print('WCAG 2.x CONTRAST RATIO OF EACH SWATCH AGAINST THE SILVER CANVAS')
print('  %-38s %-9s %-7s %s' % ('swatch', 'hex', 'ratio', 'rgb'))
for label, hx in SWATCHES.items():
    rgb = hex_to_rgb(hx)
    print('  %-38s %-9s %6.2f  %s' % (label, hx, contrast(rgb, canvas), rgb))
print('')
print('TEXT ON THE TWO CHIPS (getSubAssetTextColor picks white unless the hex is in its')
print('lightBackgrounds list; yellow500 is NOT in that list at this pin):')
for label, hx in [('yellow500', '#eab308'), ('amber500', '#f59e0b')]:
    rgb = hex_to_rgb(hx)
    print('  %-10s white #ffffff on it: %5.2f   gray900 #111827 on it: %5.2f'
          % (label, contrast(rgb, hex_to_rgb('#ffffff')), contrast(rgb, hex_to_rgb('#111827'))))
print('')
print('CIE76 dE(Lab) -- THE PAIR IN QUESTION, WITH TWO CONTROLS')
y, a = hex_to_rgb('#eab308'), hex_to_rgb('#f59e0b')
print('  SUBJECT  yellow500 vs amber500      dE76 = %6.2f' % de76(y, a))
print('  CONTROL  amber500 vs amber500       dE76 = %6.2f   (identical pair; must read 0.00)' % de76(a, a))
print('  CONTROL  blue500 vs orange500       dE76 = %6.2f   (a pair nobody disputes is distinct)'
      % de76(hex_to_rgb('#3b82f6'), hex_to_rgb('#f97316')))
print('  CONTROL  green400 vs green500       dE76 = %6.2f   (an adjacent ramp step inside one family)'
      % de76(hex_to_rgb('#34d399'), hex_to_rgb('#10b981')))
print('')
print('Lab COORDINATES OF THE SUBJECT PAIR (L*, a*, b*)')
print('  yellow500 %s' % (tuple(round(v, 2) for v in rgb_to_lab(y)),))
print('  amber500  %s' % (tuple(round(v, 2) for v in rgb_to_lab(a)),))
print('')
print('RENDERED SWATCH: NOT READ. Stated, not inferred -- see the result document.')
print('NO VERDICT IS OFFERED. V5-AC7 is judgment="true"; 3.0.0_SA_CVO~Z grades it at L9.')
