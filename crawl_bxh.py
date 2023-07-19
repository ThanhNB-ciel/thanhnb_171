# import requests
# from bs4 import BeautifulSoup
# url = 'https://lazi.vn/statistic'
# response = requests.get(
#     url)
# data = response.text
# soup = BeautifulSoup(data, "html.parser")
# table_div = soup.find(
#     "div", {'class': 'box_tbl mgtop10px'})
# table = table_div.find('table')
# rows = table.find_all('tr')

# for row in rows:
#     cells = row.find_all('td')
#     for cell in cells:
#         print(cell.text)


import requests
from bs4 import BeautifulSoup

url = 'https://lazi.vn/statistic'  # Replace with the URL of the web page
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table_div = soup.find("div", {'class': 'message_wrapper'})  # Replace 'your-div-class' with the actual class name

if table_div is None:
    print("Table div not found.")
else:
    table = table_div.find('table')
    if table is None:
        print("Table not found.")
    else:
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            for cell in cells:
                print(cell.text)
