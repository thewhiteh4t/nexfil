import asyncio
from modules.printer import clout

async def test_sub(url, resp_url):
    if url == str(resp_url):
        await clout(url)
    else:
        pass