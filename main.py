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

import autogen 

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

# Task execution using nested chats
def execute_marketing_analysis(task_description):
    leader.initiate_chat(groupchat_manager, message=f"Initiate project: {task_description}", max_turns=1)
    keywords = creative_director.initiate_chat(groupchat_manager, message="Generate keywords for Reddit search.")
    subreddits = subreddit_agent.initiate_chat(groupchat_manager, message=f"Find subreddits using keywords: {keywords}.")
    posts = post_agent.initiate_chat(groupchat_manager, message=f"Extract posts from these subreddits: {subreddits}.")
    print("IMPORTANTSTUFF", posts)
    # pull out the comments from a post url
    # Output messages to file
    output_to_file('groupchat_messages.json', groupchat.messages)
    
    analysis = data_analyst.initiate_chat(groupchat_manager, message=f"Analyze posts: {posts}.")
    review = reviewer.initiate_chat(groupchat_manager, message="Review the final report.", summary_method="last_msg")
    return review

# Example task
task_description = "Identify the best posts from subreddits talking about beekeeping products."
final_report = execute_marketing_analysis(task_description)
print(final_report)





# # Define the agents

# inner_assistant = autogen.AssistantAgent(
#     "Inner-assistant",
#     llm_config=llm_config,
#     is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
# )

# inner_code_interpreter = autogen.UserProxyAgent(
#     "Inner-code-interpreter",
#     human_input_mode="NEVER",
#     code_execution_config={
#         "work_dir": "coding",
#         "use_docker": False,
#     },
#     default_auto_reply="",
#     is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
# )

# groupchat = autogen.GroupChat(
#     agents=[inner_assistant, inner_code_interpreter],
#     messages=[],
#     speaker_selection_method="round_robin",  # With two agents, this is equivalent to a 1:1 conversation.
#     allow_repeat_speaker=False,
#     max_round=8,
# )

# manager = autogen.GroupChatManager(
#     groupchat=groupchat,
#     is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
#     llm_config=llm_config,
#     code_execution_config={
#         "work_dir": "coding",
#         "use_docker": False,
#     },
# )

# # The Leader Agent who knows the objective and tasks
# leader = autogen.AssistantAgent(
#     "Leader",
#     llm_config=llm_config,
#     system_message="""
#     I am the Leader agent, orchestrating a team of specialized agents to gather
#     and evaluate information from reddit efficiently. 
#     """
# )

# # The Creative Director Agent who brainstorms keywords for searching
# creative_director = autogen.AssistantAgent(
#     "CreativeDirector",
#     llm_config=llm_config,
#     system_message="""
#     As the Creative Director, I am responsible for generating search keywords
#     that will be used to identify relevant subreddits. 
#     """
# )



# # Inner and outer agents
# assistant_1 = autogen.AssistantAgent(
#     name="Assistant_1",
#     llm_config={"config_list": config_list},
# )

# assistant_2 = autogen.AssistantAgent(
#     name="Assistant_2",
#     llm_config={"config_list": config_list},
# )

# writer = autogen.AssistantAgent(
#     name="Writer",
#     llm_config={"config_list": config_list},
#     system_message="""
#     You are a professional writer, known for
#     your insightful and engaging articles.
#     You transform complex concepts into compelling narratives.
#     """,
# )

# reviewer = autogen.AssistantAgent(
#     name="Reviewer",
#     llm_config={"config_list": config_list},
#     system_message="""
#     You are a compliance reviewer, known for your thoroughness and commitment to standards.
#     Your task is to scrutinize content for any harmful elements or regulatory violations, ensuring
#     all materials align with required guidelines.
#     You must review carefully, identify potential issues, and maintain the integrity of the organization.
#     Your role demands fairness, a deep understanding of regulations, and a focus on protecting against
#     harm while upholding a culture of responsibility.
#     """,
# )

# user = autogen.UserProxyAgent(
#     name="User",
#     human_input_mode="NEVER",
#     is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
#     code_execution_config={
#         "last_n_messages": 1,
#         "work_dir": "tasks",
#         "use_docker": False,
#     },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
# )

# # Step 2) Orchestrate Nested Chats to Solve Tasks

# def writing_message(recipient, messages, sender, config):
#     return f"Polish the content to make an engaging and nicely formatted blog post. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"


# nested_chat_queue = [
#     {"recipient": manager, "summary_method": "reflection_with_llm"},
#     {"recipient": writer, "message": writing_message, "summary_method": "last_msg", "max_turns": 1},
#     {"recipient": reviewer, "message": "Review the content provided.", "summary_method": "last_msg", "max_turns": 1},
#     {"recipient": writer, "message": writing_message, "summary_method": "last_msg", "max_turns": 1},
# ]
# assistant_1.register_nested_chats(
#     nested_chat_queue,
#     trigger=user,
# )
# # user.initiate_chat(assistant, message=tasks[0], max_turns=1)

# res = user.initiate_chats(
#     [
#         {"recipient": assistant_1, "message": tasks[0], "max_turns": 1, "summary_method": "last_msg"},
#         {"recipient": assistant_2, "message": tasks[1]},
#     ]
# )


