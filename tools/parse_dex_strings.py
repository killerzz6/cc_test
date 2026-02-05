import re

p='apk_unzip/classes.dex'
with open(p,'rb') as f:
    b=f.read()

parts=re.findall(b'([A-Za-z0-9_\./\$]{4,200})',b)
found=[]
for p in parts:
    s=p.decode('utf-8',errors='ignore')
    if '.' in s and '/' not in s and '$' not in s:
        found.append(s)
    elif '/' in s and '.' in s:
        found.append(s)

# Heuristic filter: package-like strings (contain package separators)
cand=[x for x in set(found) if x.count('.')>=1 and len(x.split('.')[-1])>0]
print('\n'.join(sorted(cand)[:200]))
