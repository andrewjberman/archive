import json
import sys

# IV-e-114's count: full-width (about 95% of main) #0A1733 panel strips; td #111827 cell fills are not bands.
for f in sys.argv[1:]:
    m = json.load(open(f))['measured']
    s = [b for b in m['bands'] if b['bg'] == '#0A1733' and b['tag'] == 'div' and b['w'] >= 0.9 * m['mainWidth']]
    print(f, 'strips=%d' % len(s), 'mainWidth=%d' % m['mainWidth'])
    for b in s:
        print('   ', b['slot'], b['w'], b['h'], b['text'][:40])
