import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- 1. PRO SCRAPER SETUP ---
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # 🕵️ Custom User-Agent to look like a real browser
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    
    return webdriver.Chrome(options=options)

def scrape_reddit(brand_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # 🕵️ Add a real browser User-Agent to prevent blocks
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    # Path for Streamlit Cloud
    chrome_options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Search specifically for the brand and the word 'cancelled'
        url = f"https://www.reddit.com/search/?q={brand_name}+cancelled"
        driver.get(url)
        
        # ⏳ Wait up to 10 seconds for the titles to appear
        wait = WebDriverWait(driver, 10)
        # Reddit search results often use <a> tags for titles
        elements = wait.until(EC.presence_of_all_elements_with_elements_located((By.CSS_SELECTOR, 'a[slot="title"]')))
        
        titles = [el.text for el in elements if len(el.text) > 5]
        return titles
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        driver.quit()

# --- 2. STREAMLIT DASHBOARD ---
st.title("🕵️ Brand Churn Insights")

brand_input = st.text_input("Enter Brand (e.g., Lululemon, Amex):")

if st.button("Run Analysis"):
    if brand_input:
        with st.spinner(f"Searching for {brand_input} churn data..."):
            data = scrape_reddit(brand_input)
            
            if data:
                # Analysis Logic
                results = []
                for text in data:
                    sentiment = TextBlob(text).sentiment.polarity
                    results.append({"Insight": text, "Sentiment": sentiment})
                
                df = pd.DataFrame(results)
                
                # Visualizations
                st.subheader(f"Results for {brand_input}")
                st.metric("Avg Sentiment Score", f"{df['Sentiment'].mean():.2f}")
                st.dataframe(df)
                st.bar_chart(df['Sentiment'])
            else:
                st.warning("No data found. Reddit might be blocking the request or the search returned 0 results.")
    else:
        st.error("Please enter a brand name.")
