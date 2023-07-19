import requests
from bs4 import BeautifulSoup

link_lazi = []
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

with open('link_lazi.txt', 'w') as file:
    for link in link_lazi:
        file.write(f'{link}')