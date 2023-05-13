import time
import random
import sys
from datetime import datetime
import logging
import argparse
from itertools import product


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


from wi2.footprint import *



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler1 = logging.FileHandler(filename='log/main.log')
handler1.setLevel(logging.DEBUG)
handler1.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
logger.addHandler(handler1)

handler2 = logging.StreamHandler()
handler2.setLevel(logging.DEBUG)
handler2.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
logger.addHandler(handler2)




def execute(
    d, last_login=1,
    age=30,
    prefs_range = [13],
    tall_range=[130, 200],
    edu_range=[1],
):
    """
    last_login=1: 
    last_login=2: 
    """
    results = []

    try:
        # 実行開始ア合図
        logger.debug(f'年齢: {age}, 都道府県: {prefs_range}, 身長: {tall_range}, 最終ログイン: {last_login}, 学歴: {edu_range}')
        success, result, search_result, click_count = exe_pattern(
            d, age, prefs_range, last_login, tall_range, edu_background=edu_range, wait_time=2.0
        )
        logger.debug(f'検索結果: {search_result}, 足跡付けた数: {click_count}')
        if success:
            results.append(result)
        
    except Exception as e:
        print(e)
        time.sleep(30)
                        


if __name__ == '__main__':

    # コマンドライン・オプション引数の設定
    parser = argparse.ArgumentParser(description='実行時の設定を追加')
    parser.add_argument('-last-login', type=int, default=1)
    parser.add_argument('-iteration', type=int, default=10)
    parser.add_argument('-tall-sep', type=int, default=0)
    parser.add_argument('-age-start', type=int, default=34)
    parser.add_argument('-age-end', type=int, default=60)
    parser.add_argument('-edu-sep', type=int, default=0)
    parser.add_argument('-ittosanken', type=int, default=0)
    args = parser.parse_args()

    print('\n\n\n')

    if args.tall_sep == 1:
        tall_list = [
            [130, 154],
            [155, 159],
            [160, 164],
            [165, 200]
        ]
        print('tall_sep:', 1)
    elif args.tall_sep == 0:
        tall_list = [[130, 200]]
        print('tall_sep:', 0)

    if args.edu_sep == 0:
        edu_backgound = [0]
        print('edu_sep:', 0)
    elif args.edu_sep == 1:
        edu_backgound = [1, 2, 3, 4, 5]
        print('edu_sep:', 1)


    if args.ittosanken == 0:
        prefs_list = [
            [1, 2, 3, 4, 5, 6], # 北海道・東北
            [7, 8, 9, 10, 15, 16, 17, 18], # 北関東, 北陸
            [11, 12, 14], # 千葉・埼玉・神奈川
            [13], # 東京
            [19, 20, 21, 22, 24], # 中部(愛知除く)
            [23], # 愛知
            [25, 26, 28, 29, 30], # 関西(大阪除く)
            [27], # 大阪
            [31, 32, 33, 33, 34, 35, 36, 37, 38, 39], # 中四国
            [40, 41, 42, 43, 44, 45, 46, 47], # 九州・沖縄
            [48], # 海外
        ]
        print('ittosanken:', 0)
    elif args.ittosanken == 1:
        prefs_list = [
            [11, 12, 14], # 千葉・埼玉・神奈川
            [13], # 東京
        ]
        print('ittosanken:', 1)
    else:
        raise Exception('arg "-ittosanken" should be 0 or 1.')
    
    age_list = list(range(args.age_start, args.age_end))

    print('\n\n\n')

    # 準備
    d = webdriver.Chrome('./driver/chromedriver')
    d.implicitly_wait(10)
    d.get('https://with.is/search')
    a = input()

    # 反復実行
    print('\n\n\n')
    logger.debug(f'Last Login: {args.last_login}, Iteration: {args.iteration}, Age(start): {args.age_start}, Age(end): {args.age_end}')
    print('\n\n\n')
    for _ in range(args.iteration):
        tar_list = [l for l in product(tall_list, edu_backgound, prefs_list, age_list)]
        random.shuffle(tar_list)
        for tall_range, edu_range, prefs_range, age in tar_list:
            execute(d, age=age, prefs_range=prefs_range, tall_range=tall_range, edu_range=edu_range, last_login=args.last_login)