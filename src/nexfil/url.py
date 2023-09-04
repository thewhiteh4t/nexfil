import tldextract
from nexfil.printer import clout


async def test_url(url):
    url = str(url)
    proto = url.split('://')[0]
    ext = tldextract.extract(url)
    subd = ext.subdomain
    if subd != '':
        base_url = f'{proto}://{subd}.{ext.registered_domain}'
    else:
        base_url = f'{proto}://{ext.registered_domain}'

    if url.endswith('/') is False and base_url.endswith('/') is True:
        if url + '/' != base_url:
            await clout(url)
        else:
            pass
    elif url.endswith('/') is True and base_url.endswith('/') is False:
        if url != base_url + '/':
            await clout(url)
        else:
            pass
    elif url != base_url:
        await clout(url)
    else:
        pass
