import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from threading import Thread

BUTTON_PATH    = 'button.wn9odt-0:nth-child(1)'
MAIN_URL        = 'https://coinmarketcap.com/currencies/safememe/'
clicked_count   = 0

class C_Thread:
    def __init__(self, index, thread) -> None:
        self.index = index
        self.thread = thread
        pass

def get_firefox_capabilities():
    open_proxy_list =  open("proxies.txt", "r")
    proxy_list = open_proxy_list.read()
    proxies_length = len(proxy_list.split("\n"))
    proxy_info = proxy_list.split("\n")[randint(0, proxies_length - 1)]
    proxy_ip = proxy_info.split(":")[0]
    proxy_port = proxy_info.split(":")[1]
    PROXY = f"{proxy_ip}:{proxy_port}"
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    firefox_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY
    }

    return firefox_capabilities

def main(browser: WebDriver) -> bool:
    print('Running process')
    try:
        # browser.execute_script('localStorage.clear()')
        # browser.delete_all_cookies()
        # browser.refresh()
        browser.get(MAIN_URL)

    except Exception as e:
        print("exception 1 {}".format(e))
        return False

    good_button = None

    scroll_to = 0
    count = 0
    while good_button is None:
        try:
            good_button = WebDriverWait(browser, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, BUTTON_PATH))
            )
            print(good_button)
        except:
            scroll_to = scroll_to + 400
            browser.execute_script('window.scrollTo(0, {})'.format(scroll_to))
            if  count > 8:
                print("exception 3")
                return False
            # print('retrying...')
            count = count + 1
            time.sleep(2)

    try:
        elt = browser.find_element_by_css_selector('.cmc-cookie-policy-banner__close')
        elt.click()
    except:
        print()

    try:
        good_button.click()
        print('clicked')
        browser.execute_script('localStorage.clear()')
        browser.delete_all_cookies()

        time.sleep(5)
        return True
    except Exception as e:
        print("exception 2 {}".format(e))
        return False

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    broswer_count       = 1
    click_count         = 3
    live_thread_count    = 0

    broswer_count = input("How many browser can you run? \n(defualt 1, max 3): ")

    if RepresentsInt(broswer_count):
        broswer_count = int(broswer_count)
    else:
        broswer_count       = 1

    if broswer_count > 3:
        broswer_count = 3
    print(f"broswer_count {broswer_count}")

    threads = []

    browsers = []
    for i in range(0, broswer_count):
        firefox_capabilities = get_firefox_capabilities()
        browser = webdriver.Firefox(capabilities=firefox_capabilities)
        # browser = webdriver.Firefox()
        # browser.get(MAIN_URL)
        browsers.append(browser)

    def get_browser_index() -> int:
        for i in range(0, 3):
            exists = False
            for t in threads:
                if t.index is i:
                    exists = True
            if not exists:
                return i

    while True:
        temp = []
        if live_thread_count < broswer_count:
            browser_index = get_browser_index()
            thread: Thread = Thread(target=main, args=(browsers[browser_index], ))
            thread.start()
            threads.append(C_Thread(browser_index, thread))
            live_thread_count = live_thread_count + 1
            browser_index = browser_index + 1

        for t in threads:
            if  t.thread.is_alive():
                temp.append(C_Thread(t.index, t.thread))

        threads = temp
        live_thread_count = len(threads)
        time.sleep(randint(1, 4))
