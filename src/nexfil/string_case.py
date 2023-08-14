import asyncio
from nexfil.printer import clout
from nexfil.write_log import log_writer

codes = [200, 400, 405, 410, 418, 500, 503]


async def test_string(session, use_proxy, proxy_url, url, data):
    try:
        if use_proxy is True:
            response = await session.get(url, proxy=proxy_url, allow_redirects=False)
        else:
            response = await session.get(url, allow_redirects=False)
        if response.status == 404:
            pass
        elif response.status not in codes:
            log_writer(f'string_case.py, status {response.status}, {url}')
        else:
            resp_body = await response.text()
            if data not in resp_body:
                await clout(response.url)
    except asyncio.exceptions.TimeoutError as exc:
        log_writer(f'string_case.py, {exc}, {url}')
    except Exception as exc:
        log_writer(f'string_case.py, {exc}, {url}')
