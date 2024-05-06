import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions


# ua = UserAgent()
# user_agent = ua.random
# options = ChromeOptions()
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument(user_agent)
# driver = Driver(browser="chrome", headless=True, agent="user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36", no_sandbox=True, disable_gpu=True)

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

# options.binary_location = '/home/sundaiclub/agent-x/venv/lib/python3.11/site-packages/seleniumbase/drivers/chromedriver'
# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get("https://www.google.com/search?q=dog&sca_esv=4a5015327b2804e5&sca_upv=1&rlz=1C1RXQR_enUS1041US1041&ei=1U84ZqCWBu2l5NoP5f2vgAo&ved=0ahUKEwjg1JWBjPiFAxXtElkFHeX-C6AQ4dUDCBA&uact=5&oq=dog&gs_lp=Egxnd3Mtd2l6LXNlcnAiA2RvZzINEC4YgAQYsQMYQxiKBTINEAAYgAQYsQMYQxiKBTINEAAYgAQYsQMYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTINEC4YgAQYsQMYQxiKBTILEAAYgAQYkgMYigUyCxAAGIAEGJIDGIoFMg0QABiABBhDGMkDGIoFMg0QLhiABBixAxhDGIoFMhwQLhiABBixAxhDGIoFGJcFGNwEGN4EGN8E2AECSKgQUIYGWKYPcAF4AZABAJgBRKABowKqAQE1uAEDyAEA-AEBmAIGoALCAsICChAAGLADGNYEGEfCAg0QABiABBiwAxhDGIoFwgITEC4YgAQYsAMYQxjIAxiKBdgBAcICDhAAGIAEGJECGLEDGIoFwgIHEAAYgAQYCsICDRAuGIAEGNEDGMcBGArCAgcQLhiABBgKwgIREC4YgAQYkQIY0QMYxwEYigXCAhcQLhiABBiRAhixAxjRAxiDARjHARiKBcICDhAuGIAEGLEDGIMBGNQCwgIOEC4YgAQYsQMYgwEYigXCAg4QLhiABBixAxjRAxjHAcICCxAAGIAEGLEDGIMBwgIREC4YgAQYsQMY0QMYgwEYxwHCAgUQABiABMICIBAuGIAEGJECGNEDGMcBGIoFGJcFGNwEGN4EGOAE2AECwgIQEC4YgAQY0QMYQxjHARiKBcICFhAuGIAEGLEDGNEDGEMYgwEYxwEYigXCAgoQLhiABBhDGIoFwgIfEC4YgAQY0QMYQxjHARiKBRiXBRjcBBjeBBjgBNgBApgDAIgGAZAGDLoGBAgBGAi6BgYIAhABGBSSBwE2oAfHVw&sclient=gws-wiz-serp")

time.sleep(5)

html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

links = soup.find_all('a')
allcontent = []

all_comps = soup.find_all()
for element in all_comps:
    print("elemnt type:" + element.name)

# for link in links:
#     if link.get('href').startswith("/r/") and "/comments/" in link.get('href'):
#         print("found link: ", link.get('href'))
#         found_url = "https://www.reddit.com" + link.get('href')
#         allcontent.append(found_url)
#     else:
#         print("INVALID LINK??: ", link.get('href'))
driver.quit()

