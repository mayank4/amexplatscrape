import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from textblob import TextBlob
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

def scrape_reddit(brand):
    driver = get_driver()
    search_url = f"https://www.reddit.com/search/?q={brand}+cancelled+complaint"
    
    try:
        driver.get(search_url)
        time.sleep(5)  # Wait for dynamic content
        
        # Target post titles (Reddit uses h3 for titles in search)
        elements = driver.find_elements(By.TAG_NAME, "h3")
        titles = [el.text for el in elements if len(el.text) > 5]
        return titles
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
