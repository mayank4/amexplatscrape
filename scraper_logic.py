from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def scrape_reddit(brand_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # This tells the OS to find the chromium we just installed via packages.txt
    chrome_options.binary_location = "/usr/bin/chromium" 

    # We point directly to the system driver path
    service = Service("/usr/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        search_url = f"https://www.reddit.com/search/?q={brand_name}+cancelled"
        driver.get(search_url)
        time.sleep(5)
        elements = driver.find_elements(By.TAG_NAME, "h3")
        return [el.text for el in elements if len(el.text) > 5]
    finally:
        driver.quit()
