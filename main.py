import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_nature_search_results(url):
    proxies = {
        "http": "socks5h://127.0.0.1:7890",
        "https": "socks5h://127.0.0.1:7890"
    }

    response = requests.get(url, proxies=proxies)
    # response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    titles = []
    links = []
    dates = []

    count = soup.find_all('span', class_='u-display-flex')
    if len(count) == 0:
        return
    spans = count[0].find_all('span')[1].text.strip().split()
    num = int(spans[0])
    page_num = min(num // 50 + 1, 3)

    for i in range(page_num):
        buf_url = url + '&page=' + str(i + 1)
        response = requests.get(buf_url, proxies=proxies)

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('li', class_='app-article-list-row__item')
        for article in articles:
            title = article.find('a', class_='c-card__link u-link-inherit').text.strip()
            link = 'https://www.nature.com' + article.find('a', class_='c-card__link u-link-inherit')['href']
            date = article.find('time')['datetime']

            titles.append(title)
            links.append(link)
            dates.append(date)

    df = pd.DataFrame({
        'Title': titles,
        'Link': links,
        'Date': dates
    })

    return df


key_list = [
    # 'Explainable+artificial+intelligence',
    # 'Multimodal+fusion+technology',
    # 'machine+learning'
    # 'deep+learning'
    'enhanced+learning'
    # 'Reinforcement+Learning'
]

for key in key_list:
    url = 'https://www.nature.com/search?q=enhanced+learning&journal=ncomms&subject=ecology%2C+engineering%2C+mathematics-and-computing%2C+microbiology&date_range=last_5_years&order=relevance'
    print(url)
    df = scrape_nature_search_results(url)
    if df is not None:
        df.to_csv('ncomms_' + key + '.csv', index=False)
    print(key + 'done')
