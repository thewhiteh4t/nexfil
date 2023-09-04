from nexfil.printer import clout
from nexfil.write_log import log_writer


async def test_alt(session, use_proxy, proxy_url, url, alt_url):
    try:
        if use_proxy is True:
            response = await session.get(alt_url, proxy=proxy_url, allow_redirects=False)
        else:
            response = await session.get(alt_url, allow_redirects=False)
        if response.status != 200:
            pass
        else:
            await clout(url)
    except Exception as exc:
        log_writer(f'alt.py, {exc}, {url}')
