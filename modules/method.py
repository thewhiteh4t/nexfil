import asyncio
from modules.printer import clout
from modules.write_log import log_writer


async def test_method(session, url):
    try:
        response = await session.get(url, allow_redirects=True)
        if response.status != 404:
            await clout(response.url)
        else:
            pass
    except asyncio.exceptions.TimeoutError as exc:
        log_writer(f'method.py, {exc}, {url}')
    except Exception as exc:
        log_writer(f'method.py, {exc}, {url}')
