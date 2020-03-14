#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 13:29:32 2019

@author: cloud
"""

import requests as rt
from selenium import  webdriver
from selenium.webdriver.support.wait import WebDriverWait 
import random
import time
from lxml import etree
def browser_start():    
    port = [8080,4444,4445,4446,8081,8945,8745]
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.http_port", random.choice(port))
    browser = webdriver.Firefox(executable_path = '/home/cloud/file/Python_learning/Web crawler/Driver/geckodriver',firefox_profile=profile)
    return(browser)
    
url = 'https://www.youtube.com/watch?v=8JI-8pBft1w'
browser = browser_start()
browser.get(url)
time.sleep(5)

for i in range(40):
    try:
        browser.execute_script("window.scrollTo(0,window.scrollY+500);")
        time.sleep(1)
        print(i)
    except:
        break

time.sleep(2)   
rt = browser.page_source
et = etree.HTML(rt)
print(et)

commend = et.xpath('//yt-formatted-string[@id="content-text"]//text()')
commend = [ i.replace('\ufeff','') for i in  commend]
commend = [ i.replace('\n','') for i in  commend]
len(commend)
 
name = et.xpath('//a/span[@class="style-scope ytd-comment-renderer"]//text()')
name = [ i.replace('\n','').strip() for i in name]
len(name)



commend[0:len(name)]
name[0:len(name)]


import pandas as pd 
data = pd.DataFrame({'name':name[0:len(name)],'commend':commend[0:len(name)]})

data.to_csv('/home/cloud/data.csv')