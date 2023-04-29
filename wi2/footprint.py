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
    time.sleep(2)
    # 条件リセット確定
    d.find_element(By.CSS_SELECTOR, ".remove-all-conditions").click()
    time.sleep(3)


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

    json_file_name = f'./candidates/uid_{user_id}.json'
    detail = {'user_id': f'uid_{user_id}', }
    time_now = datetime.now()
    time_now_str = datetime.strftime(time_now, '%Y-%m-%d %H:%M:%S')
    detail['update_at'] = time_now_str

    if os.path.isfile(json_file_name):
        with open(json_file_name, 'r') as f:
            d = json.load(f)
            detail['datetime'] = d['datetime']
    else:
        detail['datetime'] = time_now_str

    # データのスクレイピング
    soup = BeautifulSoup(d.page_source, 'html.parser')
    
    # いいね
    like_elm = soup.find('div', class_='user-likes-count text-primary')
    like_txt = like_elm.text.replace('\n', '')
    detail['いいね'] = like_txt

    # 基本情報
    table_elm = soup.find('table', class_='profile-detail_lists')
    tr_elms = table_elm.find_all('tr')
    for tr_elm in tr_elms:
        key = tr_elm.find('th').text
        detail[key] = tr_elm.find('td').text

    with open(json_file_name, 'w', encoding='utf-8') as f:
        json.dump(detail, f, indent=4, sort_keys=True, ensure_ascii=False)
    
    return




def get_users(d, wait_time=1.5):

    soup = BeautifulSoup(d.page_source, 'html.parser')
    result_elm = soup.find('div', class_='search-controller_summary')
    result_raw = result_elm.text.replace('\n', '')
    result_txt = result_elm.text[:-2].replace(',', '')
    result_num = int(result_txt)

    if result_num == 0:
        return result_raw, result_num, []

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

    if user_ids:
        # 足跡をつける
        for user_id in user_ids:
            user_url = f'https://with.is/users/{user_id}'
            d.get(user_url)

            # ユーザーデータを抽出
            check_user(d, user_id)
            time.sleep(1)

    result['clickcount'] = len(user_ids)

    return True, result, search_result, click_count


