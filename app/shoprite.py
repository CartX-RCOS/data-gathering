from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
import json
import os

# checks if the xpath is valid or not
async def is_xpath_valid(xpath, driver):
    try:
        await driver.find_element(By.XPATH, xpath)
        return True
    except Exception as e:
        return False

# opens up shoprite website
async def scrape_shoprite_website(item_name):
    zipcode = "10954"
    products = []

    # Set options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')

    # Initialize a web driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = f"https://www.shoprite.com/sm/pickup/rsid/3000/results?q={item_name}"
        driver.get(url)

        # scraping logic here

    finally:
        driver.quit()

    return products