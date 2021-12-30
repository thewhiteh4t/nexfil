from modules.share import found

async def clout(url):
    global found
    found.append(url)
    url = str(url)
    ext = tldextract.extract(url)
    dom = str(ext.domain)
    suf = str(ext.suffix)
    orig = f'{dom}.{suf}'
    cl_dom = f'{Y}{dom}.{suf}{C}'
    url = url.replace(orig, cl_dom)
    print(f'{G}[+] {C}{url}{W}')