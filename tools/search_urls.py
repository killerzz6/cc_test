import re,os
for root,dirs,files in os.walk('apk_unzip/assets/base/res/client_zip'):
    for f in files:
        p=os.path.join(root,f)
        try:
            b=open(p,'rb').read()
        except:
            continue
        for m in re.findall(b'(https?://[\w\-\./:%?&=~#\+]+)', b, flags=re.IGNORECASE):
            print(p, m.decode('utf-8',errors='ignore'))
