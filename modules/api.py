import asyncio
from modules.printer import clout

async def test_api(session, url, endpoint):
    try:
        response = await session.get(endpoint)
        if response.status != 404:
            resp_body = loads(await response.text())
            if len(resp_body) != 0:
                tmp_vars = ['results', 'users', 'username']
                for var in tmp_vars:
                    try:
                        if resp_body.get(var) != None:
                            if len(resp_body[var]) != 0:
                                await clout(url)
                                return
                            else:
                                pass
                        else:
                            pass
                    except:
                        pass
            else:
                pass
        else:
            pass
    except Exception as exc:
        #print(f'{Y}[!] Exception [test_api] [{url}] :{W} {exc}')
        return