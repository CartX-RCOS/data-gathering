from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
import time

# Set up the WebDriver (Make sure to replace 'path_to_chromedriver' with the actual path)
driver = webdriver.Chrome()

# URL you want to load
url = f"https://www.hannaford.com/search/product?form_state=searchForm&keyword=cookies&ieDummyTextField=&productTypeId=P"

# Load the webpage
driver.get(url)

all_products = []

# list of products I need to scrape
itemsToScrape = ["icecream","chips","bread","milk","eggs","water","soda"]

for item in itemsToScrape:

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)  # Allow time to scroll to the top

    # go to the search for here and search
    # enter the name in the serach bar
    # let the page load
    search_bar = driver.find_element(By.ID, 'search-input')
    search_bar.click()
    search_bar.clear()
    search_bar.send_keys(item)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(5)

    # Function to close the feedback popup if it appears
    def close_feedback_popup():
        try:
            # Locate the "No thanks" button by class name and click it
            no_thanks_button = driver.find_element(By.CLASS_NAME, 'fsrDeclineButton')
            no_thanks_button.click()
            print("Closed the feedback popup by clicking 'No thanks'.")
            time.sleep(1) 
            return True
        except NoSuchElementException:
            # If "No thanks" button is not found, try the close button
            try:
                close_button = driver.find_element(By.CLASS_NAME, 'fsrInvite__closeWrapper')
                close_button.click()
                print("Closed the feedback popup by clicking the close button.")
                time.sleep(1)
                return True
            except NoSuchElementException:
                # If no elements are found, return False
                return False

    while True:
        try:
            # Check and close the popup if it's present
            if close_feedback_popup():
                print("Popup closed. Proceeding to check 'See More' button.")

            # Scroll down to the "See More" button
            see_more_button = driver.find_element(By.ID, 'see-more-btn')
            driver.execute_script("arguments[0].scrollIntoView(true);", see_more_button)
            time.sleep(1)

            # Click the "See More" button
            see_more_button.click()
            print("'See More' button clicked.")
            time.sleep(2)

        except NoSuchElementException:
            print("No more 'See More' button found.")
            break

    # Get the HTML content of the loaded page
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    thumbnail_container = soup.find('div', class_='entity-thumbnail-container row', id='thumbnail-container')
    product_divs = thumbnail_container.find_all('div', class_='plp_thumb_wrap product-impressions')

    for product_div in product_divs:
        product_data = {
            "root_category": product_div.get('data-root-category'),
            "categories": product_div.get('data-category'),
            "name": product_div.get('data-name'),
            "price": product_div.get('data-price'),
            "size": product_div.find('span', class_='overline text-truncate').text.strip() if product_div.find('span', class_='overline text-truncate') else 'No size information',
            "image_links": [product_div.find('img')['src']] if product_div.find('img') else [],
            "product_url": "https://www.hannaford.com" + product_div.find('div', class_='catalog-product')['data-url'] if product_div.find('div', class_='catalog-product') else 'No URL'
        }

        # add all products
        all_products.append(product_data)

json_file_path = "hannaford.json"
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_products, json_file, indent=4, ensure_ascii=False)

# Close the WebDriver
driver.quit()