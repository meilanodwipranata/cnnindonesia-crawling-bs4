from bs4 import BeautifulSoup
import requests
import time
import json
from datetime import datetime

url = 'https://www.cnnindonesia.com/indeks/2?page='
jumlah_page = 1001

list_data =[]

for i in range(1, jumlah_page):
    url_page = url + str(i)
    response = requests.get(url_page, timeout=10, headers={'User-Agent': 'Chrome'})
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    for artic in articles:
        a_tag = artic.find('a', href=True)

        # mengambil data artikel
        try:
            url_article = a_tag['href']
            ambil = requests.get(url_article, headers={"User-Agent": "Chrome"})
            soup_article = BeautifulSoup(ambil.text, 'html.parser')

            #ambil data
            domain = url_article.split('/')[2]
            crawling_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            crawling_time_epoch = int(time.time())
            title = soup_article.find('h1').get_text(strip=True)
            url = url_page
            contain_url = url_article
            categories = url_article.split('/')[3]
            
            media_url = soup.find_all('img')[0]['src']
            
            articles = soup_article.find_all('p')
            article = ' '.join([p.get_text(strip=True) for p in articles])
        
            tags = []
            posted = soup_article.find('div' ,class_='text-cnn_grey').get_text(strip=True)

            

            #if tag:
             #   for a in tag.find_all('a'):
             #       text = a.get_text(strip=True)
             #       tags.append(text)
            # print(url,contain_url,media_url)
            
            
            
            data = {
                "domain": "www.cnnindonesia.com",
                "crawling_time":crawling_time ,
                "crawling_time_epoch": crawling_time_epoch,
                "url": url,
                "title": title,
                "categories": categories,
                "article": {
                    "content_url": contain_url,
                    "posted": posted,
                    "media_url": media_url,
                    "tags": tags,
                    "article": article
    }
            }
            list_data.append(data)
            
            
        except Exception as e:
            continue

    if response.status_code == 200:
        print(f'sukses page {i}')
    else:
        print(f'gagal page {i}')
    
    time.sleep(1)
time.sleep(1)

# simpan JSON
with open('cnn_indonesia_crawling.json', 'w', encoding='utf-8') as f:
    json.dump(list_data, f, ensure_ascii=False, indent=4)

