import express from 'express';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

import { Builder, By, until } from 'selenium-webdriver';
import chrome from 'selenium-webdriver/chrome.js';
const __filename = fileURLToPath(import.meta.url);
const parsed = path.parse(__filename);

// checks if the given XPATH is valid or not
async function isXPathValid(xpath, driver) {
  try {
    await driver.findElement(By.xpath(xpath));
    return true;
  } catch (error) {
    return false;
  }
}

async function scrapeTargetWebsite(item_name) {
  const Products = [];

  // Set Chrome options to run in headless mode
  const chromeOptions = new chrome.Options();
  chromeOptions.addArguments('--headless');
  chromeOptions.addArguments('--disable-gpu');
  chromeOptions.addArguments('--disable-extensions');
  chromeOptions.addArguments('--disable-software-rasterizer');
  chromeOptions.addArguments('--disable-notifications');
  chromeOptions.addArguments('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36');

  // Initialize a Selenium WebDriver with Chrome options
  const driver = new Builder()
    .forBrowser('chrome')
    .setChromeOptions(chromeOptions)
    .build();

  let divIndex = 0;

  try {
    const url = `https://www.target.com/s?searchTerm=${item_name}&tref=typeahead%7Cterm%7C${item_name}%7C%7C%7Chistory`;

    // Load the page
    await driver.get(url);

    // Define the scroll height in pixels
    let curr_height = 0; const scroll_height = 800;
    const max_scroll_height = await driver.executeScript("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );");
    await driver.executeScript(`window.scrollBy(0, 400);`);
    curr_height = curr_height + 400;

    let foundValidXPath = false;
    let check_index = 1;

    await driver.sleep(4000);

    for (check_index = 1; check_index < 10; check_index++) {
      const xpathToCheck = `//*[@id="pageBodyContainer"]/div[1]/div[1]/div[1]/div[${check_index}]/div[1]/div[1]/section[1]/div[1]`;
      const isValid = await isXPathValid(xpathToCheck, driver);

      if (isValid) {
        foundValidXPath = true; 
        divIndex = check_index;
        break;
      }
    }

  } finally {
    await driver.quit();
  }
  return Products;
}

async function getData(){
    try {
        const item = "chocolate";
        const data = await scrapeTargetWebsite(item);
        

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

getData();