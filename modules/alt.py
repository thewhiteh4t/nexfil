import asyncio
from modules.output import clout

async def test_alt(session, url, alt_url):
    try:
        response = await session.get(alt_url, allow_redirects=False)
        if response.status != 200:
            pass
        else:
            await clout(url)
    except Exception as exc:
        #print(f'{Y}[!] Exception [test_alt] [{url}] :{W} {str(exc)}')
        return