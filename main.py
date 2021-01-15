from recipe_scrapers import scrape_me
import requests
from bs4 import BeautifulSoup
import re

headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def get_links(url):

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    links = soup.findAll("a", {"data-wpel-link": "internal"})

    for x in links:
        if x.has_attr('title'):
            print(x['title'], x['href'])

def get_max_page():
    url = "https://www.justonecookbook.com/"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    links = soup.findAll("a", {"class": "page-numbers"})
    max_page_list = []
    for x in links:
        try:
            max_page_list.append(int(x.getText().strip()))
        except:
            break
    return max(max_page_list)

def get_recipe(url):
    scraper = scrape_me(url, wild_mode=True)
    units = [' oz ', 'tsp', 'Tbsp', 'lb']


    for x in scraper.ingredients():
        for y in units:
            if not x == None:
                if y in x:
                    try:
                        x = x.replace(y, '')
                        if y == ' oz ':
                            print(int(28.3495*float(re.search(r"[-+]?\d*\.\d+|\d+", x).group())), 'grams', ''.join([i for i in x if not i.isdigit()]))
                            break
                        else:
                            print(int(float(re.search(r'\d+', x).group())), y, ''.join([i for i in x if not i.isdigit()]))
                            break
                    except:
                        break
                    break
                else:
                    print(x)
                    break
    #print(scraper.instructions())



if __name__ == '__main__':
    max_page = get_max_page()

    for x in range(1, max_page):
        url = "https://www.justonecookbook.com/page/{}/".format(x)
        #get_links(url)

    print(get_recipe('https://www.justonecookbook.com/vegetable-gyoza/'))

    '''
    print(scraper.title())
    scraper.total_time()
    scraper.yields()
    print(scraper.ingredients())
    print(scraper.instructions())
    scraper.image()
    scraper.host()
    scraper.links()
    '''



