import os, re

paths=['apk_unzip/classes.dex']
for root,dirs,files in os.walk('apk_unzip/assets'):
    for f in files:
        paths.append(os.path.join(root,f))

keywords=[b'http',b'https',b'api',b'url',b'token',b'secret',b'key',b'appid',b'wxapi',b'wx',b'wechat',b'password',b'passwd',b'signature']

results={}
for p in paths:
    try:
        b=open(p,'rb').read()
    except:
        continue
    for k in keywords:
        if re.search(k, b, re.IGNORECASE):
            # extract surrounding printable sequences
            parts=re.findall(b'([ -~]{4,200})',b)
            lines=[part.decode('utf-8','ignore') for part in parts if re.search(k, part, re.IGNORECASE)]
            results[p]=results.get(p,[])+lines

for p,lines in results.items():
    print('---',p)
    for ln in lines[:20]:
        print(ln)
    print()
