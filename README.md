# 🛒 Data Scraper Pipeline

This repository contains Python scripts and a Node.js backend that scrape pricing and product data from major U.S. retail stores and store the results directly into a MongoDB database.

---

## 🏬 Supported Retailers

- CVS  
- Hannaford  
- Walgreens  

---

## 🧪 How It Works

- Python scripts use **BeautifulSoup** and **Selenium** to scrape real-time data from retailer websites.  
- The scraped data is stored in structured JSON format (`.json` files).  
- A Node.js backend handles the database connection to **MongoDB**, inserting the parsed data for use in a larger application pipeline.  

---

## 🗂️ Project Structure

cvs.py # Scrapes CVS product data
hannaford.py # Scrapes Hannaford product data
walgreens.py # Scrapes Walgreens product data

mongodb.js # MongoDB connection logic (Node.js)
server.js # Node.js server entry point
package.json # Node.js dependencies and metadata

cvs.json # Sample scraped data from CVS
hannaford.json # Sample scraped data from Hannaford
walgreens.json # Sample scraped data from Walgreens


---

## 🛠 Tech Stack

- **Python** – Web scraping with BeautifulSoup & Selenium  
- **Node.js** – Backend service and MongoDB interface  
- **MongoDB** – NoSQL database for storing structured product data  
- **JSON** – Intermediate format for storing raw scrape results  
