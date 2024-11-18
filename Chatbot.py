import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
from typing import Optional
import random

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

def generate_lesson_plan_with_openai(
    enquiry_question: str,
    year_group: str,
    num_lessons: int,
    objectives: str,
    active_learning: str,
    adaptive_practices: str
) -> Optional[str]:
    """Generate a lesson plan using OpenAI's GPT model"""
    prompt = f"""
    As an expert educator, create a detailed lesson plan for primary school children in {year_group}.
    Design a sequence of {num_lessons} lessons to address the enquiry question: "{enquiry_question}".
    The lesson order has to be sequential, in order to build on the understanding of previous lessons.
    
    Key Requirements:
    1. Use Bloom's Taxonomy for learning objectives
    2. Include active learning components
    3. Incorporate adaptive teaching strategies
    4. Ensure progression across lessons
    
    Specific Inputs:
    - Learning Objectives: {objectives}
    - Active Learning Activities: {active_learning}
    - Adaptive Teaching Practices: {adaptive_practices}
    
    For each lesson, provide:
    1. Lesson Title & Learning Objective
    2. Key Vocabulary
    3. Main Activities (including timings)
    4. Differentiation Strategies
    5. Assessment Opportunities
    6. Resources Needed
    7. Home Learning Extensions
    
    Format the output using markdown for clear structure.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an experienced educator with expertise in lesson planning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating lesson plan: {str(e)}")
        return None

def refine_lesson_plan_with_openai(base_plan: str, user_comments: str) -> Optional[str]:
    """Refine the lesson plan using OpenAI's GPT model based on user comments."""
    prompt = f"""
    You are an expert educator. Refine the following lesson plan based on the user's comments.
    
    Base Lesson Plan:
    {base_plan}
    
    User Comments:
    {user_comments}
    
    Provide a revised lesson plan incorporating the user's feedback.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an experienced educator with expertise in lesson planning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error refining lesson plan: {str(e)}")
        return None

def get_chat_response(conversation_history, user_input):
    """Get response from OpenAI for chat refinements"""
    try:
        messages = [
            {"role": "system", "content": "You are an expert educator helping to refine and improve lesson plans. Provide specific, actionable suggestions and be ready to modify the plan based on teacher requests."}
        ] + conversation_history + [
            {"role": "user", "content": user_input}
        ]
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=0.5,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response: {str(e)}"

def main():
    # Configure page
    st.set_page_config(
        page_title="✨ Smart Lesson Planner",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for dark theme (previous CSS remains the same)
    st.markdown("""
        <style>
        /* Main container styling */
        .stApp {
            background-color: #0e1117;
        }

        
        /* Chat container */
        .chat-container {
            background-color: #1a1c23;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border: 1px solid #2d3139;
        }
        
        .chat-message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
        }
        
        .user-message {
            background-color: #2d3139;
        }
        
        .assistant-message {
            background-color: #1e222b;
        }
        
        /* Rest of the CSS remains the same */
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state for chat
    if 'generated_plan' not in st.session_state:
        st.session_state.generated_plan = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Main UI
    if not st.session_state.generated_plan:
        # Display input fields for generating a lesson plan
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="dark-container">', unsafe_allow_html=True)
            st.subheader("📝 Lesson Requirements")
            enquiry_question = st.text_area("Main enquiry question",
                                          height=100,
                                          placeholder="What is your main enquiry question?")
            
            st.subheader("📌 Adaptive Teaching")
            adaptive_practices = st.text_area("Adaptive teaching practices",
                                           height=100,
                                           placeholder="Outline your adaptive teaching approaches...")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.subheader("👩‍🏫 Year Group")
            year_group = st.selectbox("Select year group:",
                                    ["Reception", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"])
            
            

        with col2:
            st.markdown('<div class="dark-container">', unsafe_allow_html=True)
            st.subheader("🎯 Learning Objectives")
            objectives = st.text_area("Learning objectives",
                                    height=100,
                                    placeholder="Enter your learning objectives...")
            
            st.subheader("🔄 Active Learning Activities")
            active_learning = st.text_area("Active learning strategies",
                                         height=100,
                                         placeholder="Describe your active learning activities...")
            
            
            
            st.subheader("📚 Number of Lessons")
            num_lessons = st.slider("Number of lessons", 1, 10, 3)
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🚀 Generate Lesson Plan"):
            if not all([enquiry_question, objectives, active_learning, adaptive_practices]):
                st.warning("⚠️ Please fill out all fields to generate a lesson plan!")
            else:
                with st.spinner("🔄 Little gnomes working on the lesson plan..."):
                    generated_plan = generate_lesson_plan_with_openai(
                        enquiry_question,
                        year_group,
                        num_lessons,
                        objectives,
                        active_learning,
                        adaptive_practices
                    )
                    
                    if generated_plan:
                        st.session_state.generated_plan = generated_plan
                        st.success("✅ Lesson plan generated successfully!")
                        st.rerun()  # Rerun the app to update the UI
                        

    else:
        # Display the chat interface
        st.markdown('<div class="dark-container">', unsafe_allow_html=True)
        st.subheader("💬 Now you have your lesson plan!")
        st.markdown("Ask questions  or request modifications at the bottom of the page to make changes to your lesson plan.")
        
        # Ensure the generated plan is added to chat history
        if not st.session_state.chat_history:
            st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.generated_plan})
        
        # Display chat history
        for message in st.session_state.chat_history:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f'<div class="chat-message user-message">👤 You: {content}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message">🤖 Assistant: {content}</div>', 
                          unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_area("Your message:", key="chat_input", height=100)
        if st.button("Send"):
            if user_input:
                # Add user message to history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Refine lesson plan based on user input
                refined_plan = refine_lesson_plan_with_openai(st.session_state.generated_plan, user_input)
                
                # Add refined plan to history
                st.session_state.chat_history.append({"role": "assistant", "content": refined_plan})
                
                # Update the generated plan with the refined version
                st.session_state.generated_plan = refined_plan
                
        
        # Download button
        st.download_button(
            label="📥 Download Lesson Plan",
            data=st.session_state.generated_plan,
            file_name=f"lesson_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/markdown"
        )
        
        if st.button("🔄 Create New Plan"):
            st.session_state.generated_plan = None
            st.session_state.chat_history = []
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()