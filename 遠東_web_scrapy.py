import requests 
from  bs4 import BeautifulSoup
import time
import pandas as pd

url_1 = 'https://www.feds.com.tw/32'

rt = requests.get(url_1)
soup = BeautifulSoup(rt.text,'lxml')
level_1 = soup.select('ul[class="location-list"]')
level_1_1 = level_1[0].find_all('a')
location_url = ['https://www.feds.com.tw'+level_1_1[i]['href']+'/MallInfo?tab=floor' for i in range(len(level_1_1)-1)]
location_names = [level_1_1[i].text for i in range(len(level_1_1)-1)]
location_data = pd.DataFrame({'location_names': location_names,'location_url':location_url})
empty_data = pd.DataFrame(columns = ['category','subcategory','item'])
for l in range(location_data.shape[0]):
    url_2 = location_data['location_url'][l]
    rt = requests.get(url_2)
    soup = BeautifulSoup(rt.text,'lxml')
    level_2 = soup.select('div[class="floor-info-wrap b-text-center"]')
    floor_names = [level_2[i].select('h3[class="floor-title"]')[0].text for i in range(len(level_2))]
    for j in range(len(floor_names)) :#j=0
        level_3 = level_2[j].select('div[class="m-accordion"]')
        for k in range(len(level_3)):#k=0
            subcategory = level_3[k].find_all('button')[0].text.strip()
            level_4 = level_3[k].select('li[class="list"]')
            item = [level_4[i].text for i in range(len(level_4))]
            current_data = pd.DataFrame({'location':location_data['location_names'][l],'category':floor_names[j],'subcategory':subcategory,'item':item})
            empty_data = pd.concat([empty_data,current_data])

empty_data.to_csv('/home/cloud/遠東_品牌',index=False)