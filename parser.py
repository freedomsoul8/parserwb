import requests
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def parse_products(zapros, result_filename):
    url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=2,12,7,3,6,13,21&curr=rub&dest=-1113276,-79379,-1104258,-5803327&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query={zapros}&reg=0&regions=64,58,83,4,38,80,33,70,82,86,30,69,22,66,31,40,1,48&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'

    response = requests.get(url=url).json()
    print(response)

    titles = list()
    prices = list()
    sale_prices = list()
    ids = list()
    brands = list()
    element_index = list()
    ratings = list()
    feedbacks_count = list()
    elem = list()
    test_data = list()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url=f'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&cardSize=c516x688&search={zapros}')
    driver.implicitly_wait(5)

    elements = driver.find_elements(by=By.CLASS_NAME,value="product-card__brand-name")
    fb = driver.find_elements(by=By.CLASS_NAME,value="product-card__count")


    for element,f in zip(elements,fb):
        elem.append(element.text+f.text.replace(' ',''))
        print(element.text,f.text)
    print(elements)

    for i in response["data"]["products"]:
        try:
            element_index.append(elem.index(i["brand"]+i["name"]+str(i["feedbacks"])))
            print(elem.index(i["brand"]+i["name"]+str(i["feedbacks"])))
            test_data.append(i["brand"]+i["name"]+str(i["feedbacks"]))
        except:
            element_index.append('NaN')
            test_data.append(i["brand"]+i["name"]+str(i["feedbacks"]))


        titles.append(i["name"])
        prices.append(str(i["priceU"]).replace('00',''))
        sale_prices.append(str(i["salePriceU"]).replace('00',''))
        ids.append(i["id"])
        brands.append(i["brand"])
        ratings.append(i["rating"])
        feedbacks_count.append(i["feedbacks"])

    df = pd.DataFrame({"position":element_index,
                       "title":titles,
                       "prices":prices,
                       "sale_prices":sale_prices,
                       "ids":ids,
                       "brands":brands,
                       "ratings":ratings,
                       "feedbacks_count":feedbacks_count,
                       "test_data":test_data})


    df.to_excel(f'results/{result_filename}.xlsx')

    return result_filename
def parse_positions(query):

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url=f'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&cardSize=c516x688&search={query}')
    driver.implicitly_wait(5)

    product_cards = driver.find_elements(by=By.CLASS_NAME, value="product-card j-card-item j-advert-card-item advert-card-item j-good-for-listing-event")
    print(len(product_cards))
