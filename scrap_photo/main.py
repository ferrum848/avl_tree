
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import shutil, os
import requests


def download_image(url, path):
    response = requests.get(url, stream=True)
    with open(path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


site = 'http://pngimg.com'

req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')

table = soup.find_all('li', attrs={'class': 'catalog'})
list_of_categoris = []
for i in table:
    data = i.find_all('div', attrs={'class': 'sub_category'})
    for j in data:
        href = j.find_all('a')
        for k in href:
            list_of_categoris.append(k.get('href'))
print(list_of_categoris)

for sub_link in list_of_categoris:
    link = site + sub_link
    category, sub_category = sub_link.split('/')[2], sub_link.split('/')[3]
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    all_img = soup.find_all('img')
    file_name = 1
    os.makedirs(os.path.join(os.getcwd(), 'pngimg', category, sub_category))
    for i in all_img:
        image = i.get('src')
        if sub_category == image.split('/')[2]:
            url = site + image
            print(site + image)
            path = os.path.join('pngimg', category, sub_category, str(file_name) + '.png')
            file_name += 1
            download_image(url, path)


