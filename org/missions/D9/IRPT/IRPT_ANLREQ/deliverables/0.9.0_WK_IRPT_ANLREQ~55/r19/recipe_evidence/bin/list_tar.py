import hashlib
import sys
import tarfile

path = sys.argv[1]
with tarfile.open(path, 'r:gz') as t:
    rows = []
    for m in t.getmembers():
        if m.isfile():
            h = hashlib.sha256(t.extractfile(m).read()).hexdigest()
            rows.append((m.name, m.size, h))
        else:
            rows.append((m.name, m.type.decode() if isinstance(m.type, bytes) else m.type, ''))
print('members', len(rows), 'files', sum(1 for r in rows if isinstance(r[1], int)))
for r in rows:
    print(r[0], r[1], r[2])
