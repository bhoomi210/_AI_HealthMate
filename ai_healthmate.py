import streamlit as st
import time
from groq import Groq
from streamlit_option_menu import option_menu
from fpdf import FPDF
from dotenv import load_dotenv
import os

# ==============================
# Load Environment Variables
# ==============================
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# ==============================
# Streamlit Config
# ==============================
st.set_page_config(
    page_title="AI HealthMate",
    layout="wide"
)

# ==============================
# Check API Key
# ==============================
if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found in .env file")
    st.stop()

# ==============================
# Initialize Groq Client
# ==============================
client = Groq(api_key=groq_api_key)

# ==============================
# Sidebar Navigation
# ==============================
with st.sidebar:
    st.image(
        "https://i.imgur.com/4NZ6uLY.jpg",
        use_container_width=True
    )

    selected = option_menu(
        menu_title="Navigation",
        options=[
            "Home",
            "Doctor Chat",
            "Symptom Checker",
            "Nutrition Planner",
            "Health Progress",
            "Mental Health Support",
            "Find Doctor",
            "About"
        ],
        icons=[
            "house",
            "chat-dots",
            "search",
            "utensils",
            "graph-up",
            "emoji-smile",
            "hospital",
            "info-circle"
        ],
        menu_icon="list",
        default_index=0,
    )

# ==============================
# Custom CSS
# ==============================
st.markdown("""
<style>
.tip-container{
    border:2px solid #ff5733;
    padding:15px;
    border-radius:10px;
    color:white;
    background-color:#302b63;
    text-align:center;
    font-weight:bold;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# AI Response Function
# ==============================
def get_ai_response(prompt, system_role):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_role
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ==============================
# PDF Generator
# ==============================
def generate_pdf(content, filename="nutrition_plan.pdf"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, content)

    pdf.output(filename)

# ==============================
# Home Page
# ==============================
def home():
    st.title("👨‍⚕️ AI HealthMate")

    st.write("Welcome to your AI-powered healthcare companion.")

    tips = [
        "🥗 Eat colorful fruits and vegetables daily.",
        "💧 Drink enough water.",
        "🏃 Exercise at least 30 minutes everyday."
    ]

    for tip in tips:
        st.markdown(
            f'<div class="tip-container">{tip}</div>',
            unsafe_allow_html=True
        )

    st.subheader("🌟 Health Tip of the Day")

    health_tip = get_ai_response(
        "Give one unique health tip.",
        "You are a healthcare expert."
    )

    st.success(health_tip)

# ==============================
# Doctor Chat
# ==============================
def doctor_chat():
    st.title("💬 Talk to AI Doctor")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Describe your symptoms...")

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        response = get_ai_response(
            prompt,
            "You are an AI doctor."
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.markdown(response)

# ==============================
# Symptom Checker
# ==============================
def symptom_checker():
    st.title("🔍 Symptom Checker")

    symptoms = st.text_area("Enter your symptoms")

    if st.button("Check Symptoms"):

        if symptoms:

            response = get_ai_response(
                f"Analyze these symptoms: {symptoms}",
                "You are a medical symptom checker."
            )

            st.write(response)

        else:
            st.warning("Please enter symptoms.")

# ==============================
# Nutrition Planner
# ==============================
def nutrition_planner():

    st.title("🥗 Nutrition Planner")

    goal = st.selectbox(
        "Select Goal",
        [
            "Weight Loss",
            "Muscle Gain",
            "Balanced Diet"
        ]
    )

    diet = st.selectbox(
        "Diet Preference",
        [
            "Vegetarian",
            "Vegan",
            "Non-Vegetarian"
        ]
    )

    allergies = st.text_input("Food Allergies")

    if st.button("Generate Meal Plan"):

        prompt = f"""
        Create a {goal} meal plan for a {diet} person.
        Avoid: {allergies}
        """

        response = get_ai_response(
            prompt,
            "You are a professional nutritionist."
        )

        st.session_state.nutrition_plan = response

        st.success(response)

        generate_pdf(response)

        with open("nutrition_plan.pdf", "rb") as file:
            st.download_button(
                label="📥 Download PDF",
                data=file,
                file_name="nutrition_plan.pdf",
                mime="application/pdf"
            )

# ==============================
# Health Progress
# ==============================
def health_progress_tracker():

    st.title("📊 Health Progress Tracker")

    if "weight_history" not in st.session_state:
        st.session_state.weight_history = []

    weight = st.number_input(
        "Enter Weight (kg)",
        min_value=20.0,
        max_value=300.0,
        value=70.0
    )

    if st.button("Save Weight"):

        st.session_state.weight_history.append(weight)

        st.success("Weight Saved Successfully")

    if st.session_state.weight_history:
        st.line_chart(st.session_state.weight_history)

# ==============================
# Mental Health
# ==============================
def mental_health_support():

    st.title("🧠 Mental Health Support")

    feeling = st.text_area("How are you feeling today?")

    if st.button("Get Support"):

        if feeling:

            response = get_ai_response(
                feeling,
                "You are a supportive mental health assistant."
            )

            st.write(response)

        else:
            st.warning("Please write something.")

# ==============================
# Doctor Finder
# ==============================
def doctor_finder():

    st.title("👩‍⚕️ Find Doctor")

    location = st.text_input("Enter your city")

    if st.button("Search Doctor"):

        if location:

            doctors = [
                {
                    "name": "Dr. Neha Sharma",
                    "specialty": "Cardiologist"
                },
                {
                    "name": "Dr. Anil Verma",
                    "specialty": "General Physician"
                },
                {
                    "name": "Dr. Fatima Khan",
                    "specialty": "Dermatologist"
                }
            ]

            for doc in doctors:

                st.markdown(f"""
                ### 👨‍⚕️ {doc['name']}
                **Specialty:** {doc['specialty']}
                """)

        else:
            st.warning("Please enter city.")

# ==============================
# About Page
# ==============================
def about():

    st.title("📘 About AI HealthMate")

    st.write("""
    AI HealthMate is an AI-powered healthcare assistant
    built using Streamlit and Groq AI.
    """)

# ==============================
# Routing
# ==============================
if selected == "Home":
    home()

elif selected == "Doctor Chat":
    doctor_chat()

elif selected == "Symptom Checker":
    symptom_checker()

elif selected == "Nutrition Planner":
    nutrition_planner()

elif selected == "Health Progress":
    health_progress_tracker()

elif selected == "Mental Health Support":
    mental_health_support()

elif selected == "Find Doctor":
    doctor_finder()

elif selected == "About":
    about()