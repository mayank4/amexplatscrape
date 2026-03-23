import streamlit as st
import pandas as pd
from textblob import TextBlob
from scraper_logic import scrape_reddit

st.set_page_config(page_title="Brand Churn Scout", page_icon="🕵️")
st.title("🕵️ Brand Churn Scout")
st.write("Analyzing Reddit 'Goldmines' for churn insights.")

brand = st.text_input("Enter Brand (e.g., Lululemon, Amex):")

if st.button("Generate Insight Report"):
    with st.spinner(f"Scouring Reddit for {brand} data..."):
        raw_text = scrape_reddit(brand)
        
        if raw_text:
            # Process Sentiment
            processed_data = []
            for text in raw_text:
                score = TextBlob(text).sentiment.polarity
                # Tagging logic
                tag = "General"
                if any(word in text.lower() for word in ["price", "fee", "cost"]): tag = "Cost"
                if any(word in text.lower() for word in ["quality", "rip", "break"]): tag = "Product"
                
                processed_data.append({"Insight": text, "Sentiment": score, "Category": tag})
            
            df = pd.DataFrame(processed_data)
            
            # Display Metrics
            avg_sent = df['Sentiment'].mean()
            st.metric("Overall Brand Sentiment", f"{avg_sent:.2f}")
            
            # Display Charts
            st.subheader("Churn Categories")
            st.bar_chart(df['Category'].value_counts())
            
            st.subheader("Raw Insights")
            st.dataframe(df)
        else:
            st.error("No data found. Try a different keyword!")
