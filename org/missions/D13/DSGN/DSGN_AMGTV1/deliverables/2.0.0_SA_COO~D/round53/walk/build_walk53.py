"""Build round53/walk/walk53.mjs: the head of round35/walk/closewalk35.mjs (everything above its '// ---- the walk ----'
marker, unchanged) followed by round53/walk/walk53.tail.mjs. Run from anywhere; paths resolve from this file."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', 'round35', 'walk', 'closewalk35.mjs')
MARK = '// ---- the walk ----'

head = io.open(SRC, encoding='utf-8', newline='').read()
assert head.count(MARK) == 1, head.count(MARK)
head = head.split(MARK)[0]
tail = io.open(os.path.join(HERE, 'walk53.tail.mjs'), encoding='utf-8', newline='').read()
out = os.path.join(HERE, 'walk53.mjs')
io.open(out, 'w', encoding='utf-8', newline='').write(head + tail)
print('OK: wrote', out, len(head), '+', len(tail), 'characters')
