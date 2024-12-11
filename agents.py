from crewai import Agent, Task
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json
from typing import Dict

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
    model_name="gpt-3.5-turbo", #gpt-3.5-turbo
    temperature=0.7
)

# Initialize the search tool (example)
search_tool = SerperDevTool(api_key=serper_api_key)


def get_user_input() -> str:
    print("\n=== Welcome to the Job Search Assistant ===")
    print("Please provide a brief description about yourself:")
    return input("> ")


def save_profile(data: Dict, filename: str = "user_profile.json") -> None:
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def interactive_profile_gathering(initial_description: str) -> Dict:
    required_fields = {
        "technical_skills": [],
        "skill_levels": {},
        "years_of_experience": None,
        "education": None,
        "preferred_roles": [],
        "industry_preference": None,
        "salary_expectation": None
    }

    profile = {
        "initial_description": initial_description,
        **required_fields
    }

    conversation = []
    max_questions = 5

    print("\nAgent is analyzing your profile...")

    for i in range(max_questions):
        analysis_task = Task(
            description=f"""
            Based on the profile so far: {profile}
            Ask ONE important missing question to better understand the candidate's profile.
            Focus on technical skills, experience, and career goals.
            Respond with JUST the question, nothing else.
            """,
            expected_output="A single clear question about missing profile information",
            agent=job_seeker_agent
        )

        response = job_seeker_agent.execute_task(analysis_task)
        print(f"\n{response}")
        answer = input("> ")
        conversation.append({"question": response, "answer": answer})
        profile["conversation"] = conversation

        if len(conversation) >= 3 and all(profile.values()):
            break

    return profile


job_seeker_agent = Agent(
    role='Job Seeker Advisor',
    goal='Understand candidate profile and match with Sri Lankan job market opportunities',
    backstory=(
        "You are an expert Sri Lankan career counselor who understands local job market dynamics "
        "and economic conditions. You help job seekers identify their strengths and match them "
        "with sustainable career paths during the economic recovery period."
    ),
    llm=llm,
    # tools=[search_tool],
    verbose=True
)

employer_agent = Agent(
    role='Sri Lankan Industry Expert',
    goal='Identify viable employment opportunities in Sri Lankan market',
    backstory=(
        "You represent Sri Lankan employers and understand current industry needs, "
        "growth sectors, and employment trends during economic recovery. You know which "
        "sectors are actively hiring and what skills are in demand locally and for foreign employment."
    ),
    llm=llm,
    # tools=[search_tool],
    verbose=True
)

market_intelligence_agent = Agent(
    role='Sri Lankan Market Analyst',
    goal='Analyze Sri Lankan labor market trends and economic recovery patterns',
    backstory=(
        "You analyze Sri Lankan economic data, emerging industries, and workforce trends. "
        "You understand which sectors are growing despite economic challenges and where "
        "new opportunities are emerging, including foreign employment possibilities."
    ),
    llm=llm,
    # tools=[search_tool],
    verbose=True
)
