import asyncio
from nexfil.printer import clout
from nexfil.write_log import log_writer


async def test_redirect(session, use_proxy, proxy_url, url):
    try:
        if use_proxy is True:
            response = await session.get(url, proxy=proxy_url, allow_redirects=False)
        else:
            response = await session.get(url, allow_redirects=False)
    except asyncio.exceptions.TimeoutError as exc:
        log_writer(f'redirect.py, {exc}, {url}')
        return
    except Exception as exc:
        log_writer(f'redirect.py, {exc}, {url}')
        return
    try:
        location = response.headers['Location']
        if url != location:
            pass
        else:
            await clout(url)
    except KeyError:
        await clout(url)
