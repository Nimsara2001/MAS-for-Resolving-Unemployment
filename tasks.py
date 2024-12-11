from crewai import Task


# tasks.py
def create_job_search_task(job_seeker_agent, user_profile):
    return Task(
        description=f"""
        Analyze job opportunities in Sri Lanka matching:
        - Skills: {user_profile.get('technical_skills', [])}
        - Experience: {user_profile.get('years_of_experience')}
        - Location preferences: {user_profile.get('location', 'Not specified')}
        - Preferred roles: {user_profile.get('preferred_roles', [])}
        Consider both local and foreign employment opportunities.
        Focus on economically stable sectors in current market.
        """,
        expected_output="A detailed list of suitable job opportunities with requirements and prospects",
        agent=job_seeker_agent
    )

def create_market_analysis_task(market_intelligence_agent, user_profile):
    return Task(
        description=f"""
        Analyze Sri Lankan market conditions:
        - Growth sectors during economic recovery
        - Salary ranges in local currency
        - Foreign employment opportunities
        - Skills in demand locally and internationally
        Recommend best path forward considering current economic situation.
        """,
        expected_output="Comprehensive market analysis with growth sectors and opportunities",
        agent=market_intelligence_agent
    )

def create_final_recommendation_task(employer_agent, user_profile, market_analysis):
    return Task(
        description=f"""
        Create detailed career recommendation considering:
        1. Candidate profile and skills: {user_profile}
        2. Market analysis findings: {market_analysis}
        3. Economic stability of recommended path
        4. Growth potential in next 2-3 years
        
        Format output in markdown with:
        - Recommended career path
        - Required upskilling
        - Salary expectations
        - Growth roadmap
        - Alternative options
        """,
        expected_output="Detailed career recommendation report in markdown format",
        agent=employer_agent
    )