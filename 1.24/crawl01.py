# -*- coding: utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
import csv
index_url = "http://www.nfgrp.cn/data/list/wuzhong_detailp.shtml?kid="
# title = driver.find_element_by_id('document-title')
# print(driver.page_source.encode('gbk','ignore'))
def parseContent(html):
    soup = BeautifulSoup(html,'lxml')
    div = soup.find_all('div',{'class':'datagrid-body'})[1]
    table = div.table
    trs = table.find_all('tr')
    res = [] 
    for item in trs:
        tds = item.find_all('td')
        zhongming_a = tds[0].div.a
        href_num = re.findall('\d+',zhongming_a['onclick'])[0]
        href = index_url+href_num
        zhongming = zhongming_a.get_text()
        keming = tds[1].div.get_text()
        shuming = tds[2].div.get_text()
        shuzhong_daima = tds[4].get_text()
        res.append((zhongming,href,keming,shuming,shuzhong_daima))
        print('正在爬取'+zhongming+'的信息,当前编号：'+href_num)
    return res
driver = webdriver.PhantomJS()
driver.get('http://www.nfgrp.cn/data/list/wuzhong_detailpl_1.html?t=12')
time.sleep(10)
# print(driver.page_source)
res_all = []
csvFile2 = open('cw.csv','w', newline='') 
writer = csv.writer(csvFile2)
for i in range(1,727):
    if i > 1:
        fanye = driver.find_elements_by_class_name('l-btn-left')[3]
        fanye.click()
        time.sleep(10)
    html = driver.page_source    
    res_item = parseContent(html)
    for item2 in res_item:
        writer.writerow(item2)
csvFile2.close()
