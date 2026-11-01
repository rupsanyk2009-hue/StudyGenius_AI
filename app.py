import streamlit as st
import json
import random
import re
from pathlib import Path
from datetime import date, datetime, timedelta

# ============================================================
# STUDYGENIUS AI — School exhibition prototype
# Runs locally with Streamlit. No API key or internet AI service
# is required. Some "AI-style" tools use transparent local logic.
# ============================================================

st.set_page_config(
    page_title="StudyGenius AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path("studygenius_data.json")

SUBJECTS = ["Mathematics", "Science", "English", "Social Science", "French", "Computer Science"]

QUIZ_BANK = {
    "Mathematics": [
        ("What is the value of 7 × 8?", ["54", "56", "64", "48"], "56", "Multiplication: 7 × 8 = 56."),
        ("Which of these is a prime number?", ["21", "27", "29", "33"], "29", "29 has exactly two factors: 1 and 29."),
        ("What is the perimeter of a square with side 5 cm?", ["10 cm", "15 cm", "20 cm", "25 cm"], "20 cm", "Perimeter of a square = 4 × side = 20 cm."),
        ("Solve: 12 + 18 ÷ 3", ["10", "18", "20", "30"], "18", "Division comes first: 18 ÷ 3 = 6; then 12 + 6 = 18."),
        ("What is 25% of 200?", ["25", "40", "50", "75"], "50", "25% means one quarter; 200 ÷ 4 = 50.")
    ],
    "Science": [
        ("Which cell organelle is known as the powerhouse of the cell?", ["Nucleus", "Mitochondrion", "Vacuole", "Ribosome"], "Mitochondrion", "Mitochondria release usable energy for the cell."),
        ("What is the chemical formula of water?", ["CO2", "O2", "H2O", "NaCl"], "H2O", "A water molecule contains two hydrogen atoms and one oxygen atom."),
        ("Which gas do green plants absorb during photosynthesis?", ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], "Carbon dioxide", "Plants use carbon dioxide, water and light to make food."),
        ("What is the SI unit of force?", ["Joule", "Newton", "Watt", "Pascal"], "Newton", "Force is measured in newtons (N)."),
        ("Which part of the human body pumps blood?", ["Lungs", "Brain", "Heart", "Kidney"], "Heart", "The heart pumps blood around the body.")
    ],
    "English": [
        ("Which word is a synonym of 'rapid'?", ["Slow", "Quick", "Quiet", "Weak"], "Quick", "Rapid and quick have similar meanings."),
        ("Which is a noun?", ["Beautiful", "Run", "Happiness", "Quickly"], "Happiness", "Happiness names a feeling, so it is a noun."),
        ("Choose the correct plural of 'child'.", ["Childs", "Childes", "Children", "Childrens"], "Children", "The plural form of child is children."),
        ("Which punctuation mark ends a direct question?", [".", ",", "?", "!"], "?", "A question mark ends a direct question."),
        ("What is the past tense of 'write'?", ["Writed", "Written", "Wrote", "Writing"], "Wrote", "The simple past tense of write is wrote.")
    ],
    "Social Science": [
        ("Which is the largest continent?", ["Africa", "Asia", "Europe", "Australia"], "Asia", "Asia is the largest continent by area and population."),
        ("What is the capital of India?", ["Mumbai", "Kolkata", "New Delhi", "Chennai"], "New Delhi", "New Delhi is the capital of India."),
        ("Which imaginary line divides Earth into Northern and Southern Hemispheres?", ["Tropic of Cancer", "Equator", "Prime Meridian", "Arctic Circle"], "Equator", "The Equator is at 0° latitude."),
        ("What is democracy?", ["Rule by one person", "Rule by the people", "Rule by the army", "Rule by a king"], "Rule by the people", "In a democracy, people choose their representatives."),
        ("Which direction does the Sun appear to rise from?", ["West", "North", "East", "South"], "East", "Because Earth rotates west to east, the Sun appears to rise in the east.")
    ],
    "French": [
        ("What does 'Bonjour' mean?", ["Good night", "Hello / Good morning", "Goodbye", "Thank you"], "Hello / Good morning", "Bonjour is a common daytime greeting."),
        ("What is the French word for 'book'?", ["La table", "Le livre", "La maison", "Le stylo"], "Le livre", "Le livre means the book."),
        ("Choose the correct form: Je ___ étudiant(e).", ["suis", "es", "est", "sommes"], "suis", "The verb être is conjugated as je suis."),
        ("What does 'Merci' mean?", ["Please", "Sorry", "Thank you", "Welcome"], "Thank you", "Merci means thank you."),
        ("What is the plural article for 'les amis'?", ["Le", "La", "L'", "Les"], "Les", "Les is the plural definite article.")
    ],
    "Computer Science": [
        ("What does CPU stand for?", ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Control Power Unit"], "Central Processing Unit", "The CPU executes instructions in a computer."),
        ("Which one is an input device?", ["Monitor", "Printer", "Keyboard", "Speaker"], "Keyboard", "A keyboard sends data into a computer."),
        ("What does HTML mainly describe?", ["Webpage structure", "Computer hardware", "Internet speed", "Image editing"], "Webpage structure", "HTML structures content on web pages."),
        ("Which of these is a programming language?", ["Python", "Wi-Fi", "Bluetooth", "USB"], "Python", "Python is a widely used programming language."),
        ("What is a strong password practice?", ["Use your name", "Reuse one password everywhere", "Use a long unique password", "Share it with friends"], "Use a long unique password", "A long, unique password helps protect accounts.")
    ]
}

DEFAULT_DATA = {
    "profile": {"name": "Student", "class_name": "Class 9", "school": ""},
    "tasks": [],
    "goals": [],
    "quiz_history": [],
    "notes_history": [],
    "flashcards": [],
    "assistant_history": []
}

def load_data():
    if DATA_FILE.exists():
        try:
            saved = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            merged = DEFAULT_DATA.copy()
            merged.update(saved)
            return merged
        except Exception:
            return DEFAULT_DATA.copy()
    return DEFAULT_DATA.copy()

def save_data():
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

data = load_data()

# Session-only quiz state
if "active_quiz" not in st.session_state:
    st.session_state.active_quiz = None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "flash_index" not in st.session_state:
    st.session_state.flash_index = 0
if "flash_revealed" not in st.session_state:
    st.session_state.flash_revealed = False

st.markdown("""
<style>
:root { color-scheme: light; }
.stApp { background: #f5f8ff; }
[data-testid="stSidebar"] { background: #101f43; }
[data-testid="stSidebar"] * { color: #f8fbff !important; }
.hero {
  background: linear-gradient(120deg,#12234b,#2456a6);
  color: white; padding: 26px 28px; border-radius: 20px;
  margin-bottom: 18px;
}
.hero h1 { color: white; margin: 0; font-size: 2.1rem; }
.hero p { color: #dce8ff; margin: 8px 0 0 0; }
.small-muted { color: #64748b; font-size: .9rem; }
.feature-card {
  background: white; border: 1px solid #e3eaf7; border-radius: 16px;
  padding: 18px; min-height: 132px;
}
.feature-card h3 { margin: 0 0 7px 0; color: #172b55; font-size: 1.05rem; }
.feature-card p { color: #64748b; margin: 0; font-size: .9rem; }
.info-box {
  background: #eaf2ff; border-left: 4px solid #3974d6;
  border-radius: 8px; padding: 12px 15px; color: #193765;
}
.success-box {
  background: #e8f8ef; border-left: 4px solid #22a06b;
  border-radius: 8px; padding: 12px 15px; color: #145b3b;
}
div.stButton > button {
  border-radius: 10px; border: 0; font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

def page_header(title, subtitle=""):
    st.title(title)
    if subtitle:
        st.caption(subtitle)

def add_task(task, subject, due):
    data["tasks"].append({
        "task": task, "subject": subject, "due": str(due),
        "done": False, "created": datetime.now().isoformat(timespec="minutes")
    })
    save_data()

def build_notes(text):
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return [], []
    sentences = re.split(r"(?<=[.!?])\s+", clean)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    if not sentences:
        sentences = [clean]
    words = re.findall(r"[A-Za-zÀ-ÿ']+", clean.lower())
    stop = set("the a an and or but is are was were be been being to of in on for with by from as at this that these those it its into about".split())
    freq = {}
    for word in words:
        if word not in stop and len(word) > 2:
            freq[word] = freq.get(word, 0) + 1
    scored = []
    for i, sentence in enumerate(sentences):
        sw = re.findall(r"[A-Za-zÀ-ÿ']+", sentence.lower())
        score = sum(freq.get(w, 0) for w in sw if w not in stop) / max(1, len(sw))
        scored.append((score, i, sentence))
    ranked = sorted(scored, reverse=True)[:min(5, len(scored))]
    key_points = [item[2] for item in sorted(ranked, key=lambda x: x[1])]
    keywords = [w for w, _ in sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:8]]
    return key_points, keywords

def make_quiz(subject, count):
    bank = QUIZ_BANK.get(subject, QUIZ_BANK["Science"])
    questions = random.sample(bank, k=min(count, len(bank)))
    return [{"question": q, "options": opts, "answer": ans, "explanation": exp} for q, opts, ans, exp in questions]

def sidebar():
    st.sidebar.markdown("## 🎓 StudyGenius AI")
    st.sidebar.caption("Your digital learning companion")
    pages = [
        "🏠 Home Dashboard", "👤 Student Profile", "📚 Subject Library",
        "📝 Notes Generator", "🧠 Quiz Maker", "🗂️ Flashcards",
        "📅 Study Planner", "💬 Study Assistant", "🎯 Daily Goals",
        "📊 My Progress", "🎤 Exhibition Demo", "ℹ️ Help & About"
    ]
    selected = st.sidebar.radio("NAVIGATION", pages, label_visibility="collapsed")
    st.sidebar.divider()
    st.sidebar.caption("Prototype • Local data stored on this laptop")
    return selected

page = sidebar()
profile = data["profile"]
student_name = profile.get("name") or "Student"

# ---------------- HOME DASHBOARD ----------------
if page == "🏠 Home Dashboard":
    st.markdown(f"""
    <div class="hero">
      <h1>Welcome, {student_name}! 👋</h1>
      <p>Learn smarter. Study better. Make every study session count.</p>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("Your Learning Dashboard")
    cards = [
        ("📝 Notes Generator", "Turn long study text into concise revision points."),
        ("🧠 Quiz Maker", "Practise with subject-based multiple-choice questions."),
        ("🗂️ Flashcards", "Review important question-and-answer cards."),
        ("📅 Study Planner", "Organise subjects, tasks and due dates."),
        ("💬 Study Assistant", "Get simple study tips and explanations."),
        ("📊 My Progress", "See completed tasks and quiz results.")
    ]
    cols = st.columns(3)
    for i, (title, desc) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f'<div class="feature-card"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
    st.write("")
    tasks_done = sum(1 for t in data["tasks"] if t.get("done"))
    quiz_count = len(data["quiz_history"])
    goals_done = sum(1 for g in data["goals"] if g.get("done"))
    c1, c2, c3 = st.columns(3)
    c1.metric("Tasks completed", tasks_done)
    c2.metric("Quizzes attempted", quiz_count)
    c3.metric("Goals completed", goals_done)
    st.subheader("Quick Start")
    st.write("Choose a tool from the left menu. For your exhibition, try Notes Generator → Quiz Maker → Flashcards → My Progress.")

# ---------------- PROFILE ----------------
elif page == "👤 Student Profile":
    page_header("👤 Student Profile", "Personalise your learning space.")
    with st.form("profile_form"):
        name = st.text_input("Student name", value=profile.get("name", "Student"))
        class_name = st.text_input("Class / Grade", value=profile.get("class_name", "Class 9"))
        school = st.text_input("School (optional)", value=profile.get("school", ""))
        submitted = st.form_submit_button("Save Profile")
    if submitted:
        data["profile"] = {"name": name.strip() or "Student", "class_name": class_name.strip(), "school": school.strip()}
        save_data()
        st.success("Profile saved!")
        st.rerun()
    st.info("For a public exhibition, use a first name or a demo name. Avoid entering private information.")

# ---------------- SUBJECT LIBRARY ----------------
elif page == "📚 Subject Library":
    page_header("📚 Subject Library", "Choose a subject to explore its study tools.")
    descriptions = {
        "Mathematics": "Practise calculations, formulas, algebra and problem-solving.",
        "Science": "Explore biology, chemistry, physics and scientific ideas.",
        "English": "Improve grammar, vocabulary, reading and writing.",
        "Social Science": "Revise history, geography, civics and economics.",
        "French": "Practise vocabulary, articles, verbs and everyday expressions.",
        "Computer Science": "Learn digital skills, coding concepts and computer basics."
    }
    for subject in SUBJECTS:
        with st.expander(f"📘 {subject}"):
            st.write(descriptions[subject])
            st.write("Available tools: Notes Generator, Quiz Maker and Study Planner.")
            if st.button(f"Create a {subject} quiz", key=f"subquiz_{subject}"):
                st.session_state.quick_subject = subject
                st.success(f"Subject selected: {subject}. Open Quiz Maker from the menu.")

# ---------------- NOTES GENERATOR ----------------
elif page == "📝 Notes Generator":
    page_header("📝 Notes Generator", "Paste your study material and create concise revision notes.")
    st.markdown('<div class="info-box">This exhibition prototype uses local text-processing logic to select key sentences and frequent terms. It does not send your notes to an external AI service.</div>', unsafe_allow_html=True)
    subject = st.selectbox("Choose subject", SUBJECTS, key="notes_subject")
    chapter = st.text_input("Chapter / topic name", placeholder="e.g. The Fundamental Unit of Life")
    raw_text = st.text_area("Paste your chapter text here", height=220, placeholder="Paste a paragraph or your own study notes...")
    if st.button("✨ Generate Notes", type="primary"):
        points, keywords = build_notes(raw_text)
        if not points:
            st.warning("Please paste some text first.")
        else:
            st.session_state.generated_notes = {"subject": subject, "chapter": chapter, "points": points, "keywords": keywords}
            data["notes_history"].append({"subject": subject, "chapter": chapter, "date": str(date.today()), "points": points})
            save_data()
    result = st.session_state.get("generated_notes")
    if result:
        st.divider()
        st.subheader(f"Revision Notes: {result.get('chapter') or result['subject']}")
        st.caption(result["subject"])
        for point in result["points"]:
            st.markdown(f"- {point}")
        st.markdown("**Key terms**")
        st.write(" • ".join(result["keywords"]))
        st.download_button("⬇️ Download notes as text", "\n".join(result["points"]) + "\n\nKey terms: " + ", ".join(result["keywords"]), file_name="study_notes.txt")

# ---------------- QUIZ MAKER ----------------
elif page == "🧠 Quiz Maker":
    page_header("🧠 Quiz Maker", "Test your knowledge with a short practice quiz.")
    subject_default = st.session_state.get("quick_subject", "Science")
    default_index = SUBJECTS.index(subject_default) if subject_default in SUBJECTS else 1
    subject = st.selectbox("Select subject", SUBJECTS, index=default_index)
    count = st.slider("Number of questions", 3, 5, 5)
    if st.button("Generate Quiz", type="primary"):
        st.session_state.active_quiz = {"subject": subject, "questions": make_quiz(subject, count)}
        st.session_state.quiz_submitted = False
    quiz = st.session_state.active_quiz
    if quiz:
        st.divider()
        st.subheader(f"{quiz['subject']} Practice Quiz")
        with st.form("quiz_form"):
            answers = []
            for i, q in enumerate(quiz["questions"]):
                st.markdown(f"**Q{i+1}. {q['question']}**")
                choice = st.radio("Choose one answer", q["options"], key=f"quiz_{i}", index=None)
                answers.append(choice)
            submitted = st.form_submit_button("Submit Quiz")
        if submitted:
            score = sum(1 for ans, q in zip(answers, quiz["questions"]) if ans == q["answer"])
            st.session_state.quiz_result = {"score": score, "total": len(quiz["questions"]), "answers": answers}
            st.session_state.quiz_submitted = True
            data["quiz_history"].append({"subject": quiz["subject"], "score": score, "total": len(quiz["questions"]), "date": str(date.today())})
            save_data()
        if st.session_state.quiz_submitted and st.session_state.get("quiz_result"):
            result = st.session_state.quiz_result
            st.success(f"You scored {result['score']} out of {result['total']}!")
            for i, q in enumerate(quiz["questions"]):
                chosen = result["answers"][i]
                is_correct = chosen == q["answer"]
                st.markdown(f"**Q{i+1}: {'Correct' if is_correct else 'Review this one'}**")
                st.write(f"Correct answer: {q['answer']}")
                st.caption(q["explanation"])
            if st.button("Try another quiz"):
                st.session_state.active_quiz = None
                st.session_state.quiz_submitted = False
                st.rerun()

# ---------------- FLASHCARDS ----------------
elif page == "🗂️ Flashcards":
    page_header("🗂️ Digital Flashcards", "Flip a card to reveal the answer.")
    built_in = [
        ("What is photosynthesis?", "The process by which green plants use light energy to make food from carbon dioxide and water."),
        ("What is a prime number?", "A whole number greater than 1 with exactly two factors: 1 and itself."),
        ("What is a noun?", "A word that names a person, place, thing or idea."),
        ("What does 'Je suis' mean?", "I am."),
        ("What is the Equator?", "An imaginary line at 0° latitude dividing Earth into Northern and Southern Hemispheres.")
    ]
    cards = built_in + [(c["question"], c["answer"]) for c in data["flashcards"]]
    if not cards:
        st.info("No flashcards available yet.")
    else:
        idx = st.session_state.flash_index % len(cards)
        question, answer = cards[idx]
        st.caption(f"Card {idx + 1} of {len(cards)}")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#17346d,#3475d2);color:white;
        padding:42px 22px;border-radius:20px;text-align:center;min-height:190px;">
        <div style="font-size:14px;opacity:.8;">{"ANSWER" if st.session_state.flash_revealed else "QUESTION"}</div>
        <div style="font-size:25px;font-weight:700;margin-top:20px;">{answer if st.session_state.flash_revealed else question}</div>
        </div>""", unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a:
            if st.button("⬅ Previous"):
                st.session_state.flash_index = (idx - 1) % len(cards)
                st.session_state.flash_revealed = False
                st.rerun()
        with b:
            if st.button("🔄 Flip Card"):
                st.session_state.flash_revealed = not st.session_state.flash_revealed
                st.rerun()
        with c:
            if st.button("Next ➡"):
                st.session_state.flash_index = (idx + 1) % len(cards)
                st.session_state.flash_revealed = False
                st.rerun()
    st.divider()
    st.subheader("Create your own flashcard")
    with st.form("flash_form"):
        q_text = st.text_input("Question")
        a_text = st.text_area("Answer")
        add_card = st.form_submit_button("Add Flashcard")
    if add_card:
        if q_text.strip() and a_text.strip():
            data["flashcards"].append({"question": q_text.strip(), "answer": a_text.strip()})
            save_data()
            st.success("Flashcard added!")
            st.rerun()
        else:
            st.warning("Enter both a question and an answer.")

# ---------------- STUDY PLANNER ----------------
elif page == "📅 Study Planner":
    page_header("📅 Study Planner", "Plan your work and keep track of what you finish.")
    with st.form("task_form"):
        task = st.text_input("Study task", placeholder="e.g. Revise Chapter 2")
        subject = st.selectbox("Subject", SUBJECTS)
        due = st.date_input("Due date", value=date.today())
        add = st.form_submit_button("＋ Add Task")
    if add:
        if task.strip():
            add_task(task.strip(), subject, due)
            st.success("Task added to your planner.")
            st.rerun()
        else:
            st.warning("Please enter a task.")
    st.subheader("Your tasks")
    if not data["tasks"]:
        st.info("No tasks yet. Add your first study task above.")
    for i, item in enumerate(data["tasks"]):
        col1, col2, col3 = st.columns([0.12, 0.68, 0.2])
        with col1:
            checked = st.checkbox("Done", value=item.get("done", False), key=f"task_{i}", label_visibility="collapsed")
        if checked != item.get("done", False):
            item["done"] = checked
            save_data()
            st.rerun()
        with col2:
            label = f"~~{item['task']}~~" if item.get("done") else f"**{item['task']}**"
            st.markdown(label)
            st.caption(f"{item.get('subject','')} • Due: {item.get('due','')}")
        with col3:
            if st.button("Delete", key=f"del_task_{i}"):
                data["tasks"].pop(i)
                save_data()
                st.rerun()

# ---------------- STUDY ASSISTANT ----------------
elif page == "💬 Study Assistant":
    page_header("💬 Study Assistant", "Ask for general study guidance and simple explanations.")
    st.markdown('<div class="info-box">This is a basic demonstration assistant with programmed responses, not a live AI chatbot. Verify school answers with your textbook or teacher.</div>', unsafe_allow_html=True)
    prompts = [
        "How can I make a study timetable?",
        "How do I remember what I learn?",
        "Explain photosynthesis simply.",
        "How should I prepare for an exam?"
    ]
    st.write("Try asking:")
    cols = st.columns(2)
    for i, prompt in enumerate(prompts):
        with cols[i % 2]:
            if st.button(prompt, key=f"suggest_{i}"):
                st.session_state.assistant_input = prompt
    user_question = st.text_input("Your question", key="assistant_input", placeholder="Type a study-related question...")
    if st.button("Send", type="primary"):
        q = user_question.lower()
        if not q.strip():
            st.warning("Type a question first.")
        elif "timetable" in q or "schedule" in q or "plan" in q:
            reply = "Choose a realistic study time, split big chapters into smaller tasks, include short breaks, and review your plan each evening."
        elif "remember" in q or "memor" in q or "revise" in q:
            reply = "Try active recall: close your book and explain the idea in your own words. Then use flashcards and revisit the topic after a day or two."
        elif "photosynthesis" in q:
            reply = "Photosynthesis is how green plants make food. They use sunlight, water and carbon dioxide to produce glucose and release oxygen."
        elif "exam" in q or "prepare" in q:
            reply = "Make a topic checklist, revise key ideas, practise questions, check mistakes, and get enough rest before the exam."
        elif "math" in q:
            reply = "For Maths, understand the method, write each step clearly, practise a few questions, and check your answers."
        elif "french" in q:
            reply = "For French, practise vocabulary in small groups, learn verb forms with examples, and write a few original sentences each day."
        else:
            reply = "Break the topic into smaller parts, identify the main idea, write down what you already know, and ask a teacher or trusted learning resource about anything unclear."
        data["assistant_history"].append({"question": user_question, "reply": reply, "date": str(date.today())})
        save_data()
        st.markdown("**Study Assistant**")
        st.info(reply)
    if data["assistant_history"]:
        with st.expander("Recent conversation"):
            for item in data["assistant_history"][-5:][::-1]:
                st.markdown(f"**You:** {item['question']}")
                st.write(f"**Assistant:** {item['reply']}")

# ---------------- DAILY GOALS ----------------
elif page == "🎯 Daily Goals":
    page_header("🎯 Daily Goals", "Set small goals that make progress manageable.")
    with st.form("goal_form"):
        goal_text = st.text_input("Today's goal", placeholder="e.g. Revise 10 French verbs")
        add_goal = st.form_submit_button("Add Goal")
    if add_goal:
        if goal_text.strip():
            data["goals"].append({"goal": goal_text.strip(), "done": False, "date": str(date.today())})
            save_data()
            st.rerun()
        else:
            st.warning("Please type a goal.")
    today_goals = [(i, g) for i, g in enumerate(data["goals"]) if g.get("date") == str(date.today())]
    if not today_goals:
        st.info("No goals for today yet.")
    for i, goal in today_goals:
        done = st.checkbox(goal["goal"], value=goal.get("done", False), key=f"goal_{i}")
        if done != goal.get("done", False):
            data["goals"][i]["done"] = done
            save_data()
            st.rerun()

# ---------------- PROGRESS ----------------
elif page == "📊 My Progress":
    page_header("📊 My Progress", "A simple overview of your saved learning activity.")
    total_tasks = len(data["tasks"])
    done_tasks = sum(1 for t in data["tasks"] if t.get("done"))
    total_goals = len(data["goals"])
    done_goals = sum(1 for g in data["goals"] if g.get("done"))
    quizzes = data["quiz_history"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tasks completed", done_tasks, f"of {total_tasks}")
    c2.metric("Goals completed", done_goals, f"of {total_goals}")
    c3.metric("Quizzes attempted", len(quizzes))
    avg = round(sum(q["score"] / max(1, q["total"]) * 100 for q in quizzes) / len(quizzes)) if quizzes else 0
    c4.metric("Average quiz score", f"{avg}%" if quizzes else "—")
    st.subheader("Quiz history")
    if quizzes:
        st.dataframe([{"Date": q["date"], "Subject": q["subject"], "Score": f"{q['score']}/{q['total']}"} for q in quizzes[::-1]], use_container_width=True, hide_index=True)
        chart_data = {}
        for q in quizzes:
            chart_data.setdefault(q["subject"], []).append(q["score"] / max(1, q["total"]) * 100)
        st.subheader("Average score by subject")
        st.bar_chart({k: sum(v) / len(v) for k, v in chart_data.items()})
    else:
        st.info("Complete a practice quiz to see your progress here.")
    st.caption("Progress is saved in a local JSON file on the laptop running this app.")

# ---------------- EXHIBITION DEMO ----------------
elif page == "🎤 Exhibition Demo":
    page_header("🎤 Exhibition Demo", "A ready-to-use guide for presenting StudyGenius AI.")
    st.markdown("""
    <div class="hero">
      <h1>StudyGenius AI</h1>
      <p>A digital learning companion designed to help students organise, practise and review their studies.</p>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("Suggested live demonstration")
    demo_steps = [
        ("1. Introduce the problem", "Students often have long notes, limited revision time and difficulty organising tasks."),
        ("2. Show Notes Generator", "Paste a short paragraph and generate key revision points."),
        ("3. Show Quiz Maker", "Choose a subject, generate questions and answer them."),
        ("4. Show Flashcards", "Flip a card to reveal its answer."),
        ("5. Show Study Planner", "Add a task with a due date and mark it complete."),
        ("6. Show My Progress", "Explain how quiz attempts and completed tasks are recorded.")
    ]
    for heading, detail in demo_steps:
        with st.expander(heading, expanded=True):
            st.write(detail)
    st.subheader("Short presentation script")
    st.write(
        "Good morning. My project is StudyGenius AI, a digital learning platform created to make studying more organised and interactive. "
        "It brings together notes support, practice quizzes, flashcards, a study planner and progress tracking in one place. "
        "I will demonstrate how a student can revise a topic, test their understanding and plan their next study session. "
        "This version is an educational prototype. Some tools use programmed logic, and the project can be extended with a real AI model in a future version. Thank you."
    )
    st.download_button("Download presentation script", 
        "Good morning. My project is StudyGenius AI, a digital learning platform created to make studying more organised and interactive. It brings together notes support, practice quizzes, flashcards, a study planner and progress tracking in one place. I will demonstrate how a student can revise a topic, test their understanding and plan their next study session. This version is an educational prototype. Some tools use programmed logic, and the project can be extended with a real AI model in a future version. Thank you.",
        file_name="exhibition_script.txt")
    st.subheader("Sample text for a live demonstration")
    sample = ("Photosynthesis is the process by which green plants prepare their own food. "
              "Chlorophyll in the leaves absorbs energy from sunlight. Plants take in carbon dioxide from the air and water from the soil. "
              "Using light energy, they convert these materials into glucose and release oxygen. "
              "Photosynthesis is important because it provides food for plants and oxygen for many living organisms.")
    st.text_area("Copy this sample into Notes Generator", value=sample, height=130)
    st.warning("Be transparent with judges: this is a working educational prototype. The current notes and assistant features use simple programmed logic, not a connected generative AI model.")

# ---------------- HELP & ABOUT ----------------
elif page == "ℹ️ Help & About":
    page_header("ℹ️ Help & About", "Learn what the project does and how to use it.")
    st.subheader("About the project")
    st.write("StudyGenius AI is a school exhibition prototype that combines several study tools in one digital platform.")
    st.subheader("How to use")
    st.markdown("""
    1. Update your demo profile.
    2. Choose a subject from Subject Library.
    3. Paste text into Notes Generator.
    4. Practise with Quiz Maker and Flashcards.
    5. Add tasks in Study Planner and goals in Daily Goals.
    6. Check My Progress to review activity.
    """)
    st.subheader("Current prototype limitations")
    st.markdown("""
    - The notes tool selects key sentences and frequent words using local text-processing rules.
    - Quiz Maker uses a built-in sample question bank.
    - Study Assistant uses programmed study tips and responses.
    - Progress is stored locally in `studygenius_data.json` on the computer running the app.
    - The app is not a replacement for teachers, textbooks or professional advice.
    """)
    st.subheader("Privacy")
    st.write("The app stores the profile and learning activity in a local file on the host laptop. Use demo information during a public exhibition and do not enter private details.")
    if st.button("Reset all saved demo data", type="secondary"):
        data.clear()
        data.update(DEFAULT_DATA)
        save_data()
        st.success("Demo data reset.")
        st.rerun()

st.sidebar.divider()
st.sidebar.caption("Made for learning • StudyGenius AI")
