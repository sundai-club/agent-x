from seleniumbase import Driver
from bs4 import BeautifulSoup
from seleniumbase.undetected import ChromeOptions
from fake_useragent import UserAgent


ua = UserAgent()
user_agent = ua.random
options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument(user_agent)
driver = Driver(browser="chrome", headless=True, agent=user_agent, no_sandbox=True, disable_gpu=True)
driver.get("https://www.reddit.com/search/?q=dog+food")

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

