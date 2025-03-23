import streamlit as st
import random
import json
import time



# Load questions
def load_questions(filename="questions.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict) and data:
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("⚠️ Error loading questions. Please check your JSON file.")
    return {}

questions = load_questions()

# Reset the quiz
def restart_quiz():
    st.session_state.clear()
    st.rerun()

# Session State Initialization
default_values = {
    "quiz_started": False,
    "score": 0,
    "question_data": None,
    "category": None,
    "total_questions": 5,
    "questions_asked": 0,
    "answered": False,
    "user_answer": "",
    "used_questions": set(),
    "best_score": 0
}
for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.title("🧠 AI-Powered Quiz Game 🚀")

# Category & Question Selection
if not st.session_state.quiz_started:
    available_categories = list(questions.keys())

    if not available_categories:
        st.error("⚠️ No questions available! Please check your JSON file.")
    else:
        st.session_state.category = st.selectbox("📌 Choose a category:", available_categories)
        st.session_state.total_questions = st.slider("🎯 Select number of questions:", 1, 20, 5)

        if st.button("▶️ Start Quiz"):
            st.session_state.quiz_started = True
            st.session_state.questions_asked = 0
            st.session_state.score = 0
            st.session_state.question_data = None
            st.session_state.answered = False
            st.session_state.user_answer = ""
            st.session_state.used_questions.clear()
            st.rerun()

# Get a new question
def get_new_question():
    category_questions = questions.get(st.session_state.category, [])
    remaining_questions = [q for q in category_questions if q["question"] not in st.session_state.used_questions]

    if not remaining_questions:
        st.warning("⚠️ No more unique questions available in this category!")
        return

    question = random.choice(remaining_questions)
    st.session_state.question_data = question
    st.session_state.answered = False
    st.session_state.user_answer = ""
    st.session_state.used_questions.add(question["question"])

# Load question
if st.session_state.quiz_started:
    if st.session_state.question_data is None or st.session_state.questions_asked >= st.session_state.total_questions:
        get_new_question()

    if st.session_state.question_data:
        # Display question and progress bar
        st.subheader(f"📚 Category: {st.session_state.category.capitalize()}")
        st.progress(st.session_state.questions_asked / st.session_state.total_questions)
        st.write(f"**❓ Question:** {st.session_state.question_data['question']}")

        # Answer input
        user_input = st.text_input("💬 Your answer:", value=st.session_state.user_answer, key=str(st.session_state.questions_asked))

        # Check answer
        if st.button("✅ Submit Answer") and not st.session_state.answered:
            correct_answer = st.session_state.question_data["answer"].strip().lower()
            user_answer = user_input.strip().lower()

            if user_answer == correct_answer:
                st.success(f"🎉 Correct! ✅ The answer is: **{st.session_state.question_data['answer']}**")
                st.session_state.score += 1
            else:
                st.error(f"❌ Incorrect. The correct answer is: **{st.session_state.question_data['answer']}**")

            st.session_state.questions_asked += 1
            st.session_state.answered = True
            time.sleep(1)

        # Next question
        if st.session_state.answered and st.session_state.questions_asked < st.session_state.total_questions:
            if st.button("➡️ Next Question"):
                get_new_question()
                st.rerun()

        # Game Over
        if st.session_state.questions_asked >= st.session_state.total_questions:
            st.subheader(f"🎉 Game Over! Your final score: {st.session_state.score}/{st.session_state.total_questions}")

            # Update best score
            if st.session_state.score > st.session_state.best_score:
                st.session_state.best_score = st.session_state.score
                st.balloons()  # 🎉 Celebration if best score is achieved
                st.success("🎊 New High Score!")

            st.write(f"🏆 Best Score: {st.session_state.best_score}")

            if st.button("🔄 Restart Quiz"):
                restart_quiz()
