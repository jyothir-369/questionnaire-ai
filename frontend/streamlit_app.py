import streamlit as st
from pathlib import Path
import sys
import os

# Add backend to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.auth import get_authenticator
from backend.database import init_db, save_session, save_answers
from backend.rag import build_vectorstore, answer_question
from backend.export_utils import create_docx
from backend.models import Answer, Question

st.set_page_config(page_title="Questionnaire AI", layout="wide")

init_db()

authenticator = get_authenticator()

# ────────────────────────────────────────────────
# Modern login – returns a tuple (name, authentication_status, username)
name, authentication_status, username = authenticator.login(location='main')

# ────────────────────────────────────────────────
if authentication_status:
    st.title(f"Structured Questionnaire Answering Tool – Welcome {name or username}")

    if "current_answers" not in st.session_state:
        st.session_state.current_answers = []
        st.session_state.session_id = None

    tab1, tab2, tab3 = st.tabs(["1. Upload & Generate", "2. Review", "3. Export"])

    with tab1:
        q_file = st.file_uploader("Questionnaire (PDF)", type=["pdf"])
        ref_files = st.file_uploader("Reference documents", type=["pdf","txt","md"], accept_multiple_files=True)

        if st.button("Process & Generate Answers") and q_file and ref_files:
            with st.spinner("Processing..."):
                upload_dir = Path("uploaded_files")
                upload_dir.mkdir(exist_ok=True)

                q_path = upload_dir / q_file.name
                with open(q_path, "wb") as f:
                    f.write(q_file.getvalue())

                ref_paths = []
                for rf in ref_files:
                    rpath = upload_dir / rf.name
                    with open(rpath, "wb") as f:
                        f.write(rf.getvalue())
                    ref_paths.append(rpath)

                import fitz
                try:
                    doc = fitz.open(q_path)
                    text = "".join(page.get_text("text") + "\n" for page in doc)
                    doc.close()
                except Exception as e:
                    st.error(f"PDF read error: {e}")
                    st.stop()

                lines = [l.strip() for l in text.split("\n") if l.strip()]
                questions = []
                q_num = 1
                for line in lines:
                    if line.endswith("?") or any(line.startswith(f"{j}{s}") for j in range(1,100) for s in ["."," )"]):
                        questions.append(Question(number=q_num, text=line))
                        q_num += 1

                if not questions:
                    st.warning("No questions detected in PDF. Use clear numbered format.")
                    st.stop()

                st.info(f"Detected {len(questions)} questions")

                try:
                    vectorstore = build_vectorstore(ref_paths)
                except Exception as e:
                    st.error(f"Vector store failed: {e}")
                    st.stop()

                answers = []
                progress = st.progress(0)
                for i, q in enumerate(questions):
                    try:
                        ans, cites = answer_question(q.text, vectorstore)
                        answers.append(Answer(question=q, text=ans, citations=cites[:3], not_found="not found" in ans.lower()))
                    except Exception as e:
                        answers.append(Answer(question=q, text=f"Error: {str(e)}", citations=[], not_found=True))
                    progress.progress((i+1) / len(questions))

                sid = save_session(q_file.name)
                save_answers(sid, answers)

                st.session_state.current_answers = answers
                st.session_state.session_id = sid
                st.success(f"Generation done ({len(answers)} answers) → go to Review")

    with tab2:
        if st.session_state.get('current_answers'):
            edited = []
            for i, ans in enumerate(st.session_state.current_answers):
                st.subheader(f"Q{ans.question.number}: {ans.question.text}")
                new_text = st.text_area("Answer", ans.text, height=140, key=f"edit_{i}")
                st.caption("Citations: " + " • ".join(ans.citations) if ans.citations else "None")
                edited.append(Answer(question=ans.question, text=new_text, citations=ans.citations, not_found=ans.not_found))

            if st.button("Save Edits"):
                st.session_state.current_answers = edited
                if st.session_state.session_id:
                    save_answers(st.session_state.session_id, edited)
                st.success("Edits saved")

    with tab3:
        if st.session_state.get('current_answers') and st.button("Download Word"):
            try:
                bio = create_docx(st.session_state.current_answers)
                st.download_button(
                    label="Download answers.docx",
                    data=bio,
                    file_name="answers.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"Export failed: {e}")

    authenticator.logout(location='sidebar', button_name='Logout')

elif authentication_status is False:
    st.error("Incorrect username/password")
elif authentication_status is None:
    st.warning("Please enter your credentials")