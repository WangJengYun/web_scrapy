import requests
from lxml import etree
import  json
import pandas as pd
import time
from selenium import  webdriver
from selenium.webdriver.support.wait import WebDriverWait
import random
import webbrowser
from selenium.webdriver.firefox.options import Options
#------------------------------------------------------------
def parse_url(url):
    rt = requests.get('http://localhost:8050/render.html',
             params={'url': url, 'wait': 5})
    return(rt)
#-------------------------------------------------------------    
def request_view(response):
    base_url = '<head><base href="{0:s}">'.format(response.url)
    base_url = base_url.encode()
    content = response.content.replace(b'<head>',base_url)
    with open('/home/cloud/tmp.html','wb') as html_file:
        html_file.write(content)
    webbrowser.open_new_tab('/home/cloud/tmp.html')


url =  'https://shopee.tw'
rt = parse_url(url)
et = etree.HTML(rt.text)
category_href = et.xpath('//a[@class="home-category-list__category-grid"]/@href')
category_urls = [url+i for i in category_href]
category_names = et.xpath('//a[@class="home-category-list__category-grid"]//div[@class="_1i1e23"]//text()')
category_json = [{'category_name' : i , 'category_url' : j} for i,j in zip(category_names,category_urls)]

brand_url_json = []
for category_dict in category_json :
    category_url = category_dict['category_url']
    category_name = category_dict['category_name']
    rt = parse_url(category_url) 
    et = etree.HTML(rt.text)
    brand_href = et.xpath('//a[@class="ofs-carousel__shop-cover-image"]/@href')
    brand_urls = [url+i for i in brand_href]
    category_names = [category_name for i in range(len(brand_urls))]
    brand_temp = [{'category_name' : i , 'brand_url' : j} \
                        for i,j in zip(category_names,brand_urls)]
    brand_url_json.extend(brand_temp)
    print(category_name,':',len(brand_urls))

#len(brand_url_json)

num  = 0 
fault_url = []
brand_json = []
for brand_dict in brand_url_json :
    try:
        brand_url =  brand_dict['brand_url']
        category_name = brand_dict['category_name']
        rt = parse_url(brand_url) 
        et = etree.HTML(rt.text)
        brand_name = et.xpath('//*[contains(@class,"portrait-name")]/text()|//*[contains(@class,"portrait__name")]/text()')[0]
        brand_temp = {'category_name':category_name,'brand_name':brand_name}
        brand_json.append(brand_temp)
    except:
        print('fault :',brand_url )
        fault_url.append( brand_url)
    num +=1
    time.sleep(3)
    print(category_name,':',brand_name ,' ',num)
    