import crochet
#iniciar crochet
crochet.setup()     
from flask import Flask, jsonify, render_template, request, redirect, url_for
from scrapy.crawler import CrawlerRunner
from feedsnews import NewsSpider
import re
import spacy
import json  

app = Flask('Scrape With Flask')
#atribui CrwalerRunner a variável
crawl_runner = CrawlerRunner()      
quotes_list = []                   
scrape_in_progress = False
scrape_complete = False

#página inicial da aplicação com link para os endpoints
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/crawl', methods=['GET', 'POST'])
def crawl_for_quotes():
    
    global scrape_in_progress
    global scrape_complete

    #se não iniciou raspagem atualiza o valor do semáforo para True
    #inicia a rapsgem e verifica get_result
    if not scrape_in_progress:
        scrape_in_progress = True
        global quotes_list
        scrape_with_crochet(quotes_list)
    #se a rapagem estiver completa salva os dados em quotes_list
    #retorna o template com a lista com notícias raspadas
    elif scrape_complete:
        save(quotes_list)
        return render_template('crawl.html', quotes_list=quotes_list)
    return render_template('crawl.html')
"""
def get_results():    
    global scrape_complete
    if scrape_complete:
        return render_template('crawl.html', quotes_list=quotes_list)
    return crawl_for_quotes()
"""
@crochet.run_in_reactor
def scrape_with_crochet(_list):
    eventual = crawl_runner.crawl(NewsSpider, quotes_list=_list)
    eventual.addCallback(finished_scrape)

#sinaliza quando termina a raspagem
def finished_scrape(null):    
    global scrape_complete
    scrape_complete = True

def save(_list):
    buscar = 'Ibovespa'
    #fl = open('notices.json', 'w')
    elementos = []
    for lista in _list:
        for element in lista:
            if re.search('\\b'+buscar+'\\b', element, re.IGNORECASE):
                elementos.append(element)

    if len(elementos) > 0:
        with open('notices.json', 'w') as outfile:
            json.dump(elementos, outfile)                        
    outfile.close()
      
@app.route('/extract', methods=['GET', 'POST'])
def extract_entities():
    #n = open('notices.json', 'r')
    with open('notices.json') as json_file:
        noticias = json.load(json_file)
    #e = open('entidades.json', 'a') 
    nlp = spacy.load('pt')
    texto = nlp(str(noticias))    
    entities = []
    for entity in texto.ents:
        entities.append(entity.text)
    with open('entidades.json', 'a') as outfile:
            json.dump(entities, outfile)
    #e.write(str(entities))    
    return render_template('extract.html',entities=entities)
