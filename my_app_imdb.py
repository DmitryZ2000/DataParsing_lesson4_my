import requests
from lxml import html
from lxml import etree

def get_titlemeter(element: str):
    if element == 'No rank change':
        titlemeter = 'No rank change'
        rank_change = 0
    elif element.split()[1] == 'up':
        titlemeter = 'Up'
        rank_change = element.split()[2]
    elif element.split()[1] == 'down':
        titlemeter = 'Down'
        rank_change = element.split()[2]
    return titlemeter, rank_change

def get_rating(rating_list: list):
    try:
        rating = float(rating_list[0])
    except:
        rating = None
    return rating


resp = requests.get(url='https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm',
                    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})

#Создаем парсинг дерева lxml из содержимого объекта ответа
tree = html.fromstring(html=resp.content)

movies = tree.xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base']/li/div[@class='ipc-metadata-list-summary-item__c']") # Разные кавычки

print(resp.status_code)

for movie in movies:
    name = movie.xpath(".//div/div/div/a/h3/text()")[0]
    release_year = movie.xpath(".//div/div/div[@class='sc-b0691f29-7 hrgukm cli-title-metadata']/span[1]/text()")[0]
    position = movie.xpath(".//div/div/div[1]/text()[1]")[0]
    titlemeter, rank_change = get_titlemeter(movie.xpath(".//div/div/div[1]/span/@aria-label")[0])
    rating = get_rating(movie.xpath(".//div/div/span/div/span/text()"))
    print(f'{name = }, {release_year = }, {position = }, {titlemeter =}, {rank_change = }, {rating = }')


