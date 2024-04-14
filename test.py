import autogen
import json

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config = {"config_list": config_list}

# tasks = [
#     """Please identify the best posts from subreddits on reddit talking about beekeeping products.""",
#     """Make a pleasant joke about it.""",
# ]

# system input
audience = "someone who is interested in an app for honey intake monitoring"

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
    agents=[leader, creative_director, subreddit_agent],
    messages=[],
    speaker_selection_method="round_robin",
    max_round=10,
    allow_repeat_speaker=False
)

groupchat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Function to handle the output to a file
def output_to_file(filename, data):
    with open(filename, 'a') as file:
        file.write(json.dumps(data, indent=4) + '\n')

# Task execution using nested chats
def execute_marketing_analysis(task_description):
    leader.initiate_chat(groupchat_manager, message=f"Initiate project: {task_description}", max_turns=1)
    keywords = creative_director.initiate_chat(groupchat_manager, message="Generate keywords for Reddit search.")
    subreddits = subreddit_agent.initiate_chat(groupchat_manager, message=f"Find subreddits using keywords: {keywords}.")
    # posts = post_agent.initiate_chat(groupchat_manager, message=f"Extract posts from these subreddits: {subreddits}.")
    print("IMPORTANTSTUFF", subreddits)
    # pull out the comments from a post url
    # Output messages to file
    output_to_file('groupchat_messages.json', groupchat.messages)

    # analysis = data_analyst.initiate_chat(groupchat_manager, message=f"Analyze posts: {posts}.")
    # review = reviewer.initiate_chat(groupchat_manager, message="Review the final report.", summary_method="last_msg")
    return subreddits

# Example task
task_description = "Identify the best posts from subreddits talking about beekeeping products."
final_report = execute_marketing_analysis(task_description)
print(final_report)
