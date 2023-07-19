import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
import time
import numpy as np

#Lazi bảng nhận thưởng
link_lazi = []
output = []
for num in range(0,41,10):
    url = f'https://lazi.vn/event?start={num}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    lazi_links = soup.find_all(class_='nen_trang_full')
    for link in lazi_links:
        try:
            link = link.h2.a.get('href')
            if 'giai-thuong-thang' in link:
                # print(link)
                link_lazi.append(link)
        except:
            pass
for link in tqdm(link_lazi):
    try:
        response=''
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        name = soup.find('div',class_='art_content').find_all('a')

        data = {'username':[],
                'name':[],
                'note':[]}

        for item in name:
            try:
                try:
                    data['name'].append(item.find('span').text)
                except:
                    data['name'].append(item.find('strong').text)
            except:
                data['name'].append(item.text)
            data['username'].append(item.get('href').split('/')[-1])
            data['note'].append(link.rstrip('\n').split('/')[6])

        text = soup.find(class_='art_content').findAll(string=True)
        out = text[:text.index('Hình thức nhận thưởng:')]
        out= list(filter(lambda a: a != ": ", out))
        out= list(filter(lambda a: a != ", ", out))
        out= list(filter(lambda a: len(a) < 110, out))
        data1 = {'name':[],
                'prize':[],
                'top_prize':[],
                'type_prize':[]}
        prize = ''
        top_prize = ''
        type_prize = ''

        for i in out:
            if (re.search(r"(\d|[A-Z])\.\s\w+", i) and i[-1]==':') or i in ['Chuyên mục giải bài tập sẽ có 4 hạng mục tính thưởng riêng như sau:',' Điểm do người đăng bài tập chấm điểm dành cho 2 lời giải đầu tiên của mỗi bài tập.',' Hiệu số lượt thích trừ đi lượt không thích.' '* Giải nhanh:','Top \u200b6 bạn top giải nhanh tháng 10:',' Hiệu số lượt thích trừ đi lượt không thích.','* Giải nhanh:']: #loại giải
                type_prize = i
            elif re.search(r"^([0-9]{2,3}:?)\s\w+", i) or 'đồng' in i or re.search(r"\d+\.[0]{3,5}", i): #giá trị
                prize = i
            elif ("-" in i and i.rstrip()[-1]==':') or ("+" in i and i.rstrip()[-1]==':') or 'giải khuyến khích: ' in i.lower(): #top giải
                top_prize = i
            else:
                data1['name'].append(i)
                data1['prize'].append(prize)
                data1['top_prize'].append(top_prize)
                try:
                    data1['type_prize'].append(type_prize.split(':')[0])
                except: 
                    data1['type_prize'].append(type_prize)
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data)
        
        df2 = df2[~df2['username'].isin(['adminlazi','lazi.vn','statistic','setting_reward','lazi.assistant','chinh-sach-thuong-cho-thanh-vien','chat-truc-tiep-voi-gia-su-lazi-de-hoi-bai-tap','tutor'])]
        df2 = df2.reset_index(drop=True)
        
        df1 = df1[['name','top_prize','type_prize']]
        df1 = df1.dropna(how='all')
        df1 = df1[df1.name.isin(df2.name.values)]
        df1 = df1.reset_index(drop=True)
        
        df = pd.merge(df1,df2,left_index=True,right_index=True)
        # display(df)
        output.append(df)
        time.sleep(3)
    except Exception as e:
        print(e)
        print(link)

output_df = pd.concat(output)
print(output_df.head())
# output_df.to_csv('Lazivv.csv',index=False)