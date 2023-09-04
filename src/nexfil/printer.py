import tldextract

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow


async def clout(url):
    from nexfil.share import found
    found.append(url)
    url = str(url)
    ext = tldextract.extract(url)
    dom = str(ext.domain)
    suf = str(ext.suffix)
    orig = f'{dom}.{suf}'
    cl_dom = f'{Y}{dom}.{suf}{W}'
    url = url.replace(orig, cl_dom)
    print(url)


def emsg(msg):
    print(f'{R}[-] {C}{msg}{W}')


def smsg(msg, symbol):
    if ':' in msg:
        tmp = msg.split(' : ')
        msg = f'{C}{tmp[0]} : {W}{tmp[1]}'

    if symbol is None:
        print(f'{G}{msg}{W}')
    else:
        print(f'{G}[{symbol}] {C}{msg}{W}')


def wmsg(msg):
    print(f'{Y}[!] {C}{msg}{W}')


async def pprog(counter):
    print(f'{G}[>] {C}Progress : {W}{counter}', end='\r')
