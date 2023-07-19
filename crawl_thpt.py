
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from tqdm import tqdm
# import re
# import time
# import numpy as np


# subject = ["SBD","Sở GD&ĐT",'Toán','Văn','Lí','Hóa','Sinh','Sử','Địa','Ngoại ngữ','GDCD']
# data = []
# for tinh in range(63,64,1):
#     for i in tqdm(range(1,999999)):
#         SBD = f'{tinh*1000000+i:08d}'
#         # if tinh <10:
#         #     SBD = f'0{tinh*1000000+i}'
#         # else:
#         #     SBD = f'{tinh*1000000+i}'
#         # print(SBD)
#         try:
#             url = f'https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/2023/{SBD}.html'
#             response = requests.get(url)
#             html_content = response.content
#             soup = BeautifulSoup(html_content, 'html.parser')

#             table_cells = soup.find('table').find_all('tr')
#             # row_data = [cell.text.strip() for cell in table_cells]
#             diem = [None]*11
#             diem[0] = SBD
#             diem[1] = soup.find(class_="edu-institution").text
#             for cell in table_cells:
#                 row_data = cell.find_all('td')
#                 for j in range(0,len(row_data)-1,2):
#                     diem[subject.index(row_data[j].text)] = row_data[j+1].text
#             # print(diem)
#             data.append(diem)

#         except:
#             break
# df = pd.DataFrame(data)
# # print(data)
# df.columns = subject
# print(df)


import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

subject = ["SBD", "Sở GD&ĐT", 'Toán', 'Văn', 'Lí', 'Hóa', 'Sinh', 'Sử', 'Địa', 'Ngoại ngữ', 'GDCD']
data = []

def fetch_data(tinh, i):
    SBD = f'{tinh*1000000+i:08d}'  # Format SBD with leading zeros
    try:
        url = f'https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/2023/{SBD}.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table_cells = soup.find('table').find_all('tr')
        diem = [None]*11
        diem[0] = SBD
        diem[1] = soup.find(class_="edu-institution").text
        for cell in table_cells:
            row_data = cell.find_all('td')
            for j in range(0, len(row_data)-1, 2):
                diem[subject.index(row_data[j].text)] = row_data[j+1].text
        return diem
    except Exception as e:
        pass

with ThreadPoolExecutor(max_workers=1000) as executor:
    futures = []
    for tinh in range(63,64):
        for i in tqdm(range(1, 200000)):
            futures.append(executor.submit(fetch_data, tinh, i))
    results = [future.result() for future in futures]

data = [result for result in results if result is not None]

df = pd.DataFrame(data)
df.columns = subject
print(df)
