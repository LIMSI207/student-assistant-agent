import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from database import (
    init_db,
    add_student,
    search_student,
    list_students,
    count_students,
    update_student,
    delete_student,
    get_student_statistics,
    export_students_csv,
)

from auth import (
    init_auth_db,
    register_user,
    login_user
)

# ---------------- CONFIGURATION ----------------

load_dotenv()

st.set_page_config(
    page_title="Student Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()
init_auth_db()

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #080817;
    --panel: #15142d;
    --purple: #8b5cf6;
    --pink: #ec4899;
    --blue: #38bdf8;
    --green: #22c55e;
    --red: #fb5575;
}
.stApp {
    background:
      radial-gradient(ellipse at 8% 4%, #35145f 0%, transparent 30%),
      radial-gradient(ellipse at 95% 8%, #172b56 0%, transparent 28%),
      linear-gradient(135deg, #080817 0%, #111027 55%, #0b1730 100%);
    color: #f8f7ff;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { right: 1rem; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1500px; }
h1,h2,h3,h4 { color: #fff !important; font-family: 'Space Grotesk',sans-serif !important; }
p, label, [data-testid="stMarkdownContainer"] { color: #eeeaff; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1b1236 0%,#12112b 58%,#101a34 100%);
    border-right: 1px solid #493477;
}
[data-testid="stSidebar"] * { color: #eeeaff; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 9px 11px;
    border-radius: 12px;
    margin: 3px 0;
    transition: .2s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #ffffff14;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] {
    background: linear-gradient(100deg,#7138dc,#9238d8);
    border: 1px solid #b99aff;
    box-shadow: 0 5px 20px #7c3aed55;
}
[data-testid="stSidebar"] [data-testid="stButton"] button {
    background: #24194b;
    border: 1px solid #8060c9;
}
[data-testid="stSidebar"] hr { border-color: #493477 !important; }

[data-testid="stMetric"] {
    background: linear-gradient(145deg,#25204a,#14172f);
    border: 1px solid #6545a0;
    border-radius: 19px;
    padding: 19px 21px;
    box-shadow: 0 10px 30px #0005;
    min-height: 112px;
}
[data-testid="stHorizontalBlock"] [data-testid="stMetric"] {
    transition: transform .2s ease, box-shadow .2s ease;
}
[data-testid="stHorizontalBlock"] [data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px #8b5cf644;
}
[data-testid="stMetricLabel"] { color: #c9baff !important; font-weight: 700; }
[data-testid="stMetricValue"] { color: #fff !important; font-family:'Space Grotesk',sans-serif; }
[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]):nth-of-type(1) [data-testid="stMetric"]:nth-child(1) {
    border-color: #2875c9;
}
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    background: linear-gradient(100deg,#7138dc,#b832c7);
    color: white !important;
    border: 1px solid #a78bfa66;
    border-radius: 12px;
    font-weight: 700;
    padding: 10px 16px;
    transition: .2s;
    box-shadow: 0 5px 18px #7c3aed25;
}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    border-color: #e9d5ff;
    box-shadow: 0 8px 24px #a855f755;
}
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    background: #17162f !important;
    color: white !important;
    border: 1px solid #554078 !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] > div {
    background: #17162f !important;
    border-color: #554078 !important;
    color: white !important;
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
    border: 1px solid #493477;
    border-radius: 14px;
    overflow: hidden;
}
[data-testid="stPlotlyChart"], [data-testid="stVegaLiteChart"] {
    background: linear-gradient(145deg,#1c1939,#12172e);
    border: 1px solid #493477;
    border-radius: 17px;
    padding: 10px;
    box-shadow: 0 8px 25px #0004;
}}}
.panel {
    background:linear-gradient(145deg,#1c1939,#12172e);
    border:1px solid #514078;
    border-radius:18px;
    padding:18px;
}
.section-heading {
    font-family:'Space Grotesk',sans-serif;
    font-size:20px;
    font-weight:700;
    color:#fff;
    margin:12px 0 13px;
}
.small-muted { color:#aaa2c2; font-size:12px; }
div[data-testid="stAlert"] { border-radius:12px; }
hr { border-color:#40345f !important; }
.auth-wrap { max-width:760px; margin:4vh auto; }
[data-testid="stChatMessage"] {
    background: #191633;
    border: 1px solid #493477;
    border-radius: 14px;
}
@media (max-width: 800px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "user" not in st.session_state:
    st.session_state.user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



def show_result(result, success_text):

    if isinstance(result, dict) and result.get("error"):
        st.error(result["error"])

    elif isinstance(result, dict):
        st.success(result.get("message", success_text))

    else:
        st.success(success_text)


def student_options(students):

    return {
        f"#{s['id']} | {s['name']} | {s['department']}": s
        for s in students
    }


def go_to_page(target):
    st.session_state["navigation"] = target


# ==================================================
#                  LOGIN SYSTEM
# ==================================================

if st.session_state.user is None:

    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)

    login_tab, register_tab = st.tabs([
        "🔐 Login",
        "✨ Register"
    ])

    # LOGIN

    with login_tab:

        st.subheader("Welcome Back!")

        with st.form("login_form"):

            email = st.text_input("Email Address")

            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "🚀 Login",
                use_container_width=True
            )

        if submitted:

            user = login_user(email, password)

            if user:

                st.session_state.user = user

                st.success("Login Successful!")

                st.rerun()

            else:

                st.error("Invalid Email or Password.")

    # REGISTER

    with register_tab:

        st.subheader("Create Your Account")

        with st.form("register_form"):

            name = st.text_input("Full Name")

            new_email = st.text_input("Email Address")

            new_password = st.text_input(
                "Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "✨ Create Account",
                use_container_width=True
            )

        if submitted:

            if new_password != confirm_password:

                st.error("Passwords do not match.")

            else:

                success, message = register_user(
                    name,
                    new_email,
                    new_password
                )

                if success:

                    st.success(message)

                else:

                    st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# ==================================================
#                    SIDEBAR
# ==================================================

user = st.session_state.user

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;padding:8px 4px 14px;">
            <div style="font-size:42px;filter:drop-shadow(0 0 12px #8b5cf6);">🎓</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:21px;font-weight:800;color:#ffffff;">
                Student Assistant
            </div>
            <div style="font-size:12px;color:#c4b5fd;letter-spacing:2px;">AGENT WORKSPACE</div>
            <div style="height:3px;width:76px;margin:12px auto;background:linear-gradient(90deg,#8b5cf6,#ec4899);border-radius:5px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        f"### 👋 Welcome, {user['name']}"
    )

    st.caption(user["email"])

    st.divider()

    page_icons = {
        "Dashboard": "🏠",
        "Add Student": "➕",
        "View Students": "👥",
        "Search Student": "🔎",
        "Update Student": "✏️",
        "Delete Student": "🗑️",
        "Export CSV": "📥",
        "AI Assistant": "🤖"
    }

    page = st.radio(
        "NAVIGATION",
        list(page_icons.keys()),
        format_func=lambda item: f"{page_icons[item]}  {item}",
        key="navigation"
    )

    st.divider()

    st.markdown(
        """
        <div class="small-muted">
        STUDENT ASSISTANT AGENT<br>
        Powered by SQLite + Gemini
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("↪ Logout", use_container_width=True):

        st.session_state.user = None

        st.session_state.chat_history = []

        st.rerun()


# ==================================================
#                    DASHBOARD
# ==================================================

if page == "Dashboard":

    stats = get_student_statistics()
   

    total = int(stats.get("total_students", 0) or 0)
    active = int(stats.get("active_students", 0) or 0)
    inactive = int(stats.get("inactive_students", 0) or 0)
    dept = pd.DataFrame(stats.get("department_stats", []))

    c1, c2, c3 = st.columns(3)
    c1.metric("👥  Total Students", total)
    c2.metric("🟢  Active Students", active)
    c3.metric("🔴  Inactive Students", inactive)

    st.write("")
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown('<div class="section-heading">📊 Department Statistics</div>', unsafe_allow_html=True)
        if not dept.empty and "department" in dept.columns and "total_students" in dept.columns:
            dept_chart = dept[["department", "total_students"]].copy()
            dept_chart["total_students"] = pd.to_numeric(dept_chart["total_students"], errors="coerce").fillna(0)
            st.vega_lite_chart(
                dept_chart,
                {
                    "width": "container",
                    "height": 260,
                    "mark": {"type": "arc", "innerRadius": 72, "outerRadius": 112, "cornerRadius": 5},
                    "encoding": {
                        "theta": {"field": "total_students", "type": "quantitative"},
                        "color": {
                            "field": "department", "type": "nominal",
                            "scale": {"range": ["#8b5cf6", "#38bdf8", "#f59e0b", "#22c55e", "#ec4899", "#14b8a6"]}
                        },
                        "tooltip": [
                            {"field": "department", "type": "nominal", "title": "Department"},
                            {"field": "total_students", "type": "quantitative", "title": "Students"}
                        ]
                    },
                    "view": {"stroke": None},
                    "config": {"background": "#15142d", "legend": {"labelColor": "#eeeaff", "titleColor": "#eeeaff"}}
                },
                use_container_width=True
            )
        else:
            st.info("No department data available yet.")

    with right:
        st.markdown('<div class="section-heading">🟣 Student Status</div>', unsafe_allow_html=True)
        if total > 0:
            status_df = pd.DataFrame({
                "Status": ["Active", "Inactive"],
                "Students": [active, inactive]
            })
            st.vega_lite_chart(
                status_df,
                {
                    "width": "container",
                    "height": 260,
                    "mark": {"type": "arc", "innerRadius": 72, "outerRadius": 112, "cornerRadius": 5},
                    "encoding": {
                        "theta": {"field": "Students", "type": "quantitative"},
                        "color": {
                            "field": "Status", "type": "nominal",
                            "scale": {"domain": ["Active", "Inactive"], "range": ["#22c55e", "#fb5575"]}
                        },
                        "tooltip": [
                            {"field": "Status", "type": "nominal"},
                            {"field": "Students", "type": "quantitative"}
                        ]
                    },
                    "view": {"stroke": None},
                    "config": {"background": "#15142d", "legend": {"labelColor": "#eeeaff", "titleColor": "#eeeaff"}}
                },
                use_container_width=True
            )
        else:
            st.info("No student status data available yet.")

    st.markdown('<div class="section-heading">📋 Department-wise Details</div>', unsafe_allow_html=True)
    if not dept.empty:
        display_df = dept.rename(columns={
            "department": "Department",
            "total_students": "Total",
            "active_students": "Active",
            "inactive_students": "Inactive"
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No department records available.")

    st.markdown('<div class="section-heading">⚡ Quick Actions</div>', unsafe_allow_html=True)
    quick_cols = st.columns(5)
    quick_actions = [
        ("➕ Add Student", "Add Student"),
        ("👥 View Students", "View Students"),
        ("🔎 Search Student", "Search Student"),
        ("📄 Export CSV", "Export CSV"),
        ("🤖 AI Assistant", "AI Assistant")
    ]
    for col, (label, target) in zip(quick_cols, quick_actions):
        with col:
            st.button(label, key=f"quick_{target}", use_container_width=True,
                      on_click=go_to_page, args=(target,))

    st.markdown('<div class="section-heading">🕘 Recent Student Records</div>', unsafe_allow_html=True)
    recent = list_students()[-5:]
    if recent:
        st.dataframe(pd.DataFrame(recent), use_container_width=True, hide_index=True)
    else:
        st.info("No student records available yet.")


# ==================================================
#                   ADD STUDENT
# ==================================================

elif page == "Add Student":

    with st.form("add_student_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        name = col1.text_input("Student Name")

        department = col2.text_input("Department")

        status = st.selectbox(
            "Student Status",
            ["Active", "Inactive"]
        )

        submitted = st.form_submit_button(
            "＋ Add Student"
        )

    if submitted:

        result = add_student(
            name,
            department,
            status
        )

        show_result(
            result,
            "Student added successfully!"
        )


# ==================================================
#                   VIEW STUDENTS
# ==================================================

elif page == "View Students":

    students = list_students()

    if students:

        df = pd.DataFrame(students)

        c1, c2 = st.columns(2)

        departments = [
            "All"
        ] + sorted(
            df["department"].dropna().unique().tolist()
        )

        selected_dept = c1.selectbox(
            "Department",
            departments
        )

        selected_status = c2.selectbox(
            "Status",
            ["All", "Active", "Inactive"]
        )

        if selected_dept != "All":

            df = df[
                df["department"] == selected_dept
            ]

        if selected_status != "All":

            df = df[
                df["status"].str.lower()
                == selected_status.lower()
            ]

        st.caption(
            f"Showing {len(df)} student records"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No students found.")


# ==================================================
#                  SEARCH STUDENT
# ==================================================

elif page == "Search Student":


    with st.form("search_form"):

        term = st.text_input(
            "Student Name",
            placeholder="Enter student name..."
        )

        submitted = st.form_submit_button(
            "🔎 Search Student"
        )

    if submitted:

        if term.strip():

            results = search_student(term)

            if results:

                st.success(
                    f"{len(results)} student(s) found."
                )

                st.dataframe(
                    pd.DataFrame(results),
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.warning("No matching student found.")

        else:

            st.warning("Please enter a student name.")


# ==================================================
#                  UPDATE STUDENT
# ==================================================

elif page == "Update Student":


    students = list_students()

    if students:

        options = student_options(students)

        selected = options[
            st.selectbox(
                "Select Student",
                list(options.keys())
            )
        ]

        with st.form("update_form"):

            st.caption(
                f"Student ID: {selected['id']}"
            )

            new_name = st.text_input(
                "Student Name",
                value=selected["name"]
            )

            new_department = st.text_input(
                "Department",
                value=selected["department"]
            )

            new_status = st.selectbox(
                "Status",
                ["Active", "Inactive"],
                index=(
                    0 if selected["status"].lower() == "active"
                    else 1
                )
            )

            submitted = st.form_submit_button(
                "💾 Save Changes"
            )

        if submitted:

            result = update_student(
                selected["id"],
                new_name,
                new_department,
                new_status
            )

            show_result(
                result,
                "Student updated successfully!"
            )

            if not result.get("error"):

                st.rerun()

    else:

        st.info("No student records available.")


# ==================================================
#                  DELETE STUDENT
# ==================================================

elif page == "Delete Student":

    students = list_students()

    if students:

        options = student_options(students)

        selected = options[
            st.selectbox(
                "Select Student",
                list(options.keys())
            )
        ]

        st.warning(
            f"You are about to delete {selected['name']} "
            f"(ID: {selected['id']})."
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this student."
        )

        if st.button(
            "🗑️ Delete Student",
            disabled=not confirm
        ):

            result = delete_student(
                selected["id"]
            )

            show_result(
                result,
                "Student deleted successfully!"
            )

            if not result.get("error"):

                st.rerun()

    else:

        st.info("No student records available.")


# ==================================================
#                    EXPORT CSV
# ==================================================

elif page == "Export CSV":
    students = list_students()

    csv_df = pd.DataFrame(
        students,
        columns=[
            "id",
            "name",
            "department",
            "status"
        ]
    )

    st.metric(
        "Records Ready to Export",
        len(csv_df)
    )

    csv_bytes = csv_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ Download Student Report",
        data=csv_bytes,
        file_name="students_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("💾 Save CSV in Project Folder"):

        result = export_students_csv()

        show_result(
            result,
            "CSV report saved successfully!"
        )


# ==================================================
#                   AI ASSISTANT
# ==================================================

elif page == "AI Assistant":
    st.markdown(
        "### 💬 Chat with your Student Assistant"
    )

    for item in st.session_state.chat_history:

        with st.chat_message(item["role"]):

            st.markdown(item["content"])

    question = st.chat_input(
        "Ask about students, departments or statistics..."
    )

    if question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):

            st.markdown(question)

        api_key = os.getenv("GOOGLE_API_KEY")

        model_id = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        answer = ""

        with st.chat_message("assistant"):

            if not api_key:

                answer = (
                    "GOOGLE_API_KEY is missing. "
                    "Please configure your .env file."
                )

                st.error(answer)

            else:

                try:

                    from agno.agent import Agent
                    from agno.models.google import Gemini

                    agent = Agent(

                        model=Gemini(
                            id=model_id,
                            api_key=api_key
                        ),

                        tools=[
                            search_student,
                            list_students,
                            count_students,
                            get_student_statistics
                        ],

                        instructions=[
                            "You are a helpful Student Assistant.",
                            "Use database tools for student-related questions.",
                            "Never invent student names or statistics.",
                            "Never modify or delete student records through chat.",
                            "Reply in the same language as the user.",
                            "Keep answers clear and concise."
                        ],

                        markdown=True
                    )

                    with st.spinner(
                        "🤖 Gemini is thinking..."
                    ):

                        response = agent.run(question)

                    answer = str(
                        getattr(
                            response,
                            "content",
                            response
                        )
                    )

                    st.markdown(answer)

                except Exception as exc:

                    answer = (
                        f"AI Assistant Error: "
                        f"{type(exc).__name__}: {exc}"
                    )

                    st.error(answer)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })