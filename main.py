import undetected_chromedriver as uc
import time
import re
# from seleniumwire import webdriver 
# from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor
import itertools
import product_detail
import json
import os

with open("ip.json", "r", encoding="utf-8") as file:
    
    proxies = dict(json.load(file))
proxy_cycle = itertools.cycle(proxies)

def get_next_proxy():
    return next(proxy_cycle)

def open_browser(search=None ,proxy=None ,url= None):
    # Set up Chrome options
    options = uc.ChromeOptions()
    
    # if proxy:options.add_argument(f'--proxy-server={proxy}')
    service = Service(ChromeDriverManager().install())
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = uc.Chrome(options=options)
    try:
    # Go to webpage
        if search: 
            # driver.implicitly_wait(10)
            driver.get(f"https://www.etsy.com/search?q={quote_plus(search)}&ref=search_bar")
            time.sleep(5)  # Wait for the page to load
        else:
            if url:driver.get(url)
        return driver
        # else:driver.get(url)
        
    except:return None

def get_search_data(driver):
        # Get the main product container
    product_container = driver.find_element(uc.By.CSS_SELECTOR, 'ul.tab-reorder-container[data-results-grid-container]')
        # Get all product cards (li elements)
    product_cards = product_container.find_elements(uc.By.TAG_NAME, 'li')
    print(f"Found {len(product_cards)} product cards")

    collection = {}
    for card in product_cards:
        print("Processing a product card...")
        try:
            # Title
            title_elem = card.find_element(uc.By.CSS_SELECTOR, 'h3')
            title = title_elem.text.strip()

            # Product Link
            link = card.find_element(uc.By.CSS_SELECTOR, 'a').get_attribute("href")

            match = re.search(r'/listing/(\d+)', str(link))
            listing_id = match.group(1) if match else None
            try:
            # Seller Name
                seller_elem = card.find_element(uc.By.CSS_SELECTOR, 'p[data-seller-name-container] span.i756n8qyj')
                seller_name = seller_elem.text.strip()
            except:seller_name = "N/A"
            # Rating
            try:rating = card.find_element(uc.By.CSS_SELECTOR, 'span.wt-text-title-small').text.strip()
            except:rating = "N/A"

            # Number of Reviews
            try:reviews = card.find_element(uc.By.CSS_SELECTOR, 'p.wt-text-body-smaller').text.strip()
            except:reviews = "N/A"

            # Price (Discounted)
            try:sale_price = card.find_element(uc.By.CSS_SELECTOR, 'span.currency-value').text.strip()
            except:sale_price = "N/A"

            # Original Price
            try:original_price = card.find_element(uc.By.CSS_SELECTOR, 'p.search-collage-original-price span.currency-value').text.strip()
            except:original_price = "N/A"

            # Discount
            try:discount = card.find_element(uc.By.CSS_SELECTOR, 'p.search-collage-original-price span.wt-text-grey').text.strip()
            except:discount = "N/A"

            # Print results
            if listing_id not in  collection.keys():     
                collection[listing_id] = {"link":link , "title":title ,"rating": rating, "reviews":reviews , "sale_price":sale_price , "original_price":original_price , "discount":discount}
            # else:collection[listing_id].append()
            print(f"Title: {title}")
            # print(f"Seller: {seller_name}")
            print(f"Rating: {rating} | Reviews: {reviews}")
            print(f"Sale Price: ${sale_price}")
            print(f"Original Price: ${original_price}")
            print(f"Discount: {discount}")
            print(f"Link: {link}")
            print("-" * 60)

        except Exception as e: 
            print("Exception: ", e)
            return None
    return collection
        





# ---- main ----
driver = open_browser("mug")
if driver:
    collection = get_search_data(driver)
    import json
    with open('etsy_collection.json', 'w') as f:
        json.dump(collection, f, indent=4)
else:
    quit("Failed to open browser.")
    exit()


def scrape_search(Lid, data):
    proxy = get_next_proxy()
    try:
        driver = open_browser(data["url"],proxy)
        if  driver:
            data = product_detail.get(driver,data)
            return lid,data
        else:
            print(f"Failed to open browser for {data['url']}")
            return None , None
        # search_query = search.replace(" ", "+")
        # driver.get(f"https://www.etsy.com/search?q={search_query}&ref=search_bar")
        # scraping code yahan likho
    except Exception as e:
        print(f"Error: {e}")
        return None, None
    finally:pass
        # driver.quit()

# search_terms = collection.values()
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = []
    for lid, data in collection.items():
        futures.append(executor.submit(scrape_search, lid, data))
    # executor.map(scrape_search, search_terms)
    for future in futures:
        lid, updated_data = future.result()
        if lid and updated_data :
            collection[lid].update(updated_data)

