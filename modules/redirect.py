import asyncio
from modules.printer import clout
from modules.write_log import log_writer


async def test_redirect(session, url):
    try:
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
