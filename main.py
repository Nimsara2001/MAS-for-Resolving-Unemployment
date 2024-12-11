from crewai import Crew, Process
from agents import job_seeker_agent, employer_agent, market_intelligence_agent

from agents import get_user_input, interactive_profile_gathering, save_profile
from tasks import create_final_recommendation_task, create_job_search_task, create_market_analysis_task

# main.py
if __name__ == "__main__":
    initial_description = get_user_input()
    user_profile = interactive_profile_gathering(initial_description)
    save_profile(user_profile)
    
    # Create tasks with proper parameters
    job_search = create_job_search_task(job_seeker_agent, user_profile)
    market_analysis = create_market_analysis_task(market_intelligence_agent, user_profile)
    final_recommendation = create_final_recommendation_task(employer_agent, user_profile, market_analysis)
    
    # Define crew
    career_advisor_crew = Crew(
        agents=[job_seeker_agent, employer_agent, market_intelligence_agent],
        tasks=[job_search, market_analysis, final_recommendation],
        process=Process.sequential
    )
    
    result = career_advisor_crew.kickoff()
    print("\n=== Career Recommendation for Sri Lankan Job Market ===")
    print(result)