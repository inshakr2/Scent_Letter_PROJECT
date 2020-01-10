# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request as req
import pandas as pd
import pickle

# 로그인               
driver = webdriver.Chrome("c:/data/chromedriver.exe")
driver.get('https://www.instagram.com/explore/tags/해시태그 이름/')
driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button').click()
driver.implicitly_wait(1)

ID = ''
PW = ''

driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(ID)
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(PW)
driver.implicitly_wait(1)
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button').click()
time.sleep(3)

# 스크롤 다운 + url 저장
urlist = []
for i in range(1,300):
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    url = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article[2]/div[1]/div/div/div/a')
    for i in url:
        urlist.append(i.get_attribute('href'))
        print(len(urlist))
    time.sleep(1)
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

driver.quit()
len(pd.Series(urlist).unique())


# 사진 저장
word = '해시태그 이름'
urlist = list(pd.Series(urlist).unique())
file = open('사용자 지정 경로/url_해시태그 이름.txt', 'wb')
pickle.dump(urlist, file)
file.close()

head = 0
error = []
tag = {}
com = pd.DataFrame()

for link in urlist:
    try:
        head += 1
        
        driver = webdriver.Chrome("c:/data/chromedriver.exe")
        driver.implicitly_wait(3)
        driver.get(link)
        btn = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div/div[3]')
        click = len(btn.find_elements_by_class_name('Yi5aA '))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for i in range(1,click + 1):
            if i == 1:
                no = '{}_{}'.format(head, i)
                time.sleep(0.5)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                img = soup.find('img', class_ = 'FFVAD')
                tag[no] = img.get('alt')
                req.urlretrieve(img['src'], '사용자 지정 경로/{}/{}.jpg'.format(word, no))
                driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div/div[2]/button').click()
            elif (i > 1) and (i < click):
                no = '{}_{}'.format(head,i)
                time.sleep(0.5)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                img = soup.find_all('img', class_ = 'FFVAD')[1]
                tag[no] = img.get('alt')
                req.urlretrieve(img['src'], '사용자 지정 경로/{}/{}.jpg'.format(word, no))
                driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div/div[2]/button[2]').click()
            else:
                no = '{}_{}'.format(head,i)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                img = soup.find_all('img', class_ = 'FFVAD')[-1]
                tag[no] = img.get('alt')
                req.urlretrieve(img['src'], '사용자 지정 경로/{}/{}.jpg'.format(word, no))
                print(head)
                driver.quit()

            ### 댓글, 해시태그 ###
#        n_comment = int([j for i in re.findall('댓글 \d+,*\d*', driver.find_element_by_xpath('/html/head/meta[8]').get_attribute('content')) for j in re.findall(' \d+,*\d*', i)][0].replace(',', ''))
#
#        n_com_comment = sum([int(j) for i in soup.select('.EizgU') for j in re.findall('\d+', i.get_text())])
#
#        cn = 0
#        while True:
#            html = driver.page_source
#            soup = BeautifulSoup(html, 'html.parser')
#            n_comment = int([j for i in re.findall('댓글 \d+,*\d*', driver.find_element_by_xpath('/html/head/meta[8]').get_attribute('content')) for j in re.findall(' \d+,*\d*', i)][0].replace(',', ''))
#            n_com_comment = sum([int(j) for i in soup.select('.EizgU') for j in re.findall('\d+', i.get_text())])
#            if (n_comment - n_com_comment) // 12 - cn > 1:
#                cn += 1
#                driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li/div/button').click()
#                print((n_comment - n_com_comment) // 12 - cn)
#            else:
#                break
#
#        post = [i.get_text() for i in soup.select('#react-root > section > main > div > div > article > div.eo2As > div.EtaWk > ul > div > li > div > div > div.C4VMK > span > a')]
#
#        hash = [j for i in post if len(re.findall('#\w+',i)) != 0 for j in re.findall('#\w+',i)]
#
#        comment = [i.get_text() for i in soup.select('#react-root > section > main > div > div > article > div.eo2As > div.EtaWk > ul > ul > div > li > div > div > div.C4VMK > span')]
#
#        for i in comment:
#            if len(re.findall('#\w+', i)) != 0:
#                for j in re.findall('#\w+', i):
#                    hash.append(j)
#        comment = [re.sub('#\w+', '', i) for i in comment]
#        comment = [re.sub('@\w+\.*\_*\.*\_*\w+\s*', '', i) for i in comment]
#        comment = [re.sub('\W', ' ', i) for i in comment]
#        comment = [re.sub('\s{2,}', ' ', i) for i in comment]
#        comment = [i.strip() for i in comment if len(i) >= 2]
#        df = pd.DataFrame({'head' : head, 'hash' : [hash], 'comment' : [comment]})
#        com = com.append(df)
    except:
        error.append(link)
        tag[head] = 'error'
        print(head, link)
        driver.quit()


