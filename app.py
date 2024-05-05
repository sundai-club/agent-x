from pydantic import BaseModel
from fastapi import FastAPI
from reddit_crawling_agent import reddit_analysis

app = FastAPI()


class Item(BaseModel):
    message: str


@app.post("/post-message/test")
def post_message(item: Item):
    test_msg = [{'content': 'Review the final report.', 'role': 'assistant'}, {
        'content': 'Before reviewing the final report, our team will follow these steps to ensure an efficient gathering and evaluation of information:\n\n1. Review the report outline to understand the structure and content.\n2. Divide the team into groups to focus on specific sections of the report.\n3. Assign team members to gather data and information relevant to their assigned sections.\n4. Conduct thorough research and analysis to verify the accuracy and relevance of the information collected.\n5. Compile the findings and recommendations into a cohesive draft report for review.\n6. Seek feedback from team members to refine the content and ensure consistency.\n7. Finalize the report by incorporating all feedback and ensuring that it meets the requirements and objectives set at the beginning of the project.\n\nFollowing these steps will help our team gather and evaluate information efficiently, leading to a comprehensive and well-structured final report for your review.',
        'name': 'Leader', 'role': 'user'}, {
                    'content': '1. document review process\n2. review team steps for evaluation\n3. evaluate final report steps\n4. gather information efficiently\n5. report review process\n6. review methodology steps\n7. analysis of final report\n8. team feedback for report refinement\n9. finalize project report\n10. ensure report meets project objectives',
                    'name': 'CreativeDirector', 'role': 'user'}, {
                    'content': 'Based on the keywords provided, I have found a few relevant subreddits that you might find helpful:\n\n1. r/projectmanagement\n2. r/Research\n3. r/businessanalysis\n4. r/technicalwriting\n5. r/dataanalysis\n6. r/corporatecommunications\n\nThese subreddits cover topics related to project management, research, analysis, writing, and communication, which could be useful for discussions and insights on reviewing and evaluating reports.',
                    'name': 'SubredditAgent', 'role': 'user'}, {
                    'content': "I will retrieve and analyze posts from the identified subreddits to gather insights on reviewing and evaluating reports. Let's begin with the first subreddit, r/projectmanagement. I will be back shortly with the relevant information and insights.",
                    'name': 'PostAgent', 'role': 'user'}, {
                    'content': "I will now gather and analyze posts from the subreddit r/projectmanagement to gather insights on reviewing and evaluating reports. Let's see what information and insights we can extract from the discussions in this subreddit.",
                    'name': 'DataAnalyst', 'role': 'user'}, {
                    'content': 'Analyzing posts from the subreddit r/projectmanagement can provide valuable insights into effective strategies and best practices for reviewing and evaluating reports. By examining the discussions and recommendations shared by project management professionals, we can gain a deeper understanding of the key considerations and approaches in this context. Once the analysis is done, we can incorporate any relevant findings into our report evaluation process to enhance its quality and effectiveness.',
                    'role': 'assistant'}, {
                    'content': 'Analyzing posts from the subreddit r/projectmanagement can indeed provide valuable insights for our review process. We can gain knowledge about effective strategies, best practices, and common challenges faced by project managers when reviewing and evaluating reports. By incorporating these insights into our evaluation process, we can improve our approach and ensure a more thorough and accurate assessment of the final report. I will proceed with the analysis and extract relevant information to enhance our review process.',
                    'name': 'Leader', 'role': 'user'}, {
                    'content': 'Great! Analyzing posts from the subreddit r/projectmanagement will provide valuable insights that can help improve your review process. If you need any assistance or guidance during the analysis, feel free to let me know. Good luck with extracting meaningful information to enhance your report evaluation process!',
                    'name': 'CreativeDirector', 'role': 'user'}, {
                    'content': "If you need any further assistance with analyzing the posts from the subreddit r/projectmanagement or have any other requests, feel free to let me know. I'm here to help! Good luck with gathering valuable insights to improve your report evaluation process.",
                    'name': 'SubredditAgent', 'role': 'user'}]

    return {"market_analysis": test_msg}


@app.post("/post-message")
def post_message(item: Item):
    return {"market_analysis": reddit_analysis(item.message)}
