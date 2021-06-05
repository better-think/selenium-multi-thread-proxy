# import sys
# import os
# import pathlib
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from threading import Thread

BUTTON_XPATH    = '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[4]/div/div[2]/button[1]'
MAIN_URL        = 'https://coinmarketcap.com/currencies/safememe/'
clicked_count   = 0


def get_proxy(proxy_username: str, proxy_password: str) -> Proxy:
    open_proxy_list =  open("proxies.txt", "r")
    proxy_list = open_proxy_list.read()
    proxies_length = len(proxy_list.split("\n"))
    proxy_info = proxy_list.split("\n")[randint(0, proxies_length - 1)]
    proxy_ip = proxy_info.split(":")[0]
    proxy_port = proxy_info.split(":")[1]
    # proxy_username = proxy_info.split(":")[2]
    # proxy_password = proxy_info.split(":")[3]
    myProxy = f"{proxy_ip}: {proxy_port}"
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy,
        'ftpProxy': myProxy,
        'sslProxy': myProxy,
        'noProxy': '',
        'socksUsername': proxy_username,
        'socksPassword': proxy_password
    })
    print(f"You are loging in this proxy : ip address : {proxy_ip}, port : {proxy_port}, user name : {proxy_username}, password : {proxy_password}")
    return proxy

def main(u: str, p: str):
    print('Running process')
    proxy: Proxy = get_proxy(u, p)
    browser = webdriver.Firefox(proxy=proxy)
    browser.get(MAIN_URL)
    good_button = None

    scroll_to = 0
    while good_button is None:
        try:
            good_button = WebDriverWait(browser, 0.3).until(
                EC.presence_of_element_located((By.XPATH, BUTTON_XPATH))
            )
            # good_button = browser.find_element_by_xpath(BUTTON_XPATH)
        except:
            scroll_to = scroll_to + 400
            browser.execute_script('window.scrollTo(0, {})'.format(scroll_to))
            # print('retrying...')
            pass

    good_button.click()
    print('clicked')
    # clicked_count = clicked_count + 1
    time.sleep(3)
    browser.quit()

if __name__ == '__main__':
    broswer_count       = 3
    click_count         = 3
    live_tread_count    = 0
    proxy_username      = ""
    proxy_password      = ""


    broswer_count = input("How many browser can you run? \n(defualt 3): ")
    click_count = input("How many click do you want for a minute? \n(default 3): ")

    proxy_username = input("Proxy user name: ")
    proxy_password = input("Proxy password: ")

    if not isinstance(broswer_count, int):
        broswer_count = 3
    if not isinstance(broswer_count, int):
        click_count = 3

    print(f"broswer_count {broswer_count}")
    print(f"click_count {click_count}")

    treads = []
    while True:
        temp = []
        if live_tread_count < broswer_count:
            tread: Thread = Thread(target=main, args=(proxy_username, proxy_password))
            tread.start()
            treads.append(tread)
            live_tread_count += 1
            pass
        for tread in treads:
            if tread.is_alive():
                temp.append(tread)

        treads = temp
        live_tread_count = len(treads)
        time.sleep(randint(1, 4))

    print('completed')
