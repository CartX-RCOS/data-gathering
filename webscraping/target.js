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

// Function to deduplicate data based on a unique identifier (index 0)
function deduplicateData(existingData, newData) {
  const uniqueIdentifiers = new Set(existingData.map(item => item[0]));
  const deduplicatedData = [...existingData];

  for (const newItem of newData) {
    if (!uniqueIdentifiers.has(newItem[0])) {
      deduplicatedData.push(newItem);
      uniqueIdentifiers.add(newItem[0]);
    }
  }

  return deduplicatedData;
}

async function scrapeTargetWebsite(item_name) {
  const Products = [];

  // Set Chrome options to run in headless mode
  const chromeOptions = new chrome.Options();
//   chromeOptions.addArguments('--headless');
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

    if (divIndex == 9){
      await driver.quit();
    }

    // -------------------------------------------------------------------------------------------------------------------------
    for (let item_number = 1; item_number <= 25; item_number++) {
      try {
        const xpath_type = `//*[@id="pageBodyContainer"]/div[1]/div[1]/div[1]/div[${check_index}]/div[1]/div[1]/section[1]/div[1]/div[${item_number}]`;
        const xpath_element = await driver.wait(until.elementLocated(By.xpath(xpath_type), 1000));
        const element_type = await xpath_element.getText();

        // advertisement is found
        if (element_type === "Sponsored") {continue;}

        // Split the string by newline characters
        const element_typeArray = element_type.split('\n');

        const image_xpath = `//*[@id="pageBodyContainer"]/div[1]/div[1]/div[1]/div[${divIndex}]/div[1]/div[1]/section[1]/div[1]/div[${item_number}]/div[1]/div[1]/div[1]/div[1]/h3[1]/div[1]/div[1]/a[1]/div[1]/picture[1]/img[1]`;
        const image_element = await driver.findElement(By.xpath(image_xpath));
        const image_source = await image_element.getAttribute("src");

            Products.push(
                {
                    "name": element_typeArray[0],
                    "brand": element_typeArray[1],
                    "price": "null",
                    "img": image_source
                }
            );

        // page scroll 
        if (max_scroll_height > curr_height) {
          await driver.executeScript(`window.scrollBy(0, ${scroll_height});`); 
          await driver.sleep(0.5);
          curr_height += scroll_height;
        }

      } catch (error) {
        console.log(`${error}`);
      }
    }
  // -------------------------------------------------------------------------------------------------------------------------

  } finally {
    await driver.quit();
  }
  return Products;
}


async function getData(){
    try {
        const item = "chocolate";

        const data = await scrapeTargetWebsite(item);

        console.log(data);

        // stores the data
        const storageSubfolder = 'storage'; 
        const targetSubfolder = 'target';
        const fileName = path.join(parsed.dir, storageSubfolder, targetSubfolder, `${item}.json`);

        // Check if the file exists
        if (fs.existsSync(fileName)) {
        // Load the existing data from the file
        const existingData = JSON.parse(fs.readFileSync(fileName));

        // Merge and deduplicate the data (based on a unique identifier)
        const newData = deduplicateData(existingData, data);

        // Save the merged data back to the file
        fs.writeFileSync(fileName, JSON.stringify(newData, null, 2));
        } else {
        // If the file doesn't exist, create it with the scraped data
        fs.writeFileSync(fileName, JSON.stringify(data, null, 2));
        }

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

getData();