from nexfil.printer import clout
from nexfil.write_log import log_writer
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


async def test_driver(driver, url, data, timeout):
    if 'Just a moment' in driver.title:
        try:
            match = WebDriverWait(driver, timeout).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, data['found'])),
                    EC.presence_of_element_located((By.XPATH, data['not_found']))
                )
            )
            for case in data:
                try:
                    match.find_element(By.XPATH, data[case])
                    if case == 'found':
                        await clout(url)
                except NoSuchElementException:
                    pass
        except TimeoutException:
            if 'Ray ID' in driver.page_source:
                log_writer(f'headless.py, Cloudflare bypass failed, {url}')
            else:
                log_writer(f'headless.py, Timed out, {url}')
    else:
        try:
            match = WebDriverWait(driver, timeout).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, data['found'])),
                    EC.presence_of_element_located((By.XPATH, data['not_found']))
                )
            )
            for case in data:
                try:
                    match.find_element(By.XPATH, data[case])
                    if case == 'found':
                        await clout(url)
                except NoSuchElementException:
                    pass
        except TimeoutException:
            log_writer(f'headless.py, Timed out, {url}')
