import asyncio
from modules.printer import clout
from modules.write_log import log_writer

codes = [200, 301, 302, 400, 405, 410, 418, 500, 503]


async def test_string(session, url, data):
    try:
        response = await session.get(url)
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
