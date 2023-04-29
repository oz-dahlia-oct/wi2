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
    d.execute_script('window.scrollBy(0, -1000);')


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




def check_user(d, user_id):

    detail = {'user_id': f'uid_{user_id}', }
    soup = BeautifulSoup(d.page_source, 'html.parser')
    
    return detail




def get_users(d, wait_time=1.5):

    soup = BeautifulSoup(d.page_source, 'html.parser')
    result_elm = soup.find('div', class_='search-controller_summary')
    result_raw = result_elm.text.replace('\n', '')
    result_txt = result_elm.text[:-2].replace(',', '')
    result_num = int(result_txt)
    scroll_count = result_num // 10

    for i in range(scroll_count):
        d.execute_script('window.scrollBy(0, 1000);')
        time.sleep(0.2)

    soup = BeautifulSoup(d.page_source, 'html.parser')
    user_elms = soup.find_all('div', class_='user-card-small is-basic touching-effect-user-card user-area')
    user_ids = [elm['data-user-id'] for elm in user_elms]

    return result_raw, result_num, user_ids




def exe_pattern(d, age, prefs, last_login, tall=[1, 999], edu_background=1, wait_time=1.7):

    result = {'age': age, 'pref': prefs}

    # 検索条件を設定して検索実行
    search(d, age=age, prefs=prefs, login=f'{last_login}', tall=tall, edu_background=edu_background)
    
    # 検索結果なしの場合をチェック
    # **** 実装予定 ******

    # 検索結果画面からユーザー数、ユーザーIDを取得
    search_result, click_count, user_ids = get_users(d, wait_time=wait_time)
    result['search_result'] = search_result

    # 足跡をつける
    for user_id in user_ids:
        user_url = f'https://with.is/users/{user_id}'
        d.get(user_url)

        # ユーザーデータを抽出
        user_detail = check_user(d, user_id)
        time.sleep(1)

    result['clickcount'] = len(user_ids)

    return True, result, search_result, click_count


