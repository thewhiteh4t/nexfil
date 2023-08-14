from json import loads
from nexfil.printer import clout
from nexfil.write_log import log_writer


async def test_api(session, use_proxy, proxy_url, url, endpoint):
    try:
        if use_proxy is True:
            response = await session.get(endpoint, proxy=proxy_url)
        else:
            response = await session.get(endpoint)
        if response.status != 404:
            resp_body = loads(await response.text())
            if len(resp_body) != 0:
                tmp_vars = ['results', 'users', 'username']
                for var in tmp_vars:
                    try:
                        if resp_body.get(var) is not None:
                            if len(resp_body[var]) != 0:
                                await clout(url)
                                return
                            else:
                                pass
                        else:
                            pass
                    except Exception:
                        pass
            else:
                pass
        else:
            pass
    except Exception as exc:
        log_writer(f'api.py, {exc}, {url}')
        return
