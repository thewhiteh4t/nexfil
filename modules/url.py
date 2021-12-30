import asyncio
import tldextract
from modules.printer import clout

async def test_url(url):
    url = str(url)
    proto = url.split('://')[0]
    ext = tldextract.extract(url)
    subd = ext.subdomain
    if subd != '':
        base_url = proto + '://' + subd  + '.' + ext.registered_domain
    else:
        base_url = proto + '://' + ext.registered_domain

    if url.endswith('/') == False and base_url.endswith('/') == True:
        if url + '/' != base_url:
            await clout(url)
        else:
            pass
    elif url.endswith('/') == True and base_url.endswith('/') == False:
        if url != base_url + '/':
            await clout(url)
        else:
            pass
    elif url != base_url:
        await clout(url)
    else:
        pass