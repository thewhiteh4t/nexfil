import asyncio
from modules.printer import clout

async def test_method(session, url):
    try:
        response = await session.get(url, allow_redirects=True)
        if response.status != 404:
            await clout(response.url)
        else:
            pass
    except asyncio.exceptions.TimeoutError:
        #print(f'{Y}[!] Timeout :{C} {url}{W}')
        return
    except Exception as exc:
        #print(f'{Y}[!] Exception [test_method] [{url}] :{W} {exc}')
        return