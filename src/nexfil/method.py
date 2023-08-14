import asyncio
from nexfil.printer import clout
from nexfil.write_log import log_writer


async def test_method(session, use_proxy, proxy_url, url):
    try:
        if use_proxy is True:
            response = await session.get(url, proxy=proxy_url, allow_redirects=True)
        else:
            response = await session.get(url, allow_redirects=True)
        if response.status != 404:
            await clout(response.url)
        else:
            pass
    except asyncio.exceptions.TimeoutError as exc:
        log_writer(f'method.py, {exc}, {url}')
    except Exception as exc:
        log_writer(f'method.py, {exc}, {url}')
