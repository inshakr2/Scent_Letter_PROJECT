# -*- coding: utf-8 -*-

import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd
import numpy as np
import os
import time
import datetime

'''
새로 접속시
'''
file = open('사용자 지정 경로/group_list.txt','rb')     
group = pickle.load(file)
file.close()
len(group)
group.keys()

url = []
for i in range(3, 12):
    for j in group[i]:
        url.append(j)
len(url)

main_perf = pd.DataFrame()
error = []

'''
끊고 다시 접속시
file = open('사용자 지정 경로/main_perf.txt','rb')     
main_perf = pickle.load(file)
file.close()
len(main_perf)

file = open('사용자 지정 경로/error.txt','rb')     
error = pickle.load(file)
file.close()
len(error)

start = datetime.datetime.now()
torexe = os.popen(r'사용자 지정 경로\Tor Browser\Browser\TorBrowser\Tor\tor.exe')
profile = webdriver.FirefoxProfile()
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9050)
profile.set_preference("network.proxy.socks_remote_dns", False)
profile.update_preferences()
driver = webdriver.Firefox(firefox_profile= profile, executable_path=r'사용자 지정 경로\geckodriver.exe')
driver.implicitly_wait(3)
driver.get("http://check.torproject.org")
print(driver.find_element_by_xpath('/html/body/div[2]/p[1]/strong').text)
'''
u = 10
for u in range(len(main_perf), len(url)):
    try:
        if u % 20 == 0:
            start = datetime.datetime.now()
            torexe = os.popen(r'사용자 지정 경로\Tor Browser\Browser\TorBrowser\Tor\tor.exe')
            profile = webdriver.FirefoxProfile()
            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.socks', '127.0.0.1')
            profile.set_preference('network.proxy.socks_port', 9050)
            profile.set_preference("network.proxy.socks_remote_dns", False)
            profile.update_preferences()
            driver = webdriver.Firefox(firefox_profile= profile, executable_path=r'사용자 지정 경로\geckodriver.exe')
            driver.implicitly_wait(3)
            driver.get("http://check.torproject.org")
            print(driver.find_element_by_xpath('/html/body/div[2]/p[1]/strong').text)
            
        end = datetime.datetime.now()
        driver.get('http://www.fragrantica.com' + url[u])
        driver.implicitly_wait(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        if u % 20 == 19:
            driver.quit()
        
        # 향수 이름
        name = soup.select_one('#col1 > div > div > h1 > span').get_text()
                               
        # 향수 브랜드
        brand = soup.select_one('#p2 > div.subTtl > a').get_text()
    
        # 향수 계열
        group = soup.select_one('#col1 > div > div > p > span:nth-child(2) > span:nth-child(1)').text
        
        # main accords
        a = []
        for i in soup.select('#prettyPhotoGallery > div:nth-child(1) > div > span'):
            a.append(i.get_text())
        b = []
        for i in soup.select('#prettyPhotoGallery > div:nth-child(1) > div > div'):
            b.append(int(re.search('\d+', i.get('style')).group()))
        accords = {}
        for i in range(len(b)):
            accords[a[i+1]] = b[i]
    
        # main notes according to your votes
        note = {}
        for i in soup.select_one('#userMainNotes').get('title').split(';'):
            if i == '':
                pass
            else:
                temp = i.split(':')
                note[int(temp[0])] = int(temp[1])

        # perfume pyramid
        r_note = {}
        for i in soup.select('.effect6 > div > p'):
            a = []
            for j in i.select('span'):
                a.append(int(j.get('title')))
            r_note[i.get_text(strip = True)] = a
        del r_note['drag slider to vote']
    
        a = []
        for i in soup.select('#diagramresult > div'):
            a.append(i.get('id').replace('cls', '').rstrip('D'))
        b = []
        for i in soup.select('#diagramresult > div'):
            b.append(int(re.search('\d+', i.get('style').split(';')[1]).group()))
        vote = {}
        for i in range(len(b)):
            vote[a[i]] = b[i]
        
        # total people voted
        n_vote = int(soup.select_one('#peopleD').text)
    
        # longevity
        a = []
        for i in soup.select('.divLong > table > tbody > tr > td:nth-child(1)'):
            a.append(i.get_text(strip = True))
        b = []
        for i in soup.select('.divLong > table > tbody > tr > .ndSum'):
            b.append(int(i.get_text(strip = True)))
        longevity = {}
        for i in range(len(b)):
            longevity[a[i]] = b[i]
    
        # sillage
        a = []
        for i in soup.select('.voteLS > tbody > tr > td > table > tbody > tr > td:nth-child(1)'):
            a.append(i.get_text())
        b = []
        for i in soup.select('.voteLS > tbody > tr > td > table > tbody > tr > .ndSum'):
            b.append(int(i.get_text(strip = True)))
        sillage = {}
        for i in range(len(b)):
            sillage[a[i]] = b[i]
    
        perf = pd.DataFrame({'name':name, 'brand':brand, 'group':group, 
                             'accords':[accords], 'note':[note], 'r_note':[r_note],
                             'vote':[vote], 'n_vote':n_vote, 'longevity':[longevity],
                             'sillage':[sillage]})
        
        main_perf = main_perf.append(perf, ignore_index=True)
        print(u, end - start)
#        file = open('사용자 지정 경로/main_perf.txt', 'wb')
#        pickle.dump(main_perf, file)
#        file.close()
        
    except:
        print(u, '오류', 300 - (end - start).seconds)
        perf = pd.DataFrame({'name':np.nan, 'brand':np.nan, 'group':np.nan, 
                             'accords':np.nan, 'note':np.nan, 'r_note':np.nan,
                             'vote':np.nan, 'n_vote':np.nan, 'longevity':np.nan,
                             'sillage':np.nan},index = [u])
        main_perf = main_perf.append(perf, ignore_index=True)
        file = open('사용자 지정 경로/main_perf.txt', 'wb')
        pickle.dump(main_perf, file)
        file.close()
        error.append(u)
        file = open('사용자 지정 경로/error.txt', 'wb')
        pickle.dump(error, file)
        file.close()
        driver.quit()
        if (300 - (end - start).seconds) > 0:
            time.sleep(300 - (end - start).seconds)
        else:
            time.sleep(60)
        start = datetime.datetime.now()
        torexe = os.popen(r'사용자 지정 경로\Tor Browser\Browser\TorBrowser\Tor\tor.exe')
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9050)
        profile.set_preference("network.proxy.socks_remote_dns", False)
        profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile= profile, executable_path=r'사용자 지정 경로\geckodriver.exe')
        driver.implicitly_wait(3)
        driver.get("http://check.torproject.org")
        print(driver.find_element_by_xpath('/html/body/div[2]/p[1]/strong').text)


# error 번호 다시 수행
#file = open('사용자 지정 경로/group_list.txt','rb')     
#group = pickle.load(file)
#file.close()
#len(group)
#group.keys()
#
#url = []
#for i in range(3, 12):
#    for j in group[i]:
#        url.append(j)
#len(url)
#
#file = open('사용자 지정 경로/main_perf.txt','rb')     
#main_perf = pickle.load(file)
#file.close()
#len(main_perf)
#
#file = open('사용자 지정 경로/error.txt','rb')     
#error = pickle.load(file)
#file.close()
#len(error)
#
#cn = 0
#error2 = []
#for u in error:
#    try:
#        if cn % 20 == 0:
#            start = datetime.datetime.now()
#            torexe = os.popen(r'사용자 지정 경로\Tor Browser\Browser\TorBrowser\Tor\tor.exe')
#            profile = webdriver.FirefoxProfile()
#            profile.set_preference('network.proxy.type', 1)
#            profile.set_preference('network.proxy.socks', '127.0.0.1')
#            profile.set_preference('network.proxy.socks_port', 9050)
#            profile.set_preference("network.proxy.socks_remote_dns", False)
#            profile.update_preferences()
#            driver = webdriver.Firefox(firefox_profile= profile, executable_path=r'사용자 지정 경로\geckodriver.exe')
#            driver.implicitly_wait(3)
#            driver.get("http://check.torproject.org")
#            print(driver.find_element_by_xpath('/html/body/div[2]/p[1]/strong').text)
#            
#        end = datetime.datetime.now()
#        driver.get('http://www.fragrantica.com' + url[u])
#        driver.implicitly_wait(1)
#        html = driver.page_source
#        soup = BeautifulSoup(html, 'html.parser')
#        print(1)
#        
#        if cn % 20 == 19:
#            driver.quit()
#        
#        name = soup.select_one('#col1 > div > div > h1 > span').get_text()
#        brand = soup.select_one('#p2 > div.subTtl > a').get_text()
#    
#        group = soup.select_one('#col1 > div > div > p > span:nth-child(2) > span:nth-child(1) > a').text
#        print(2)
#        
#        a = []
#        for i in soup.select('#prettyPhotoGallery > div:nth-child(1) > div > span'):
#            a.append(i.get_text())
#        b = []
#        for i in soup.select('#prettyPhotoGallery > div:nth-child(1) > div > div'):
#            b.append(int(re.search('\d+', i.get('style')).group()))
#        accords = {}
#        for i in range(len(b)):
#            accords[a[i+1]] = b[i]
#        print(3)
#        
#        note = {}
#        for i in soup.select_one('#userMainNotes').get('title').split(';'):
#            if i == '':
#                pass
#            else:
#                temp = i.split(':')
#                note[int(temp[0])] = int(temp[1])
#        print(4)
#
#        r_note = {}
#        for i in soup.select('.effect6 > div > p'):
#            a = []
#            for j in i.select('span'):
#                a.append(int(j.get('title')))
#            r_note[i.get_text(strip = True)] = a
#        del r_note['drag slider to vote']
#        print(5)
#        
#        a = []
#        for i in soup.select('#diagramresult > div'):
#            a.append(i.get('id').replace('cls', '').rstrip('D'))
#        b = []
#        for i in soup.select('#diagramresult > div'):
#            b.append(int(re.search('\d+', i.get('style').split(';')[1]).group()))
#        vote = {}
#        for i in range(len(b)):
#            vote[a[i]] = b[i]
#        print(6)
#        
#        n_vote = int(soup.select_one('#peopleD').text)
#    
#        a = []
#        for i in soup.select('.divLong > table > tbody > tr > td:nth-child(1)'):
#            a.append(i.get_text(strip = True))
#        b = []
#        for i in soup.select('.divLong > table > tbody > tr > .ndSum'):
#            b.append(int(i.get_text(strip = True)))
#        longevity = {}
#        for i in range(len(b)):
#            longevity[a[i]] = b[i]
#        print(7)
#    
#        a = []
#        for i in soup.select('.voteLS > tbody > tr > td > table > tbody > tr > td:nth-child(1)'):
#            a.append(i.get_text())
#        b = []
#        for i in soup.select('.voteLS > tbody > tr > td > table > tbody > tr > .ndSum'):
#            b.append(int(i.get_text(strip = True)))
#        sillage = {}
#        for i in range(len(b)):
#            sillage[a[i]] = b[i]
#        print(8)
#        
#        main_perf.iloc[u, :] = [name, brand, group, [accords], [note], [r_note],
#                                [vote], n_vote, [longevity], [sillage]]
#        print(9)
#        print(u, end - start)
#        file = open('사용자 지정 경로/main_perf.txt', 'wb')
#        pickle.dump(main_perf, file)
#        file.close()
#        cn += 1
#        
#    except:
#        print(u, '오류', 300 - (end - start).seconds)
#        perf = pd.DataFrame({'name':np.nan, 'brand':np.nan, 'group':np.nan, 
#                             'accords':np.nan, 'note':np.nan, 'r_note':np.nan,
#                             'vote':np.nan, 'n_vote':np.nan, 'longevity':np.nan,
#                             'sillage':np.nan},index = [u])
#        main_perf.iloc[u, :] = np.nan
#        file = open('사용자 지정 경로/main_perf.txt', 'wb')
#        pickle.dump(main_perf, file)
#        file.close()
#        error2.append(u)
#        file = open('사용자 지정 경로/error2.txt', 'wb')
#        pickle.dump(error2, file)
#        file.close()
#        driver.quit()
#        if (300 - (end - start).seconds) > 0:
#            time.sleep(300 - (end - start).seconds)
#        else:
#            time.sleep(60)
#        start = datetime.datetime.now()
#        torexe = os.popen(r'사용자 지정 경로\Tor Browser\Browser\TorBrowser\Tor\tor.exe')
#        profile = webdriver.FirefoxProfile()
#        profile.set_preference('network.proxy.type', 1)
#        profile.set_preference('network.proxy.socks', '127.0.0.1')
#        profile.set_preference('network.proxy.socks_port', 9050)
#        profile.set_preference("network.proxy.socks_remote_dns", False)
#        profile.update_preferences()
#        driver = webdriver.Firefox(firefox_profile= profile, executable_path=r'사용자 지정 경로\geckodriver.exe')
#        driver.implicitly_wait(3)
#        driver.get("http://check.torproject.org")
#        print(driver.find_element_by_xpath('/html/body/div[2]/p[1]/strong').text)