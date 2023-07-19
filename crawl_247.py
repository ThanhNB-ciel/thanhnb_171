import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from tqdm import tqdm
import numpy as np

with open("link_topdua.txt", 'r') as file:
    urls = file.readlines()
    
    
# lấy ra từng link
links = []
for i in urls:
    i = i.replace("\n", "")
    if '2020' in i or '2021' in i :
        continue
    else:
        links.append(f'https://hoidap247.com{i}')
# for qua từng link để lấy data 
l = []
for link in tqdm(links):
    data_list = [] 
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find("div", {"id": "contentPost"})
    _date = data.find('time')
    # break

    tables = data.find_all("table")
    # print(table)
    for table in tables:
        for row in table.find_all("tr"):
            try:
                data_row = []
                for cell in row.find_all("td"):
                    data_row.append(cell.text.strip())
                if len(data_row) > 1:
                    data_list.append(data_row)
                    print(len(date_row))
            except:
                pass
    df = pd.DataFrame(data_list[1:], columns=data_list[0])
    # print(df)
    df["date"] = int(_date["datetime"])
    df['date'] = pd.to_datetime(df['date'],unit ='ms' ).dt.strftime('%m-%Y')
    df['date'] = pd.to_datetime(df['date'], format='%m-%Y')
    df['date'] = df['date'] - pd.DateOffset(months=1)
    df['date'] = df['date'].dt.strftime('%m-%Y')
    l.append(df)
    
 

dfx = pd.concat(l)
dfx = dfx.iloc[:, 0:7]
# dfx.to_csv('df_247.csv')
print(dfx)

