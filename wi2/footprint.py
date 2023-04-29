import time
import random
import os
from pprint import pprint
import json
from datetime import datetime


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import pandas as pd




def search(d, prefs, age=30, login=1, tall=[130, 200], edu_background=1):

    # 検索条件編集画面に移動
    d.get('https://with.is/search/edit')
    time.sleep(2)


    # 条件リセットボタンクリック
    d.find_element(By.NAME, "button").click()
    # 条件リセット確定
    d.find_element(By.CSS_SELECTOR, ".remove-all-conditions").click()
    time.sleep(2)


    # 居住地
    d.find_element(By.CSS_SELECTOR, ".open-addresses-dialog > .selected-by-dialog").click()
    # d.find_element(By.CLASS_NAME, "type-block_selected open-addresses-dialog")
    for pref in prefs:
        d.find_element(By.XPATH, f"//label[@for='search_form_addresses_{pref}']").click()
    # ×クリック
    d.find_element(By.CSS_SELECTOR, ".close-addresses-dialog > .icon-close-dialog").click()


    # 年齢（開始）
    dropdown = d.find_element(By.ID, "search_form_min_age")
    dropdown = Select(dropdown)
    dropdown.select_by_value(f'{age}')
    # 年齢（終了）
    dropdown = d.find_element(By.ID, "search_form_max_age")
    dropdown = Select(dropdown)
    dropdown.select_by_value(f'{age}')


    # 身長（開始）
    dropdown = d.find_element(By.ID, "search_form_min_height")
    dropdown = Select(dropdown)
    dropdown.select_by_value(f'{tall[0]}')
    # 身長（終了）
    dropdown = d.find_element(By.ID, "search_form_max_height")
    dropdown = Select(dropdown)
    dropdown.select_by_value(f'{tall[1]}')


    # スクロール
    d.execute_script('window.scrollBy(0, 1000);')


    # 学歴
    d.find_element(By.CSS_SELECTOR, ".open-educations-dialog > .selected-by-dialog").click()
    d.find_element(By.XPATH, f"//label[@for='search_form_educations_{edu_background}']")
    # ×クリック
    d.find_element(By.CSS_SELECTOR, ".close-educations-dialog > .icon-close-dialog").click()


    # ラストログイン
    dropdown = d.find_element(By.ID, "search_form_last_login")
    dropdown = Select(dropdown)
    dropdown.select_by_value(f'{login}')

    # 検索ボタンクリック
    d.find_element(By.CSS_SELECTOR, ".search-submit-button").click()
    time.sleep(2)




def check_user():
    pass




def scan_users(d, wait_time=1.5, scroll_count=50):

    for i in range(scroll_count):
        d.execute_script('window.scrollBy(0, 1000);')
        time.sleep(0.2)

    return 100




def exe_pattern(d, age, prefs, last_login, tall=[1, 999], edu_background=1, wait_time=1.7):

    result = {'age': age, 'pref': prefs}

    # 検索条件を設定して検索実行
    search(d, age=age, prefs=prefs, login=f'{last_login}', tall=tall, edu_background=edu_background)
    time.sleep(2)
    
    # 検索結果なしの場合をチェック

    # 検索結果（件数）を取得・表示
    result['search_result'] = "" # あとで変更

    # スクロール数を計算

    # ユーザーに足跡をつける
    scroll_count = 20 # あとで削除
    click_count = scan_users(
        d, wait_time=wait_time, scroll_count=scroll_count
    )

    result['clickcount'] = click_count
    return True, result, result['search_result'], click_count


