import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Insight Hub",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "page_index" not in st.session_state:
    st.session_state.page_index = 0
    st.session_state.creation_date = datetime.now().strftime("%Y-%m-%d")
    st.session_state.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define pages
pages = [
    "👥 WHO - Stakeholders & Team",
    "🎯 WHY - Business Justification",
    "📋 WHAT - Project Scope",
    "⚙️ HOW - Execution Plan",
    "📅 WHEN - Timeline & Milestones",
    "📑 Summary & Export"
]

# Sidebar Navigation (Instant Update)
selected_page = st.sidebar.radio("Navigation", pages, index=st.session_state.page_index, key="sidebar_nav")

if selected_page != pages[st.session_state.page_index]:
    st.session_state.page_index = pages.index(selected_page)
    st.experimental_rerun()  # Force immediate update on sidebar selection

# Function to navigate between pages
def navigate(direction):
    """ Navigate forward (+1) or backward (-1) """
    new_index = st.session_state.page_index + direction
    if 0 <= new_index < len(pages):
        st.session_state.page_index = new_index
        st.experimental_rerun()  # Force page reload instantly

# **Main Content Area**
st.title("🚀 Insight Hub - Define Your Project")

# **STEP 1: WHO**
if pages[st.session_state.page_index] == "👥 WHO - Stakeholders & Team":
    st.subheader("👥 WHO: Stakeholders & Team")
    st.session_state.owner = st.text_input("Project Owner *", st.session_state.get("owner", ""))
    st.session_state.owner_role = st.selectbox("Owner's Role *", ["Project Manager", "Technical Lead", "Business Analyst", "Department Head", "Other"], index=0)
    st.session_state.team = st.text_area("Team Members & Stakeholders *", st.session_state.get("team", ""), height=100)
    st.session_state.department = st.multiselect("Involved Departments", ["IT", "Finance", "Marketing", "Operations", "HR", "Sales", "R&D", "Legal"], st.session_state.get("department", []))

# **STEP 2: WHY**
elif pages[st.session_state.page_index] == "🎯 WHY - Business Justification":
    st.subheader("🎯 WHY: Business Justification")
    st.session_state.problem = st.text_area("Problem Statement *", st.session_state.get("problem", ""), height=100)
    st.session_state.outcome = st.text_area("Expected Outcomes *", st.session_state.get("outcome", ""), height=100)
    st.session_state.success = st.text_area("Success Criteria *", st.session_state.get("success", ""), height=100)

# **STEP 3: WHAT**
elif pages[st.session_state.page_index] == "📋 WHAT - Project Scope":
    st.subheader("📋 WHAT: Project Scope")
    st.session_state.type = st.selectbox("Project Type *", ["Business Intelligence", "Data Engineering", "AI & Machine Learning", "Other"], index=0)
    st.session_state.details = st.text_area("Project Details *", st.session_state.get("details", ""), height=150)

# **STEP 4: HOW**
elif pages[st.session_state.page_index] == "⚙️ HOW - Execution Plan":
    st.subheader("⚙️ HOW: Execution Strategy")
    st.session_state.resources = st.text_area("Required Resources *", st.session_state.get("resources", ""), height=100)
    st.session_state.team_size = st.number_input("Team Size *", min_value=1, max_value=100, value=st.session_state.get("team_size", 5))
    st.session_state.budget = st.text_input("Estimated Budget *", st.session_state.get("budget", ""))

# **STEP 5: WHEN**
elif pages[st.session_state.page_index] == "📅 WHEN - Timeline & Milestones":
    st.subheader("📅 WHEN: Timeline & Milestones")
    st.session_state.timeline = st.text_input("Project Duration *", st.session_state.get("timeline", ""))
    st.session_state.milestones = st.text_area("Key Milestones *", st.session_state.get("milestones", ""), height=150)

# **STEP 6: SUMMARY & EXPORT**
elif pages[st.session_state.page_index] == "📑 Summary & Export":
    st.subheader("📑 Project Summary")
    
    st.write("### 👥 WHO: Stakeholders & Team")
    st.write(f"**Project Owner:** {st.session_state.get('owner', 'Not provided')}")
    
    st.write("### 🎯 WHY: Business Justification")
    st.write(f"**Problem:** {st.session_state.get('problem', 'Not provided')}")
    
    st.write("### 📋 WHAT: Project Scope")
    st.write(f"**Project Type:** {st.session_state.get('type', 'Not selected')}")
    
    # **Fully Working PDF Export**
    if st.button("📄 Download as PDF"):
        pdf_filename = "project_summary.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, "Project Summary")
        c.drawString(100, 730, f"Owner: {st.session_state.get('owner', 'Not provided')}")
        c.drawString(100, 710, f"Problem: {st.session_state.get('problem', 'Not provided')}")
        c.drawString(100, 690, f"Project Type: {st.session_state.get('type', 'Not selected')}")
        c.save()

        with open(pdf_filename, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="project_summary.pdf">📥 Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)

# **Navigation Buttons (Instant Update)**
col1, col2 = st.columns([0.5, 0.5])
with col1:
    if st.session_state.page_index > 0:
        if st.button("⬅️ Previous"):
            navigate(-1)
with col2:
    if st.session_state.page_index < len(pages) - 1:
        if st.button("Next ➡️"):
            navigate(1)

# **Progress Bar**
progress = (st.session_state.page_index + 1) / len(pages)
st.progress(progress)
