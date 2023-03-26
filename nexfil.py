#!/usr/bin/env python3

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
uname = args.u
ulist = args.l
fname = args.f
tout = args.t
vers = args.v
update = args.U
proxy_mode = args.pm
proxy_proto = args.proto
proxy_host = args.ph
proxy_port = args.pp

import sys

if vers is True:
    print(SCRIPT_V)
    sys.exit()

USE_PROXY = False
if proxy_host is not None and proxy_port is not None:
    USE_PROXY = True

from json import loads
from packaging import version
from requests import get
from modules.write_log import log_writer


def chk_update():
    try:
        print('> Fetching Metadata...', end='')
        rqst = get('https://raw.githubusercontent.com/thewhiteh4t/nexfil/master/metadata.json', timeout=5)
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
        log_writer(f'nexfil.py, {upd_exc}')
    sys.exit()


if update is True:
    chk_update()

if uname is None and ulist is None and fname is None:
    print('''
Please provide one of the following :
\t* Username [-u]
\t* Comma separated usernames [-l]
\t* File containing list of usernames [-f]
''')
    sys.exit()

if uname is not None:
    MODE = 'single'
    if len(uname) > 0:
        if uname.isspace():
            print('Error : Username Missing!')
            sys.exit()
        else:
            pass
    else:
        print('Error : Username Missing!')
        sys.exit()
elif fname is not None:
    MODE = 'file'
elif ulist is not None:
    MODE = 'list'
    tmp = ulist
    if ',' not in tmp:
        print('Error : Invalid Format!')
        sys.exit()
    else:
        ulist = tmp.split(',')
else:
    pass

from modules.printer import smsg, emsg, wmsg, clout, pprog

smsg('Importing Modules...', '+')

import asyncio
import aiohttp

from datetime import datetime
from os import getenv, path, makedirs, getcwd

from modules.url import test_url
from modules.alt import test_alt
from modules.api import test_api
from modules.sub import test_sub
from modules.string_case import test_string
from modules.method import test_method
from modules.redirect import test_redirect
from modules.headless import test_driver
import modules.share

from selenium.common.exceptions import WebDriverException

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    home = getcwd()
else:
    home = getenv('HOME')

codes = [200, 301, 302, 405, 418]
log_file = home + '/.local/share/nexfil/exceptions.log'
loc_data = home + '/.local/share/nexfil/dumps/'

if not path.exists(loc_data):
    makedirs(loc_data)

modules.share.LOG_FILE_PATH = log_file


def print_banner():
    with open('metadata.json', 'r') as metadata:
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
        proxy_url = f'{proxy_proto}://{proxy_host}:{proxy_port}'
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
            await test_driver(browser, url, data, tout)
        else:
            if USE_PROXY is True:
                response = await session.head(
                    url,
                    allow_redirects=True,
                    proxy=proxy_url
                )
            else:
                response = await session.head(url, allow_redirects=True)
            if response.status in codes:
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
                modules.share.errors.append(url)
            else:
                pass
    except asyncio.exceptions.TimeoutError as exc:
        modules.share.timedout.append(url)
        log_writer(f'nexfil.py, {exc}, {url}')
    except aiohttp.ClientError as exc:
        modules.share.errors.append(url)
        log_writer(f'nexfil.py, {exc}, {url}')
    except WebDriverException as exc:
        modules.share.errors.append(url)
        log_writer(f'nexfil.py, {exc}, {url}')

    modules.share.COUNTER += 1
    await pprog(modules.share.COUNTER)


def autosave(uname, ulist, mode, found, start_time, end_time):
    if mode == 'single':
        filename = f'{uname}_{str(int(datetime.now().timestamp()))}.txt'
        username = uname
    elif mode == 'list' or mode == 'file':
        filename = f'session_{str(int(datetime.now().timestamp()))}.txt'
        username = ulist
    else:
        pass

    with open(loc_data + filename, 'w') as outfile:
        outfile.write(f'nexfil v{SCRIPT_V}\n')
        outfile.write(f'{"-" * 40}\n')
        if isinstance(username, list):
            outfile.write(f'Username : {", ".join(username)}\n')
        else:
            outfile.write(f'Username : {username}\n')
        outfile.write(f'Start Time : {start_time.strftime("%c")}\n')
        outfile.write(f'End Time : {end_time.strftime("%c")}\n')
        outfile.write(f'Total Hits : {len(found)}\n')
        outfile.write(f'Total Timeouts : {len(modules.share.timedout)}\n')
        outfile.write(f'Total Errors : {len(modules.share.errors)}\n\n')
        outfile.write('URLs : \n\n')
        for url in found:
            outfile.write(f'{url}\n')
        outfile.write(f'\n{"-" * 40}\n')
    smsg(f'Saved : {loc_data + filename}', '+')


async def main(uname):
    tasks = []
    smsg(f'Target : {uname}', '+')
    print()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
    }

    timeout = aiohttp.ClientTimeout(sock_connect=tout, sock_read=tout)
    conn = aiohttp.TCPConnector(ssl=False)

    if USE_PROXY is True:
        smsg('Proxy      : ON', '+')
        smsg(f'Proxy Mode : {proxy_mode}', '+')
        smsg(f'Proxy Type : {proxy_proto}', '+')
        smsg(f'Proxy Host : {proxy_host}', '+')
        smsg(f'Proxy Port : {proxy_port}', '+')
        log_writer('Proxy will be used!')
        log_writer(f'Proxy details : {proxy_mode}, {proxy_proto}, {proxy_host}, {proxy_port}')

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

if __name__ == "__main__":
    try:
        log_writer('----- STARTING -----')
        print_banner()

        wmsg('Loading URLs...')
        with open('url_store.json', 'r', encoding='utf-8') as url_store:
            raw_data = url_store.read()
            urls_json = loads(raw_data)
        smsg(f'{len(urls_json)} URLs Loaded!', '+')

        smsg(f'Timeout : {tout} secs', '+')

        start_time = datetime.now()

        if MODE == 'single':
            asyncio.run(main(uname))
        elif MODE == 'list':
            for uname in ulist:
                ulist[ulist.index(uname)] = uname.strip()
                asyncio.run(main(uname))
        elif MODE == 'file':
            ulist = []
            try:
                with open(fname, 'r') as wdlist:
                    tmp = wdlist.readlines()
                    for user in tmp:
                        ulist.append(user.strip())
                for uname in ulist:
                    uname = uname.strip()
                    asyncio.run(main(uname))
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
        smsg(f'Total Profiles Found : {len(modules.share.found)}', '>')
        smsg(f'Total Timeouts       : {len(modules.share.timedout)}', '>')
        smsg(f'Total Exceptions     : {len(modules.share.errors)}', '>')
        print()

        if len(modules.share.found) != 0:
            autosave(uname, ulist, MODE, modules.share.found, start_time, end_time)
        else:
            pass
        log_writer('----- COMPLETED -----')
    except KeyboardInterrupt:
        print()
        emsg('Keyboard Interrupt.')
        log_writer('nexfil.py, recieved keyboard interrupt')
        log_writer('----- COMPLETED -----')
        sys.exit()
