import asyncio
from modules.printer import clout


async def test_redirect(session, url):
    try:
        response = await session.get(url, allow_redirects=False)
    except asyncio.exceptions.TimeoutError:
        # print(f'{Y}[!] Timeout :{C} {url}{W}')
        return
    except Exception:
        # print(f'{Y}[!] Exception [test_redirect] [{url}] :{W} {str(exc)}')
        return
    try:
        location = response.headers['Location']
        if url != location:
            pass
        else:
            await clout(url)
    except KeyError:
        await clout(url)
