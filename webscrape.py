from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import hashlib
import pandas as pd
import datetime
import time


def scrape_marketplace(ilinks, usedb):
    
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options, executable_path="/usr/bin/chromedriver") # PATH TO CHROMEDRIVER
    
    cars = {'Name': [],
            'Price': [],
            'Location': [],
            'Mileage': [],
            'Link': [],
            'Hash': []
            }
            
    #output = ""
    
    for ilink in ilinks:
        
        driver.get(ilink)
        time.sleep(1)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        
        results = soup.find('div', class_='bq4bzpyk j83agx80 btwxx1t3 lhclo0ds jifvfom9 muag1w35 dlv3wnog enqfppq2 rl04r1d5')
        
        listings = results.find_all('div', class_='b3onmgus ph5uu5jm g5gj957u buofh1pr cbu4d94t rj1gh0hx j83agx80 rq0escxv fnqts5cd fo9g3nie n1dktuyu e5nlhep0 ecm0bbzt')
        
        for listing in listings:
            name = listing.find('span', class_='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7')
            price = listing.find('span', class_='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j keod5gw0 nxhoafnm aigsh9s9 tia6h79c fe6kdd0r mau55g9w c8b282yb iv3no6db a5q79mjw g1cxx5fr lrazzd5p oo9gr5id')
            try:
                location, mileage = listing.find_all('span', class_='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5')
            except ValueError as e:
                continue
            link = listing.find('a', class_='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 p8dawk7l').attrs['href']
            
            name = "none" if name == None else name.text.strip()
            price = "0" if price == None else price.text.strip()
            location = "none" if location == None else location.text.strip()
            mileage = "0" if mileage == None else mileage.text.strip()
            link= "none" if link == None else link
            
            cars['Name'].append(name)
            cars['Price'].append(price)
            cars['Location'].append(location)
            cars['Mileage'].append(mileage)
            cars['Link'].append("https://www.facebook.com"+link)
            cars['Hash'].append(create_hash(name, price))
        
    df = pd.DataFrame(cars, columns = ['Name', 'Price', 'Location', 'Mileage', 'Link', 'Hash'])
    print(df)
    df.to_csv('/home/owen/Workspace/python/marketplace-webscrape/results/out'+str(datetime.datetime.now().year)+str(datetime.datetime.now().day)+str(datetime.datetime.now().hour)+str(datetime.datetime.now().minute)+'.csv')
    
    driver.quit()     
    return(df)
    
def handle_io(links, make_db):
    output = scrape_marketplace(links, make_db)
        
def make_links(queries, maxprice):
    for query in range(len(queries)):
        queries[query] = "https://www.facebook.com/marketplace/112213565457929/search/?query="+queries[query]+"&maxPrice="+str(maxprice)+"&vertical=C2C&sort=BEST_MATCH"
    return queries
    
def create_hash(str1, str2):
    result = hashlib.md5((str1+str2).encode())
    return(result.hexdigest())

    
if __name__ == "__main__":
    #options
    make_db = True   
    maxprice = 5000
    queries = ["lexus", "ford", "toyota", "subaru", "honda"]
    
    links = make_links(queries, maxprice)
    handle_io(links, make_db)