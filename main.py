import re
from bs4 import BeautifulSoup
import urllib3
import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['mu_db']
article = mydb['article']



url = 'https://www.manutd.com/fr'
http = urllib3.PoolManager()

request = http.request('GET', url)


soup = BeautifulSoup(request.data, 'html5lib')
mu_articles = soup.find_all('div', class_="mu-item")


def get_mu_articles(articles):

    articles_result = list()

    for article in articles:
        article_title = article.h2.text
        article_preview = article.p.text
        article_link = article.a['href']    

        articles_obj = {'title': article_title, 'preview': article_preview, 'link': article_link}
        articles_result.append(articles_obj)

    return articles_result


 
articles_array = get_mu_articles(mu_articles)


def insert_article_todb(db_list):

    insert =  article.insert_many(db_list)
    print(insert.inserted_ids)


insert_article_todb(articles_array)
