"""
This module provides functionality to autonomously crawl and scrape Reddit posts using
selenium and BeautifulSoup. It uses autonomous agents configured via the autogen library to handle specific tasks related
to web searching on Reddit, including extracting post contents and comments, and gathering URLs for posts based on search
keywords. It employs headless Chrome browsers for web navigation, ensuring that operations can be conducted without
the need for a GUI.

Classes:
    AssistantAgent: Manages and executes operations for scraping Reddit data.
    UserProxyAgent: Proxies user inputs and manages conversation states and terminations.

Functions:
    crawl_reddit_imp(url: str) -> str: Crawls a specific Reddit URL to extract detailed post data.
    crawl_reddit_post_url_imp(keywords: str) -> list: Searches Reddit with specified keywords and extracts post URLs.
    crawl_reddit(url: Annotated[str, "link to the reddit post"]) -> str: Agent-registered function to scrape a Reddit post.
    crawl_reddit_post_url(keywords: Annotated[str, "keywords to search for"]) -> str: Agent-registered function to find Reddit posts by keywords.

Dependencies:
    pydantic: Used for data parsing and validation through BaseModel.
    selenium: Utilized for browser automation tasks.
    BeautifulSoup: Employed for parsing HTML contents.
    autogen: Provides framework support for autonomous agents.
"""
import time
from typing import Literal

from pydantic import BaseModel, Field
from typing_extensions import Annotated

import autogen
from autogen.cache import Cache

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
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
    code_execution_config={
        "use_docker": False,
    },
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "use_docker": False,
    },
)


def crawl_reddit_imp(url: str):
    """
    Performs a detailed crawl of a specific Reddit post URL using Selenium with a headless Chrome browser.
    It extracts the title, content, and author of the post, as well as all associated comments.

    Args:
        url (str): The URL of the Reddit post to be crawled.

    Returns:
        str: A formatted string containing the main post's title, author, content, and all comments with their respective authors.

    Raises:
        WebDriverException: An error occurred with the Selenium WebDriver during the process.
        Exception: Generic exceptions could include errors during HTML parsing or during web navigation.
    """
    print("Crawling Reddit post at: ", url)
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

    return allcontent


def crawl_reddit_post_url_imp(keywords: str):
    """
    Searches Reddit for posts matching specified keywords and returns a list of URLs for those posts. This function uses
    Selenium with a headless Chrome browser to navigate the Reddit search page and parse results using BeautifulSoup.

    Args:
        keywords (str): The keywords to use for searching posts on Reddit.

    Returns:
        list: A list of unique URLs pointing to Reddit posts that match the search criteria.

    Raises:
        WebDriverException: An error occurred with the Selenium WebDriver during the process.
        Exception: Generic exceptions could include errors during HTML parsing or during web navigation.
    """
    url = "https://www.reddit.com/search/?q=" + keywords.replace(" ", "+")
    print("Crawling Reddit posts at: ", url)
    # Create a new instance of the Firefox driver
    try:
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        driver = webdriver.Chrome(options=options)

        # Load a URL
        driver.get(url)

        time.sleep(3)

        # Get the HTML content
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

    except Exception as e:
        print("Error in crawling Reddit posts at: ", url)
        print(e)
    # Now you can use the soup object to parse and manipulate the HTML content
    # For example, you can find elements by tag name, class, etc.

    # Close the browser
    driver.quit()

    allcontent = []

    # Find all <p> elements and concatenate their content into a string
    links = soup.find_all('a')

    for element in soup.find_all():
        print("element:")
        print(element.name)

    for link in links:
        if link.get('href').startswith("/r/") and "/comments/" in link.get('href'):
            print("found link: ", link.get('href'))
            found_url = "https://www.reddit.com" + link.get('href')
            allcontent.append(found_url)
        else:
            print("INVALID LINK??: ", link.get('href'))

    return list(set(allcontent))


@user_proxy.register_for_execution()
@chatbot.register_for_llm(description="scrawl and scrap reddit post content")
def crawl_reddit(
        url: Annotated[str, "link to the reddit post"],
) -> str:
    """
    Facilitates scraping of a specific Reddit post's content by invoking the `crawl_reddit_imp` function.
    This function is designed to be registered with an autonomous agent for execution.

    Args:
        url (Annotated[str, "link to the reddit post"]): The URL of the Reddit post to be scraped.

    Returns:
        str: The detailed content of the Reddit post including post details and comments.
    """
    return crawl_reddit_imp(url)


@user_proxy.register_for_execution()
@chatbot.register_for_llm(description="get the link to the reddit posts")
def crawl_reddit_post_url(
        keywords: Annotated[str, "keywords to search for"],
) -> str:
    """
    Facilitates the search of Reddit posts by keywords and retrieves their URLs by invoking the `crawl_reddit_post_url_imp` function.
    This function is designed to be registered with an autonomous agent for execution.

    Args:
        keywords (Annotated[str, "keywords to search for"]): Keywords to search for on Reddit.

    Returns:
        list: A list of URLs to the Reddit posts that match the specified keywords.
    """
    return crawl_reddit_post_url_imp(keywords)


print(chatbot.llm_config["tools"])


def reddit_analysis(task_description):
    with Cache.disk() as cache:
        # start the conversation
        res = user_proxy.initiate_chat(
            chatbot, message=task_description, summary_method="reflection_with_llm", cache=cache
        )
    return res.chat_history


if __name__ == '__main__':
    # Example task
    task_description = "find reddit posts related to beekeeping and give me the summary with the link to the posts"
    reddit_analysis(task_description)
