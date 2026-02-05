import re
from collections import Counter
b=open('apk_unzip/classes.dex','rb').read()
parts=re.findall(b'L([a-zA-Z0-9_/$\-]{3,200});',b)
pkgs=[p.decode('utf-8','ignore').replace('/','.') for p in parts]
roots=[p.split('.')[0] for p in pkgs if p]
cnt=Counter(roots)
for k,v in cnt.most_common(30):
    print(f"{k}: {v}")

# show some full package examples for top roots
top=[k for k,_ in cnt.most_common(10)]
examples=set()
for p in pkgs:
    if any(p.startswith(t+'.') for t in top):
        examples.add(p)
for e in sorted(list(examples))[:200]:
    print(e)
