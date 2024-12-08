from crewai import Task
from agents import job_seeker_agent, employer_agent, market_intelligence_agent

# Task for Job Seeker Agent
job_search_task = Task(
    description=(
        "Search for job opportunities based on the user's skills, location, and preferences. "
        "Provide a list of matched jobs and relevant training recommendations."
    ),
    expected_output="A list of matched job postings and suggested training programs.",
    agent=job_seeker_agent
)

# Task for Employer Agent
candidate_search_task = Task(
    description=(
        "Post job descriptions and search for potential candidates who match the required skills "
        "and location. Provide a report of suitable candidates and feedback on hiring needs."
    ),
    expected_output="A list of suitable candidates and a hiring feedback report.",
    agent=employer_agent
)

# Task for Market Intelligence Agent
market_analysis_task = Task(
    description=(
        "Analyze recent job market and economic data to forecast skill demands. "
        "Provide insights on which skills are in demand and economic trends affecting employment."
    ),
    expected_output="A detailed report on skill demand forecasts and economic trends.",
    agent=market_intelligence_agent
)
