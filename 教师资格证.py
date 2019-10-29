#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 14:57
# @Author  : Sand
# @FileName: 教师资格证.py
# @Project : automation


import os
import requests
from selenium import webdriver

key_words = ["2019年", "下半年", "中小学教师资格考试", '笔试', '报名']
URL = "http://www.hbea.edu.cn/html/zhks/index.shtml"
base_path = os.path.dirname(os.path.abspath(__file__)) + '\.'
driver_path = os.path.abspath(base_path + '\driver\chromedriver.exe')

locator_headlines = "//*[@id='c01']/table[2]/tbody/tr/td/li/a"

# driver = webdriver.Chrome(executable_path=driver_path)
# driver.get(URL)
#
# headlines = driver.find_elements_by_xpath(locator_headlines)

rep = requests.get(URL)
print(rep.json())

# for item in headlines:
#     head_line = item.text
#     link = item.get_attribute('href')
#     count = 0
#     for key_word in key_words:
#         if key_word in head_line:
#             count += 1
#     if count == len(key_words):
#         print(head_line, link)
#     else:
#         count = 0
#
# driver.quit()
