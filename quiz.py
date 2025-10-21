import streamlit as st
import json
import base64
import random
import os

st.set_page_config(page_title="📚 Quiz App", layout="centered")
QUESTION_DIR = "questions"
PDF_DIR = "study_guide"
st.sidebar.title("📘 Select Class & Page")

# List class options
quiz_files = [f for f in os.listdir(QUESTION_DIR) if f.endswith(".json")]
class_options = [f.replace(".json", "").upper() for f in quiz_files]

selected_class = st.sidebar.selectbox("Choose Class", class_options)
page = st.sidebar.radio("Go to", ["Quiz", "Study Guide"])

# Quiz Page
if page == "Quiz":
    st.title(f"🧪 {selected_class} Quiz")

    file_path = os.path.join(QUESTION_DIR, f"{selected_class.lower()}.json")
    try:
        with open(file_path, "r") as f:
            questions = json.load(f)
    except Exception as e:
        st.error(f"Failed to load quiz for {selected_class}: {e}")
        st.stop()

    # Shuffle only once per class
    if "shuffled_questions" not in st.session_state or st.session_state.get("current_class") != selected_class:
        random.shuffle(questions)
        st.session_state.shuffled_questions = questions
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.submitted = False
        st.session_state.selected = None
        st.session_state.current_class = selected_class

    q_index = st.session_state.current_q
    current_q = st.session_state.shuffled_questions[q_index]

    st.write(f"**Question {q_index + 1} of {len(questions)}**")
    selected = st.radio(current_q["question"], current_q["options"], key=f"radio_{q_index}")

    if st.button("Submit Answer") and not st.session_state.submitted:
        st.session_state.selected = selected
        st.session_state.submitted = True
        if selected == current_q["answer"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrect. The correct answer is: **{current_q['answer']}**")
            if "why" in current_q:
                st.info(f"💡 Explanation: {current_q['why']}")

    if st.session_state.submitted:
        if st.button("Next Question"):
            if q_index < len(questions) - 1:
                st.session_state.current_q += 1
                st.session_state.submitted = False
                st.session_state.selected = None
                st.rerun()
            else:
                st.balloons()
                st.success(f"🎉 Quiz complete! Final score: **{st.session_state.score} / {len(questions)}**")

# Study Guide Page
elif page == "Study Guide":
    st.title(f"📘 Study Guide: {selected_class}")

    # Map class to PDF URL
    pdf_urls = {
        "CSE 185": "https://raw.githubusercontent.com/rcamacho11/StudyGuide/8b1832f922475b3970228a5941eac234c7ae0cfe/study_guides/cse185.pdf",
        # Add more here for other classes
    }

    if selected_class in pdf_urls:
        pdf_url = pdf_urls[selected_class]
        pdfjs_viewer = f"https://mozilla.github.io/pdf.js/web/viewer.html?file={pdf_url}"

        st.markdown(
            f'<iframe src="{pdfjs_viewer}" width="100%" height="900px" style="border: none;"></iframe>',
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ No PDF study guide found for this class yet.")
