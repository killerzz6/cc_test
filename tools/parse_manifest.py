import re

p = 'apk_unzip/AndroidManifest.xml'
with open(p, 'rb') as f:
    b = f.read()

# 找到所有可打印 ASCII / 常见 UTF-8 片段
parts = re.findall(b'([\x20-\x7E]{4,})', b)

interesting = []
for p in parts:
    s = p.decode('utf-8', errors='ignore')
    if any(k in s for k in ['package', 'uses-permission', 'activity', 'service', 'receiver', 'android:label', 'android:exported', 'application']):
        interesting.append(s)

if interesting:
    print('\n'.join(sorted(set(interesting))))
else:
    print('No interesting strings found')
