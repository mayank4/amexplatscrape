from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def scrape_reddit(brand_name):
    # Set up headless mode for hosting
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Target the 'Search' page for the specific brand
    search_url = f"https://www.reddit.com/search/?q={brand_name}+cancelled+worth+it"
    driver.get(search_url)
    
    time.sleep(5) # Give it time to load the dynamic content
    
    # We look for post elements. Reddit's HTML changes, so we target 
    # elements that look like post titles.
    elements = driver.find_elements(By.TAG_NAME, "h3")
    data = [el.text for el in elements if len(el.text) > 5]
    
    driver.quit()
    return data
