# app.py
import streamlit as st
from crewai import Crew, Process, Task

# Add imports at top
from agents import (
    job_seeker_agent, employer_agent, market_intelligence_agent, save_profile
)
from tasks import (
    create_job_search_task, create_market_analysis_task,
    create_final_recommendation_task
)


def process_career_recommendation():
    if "processing_started" not in st.session_state:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🔍 Starting the career analysis process..."
        })
        st.session_state.processing_started = True

    with st.status("Creating career recommendations...") as status:
        # Job Seeker Analysis
        st.write("📊 Job Seeker Agent analyzing profile...")
        job_search = create_job_search_task(job_seeker_agent, st.session_state.profile)
        job_search_result = job_seeker_agent.execute_task(job_search)
        # st.session_state.messages.append({
        #     "role": "assistant",
        #     "content": f"👨‍💼 **Job Seeker Agent's Analysis:**\n\n{job_search_result}"
        # })

        # Market Intelligence Analysis
        st.write("📈 Market Intelligence Agent analyzing conditions...")
        market_analysis = create_market_analysis_task(market_intelligence_agent, st.session_state.profile)
        market_analysis_result = market_intelligence_agent.execute_task(market_analysis)
        # st.session_state.messages.append({
        #     "role": "assistant",
        #     "content": f"📊 **Market Intelligence Agent's Findings:**\n\n{market_analysis_result}"
        # })

        # Employer Analysis and Final Recommendation
        st.write("🎯 Employer Agent creating final recommendations...")
        final_recommendation = create_final_recommendation_task(
            employer_agent,
            st.session_state.profile,
            market_analysis_result
        )
        final_result = employer_agent.execute_task(final_recommendation)
        
        # Update session state
        st.session_state.final_recommendation = final_result
        st.session_state.current_stage = "complete"

        # Add summary message
        st.session_state.messages.append({
            "role": "assistant",
            "content":"🚀 Final Career Recommendations:"
        })

        status.update(label="Analysis complete!", state="complete")
        st.rerun()


def init_session_state():
    # Initialize all state variables at start
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Hello! Please provide a brief description about yourself:"
        }]
    if "waiting_for_description" not in st.session_state:
        st.session_state.waiting_for_description = True
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = None
    if "current_stage" not in st.session_state:
        st.session_state.current_stage = "initial"
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    if "profile" not in st.session_state:
        st.session_state.profile = {
            "technical_skills": [],
            "skill_levels": {},
            "years_of_experience": None,
            "education": None,
            "preferred_roles": [],
            "industry_preference": None,
            "salary_expectation": None,
            "conversation": []
        }


def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💼" if message["role"] == "assistant" else None):
            st.markdown(message["content"])


def get_initial_description():
    # Only handle user input, greeting is already displayed
    if prompt := st.chat_input("Type your message..."):
        # Verify this is actually a description before proceeding
        if st.session_state.waiting_for_description:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.current_stage = "questioning"
            st.session_state.initial_description = prompt
            st.session_state.profile["initial_description"] = prompt
            st.session_state.waiting_for_description = False
            return prompt
    return None


def handle_profile_gathering():
    if st.session_state.question_count < 5:
        # Display current profile status
        st.write(f"Questions answered: {st.session_state.question_count}/5")
        
        # Get or create next question
        if not hasattr(st.session_state, 'current_question'):
            analysis_task = Task(
                description=f"""
                Based on the profile so far: {st.session_state.profile}
                Ask ONE important missing question focusing on:
                - Technical skills and proficiency levels
                - Years of experience
                - Education and qualifications
                - Preferred job roles
                - Industry preferences
                - Expected salary range in LKR
                Previous conversation: {st.session_state.profile.get('conversation', [])}
                Ask only what's missing. Be specific and direct.
                """,
                expected_output="A single clear question about missing profile information",
                agent=job_seeker_agent
            )
            
            question = job_seeker_agent.execute_task(analysis_task)
            st.session_state.current_question = question
            st.session_state.messages.append({
                "role": "assistant", 
                "content": question
            })
            st.rerun()  # Ensure question is displayed before accepting input

        # Handle user input
        if prompt := st.chat_input("Your answer..."):
            # Validate input is not empty
            if prompt.strip():
                # Update messages
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Update profile based on question context
                if "technical skills" in st.session_state.current_question.lower():
                    st.session_state.profile["technical_skills"] = [s.strip() for s in prompt.split(",")]
                elif "experience" in st.session_state.current_question.lower():
                    st.session_state.profile["years_of_experience"] = prompt
                elif "education" in st.session_state.current_question.lower():
                    st.session_state.profile["education"] = prompt
                elif "role" in st.session_state.current_question.lower():
                    st.session_state.profile["preferred_roles"] = [r.strip() for r in prompt.split(",")]
                elif "industry" in st.session_state.current_question.lower():
                    st.session_state.profile["industry_preference"] = prompt
                elif "salary" in st.session_state.current_question.lower():
                    st.session_state.profile["salary_expectation"] = prompt

                # Store conversation
                st.session_state.profile["conversation"].append({
                    "question": st.session_state.current_question,
                    "answer": prompt
                })
                
                # Update state
                st.session_state.question_count += 1
                delattr(st.session_state, 'current_question')

                # Check completion
                if st.session_state.question_count >= 5:
                    st.session_state.current_stage = "processing"
                    save_profile(st.session_state.profile)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Thank you! Starting market analysis..."
                    })
                
                st.rerun()


def main():
    st.title("Sri Lankan Job Market Career Advisor")
    
    # Initialize state
    init_session_state()
    
    # Display chat history
    display_chat()
    
    # Handle different stages
    if st.session_state.current_stage == "initial":
        get_initial_description()
    elif st.session_state.current_stage == "questioning":
        handle_profile_gathering()
    elif st.session_state.current_stage == "processing":
        process_career_recommendation()
    elif st.session_state.current_stage == "complete":
        st.markdown(st.session_state.final_recommendation)


if __name__ == "__main__":
    main()
