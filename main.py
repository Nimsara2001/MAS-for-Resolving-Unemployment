from crewai import Crew, Process
from agents import job_seeker_agent, employer_agent, market_intelligence_agent
from tasks import job_search_task, candidate_search_task, market_analysis_task

# Define the crew with agents and tasks
job_market_crew = Crew(
    agents=[job_seeker_agent, employer_agent, market_intelligence_agent],
    tasks=[job_search_task, candidate_search_task, market_analysis_task],
    process=Process.sequential  # Agents execute tasks one after the other
)

# Example usage
if __name__ == "__main__":
    # Input data for the kickoff process
    inputs = {
        'skills': 'Python, Data Analysis',
        'location': 'New York',
        'job_preferences': 'Remote work, Technology sector'
    }

    # Execute the crew's tasks
    result = job_market_crew.kickoff(inputs=inputs)
    print(result)
