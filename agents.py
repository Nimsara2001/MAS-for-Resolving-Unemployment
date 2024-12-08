from crewai import Agent
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
serper_api_key = os.getenv('SERPER_API_KEY')

# Check if API key is present
if not openai_api_key:
    raise ValueError("No OpenAI API key found. Please set OPENAI_API_KEY in your .env file.")
if not serper_api_key:
    raise ValueError("No Serper API key found. Please set SERPER_API_KEY in your .env file.")

# Initialize the Chat LLM
llm = ChatOpenAI(
    api_key=openai_api_key,
    model_name="gpt-4-turbo-preview",
    temperature=0.7
)


# Initialize the search tool (example)
search_tool = SerperDevTool(api_key=serper_api_key)

# Job Seeker Agent
job_seeker_agent = Agent(
    role='Job Seeker',
    goal='Find suitable jobs and recommend relevant training programs.',
    backstory=(
        "You are a proactive job seeker who searches for jobs, requests career advice,"
        "and identifies training opportunities to enhance employability."
    ),
    llm=llm,
    tools=[search_tool],
    verbose=True
)

# Employer Agent
employer_agent = Agent(
    role='Employer',
    goal='Identify potential candidates and refine hiring strategies.',
    backstory=(
        "You are responsible for posting job openings, searching for suitable candidates,"
        "and providing feedback to improve the hiring process."
    ),
    llm=llm,
    tools=[search_tool],
    verbose=True
)

# Market Intelligence Agent
market_intelligence_agent = Agent(
    role='Market Intelligence Analyst',
    goal='Analyze labor market trends to provide insights on skill demands.',
    backstory=(
        "You analyze job data and economic trends to forecast which skills are in demand"
        "and provide insights to both job seekers and employers."
    ),
    llm=llm,
    tools=[search_tool],
    verbose=True
)
