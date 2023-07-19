from bs4 import BeautifulSoup
import pandas as pd
import requests 

# #Đọc từ file txt
# with open('lazi.txt', 'r') as html_content:
#     # html_content = file.readlines()
#     soup = BeautifulSoup(html_content, 'html.parser')
#     t = 't5_t6'

#Đọc từ html
url = 'https://lazi.vn/statistic'
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')
t = 't6_t7'


table_data = []
header = []
Note = []
tables = soup.find_all('table')  # Adjust the selection criteria if necessary

titles = soup.find_all(class_=['line_height_common','font_h2'])
for title in titles:
    # print(title.text)
    Note.append(title.text)
Note.pop(0)

for table in tables:
    table_rows = table.find_all('tr')
    data = []

    for row in table_rows:
        if row.find('a') != None:
            table_cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in table_cells]
            row_data.append(row.find('a').get('href').split('/')[-1])
            # print('-------------------')
            data.append(row_data)
        else:
            table_cells = row.find_all('th')
            row_data = [cell.text.strip() for cell in table_cells]
            row_data.append('username')
            header.append(row_data)

    table_data.append(data)
count = 0
i = 1
datafr = []
for data in range(len(table_data)):
    try:
        if i ==3:
            count +=3
            i=1
        dfs = pd.DataFrame(table_data[data])
        dfs.columns = header[data]
        dfs['Loai_giai_thuong'] = Note[count].split('.')[1].split(':')[0]
        dfs['Time'] = Note[count+i].split('(')[1].split(')')[0]
        dfs['Time'] = dfs['Time'].str.replace('/','-') 
        dfs['Note'] = t

        # display(dfs)
        datafr.append(dfs)
        i+=1
    except:
        pass
    
for i in range(0,len(datafr)-1,2):
    df = pd.concat([datafr[i],datafr[i+1]])
    df = df.drop(['STT'], axis=1)
    try:
        df = df.drop(['Avatar'], axis=1)
    except:
        pass
    df.to_csv(f'lazi{df.Note[1].values[0]}.csv',index=False)
    print(df)

# dfs = [pd.DataFrame(data) for data in table_data]