from modules.printer import clout
from modules.write_log import log_writer


async def test_alt(session, url, alt_url):
    try:
        response = await session.get(alt_url, allow_redirects=False)
        if response.status != 200:
            pass
        else:
            await clout(url)
    except Exception as exc:
        log_writer(f'alt.py, {exc}, {url}')
