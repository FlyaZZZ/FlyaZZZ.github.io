# -*- encoding=utf-8 -*-
#爬取携程旅游信息
#2017/8/14

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import csv
import time

driver = webdriver.Chrome()

#打开网页
def gethtml(place):
    try:
        driver.get('http://vacations.ctrip.com/')
        welcome = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.jewel_pop_box > div.jewel_pop > span")))
        welcome.click()
        seaech = driver.find_element_by_css_selector('#searchpanel > div.search_wrap > div.new_search_content > div > input')
        check = driver.find_element_by_css_selector('#searchpanel > div.search_wrap > a.main_search_btn')
        seaech.send_keys(place)
        check.click()
        return driver.page_source
    except TimeoutException:
        gethtml(place)

#换页
def changepage(page):
    try:
        time.sleep(4)
        js="var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        p =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#ipt_page_txt')))
        submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#ipt_page_btn')))
        p.clear()
        p.send_keys(page)
        submit.click()
        return driver.page_source
    except:
        return changepage(page)

#解析页面
def checkpage(html):
    soup = BeautifulSoup(html,'lxml')
    links = soup.find_all('div',class_='main_mod product_box flag_product ')
    for link in links:
        name =link.h2.get_text()
        href = 'http:' + link.h2.a['href']
        price = link.find('span',class_='sr_price').get_text()[:-1]
        try:
            agree =  link.find('p',class_='grade').get_text()[:-1]
        except:
            agree = ''
        try:
            alp = link.find('div',class_='comment')
            people = alp.em.string[:-3]
            about = alp.a.get_text()[:-3]
        except:
            people = ''
            about = ''
        yield {
            '产品':name,
            '链接':href,
            '价格':price,
            '评分':agree,
            '人数':people,
            '点评':about,
        }

    
#创建文件夹
def make(place):
    path = 'D:/download_shuoshu/'
    if not os.path.exists:
        os.makedirs(path)
    with open(path + place +'旅游信息.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['产品','链接','价格','评分','人数','点评'])
        f.close()
    def save_to_csv(i):
        with open(path + place +'旅游信息.csv','a') as f:
            writer = csv.writer(f)
            try:
                writer.writerow([ i['产品'],i['链接'],i['价格'],i['评分'], i['人数'],i['点评'] ])
            except:
                pass
            f.close()
    return save_to_csv

#主函数
def main(place):
    save = make(place)
    html = gethtml(place)
    for i in checkpage(html):
        save(i)
        print(i)
    for i in range(2,101):
        
        html = changepage(i)
        for fil in checkpage(html):
            save(fil)
            print(fil)
    driver.quit() 

#执行程序
if __name__ == '__main__':
    place = input('请输入要查询的地点：')
    main(place)