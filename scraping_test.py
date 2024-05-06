from seleniumbase import Driver
from bs4 import BeautifulSoup
from seleniumbase.undetected import ChromeOptions
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import ChromeOptions


ua = UserAgent()
user_agent = ua.random
options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument(user_agent)
driver = Driver(browser="chrome", headless=True, agent="user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36", no_sandbox=True, disable_gpu=True)
driver.get("https://www.reddit.com/search/?q=dog+food")

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

options.binary_location = '/home/sundaiclub/agent-x/venv/lib/python3.11/site-packages/seleniumbase/drivers/chromedriver'
driver = webdriver.Chrome(options=options)

html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

links = soup.find_all('a')
allcontent = []

for link in links:
    if link.get('href').startswith("/r/") and "/comments/" in link.get('href'):
        print("found link: ", link.get('href'))
        found_url = "https://www.reddit.com" + link.get('href')
        allcontent.append(found_url)
    else:
        print("INVALID LINK??: ", link.get('href'))
driver.quit()

