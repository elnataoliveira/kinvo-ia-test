import crochet
#iniciar crochet
crochet.setup()     
from flask import Flask, jsonify
from scrapy.crawler import CrawlerRunner
from feedsnews import NewsSpider
import re
import spacy  

app = Flask('Scrape With Flask')
#rodar crawl
crawl_runner = CrawlerRunner()      
quotes_list = []                   
scrape_in_progress = False
scrape_complete = False

@app.route('/crawl')
def crawl_for_quotes():
    
    global scrape_in_progress
    global scrape_complete

    if not scrape_in_progress:
        scrape_in_progress = True
        global quotes_list
        scrape_with_crochet(quotes_list)
        return get_results()
    elif scrape_complete:
        save(quotes_list)
        return jsonify(quotes_list)
    return 'SCRAPE IN PROGRESS ATUALIZE A PÁGINA'

def get_results():
    
    global scrape_complete
    if scrape_complete:
        return jsonify(quotes_list)
    return crawl_for_quotes()

@crochet.run_in_reactor
def scrape_with_crochet(_list):
    eventual = crawl_runner.crawl(NewsSpider, quotes_list=_list)
    eventual.addCallback(finished_scrape)

def finished_scrape(null):
    
    global scrape_complete
    scrape_complete = True

def save(_list):
    fl = open('notices.json', 'a')
    elementos = []
    for lista in _list:
        for element in lista:
            if re.search('\\bB3\\b', element, re.IGNORECASE):
                elementos.append(element)
    fl.write(str(elementos))                         
    fl.close()
      
@app.route('/extract')
def extract_entities():
    f = open('notices.json', "r") 
    nlp = spacy.load('pt')
    texto = nlp(f.read())    
    entities = []
    for entity in texto.ents:
        entities.append(entity.text)
    if len(entities) == 0:
        return 'Nenhuma notícia encontrada'

    return jsonify({'entities' : entities})
