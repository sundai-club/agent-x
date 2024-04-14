# filename: scrape_financial_news.py

import requests
from bs4 import BeautifulSoup

# Replace with the actual URL of the financial news website
url = "https://www.actualwebsite.com/" 

response = requests.get(url)

assert response.status_code == 200  # Ensure we're successful in getting the website content

soup = BeautifulSoup(response.content, 'html.parser')

# This structure of the financial news website's HTML might differ 
# You might need to inspect the website to know the exact structure 
news_headlines = soup.find_all('h2', {'class': 'news-headline'})

for headline in news_headlines:
    news_title = headline.text.strip()
    news_url = headline.find('a').get('href')
    print(f"News Title: {news_title}")
    print(f"News URL: {news_url}")
    print("\n")