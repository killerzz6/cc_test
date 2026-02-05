import re
b=open('apk_unzip/classes.dex','rb').read()
parts=re.findall(b'([A-Za-z0-9_\./\$]{6,200})',b)
cands=set()
for p in parts:
    s=p.decode('utf-8',errors='ignore')
    if any(k in s for k in ['Activity','Service','Receiver','Fragment','Provider','Main', 'Launcher']):
        if '.' in s or '/' in s:
            s2=s.replace('/','.')
            cands.add(s2)
for c in sorted(cands)[:400]:
    print(c)
