#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
import tkinter.ttk as ttk
import concurrent.futures
from time import sleep
import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def crow_func(key_words):
    options = webdriver.ChromeOptions()
    userdata_dir = 'C://chrome_profile'  # C直下

    options.add_argument("start-maximized")    # ウィンドウの最大化
    options.add_argument('--disable-extensions') # エクステンション無効
    options.add_argument("--disable-dev-shm-usage") # シェアドメモリの保持場所が/dev/shm => /tmp(安定する?)

    # プロファイルの確認
    if os.path.isdir(userdata_dir):
        options.add_argument('--user-data-dir=' + userdata_dir)
    else:
        # プロファイルの確認ができなればCドライブ直下にファイルを作成する
        os.makedirs(userdata_dir, exist_ok=True)
        options.add_argument('--user-data-dir=' + userdata_dir)

    ######################################################

    # 通知を無効にする
    prefs = {"profile.default_content_setting_values.notifications" : 2}    # https://stackoverflow.com/questions/41400934/
    options.add_experimental_option("prefs",prefs)
    # 上部のバー「自動制御中です」を非表示にする
    options.add_experimental_option("excludeSwitches", ['enable-automation']);

    site_urls = [
        # アマゾン  メルカリ ヤフオク ヤフショ
        'https://www.amazon.co.jp/s?k=' + key_words + '&__mk_ja_JP=カタカナ&ref=nb_sb_noss',
        'https://shopping.yahoo.co.jp/search?X=2&p=' + key_words + '&tab_ex=commerce&ship=on&area=40&sc_i=shp_pc_search_nrwtr_item&ship2=on',
        'https://auctions.yahoo.co.jp/search/search?p=' + key_words + '&va=' + key_words + '&exflg=1&b=1&n=100&s1=cbids&o1=a&mode=1',
        'https://www.mercari.com/jp/search/?sort_order=price_asc&keyword=' + key_words + '&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=&status_on_sale=1',
    ]

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def browser_func(url):
        driver.execute_script(f"window.open('{url}')")
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(browser_func, url)for url in site_urls]

        driver.switch_to.window(driver.window_handles[0])
        driver.close()
    except Exception as e:
        print(str(idx),'：',e)
        pass
    
    
                
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('ECサイト一括起動-2.0')
        self.geometry('450x110')
        self.option_add('*font', ('FixedSys', 14))
        self.wm_attributes('-topmost', True)
        
        self.s = ttk.Style()
        self.s.configure('My.TFrame')
        
        self.ifreme = ttk.Frame(self, style='My.TFrame')
        self.ifreme.pack(expand=True, fill=tk.BOTH, padx=16, pady=16)
        
        ### 検索ワード入力エリア
        self.frame_word = ttk.Frame(self.ifreme, padding=10, style='My.TFrame')
        self.frame_word.pack(fill=tk.X)
        
        # タイトルラベル
        self.word_lb = tk.Label(self.frame_word, text="商品タイトル", width=40, anchor="w")
        self.word_lb.grid(column=0, row=0)
        # 検索ワード　エントリー
        self.word_entry = tk.Entry(self.frame_word, width=40)
        self.word_entry.grid(column=0, row=1, padx=(0, 0), ipady=4)
        self.word_entry.bind("<Return>", self.word_func_entry)
        # 検索ボタン
        self.seach_button =  tk.Button(self.frame_word, text="検索", width=5, relief='groove', fg='#2196F3', bg='white', command=self.word_serch)
        self.seach_button.grid(column=1, row=1, ipadx=10, ipady=5, padx=5)

    def word_func_entry(self, event):
        key_words = self.word_entry.get()
        crow_func(key_words)
    
    def word_serch(self):
        key_words = self.word_entry.get()
        crow_func(key_words)

def main():
    app = App()    
    app.mainloop()
    
if __name__ == "__main__":
    main()