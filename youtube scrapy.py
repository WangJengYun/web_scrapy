import requests
from lxml import etree
import re
import json
import shutil
from urllib.parse import parse_qs
import os 
import time 

target_url = 'https://www.youtube.com/watch?v=pzzQ9rrVPvM&list=PL1f_B9coMEeCiJeQN_w00Irur8YnNzfPX'
folder_path = 'D:\\sharing_file\\AIA人工智慧課程\\CNN\\vedio\\part7\\'

os.makedirs(folder_path, exist_ok=True)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36', 'Connection':'keep-alive'}

# rt_level_1
rt_level_1 = requests.get(target_url)
et = etree.HTML(rt_level_1.text)
vedio_list_name = [i.strip() for i in et.xpath('//h4[@class="yt-ui-ellipsis yt-ui-ellipsis-2"]//text()')]
vedio_list_path = et.xpath('//div[@class="playlist-videos-container yt-scrollbar-dark yt-scrollbar"]//a/@href')
vedio_urls = ['https://www.youtube.com'+s for s in vedio_list_path]

iteration = range(len(vedio_list_name))
times = 0
while(bool(iteration)):
    
    fail_vedio  = []
    for index in iteration :
        # rt_level_2
        vedio_url,vedio_name = vedio_urls[index],vedio_list_name[index]
        rt_level_2 = requests.get(vedio_url)
        et = etree.HTML(rt_level_2.text)
    
        m = re.search('"args":{(.*?)},', rt_level_2.text)
        m = re.search('"url_encoded_fmt_stream_map":"(.*?)"', rt_level_2.text)
        m1 = m.group(0).replace('\\u0026','&')
        m2 = re.search(':"(.*?)"',m1).group(1).split('&')
        m3 = [s for s  in m2 if s.__contains__('url')]
        url = parse_qs(m3[0])['url'][0]
        # rt_level_3
        rt_level_3 = requests.get(url,stream = True,headers = headers)
        time.sleep(times)
        saving_path  = folder_path  +'%s.mp4'%(vedio_name)
        with open(saving_path,'wb') as file:
            shutil.copyfileobj(rt_level_3.raw,file)
        time.sleep(times)
        statinfo = os.stat(saving_path)
        if statinfo.st_size == 0:
            fail_vedio.append(index)
        print('-----finish %s-----'%(vedio_name))
    iteration = fail_vedio
    print(iteration)
    times += 3 