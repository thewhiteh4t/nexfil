SCRIPT_V = '1.0.5'

import argparse

parser = argparse.ArgumentParser(description=f'nexfil - Find social media profiles on the web | v{SCRIPT_V}')
parser.add_argument('-u', help='Specify username', type=str)
parser.add_argument('-f', help='Specify a file containing username list', type=str)
parser.add_argument('-l', help='Specify multiple comma separated usernames', type=str)
parser.add_argument('-t', help='Specify timeout [Default : 10]', type=int)
parser.add_argument('-v', help='Prints version', action='store_true')
parser.add_argument('-U', help='Check for Updates', action='store_true')
parser.add_argument('-pm', help='Proxy mode [Available : single, file] [Default : single]', type=str)
parser.add_argument('-proto', help='Proxy protocol [Available : http, https] [Default : http]', type=str)
parser.add_argument('-ph', help='Proxy Hostname', type=str)
parser.add_argument('-pp', help='Proxy port', type=int)

parser.set_defaults(
    t=10,
    v=False,
    U=False,
    pm='single',
    proto='http'
)

args = parser.parse_args()
UNAME = args.u
ULIST = args.l
FNAME = args.f
TOUT = args.t
VERS = args.v
UPDATE = args.U
PROXY_MODE = args.pm
PROXY_PROTO = args.proto
PROXY_HOST = args.ph
PROXY_PORT = args.pp

import sys

if VERS is True:
    print(SCRIPT_V)
    sys.exit()

USE_PROXY = False
if PROXY_HOST is not None and PROXY_PORT is not None:
    USE_PROXY = True

from json import loads
from packaging import version
from requests import get
from nexfil.write_log import log_writer


def chk_update():
    try:
        print('> Fetching Metadata...', end='')
        rqst = get('https://raw.githubusercontent.com/thewhiteh4t/nexfil/master/src/nexfil/metadata.json', timeout=5)
        fetch_sc = rqst.status_code
        if fetch_sc == 200:
            print('OK')
            metadata = rqst.text
            json_data = loads(metadata)
            gh_version = json_data['version']
            if version.parse(gh_version) > version.parse(SCRIPT_V):
                print(f'> New Update Available : {gh_version}')
            else:
                print('> Already up to date.')
    except Exception as upd_exc:
        print(f'Exception : {str(upd_exc)}')
        log_writer(f'nexfil, {upd_exc}')
    sys.exit()


if UPDATE is True:
    chk_update()

if UNAME is None and ULIST is None and FNAME is None:
    print('''
Please provide one of the following :
\t* Username [-u]
\t* Comma separated usernames [-l]
\t* File containing list of usernames [-f]
''')
    sys.exit()

if UNAME is not None:
    MODE = 'single'
    if len(UNAME) > 0:
        if UNAME.isspace():
            print('Error : Username Missing!')
            sys.exit()
        else:
            pass
    else:
        print('Error : Username Missing!')
        sys.exit()
elif FNAME is not None:
    MODE = 'file'
elif ULIST is not None:
    MODE = 'list'
    tmp = ULIST
    if ',' not in tmp:
        print('Error : Invalid Format!')
        sys.exit()
    else:
        ULIST = tmp.split(',')
else:
    pass

from nexfil.printer import smsg, emsg, wmsg, clout, pprog

smsg('Importing Modules...', '+')

import asyncio
import aiohttp

from datetime import datetime
from os import getenv, path, makedirs, getcwd

from nexfil.url import test_url
from nexfil.alt import test_alt
from nexfil.api import test_api
from nexfil.sub import test_sub
from nexfil.string_case import test_string
from nexfil.method import test_method
from nexfil.redirect import test_redirect
from nexfil.headless import test_driver
import nexfil.share

from selenium.common.exceptions import WebDriverException

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    home = getcwd()
else:
    home = getenv('HOME')

CODES = [200, 301, 302, 405, 418]
LOG_FILE = home + '/.local/share/nexfil/exceptions.log'
LOC_DATA = home + '/.local/share/nexfil/dumps/'

if not path.exists(LOC_DATA):
    makedirs(LOC_DATA)

nexfil.share.LOG_FILE_PATH = LOG_FILE


def print_banner():
    metadata_path = path.join(path.dirname(__file__), 'metadata.json')
    with open(metadata_path, 'r') as metadata:
        json_data = loads(metadata.read())
        twitter_url = json_data['twitter']
        comms_url = json_data['comms']

    banner = r'''
__   _ _____ _     _ _____ _____ _
| \  | |____  \___/  |____   |   |
|  \_| |____ _/   \_ |     __|__ |_____'''

    smsg(f'{banner}', None)
    print()
    smsg('Created By   : thewhiteh4t', '>')
    smsg(f' |---> Twitter   : {twitter_url}', None)
    smsg(f' |---> Community : {comms_url}', None)
    smsg(f'Version      : {SCRIPT_V}', '>')
    print()


async def query(session, browser, url, test, data, uname):
    if USE_PROXY is False:
        proxy_url = ''
    else:
        proxy_url = f'{PROXY_PROTO}://{PROXY_HOST}:{PROXY_PORT}'
    try:
        if test == 'method':
            await test_method(session, USE_PROXY, proxy_url, url)
        elif test == 'string':
            await test_string(session, USE_PROXY, proxy_url, url, data)
        elif test == 'redirect':
            await test_redirect(session, USE_PROXY, proxy_url, url)
        elif test == 'api':
            data = data.format(uname)
            await test_api(session, USE_PROXY, proxy_url, url, data)
        elif test == 'alt':
            data = data.format(uname)
            await test_alt(session, USE_PROXY, proxy_url, url, data)
        elif test == 'headless' and browser is not False:
            browser.get(url)
            await test_driver(browser, url, data, TOUT)
        else:
            if USE_PROXY is True:
                response = await session.head(
                    url,
                    allow_redirects=True,
                    proxy=proxy_url
                )
            else:
                response = await session.head(url, allow_redirects=True)
            if response.status in CODES:
                if test is None:
                    await clout(response.url)
                elif test == 'url':
                    await test_url(response.url)
                elif test == 'subdomain':
                    await test_sub(url, response.url)
                else:
                    pass
            elif response.status == 404 and test == 'method':
                await test_method(session, USE_PROXY, proxy_url, url)
            elif response.status != 404:
                nexfil.share.errors.append(url)
            else:
                pass
    except asyncio.exceptions.TimeoutError as exc:
        nexfil.share.timedout.append(url)
        log_writer(f'nexfil, {exc}, {url}')
    except aiohttp.ClientError as exc:
        nexfil.share.errors.append(url)
        log_writer(f'nexfil, {exc}, {url}')
    except WebDriverException as exc:
        nexfil.share.errors.append(url)
        log_writer(f'nexfil, {exc}, {url}')

    nexfil.share.COUNTER += 1
    await pprog(nexfil.share.COUNTER)


def autosave(uname, ulist, mode, found, start_time, end_time):
    if mode == 'single':
        filename = f'{uname}_{str(int(datetime.now().timestamp()))}.txt'
        username = uname
    elif mode == 'list' or mode == 'file':
        filename = f'session_{str(int(datetime.now().timestamp()))}.txt'
        username = ulist
    else:
        pass

    with open(LOC_DATA + filename, 'w') as outfile:
        outfile.write(f'nexfil v{SCRIPT_V}\n')
        outfile.write(f'{"-" * 40}\n')
        if isinstance(username, list):
            outfile.write(f'Username : {", ".join(username)}\n')
        else:
            outfile.write(f'Username : {username}\n')
        outfile.write(f'Start Time : {start_time.strftime("%c")}\n')
        outfile.write(f'End Time : {end_time.strftime("%c")}\n')
        outfile.write(f'Total Hits : {len(found)}\n')
        outfile.write(f'Total Timeouts : {len(nexfil.share.timedout)}\n')
        outfile.write(f'Total Errors : {len(nexfil.share.errors)}\n\n')
        outfile.write('URLs : \n\n')
        for url in found:
            outfile.write(f'{url}\n')
        outfile.write(f'\n{"-" * 40}\n')
    smsg(f'Saved : {LOC_DATA + filename}', '+')


async def main(uname, urls_json):
    tasks = []
    smsg(f'Target : {uname}', '+')
    print()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
    }

    timeout = aiohttp.ClientTimeout(sock_connect=TOUT, sock_read=TOUT)
    conn = aiohttp.TCPConnector(ssl=False)

    if USE_PROXY is True:
        smsg('Proxy      : ON', '+')
        smsg(f'Proxy Mode : {PROXY_MODE}', '+')
        smsg(f'Proxy Type : {PROXY_PROTO}', '+')
        smsg(f'Proxy Host : {PROXY_HOST}', '+')
        smsg(f'Proxy Port : {PROXY_PORT}', '+')
        log_writer('Proxy will be used!')
        log_writer(f'Proxy details : {PROXY_MODE}, {PROXY_PROTO}, {PROXY_HOST}, {PROXY_PORT}')

    wmsg('Finding Profiles...')
    print()

    wmsg('Initializing Chrome Driver...')
    try:
        import undetected_chromedriver as uc
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        if USE_PROXY is True:
            options.add_argument(f'--proxy-server={proxy_proto}://{proxy_host}:{proxy_port}')
        caps = options.capabilities
        caps["pageLoadStrategy"] = "eager"
        driver = uc.Chrome(options=options, desired_capabilities=caps)
        smsg('Chromedriver is Ready!', '+')
        print()
    except ModuleNotFoundError:
        emsg('undetected_chromedriver not found!')
        wmsg('Some websites will be skipped!')
        print()
        driver = False
    except TypeError:
        emsg('Chrome not found!')
        wmsg('Some websites will be skipped!')
        print()
        driver = False

    async with aiohttp.ClientSession(connector=conn, headers=headers, timeout=timeout, trust_env=True) as session:
        for block in urls_json:
            curr_url = block['url'].format(uname)
            test = block['test']
            data = block['data']
            task = asyncio.create_task(query(session, driver, curr_url, test, data, uname))
            tasks.append(task)
        await asyncio.gather(*tasks)


def cli():
    try:
        log_writer('----- STARTING -----')
        print_banner()

        wmsg('Loading URLs...')
        url_store_path = path.join(path.dirname(__file__), 'url_store.json')
        with open(url_store_path, 'r', encoding='utf-8') as url_store:
            raw_data = url_store.read()
            urls_json = loads(raw_data)
        smsg(f'{len(urls_json)} URLs Loaded!', '+')

        smsg(f'Timeout : {TOUT} secs', '+')

        start_time = datetime.now()

        if MODE == 'single':
            asyncio.run(main(UNAME, urls_json))
        elif MODE == 'list':
            for uname in ULIST:
                ULIST[ULIST.index(uname)] = uname.strip()
                asyncio.run(main(uname, urls_json))
        elif MODE == 'file':
            ulist = []
            try:
                with open(FNAME, 'r') as wdlist:
                    tmp = wdlist.readlines()
                    for user in tmp:
                        ulist.append(user.strip())
                for uname in ulist:
                    uname = uname.strip()
                    asyncio.run(main(uname, urls_json))
            except Exception as exc:
                wmsg(f'Exception [file] : {str(exc)}')
                log_writer(exc)
                sys.exit()
        else:
            pass

        end_time = datetime.now()
        delta = end_time - start_time
        str_d = datetime.strptime(str(delta), '%H:%M:%S.%f')
        h_delta = datetime.strftime(str_d, "%H Hours %M Minutes %S Seconds")

        print('\n')
        smsg(f'Completed In         : {h_delta}', '>')
        smsg(f'Total Profiles Found : {len(nexfil.share.found)}', '>')
        smsg(f'Total Timeouts       : {len(nexfil.share.timedout)}', '>')
        smsg(f'Total Exceptions     : {len(nexfil.share.errors)}', '>')
        print()

        if len(nexfil.share.found) != 0:
            autosave(UNAME, ULIST, MODE, nexfil.share.found, start_time, end_time)
        else:
            pass
        log_writer('----- COMPLETED -----')
    except KeyboardInterrupt:
        print()
        emsg('Keyboard Interrupt.')
        log_writer('nexfil, recieved keyboard interrupt')
        log_writer('----- COMPLETED -----')
        sys.exit()
