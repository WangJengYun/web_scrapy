import requests
from pyquery import PyQuery as pq
import pandas as pd
import time

url = 'https://www.skm.com.tw/'
rt = requests.get(url)
doc = pq(rt.text)
level_1 = doc('td[class="locate"] li[class="skm-col s3 m3 l3"] a')

locaton_url = [url + i.attr('href').replace('BranchPagesHome','BranchBrand') for i in level_1.items()]
locaton_names = [i.text() for i in level_1.items()]
locaion_data = pd.DataFrame({'locaton_names':locaton_names,'locaton_url':locaton_url})

L_C_S_I_Data = pd.DataFrame(columns = ['locaton_name','category_name','subcategory_name','item'])
for l in range(locaion_data.shape[0]): #l=3
    time.sleep(2)
    print('location :',l,':',locaton_names[l] )
    url_2 = locaton_url[l]
    rt = requests.get(url_2)
    doc = pq(rt.text)
    level_2 = doc('div[ng-class="{ \'active\': GlobalNavBranchBrands == \'categories\' }"]  a')
    category_url = ['https://www.skm.com.tw/BranchPages/'+i.attr('href') for i in level_2.items()][1:]
    category_names = [i.text() for i in level_2.items()][1:]
    #category_data = pd.DataFrame({'category_names':category_names,'category_url ':category_url })
    C_S_I_data = pd.DataFrame(columns = ['category_name','subcategory_name','item'])
    for j in range(len(category_names)) : #j=2
        time.sleep(5)
        print('category :',j,':',category_names[j])
        time.sleep(5)
        subcategory_Data = subcategory_items(category_url[j])
        subcategory_Data['category_name'] = category_names[j]
        C_S_I_data = pd.concat([C_S_I_data,subcategory_Data])    
    C_S_I_data['locaton_name']  =  locaton_names [l]
    L_C_S_I_Data = pd.concat([L_C_S_I_Data,C_S_I_data])
    
L_C_S_I_Data.to_csv('/home/cloud/新光三越_品牌.csv',index=False)

def subcategory_items(url) : 
    url_3 = url
    rt = requests.get(url_3)
    doc = pq(rt.text)
    level_3 = doc('div[class="skm-container "] li:not(.active) a')
    subcategory_names = [i.text() for i in level_3.items()] 
    subcategory_url = ['https://www.skm.com.tw/BranchPages/'+i.attr('href') for i in level_3.items()]
    current_Data = pd.DataFrame(columns = ['subcategory_name','item'])
    for k in range(len(subcategory_names)):
        print('page :',k,':',subcategory_names[k])
        #page = 0
        time.sleep(15)
        current_url = subcategory_url[k]
        #current_url  = 'https://www.skm.com.tw/BranchPages/BranchBrand?fPages=5&UUID=4e76109e-f0db-4198-ab3e-63264964844e&dShopUUID=%%&shopfloor=%%&BrandClass=fca357dd-302d-4748-93fd-92dda99b6bd6&sBrandClass=74d51528-baf8-4fe4-a222-581cde7a284b'
        next_url = ''
        items = []
        while True :
            rt = requests.get(current_url)
            doc = pq(rt.text)
            level_4 = doc('div[class="thumbnail"]')
            items.extend([i.text() for i in level_4.items()])
            level_5 = doc('ul[class="skm-ul skm-ul-paging"] li:last-child a')
            next_url = ['https://www.skm.com.tw/BranchPages/' + i.attr('href') for i in level_5.items()]   
            #page += 1 ; print(page)
            if current_url == next_url[0]:
                break 
            else :
                current_url = next_url[0]
        subcategory_Data = pd.DataFrame({'subcategory_name':subcategory_names[k],'item':items})
        current_Data = pd.concat([current_Data,subcategory_Data])
    return current_Data 



