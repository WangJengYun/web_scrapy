import requests 
from  bs4 import BeautifulSoup
import time
import pandas as pd

url = 'https://www.breezecenter.com/zh_tw'
rt = requests.get(url)
soup = BeautifulSoup(rt.text,'lxml')
level_1 = soup.select('div[class="team-caption"] a')

location = [level_1[i].text.strip() for i in range(len(level_1)) if (i+1)%3 == 1]
location_url = [level_1[i]['href'] for i in range(len(level_1)) if (i+1)%3 == 1]

location_data = pd.DataFrame({'location':location,'location_url':location_url})

current_data = pd.DataFrame(columns=['locaion','brank_names','brank_urls'])
for i in range(location_data.shape[0]):#i=1
    url = location_data['location_url'][i]
    rt = requests.get(url)
    soup = BeautifulSoup(rt.text,'lxml')
    level_2 = soup.select('div[id="portfolioList"] a')
    brank_urls = [level_2[i]['href'] for  i in range(len(level_2))]
    brank_names = [level_2[i].text.strip() for  i in range(len(level_2))]
    brank_Data = pd.DataFrame({'locaion':location_data['location'][i],'brank_names':brank_names,'brank_urls':brank_urls})
    current_data = pd.concat([current_data,brank_Data])

j=0
brank_label = []
for i in current_data['brank_urls']:
    #rt = requests.get('https://www.breezecenter.com/zh_tw/brands/1292')
    time.sleep(10)
    rt = requests.get(i)
    soup = BeautifulSoup(rt.text,'lxml')
    temp2 = soup.select('div[class="text-center"] span')
    brank_labels = [temp2[i].text.strip() for i in range(len(temp2))]
    brank_label.append(','.join(brank_labels))
    j += 1
    print(j)

current_data['category'] = brank_label

current_dat.to_csv('/home/cloud/微風_品牌',index=False)
