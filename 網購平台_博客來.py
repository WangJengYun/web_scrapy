import requests
from lxml import etree
import  json
import pandas as pd
import time
from selenium import  webdriver
from selenium.webdriver.support.wait import WebDriverWait
import random
#---------------------------------------------------------------------
# before requests ,setting up 
#proxies = {'http' : '218.86.128.100:8118'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36', 'Connection':'keep-alive'}
#--------------------------------------------------------------------------
def browser_start():    
    port = [8080,4444,4445,4446,8081,8945,8745]
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.http_port", random.choice(port))
    browser = webdriver.Firefox(executable_path = '/home/cloud/下載/geckodriver',firefox_profile=profile)
    return(browser)
#---------------------------------------------------------------------
def dict_recommender_category(list_snippet_HTML):
    for component in list_snippet_HTML:
        dict_empty = dict()
        dict_empty['href'] = 'http://'+component.attrib['href'][2:]
        dict_empty['rc_name'] = component.text.strip()
        yield dict_empty
# ----------------------------------
def product_info(et,category):
    products = et.xpath('//ul[@class="cntli_001 cntli_001m clearfix"]/li[not(@atrri) and not(@class="hr_a")]')        
    for product in products:
        dict_empty = dict()
        dict_empty['category'] = category
        dict_empty['product'] = product.xpath('./h4/a/text()')[0]
        dict_empty['price'] = product.xpath('./ul[@class="price"]/li/strong/b/text()')[0]
        dict_empty['rank'] = product.xpath('./h3[@class="place"]/text()')[0]
        yield dict_empty
# ----------------------------------
def brand_info(et,category):
    level_2 = et.xpath('//ul[@class="cntli_menu_002"]/li');o = 0      
    for component_1 in level_2: #component_1 = level_2[6]
        level_2_category_name = component_1.xpath('./h4/span/a/text()')[0]
        level_2_subcategory_names = component_1.xpath('./ul/li[not(@class)]/span/a/text()')
        level_2_subcategory_urls = component_1.xpath('./ul/li[not(@class)]/span/a/@href')
        length_subcategory = len(level_2_subcategory_names)
        o+=1;print(o,':',level_2_category_name)
        if level_2_category_name == '18禁情趣商品':
            continue
        is_start_webdriver = False
        method = 'requests'
        for i in range(length_subcategory): 
            url = level_2_subcategory_urls[i]
            subcategory_name = level_2_subcategory_names[i]
            print(url)
            if subcategory_name == '限制級遊戲':
                continue
            if method == 'requests':
                try:
                    rt = requests.get(url,timeout=10,headers = headers)
                    et = etree.HTML(rt.text)
                    print(rt)
                    print(et)
                    if et is None :
                        method = 'selenium'
                except:
                    if et is None :
                        method = 'selenium'            
            if method == 'selenium':
                if is_start_webdriver == False:
                    is_start_webdriver = True
                    browser = browser_start()                
                try: 
                    #url = 'https://www.books.com.tw/web/sys_botm/watch/2604?loc=P_001_2_024'
                    browser.get(url)
                    browser.implicitly_wait(10)
                    rt = browser.page_source
                    et = etree.HTML(rt)
                    print(et)
                    time.sleep(2)
                    #raise MaxRetryError
                except:
                    browser.close()
                    is_start_webdriver = False
                    et = None
                    while et is None :
                        print('最後防線')
                        browser = browser_start() 
                        time.sleep(60)
                        browser.get(url)
                        rt = browser.page_source
                        et = etree.HTML(rt)
                        print(et)
                        browser.close()  
            brands = et.xpath('//ul[@class="clearfix"]/li//a/text()')
            yield from  loop_for_brand(category,level_2_category_name,subcategory_name,brands)
            time.sleep(1)
            print(i,':',subcategory_name)
        if is_start_webdriver == True:
            browser.close()            
# ----------------------------------           
def loop_for_brand(category,level_2_category_name,subcategory_name,brands):
    for brand in brands :
        dict_empty = dict()
        if subcategory_name in brands :
            brand = subcategory_name
            subcategory_name =  level_2_category_name
            dict_empty['type'] = category
            dict_empty['category'] = level_2_category_name
            dict_empty['subcategory'] = subcategory_name
            dict_empty['brand'] = brand
            yield dict_empty
            break
        else : 
            dict_empty['type'] = category
            dict_empty['category'] = level_2_category_name
            dict_empty['subcategory'] = subcategory_name
            dict_empty['brand'] = brand
            yield dict_empty

rt = requests.get("https://www.books.com.tw/web/sys_hourstop/home?loc=act_menu_0_001",timeout=10,headers = headers)
et = etree.HTML(rt.text)
recommender_category = et.xpath('//li[@class="open "][last()]//a')
DF_list_dict_1 = list(dict_recommender_category(recommender_category))

DF_list_dict_3_1 = []
DF_list_dict_3_2 = []
for component in DF_list_dict_1:#component = DF_list_dict_1[1]
    url  = component['href']
    rc_name = component['rc_name']
    et = None
    try :
        rt = requests.get(url,timeout = 10)
        et = etree.HTML(rt.text)
        #print(url)
        if et is None :
            raise IOError
    except:
        browser = browser_start()  
        browser.get(url)
        rt = browser.page_source
        et = etree.HTML(rt)
        browser.close()
    print(et)
    DF_list_dict_2_1 = list(product_info(et,rc_name))
    DF_list_dict_2_2 = list(brand_info(et,rc_name))
    print(len(DF_list_dict_2_2))
    DF_list_dict_3_1.extend(DF_list_dict_2_1)
    DF_list_dict_3_2.extend(DF_list_dict_2_2)
    time.sleep(300)
    print(rc_name)
    
DF_1 = pd.DataFrame(DF_list_dict_3_1)
DF_2 = pd.DataFrame(DF_list_dict_3_2)

DF_1.to_csv('/home/cloud/博客來_top100.csv',index=False)
DF_2.to_csv('/home/cloud/博客來_品牌.csv',index=False)