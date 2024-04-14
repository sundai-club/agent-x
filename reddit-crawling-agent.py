from typing import Literal

from pydantic import BaseModel, Field
from typing_extensions import Annotated

import autogen
from autogen.cache import Cache

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions

config_list = autogen.config_list_from_json(
    [
        {
            "model": "gpt-3.5-turbo",
            "api_key": "API KEY"
        },
    ],
    filter_dict={
        "model": ["gpt-3.5-turbo"],
    },
)

llm_config = {
    "config_list": config_list,
    "timeout": 120,
}

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="For crawling or scraping reddit, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
)

def crawl_reddit(url: str):
    # Create a new instance of the Firefox driver
    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    # Load a URL
    driver.get(url)
    # Get the HTML content
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # Now you can use the soup object to parse and manipulate the HTML content
    # For example, you can find elements by tag name, class, etc.

    # Close the browser
    driver.quit()

    # Find the post title and content
    title = soup.find('h1').text.strip() if soup.find('h1') else "No title found"
    post = soup.find('shreddit-post')
    author = post.get('author')

    allcontent = ''

    # Find all <p> elements and concatenate their content into a string
    paragraphs = post.find_all('p', class_='')
    content = ' '.join([p.text.strip() for p in paragraphs])
    allcontent += "user " + author + " posted: " + title + ". " + content + "\n"

    # Find all the comments
    comments = soup.find_all('shreddit-comment')
    for comment in comments:
        author = comment.get('author')
        paragraphs = comment.find_all('p', class_='')
        content = ' '.join([p.text.strip() for p in paragraphs])
        allcontent += "user " + author + " commented: " + content + "\n"

@user_proxy.register_for_execution()
@chatbot.crawl_reddit(description="scrawl and scrap reddit post content")
def currency_calculator(
    url: Annotated[str, "link to the reddit post"],
) -> str:
    return crawl_reddit(url)

print(chatbot.llm_config["tools"])

with Cache.disk() as cache:
    # start the conversation
    res = user_proxy.initiate_chat(
        chatbot, message="can you crawl https://www.reddit.com/r/ETFs/comments/13eoe68/etffund_comparison_tool/", summary_method="reflection_with_llm", cache=cache
    )