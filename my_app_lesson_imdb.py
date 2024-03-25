#Скрейпинг сайта https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm
#Результат сохраняется в локальную базу данныз MongoDB

import requests
from lxml import html
from pymongo import MongoClient

def insert_to_db(list_movies):
    client = MongoClient("mongodb://localhost:27017")    
    collection = client["imdb_movies"]["top_movies"]
    collection.insert_many(list_movies)
    client.close()

def get_titlemeter(element):
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

all_movies = []

resp = requests.get(url='https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm',
                    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

tree = html.fromstring(html=resp.content)

movies = tree.xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base']/li/div[@class='ipc-metadata-list-summary-item__c']")

for movie in movies:
    m = {}
    m = {
        'position' : int(movie.xpath(".//div/div/div[1]/text()[1]")[0]),
        'name' : movie.xpath(".//div/div/div/a/h3/text()")[0],
        'release_year' : int(movie.xpath(".//div/div/div[@class='sc-b0691f29-7 hrgukm cli-title-metadata']/span[1]/text()")[0]),       
        'rating' : get_rating(movie.xpath(".//div/div/span/div/span/text()"))
    }
    titlemeter, rank_change =  get_titlemeter(movie.xpath(".//div/div/div[1]/span/@aria-label")[0])
    m['titlemeter'] = titlemeter
    m['rank_change'] = rank_change
    all_movies.append(m)

insert_to_db(all_movies)
print(f'Количество переданных записей = {len(all_movies)}')
