#!/usr/bin/env python3

script_v = '1.0.2'

import argparse

parser = argparse.ArgumentParser(description=f'nexfil - Find social media profiles on the web | v{script_v}')
parser.add_argument('-u', help='Specify username', type=str)
parser.add_argument('-f', help='Specify a file containing username list', type=str)
parser.add_argument('-l', help='Specify multiple comma separated usernames', type=str)
parser.add_argument('-t', help='Specify timeout [Default : 5]', type=int)
parser.add_argument('-v', help='Prints version', action='store_true')
parser.add_argument('-U', help='Check for Updates', action='store_true')
parser.add_argument('-pm', help='Proxy mode [Available : single, file] [Default : single]', type=str)
parser.add_argument('-proto', help='Proxy protocol [Available : http, https] [Default : http]', type=str)
parser.add_argument('-ph', help='Proxy Hostname', type=str)
parser.add_argument('-pp', help='Proxy port', type=int)

parser.set_defaults(
    t=5,
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

if vers == True:
    print(script_v)
    exit()

from json import loads
from packaging import version
from requests import get, exceptions

def chk_update():
    try:
        print('> Fetching Metadata...', end='')
        rqst = get('https://raw.githubusercontent.com/thewhiteh4t/nexfil/master/metadata.json', timeout=5)
        sc = rqst.status_code
        if sc == 200:
            print('OK')
            metadata = rqst.text
            json_data = loads(metadata)
            gh_version = json_data['version']
            if version.parse(gh_version) > version.parse(script_v):
                print(f'> New Update Available : {gh_version}')
            else:
                print('> Already up to date.')
    except Exception as exc:
        print(f'Exception : {str(exc)}')
    exit()

if update == True:
    chk_update()

if uname == None and ulist == None and fname == None:
    print('''
Please provide one of the following :
\t* Username [-u]
\t* Comma separated usernames [-l]
\t* File containing list of usernames [-f]
''')
    exit()

if uname != None:
    mode = 'single'
    if len(uname) > 0:
        if uname.isspace():
            print('Error : Username Missing!')
            exit()
        else:
            pass
    else:
        print('Error : Username Missing!')
        exit()
elif fname != None:
    mode = 'file'
elif ulist != None:
    mode = 'list'
    tmp = ulist
    if ',' not in tmp:
        print('Error : Invalid Format!')
        exit()
    else:
        ulist = tmp.split(',')
else:
    pass

from modules.printer import smsg
from modules.printer import emsg
from modules.printer import wmsg
from modules.printer import clout
from modules.printer import pprog

smsg('Importing Modules...', '+')

import socket
import asyncio
import aiohttp
import logging
import tldextract

from datetime import datetime
from os import getenv, path, makedirs, getcwd
from sys import platform

from modules.url import test_url
from modules.alt import test_alt
from modules.api import test_api
from modules.sub import test_sub
from modules.string import test_string
from modules.method import test_method
from modules.redirect import test_redirect
from modules.share import found
from modules.share import timedout
from modules.share import errors

if platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    home = getcwd()
else:
    home = getenv('HOME')

gh_version = ''
twitter_url = ''
comms_url = ''
codes = [200, 301, 302, 403, 405, 410, 418, 500]
log_file = home + '/.local/share/nexfil/exceptions.log'
loc_data = home + '/.local/share/nexfil/dumps/'

def banner():
    with open('metadata.json', 'r') as metadata:
        json_data = loads(metadata.read())
        gh_version = json_data['version']
        twitter_url = json_data['twitter']
        comms_url = json_data['comms']

    banner = r'''
__   _ _____ _     _ _____ _____ _
| \  | |____  \___/  |____   |   |
|  \_| |____ _/   \_ |     __|__ |_____'''

    smsg(f'{banner}', None)
    print()
    smsg(f'Created By   : thewhiteh4t', '>')
    smsg(f' |---> Twitter   : {twitter_url}', None)
    smsg(f' |---> Community : {comms_url}', None)
    smsg(f'Version      : {script_v}', '>')
    print()

from modules.share import counter

async def query(session, url, test, data, uname):
    global counter
    try:
        if test == 'method':
            await test_method(session, url)
        elif test == 'string':
            await test_string(session, url, data)
        elif test == 'redirect':
            await test_redirect(session, url)
        elif test == 'api':
            data = data.format(uname)
            await test_api(session, url, data)
        elif test == 'alt':
            data = data.format(uname)
            await test_alt(session, url, data)
        else:
            response = await session.head(url, allow_redirects=True)
            if response.status in codes:
                if test == None:
                    await clout(response.url)
                elif test == 'url':
                    await test_url(response.url)
                elif test == 'subdomain':
                    await test_sub(url, response.url)
                else:
                    pass
            elif response.status == 404 and test == 'method':
                await test_method(session, url)
            elif response.status != 404:
                errors.append(url)
                pass
            else:
                pass

    except asyncio.exceptions.TimeoutError:
        timedout.append(url)
    except aiohttp.client_exceptions.ClientConnectorError:
        errors.append(url)

    counter += 1
    await pprog(counter)

def autosave(uname, ulist, mode, found, start_time, end_time):
    if not path.exists(loc_data):
        makedirs(loc_data)
    else:
        pass

    if mode == 'single':
        filename = f'{uname}_{str(int(datetime.now().timestamp()))}.txt'
        username = uname
    elif mode == 'list' or mode == 'file':
        filename = f'session_{str(int(datetime.now().timestamp()))}.txt'
        username = ulist
    else:
        pass

    with open(loc_data + filename, 'w') as outfile:
        outfile.write(f'nexfil v{script_v}\n')
        outfile.write(f'{"-" * 40}\n')
        if type(username) == list:
            outfile.write(f'Username : {", ".join(username)}\n')
        else:
            outfile.write(f'Username : {username}\n')
        outfile.write(f'Start Time : {start_time.strftime("%c")}\n')
        outfile.write(f'End Time : {end_time.strftime("%c")}\n')
        outfile.write(f'Total Hits : {len(found)}\n')
        outfile.write(f'Total Timeouts : {len(timedout)}\n')
        outfile.write(f'Total Errors : {len(errors)}\n\n')
        outfile.write(f'URLs : \n\n')
        for url in found:
            outfile.write(f'{url}\n')
        outfile.write(f'\nURLs Timed Out : \n\n')
        for url in timedout:
            outfile.write(f'{url}\n')
        outfile.write(f'\nErrors : \n\n')
        for url in errors:
            outfile.write(f'{url}\n')
        outfile.write(f'\n{"-" * 40}\n')
    smsg(f'Saved : {loc_data + filename}', '+')

async def main(uname):
    tasks = []
    smsg(f'Target : {uname}', '+')
    print()

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:88.0) Gecko/20100101 Firefox/88.0'
    }

    timeout = aiohttp.ClientTimeout(sock_connect=tout, sock_read=tout)
    conn = aiohttp.TCPConnector(
        family=socket.AF_INET,
        ssl=False
    )

    if proxy_host is not None and proxy_port is not None:
        smsg('Proxy      : ON', '+')
        smsg(f'Proxy Mode : {proxy_mode}', '+')
        smsg(f'Proxy Type : {proxy_proto}', '+')
        smsg(f'Proxy Host : {proxy_host}', '+')
        smsg(f'Proxy Port : {proxy_port}', '+')

        from modules.hide import single_proxy
        single_proxy(proxy_proto, proxy_host, proxy_port)

    wmsg('Finding Profiles...')
    print()

    async with aiohttp.ClientSession(connector=conn, headers=headers, timeout=timeout, trust_env=True) as session:
        for block in urls_json:
            curr_url = block['url'].format(uname)
            test = block['test']
            data = block['data']
            task = asyncio.create_task(query(session, curr_url, test, data, uname))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        banner()

        wmsg('Loading URLs...')
        with open('url_store.json', 'r', encoding='utf-8') as url_store:
            raw_data = url_store.read()
            urls_json = loads(raw_data)
        smsg(f'{len(urls_json)} URLs Loaded!', '+')

        smsg(f'Timeout : {tout} secs', '+')

        start_time = datetime.now()

        if mode == 'single':
            asyncio.run(main(uname))
        elif mode == 'list':
            for uname in ulist:
                ulist[ulist.index(uname)] = uname.strip()
                asyncio.run(main(uname))
        elif mode == 'file':
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
                exit()
        else:
            pass

        end_time = datetime.now()
        delta = end_time - start_time
        str_d = datetime.strptime(str(delta), '%H:%M:%S.%f')
        h_delta = datetime.strftime(str_d, "%H Hours %M Minutes %S Seconds")

        print('\n')
        smsg(f'Completed In         : {h_delta}', '>')
        smsg(f'Total Profiles Found : {len(found)}', '>')
        smsg(f'Total Timeouts       : {len(timedout)}', '>')
        smsg(f'Total Exceptions     : {len(errors)}', '>')
        print()

        if len(found) != 0:
            autosave(uname, ulist, mode, found, start_time, end_time)
        else:
            pass
    except KeyboardInterrupt:
        print()
        emsg(f'Keyboard Interrupt.')
        exit()
