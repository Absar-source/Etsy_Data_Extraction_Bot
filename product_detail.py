import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

def get(driver,data:dict):
    


    # image_urls = WebDriverWait(driver,40).until(EC.presence_of_element_located((uc.By.ID,"photos")))
    images_url = driver.find_element(uc.By.ID,"photos") 
    images_url_html = images_url.get_attribute("outerHTML")
    img_soup = BeautifulSoup(images_url_html, 'html.parser')


    product_details =  driver.find_element(uc.By.ID,"product_details_content_toggle")
    product_details_html = product_details.get_attribute("outerHTML")
    product_soup = BeautifulSoup(product_details_html,"html.parser")


    # deliver_details = driver.find_element(uc.By.ID,"shipping_and_returns")
    # deliver_details_html = deliver_details.get_attribute("outerHTML")

    tag_class = driver.find_element(uc.By.ID, 'reviews')
    tags_html = tag_class.get_attribute('innerHTML')
    tag_soup = BeautifulSoup(tags_html, 'html.parser')

    seller_deltails = driver.find_element(uc.By.CLASS_NAME,"lp-meet-your-seller-container").get_attribute("innerHTML")
    seller_soup = BeautifulSoup(seller_deltails, 'html.parser')

    avail_details_html = driver.find_element(uc.By.CLASS_NAME,"recs-appears-logger").get_attribute("innerHTML")
    availability  = BeautifulSoup(avail_details_html, 'html.parser').text

    day_views = None
    basket = None
    day_sale = None
    left = None
    if "left" in availability and "views in" in availability:
        res = str(availability).split(" ")
        left,day_views = res[1],res[4]

    elif "views in" in availability:day_views = str(availability).split(" ")[0]
    if "people bought" in availability: day_sale = str(availability).split(" ")[2]
    if "baskets" in availability and "Rare find" in availability  : basket = str(availability).split(" ")[4]
    elif "baskets" in availability: basket = str(availability).split(" ")[1]
    if "baskets" in availability: basket = str(availability).split(" ")[1]

            

    # Extract materials
    materials = ""
    capacity = ""
    is_digital=None
    for li in product_soup.select('li'):# and materials:

        if "Materials:" in li.text:
            
            materials = li.text.replace("Materials:", "").strip()
    # Extract capacity
        if "Capacity:" in li.text:# and capacity:
            capacity = li.text.replace("Capacity:", "").strip()
        if "Digital download" in li.text:is_digital="yes"
        # if materials!="" and capacity!="" and : break

            


    # Extract description
    desc = product_soup.select_one('div[data-id="description-text"] p')
    description = desc.get_text(separator="\n").strip() if desc else ""

    # Extract bullet points
    bullets = []
    for line in description.split("\n"):
        if line.strip().startswith(".:"):
            bullets.append(line.strip(".: ").strip())

    # Optional: Extract designer
    designer_tag = product_soup.select_one(".how-its-made-label-product-details a")
    designer = designer_tag.text.strip() if designer_tag else ""
    designer_url = designer_tag['href'] if designer_tag else ""

    #extract img urls
    image_urls = [img['src'] for img in img_soup.select('img[data-index]') if 'src' in img.attrs]

    # extract tags
    tags = [tag.get_text(strip=True) for tag in tag_soup.select('[data-tag]')]


    # getting seller details/
    # extract shop details

    # 1. Rating and number of reviews
    rating_tag = seller_soup.select_one('div[data-rating-and-reviews-meet-your-seller] a')
    # print(rating_tag)
    rating = None
    reviews = None
    if rating_tag:
        rating_text = rating_tag.get_text(strip=True)
        parts = rating_text.split('(')
        if len(parts) == 2:
            rating = parts[0]
            reviews = parts[1].replace('reviews)', '').strip()

    # 2. Total sales
    sales = None
    for div in seller_soup.find_all('div'):
        if div.text.strip().endswith("sales"):
            sales = div.text.strip()
            break

    # 3. Location ("From")
    # Step 1: Find all divs with the target class
    target_divs = seller_soup.find_all('div', class_='wt-display-flex-xs wt-flex-gap-xs-1 wt-align-items-center')

    location = None
    for c, div in enumerate(target_divs):
        # Step 2: Check if text directly inside div (not inside any nested tag) exists
        direct_texts = [t for t in div.stripped_strings]
        # Location usually has only one or two words after icon span
        if len(direct_texts) == 1 and c==2:#',' in direct_texts[0]:
            location = direct_texts[0]
            break



    data.update( {
            "description": description,
            "tags": tags,
            "materials":materials,
            "capacity":capacity,
            "designer":designer_url,
            "location": location,
            "total_sale":sales,
            # "quantity": quantity,
            # "variations": variations,
            "is_digital": is_digital,
            "images": image_urls,
            "day_views":day_views,
            "day_sale":day_sale,
            "left": left,
            "basket":basket,
            # "category_path": category_path
        })
    if  not rating and rating!=data['rating']:
        data.update({"rating":rating})
    elif not reviews and reviews!= data['reviews']:
        data.update({"reviews":reviews})

    # print("tags" , tags)
    # print("Materials:", materials)
    # print("Capacity:", capacity)
    # print("Designer:", designer)
    # print("Designer URL:", designer_url)
    # print("Description:", description[:100], "...")
    # print("Bullets:", bullets)
    # print("images urls: " , image_urls)
    # print("rating:",rating)
    # print("designer:" , designer)
    # print('sales:' , sales)
    # # print("sale_price:" , sale_price)
    # print("is_digital:" ,is_digital)
    # print("day_views",day_views,)
    # print("day_sale",day_sale,)
    # print("left", left,)
    # print("basket",basket,)
    # print("--------------------\n")
