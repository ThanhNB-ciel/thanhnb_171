from bs4 import BeautifulSoup
import pandas as pd
import requests 
url = 'https://lazi.vn/statistic'
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')
table_data = []
tables = soup.find_all('table')  # Adjust the selection criteria if necessary

for table in tables:
    table_rows = table.find_all('tr')
    data = []

    for row in table_rows:
        table_cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in table_cells]
        data.append(row_data)

    table_data.append(data)

dfs = [pd.DataFrame(data) for data in table_data]

data_1  = []
for df in dfs:
    data_1.append(df)    
    print(data_1)

dfx = pd.DataFrame(data_1)
# data_1.to_csv('bxh.csv')

    


