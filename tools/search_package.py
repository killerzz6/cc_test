import re

for fn in ['apk_unzip/AndroidManifest.xml','apk_unzip/classes.dex']:
    print('===',fn)
    b=open(fn,'rb').read()
    for m in re.finditer(b'package',b):
        start=max(0,m.start()-120)
        end=min(len(b),m.end()+120)
        s=b[start:end].replace(b'\x00',b'.')
        print(s.decode('utf-8',errors='ignore'))
    print()