import autogen
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Configuration and Initialization
config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config = {"config_list": config_list}

# Define specialized agents
leader = autogen.AssistantAgent("Leader", llm_config=llm_config, system_message="I orchestrate the team to gather and evaluate information efficiently.")
creative_director = autogen.AssistantAgent("CreativeDirector", llm_config=llm_config, system_message="I generate search keywords to find relevant subreddits.")
subreddit_agent = autogen.AssistantAgent("SubredditAgent", llm_config=llm_config, system_message="I locate subreddits based on the provided keywords.")
post_agent = autogen.AssistantAgent("PostAgent", llm_config=llm_config, system_message="I retrieve and analyze posts from the identified subreddits.")
data_analyst = autogen.AssistantAgent("DataAnalyst", llm_config=llm_config, system_message="I analyze the posts to extract marketing insights.")
reviewer = autogen.AssistantAgent("Reviewer", llm_config=llm_config, system_message="I ensure the content complies with standards and regulations.")

# Main chat and manager
groupchat = autogen.GroupChat(
    agents=[leader, creative_director, subreddit_agent, post_agent, data_analyst, reviewer],
    messages=[],
    speaker_selection_method="round_robin",
    max_round=10,
    allow_repeat_speaker=False
)

groupchat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Web crawler function
def crawl_reddit(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    posts = soup.find_all('div', class_='Post')
    content = [{'title': post.find('h3').text if post.find('h3') else "No title",
                'text': post.find('p').text if post.find('p') else "No content"} for post in posts]
    driver.quit()
    return content

# Function to handle the output to a file
def output_to_file(filename, data):
    with open(filename, 'a') as file:
        file.write(json.dumps(data, indent=4) + '\n')

import re

def execute_marketing_analysis(task_description):
    # Initiate project and gather data
    leader.initiate_chat(groupchat_manager, message=f"Initiate project: {task_description}")
    creative_director.initiate_chat(groupchat_manager, message="Generate keywords for Reddit search.")
    subreddit_result = subreddit_agent.initiate_chat(groupchat_manager, message="Find subreddits using keywords.")
    post_agent.initiate_chat(groupchat_manager, message="Extract posts from these subreddits.")
    
    # Extract subreddit names from the messages
    subreddit_names = []
    for message in groupchat.messages:
        found = re.findall(r"r/\w+", message.content)  # Regex to find patterns like 'r/subredditName'
        subreddit_names.extend(found)

    # Assume you have a function to convert subreddit names to URLs or directly use them
    subreddit_urls = [f"https://www.reddit.com/{name}" for name in subreddit_names]

    # Use the extracted URLs for further processing
    posts_data = [crawl_reddit(url) for url in subreddit_urls]
    data_analyst.initiate_chat(groupchat_manager, message=f"Analyze posts: {json.dumps(posts_data)}")
    review = reviewer.initiate_chat(groupchat_manager, message="Review the final report.", summary_method="last_msg")

    # Output messages to file
    output_to_file('groupchat_messages.json', groupchat.messages)

    return review.content  # Assuming the review message has a 'content' attribute with the final text


# Example task execution
task_description = "Identify the best posts from subreddits talking about beekeeping products."
final_report = execute_marketing_analysis(task_description)
print(final_report)


# # Example task execution
# task_description = "Identify the best posts from subreddits talking about beekeeping products."
# final_report = execute_marketing_analysis(task_description)
# print(final_report)
