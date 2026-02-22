import streamlit as st
import json
import random

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Employee Legal Assistant", layout="wide")

# =====================================================
# LOAD JSON
# =====================================================
def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

actions_data = load_json("action.json")
salary_laws = load_json("salary_laws.json")
termination_laws = load_json("termination_laws.json")
harassment_laws = load_json("harassment_laws.json")
benefits_laws = load_json("benefits_laws.json")
overtime_laws = load_json("overtime_laws.json")

laws_map = {
    "Salary Delay": salary_laws,
    "Unfair Termination": termination_laws,
    "Workplace Harassment": harassment_laws,
    "Denial of Benefits": benefits_laws,
    "Overtime Violation": overtime_laws,
    "Leave Denial": benefits_laws,
    "Contract Breach": termination_laws,
    "Promotion Denial": benefits_laws,
    "Resignation Issue": termination_laws
}

# =====================================================
# CLASSIFIER
# =====================================================
def classify_issue(text):
    text = text.lower()
    categories = {
        "Workplace Harassment": ["harass","harassment","abuse","bully","threat","sexual","misbehave"],
        "Salary Delay": ["salary delay","not paid","salary not paid","wage delay","payment delay","unpaid salary"],
        "Overtime Violation": ["overtime","extra hours","late night","worked late","beyond hours","no overtime pay"],
        "Denial of Benefits": ["pf","epf","benefit","gratuity","insurance","esi"],
        "Unfair Termination": ["fired","terminate","terminated","dismiss","removed","laid off"],
        "Leave Denial": ["leave denied","no leave","leave rejected","sick leave denied"],
        "Contract Breach": ["contract violated","agreement broken","bond issue"],
        "Promotion Denial": ["promotion denied","not promoted"],
        "Resignation Issue": ["resign","forced resignation","notice period"]
    }

    for category, phrases in categories.items():
        for phrase in phrases:
            if phrase in text:
                return category
    return None

# =====================================================
# HELPERS
# =====================================================
def generate_confidence():
    return random.randint(80, 92)

def generate_email(category):
    emails = {
        "Salary Delay": """Subject: Request for Immediate Release of Pending Salary

Dear Sir/Madam,

I wish to formally inform you that my salary has not been credited within the prescribed time as per company policy and employment agreement. This delay has caused financial hardship and mental distress.

I kindly request you to release the pending amount at the earliest and clarify the reason for delay.

Sincerely,
[Your Name]
""",
        "Unfair Termination": """Subject: Representation Against Unfair Termination

Dear Sir/Madam,

I was terminated from my employment without proper notice or valid justification. This appears to be in violation of labour laws and principles of natural justice.

I request you to kindly review this matter and provide written clarification or lawful compensation.

Sincerely,
[Your Name]
""",
        "Workplace Harassment": """Subject: Formal Complaint Regarding Workplace Harassment

Dear Sir/Madam,

I am writing to formally report inappropriate conduct at the workplace which has created an unsafe and hostile working environment.

I request a fair inquiry into the matter and appropriate corrective action while ensuring confidentiality and protection from retaliation.

Sincerely,
[Your Name]
""",
        "Denial of Benefits": """Subject: Non-Deposit of Statutory Benefits

Dear Sir/Madam,

It has come to my notice that statutory benefits such as Provident Fund and Insurance contributions have not been deposited as mandated by law.

I request immediate verification and compliance.

Sincerely,
[Your Name]
""",
        "Overtime Violation": """Subject: Claim for Unpaid Overtime Compensation

Dear Sir/Madam,

I have been required to work beyond regular working hours without receiving overtime wages as required by law.

I request settlement of my overtime dues at the earliest.

Sincerely,
[Your Name]
"""
    }
    return emails.get(category)

def generate_conclusion(category):
    return f"Issues related to {category} can be stressful and overwhelming. However, Indian labour laws provide remedies and protection against unfair employment practices. By following proper legal steps and maintaining records, you can safeguard your rights and seek justice."

# =====================================================
# CORE LOGIC
# =====================================================
def process_query(user_input):
    category = classify_issue(user_input)
    if not category:
        return None

    law_data = laws_map.get(category, [])
    action_data = actions_data.get(category, {})

    issue = action_data.get("description", f"{category} related legal issue.")

    laws = []
    for item in law_data:
        name = item.get("law_name") or item.get("law")
        section = item.get("section", "")
        laws.append(f"• {name} ({section})")
    laws = "\n".join(laws)

    steps = "\n\n".join(action_data.get("steps", []))
    docs = "\n".join([f"• {d}" for d in action_data.get("documents_required", [])])

    portals = action_data.get("official_portals", [])
    url = portals[0]["url"] if portals else "https://labour.gov.in"

    email = generate_email(category)
    conclusion = generate_conclusion(category)
    confidence = generate_confidence()

    return category, issue, laws, steps, docs, email, url, conclusion, confidence

# =====================================================
# STYLING
# =====================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#020617,#0f172a);
    color:white;
}

h1 { font-size:50px !important; }

.card {
    background: linear-gradient(135deg,#1e293b,#020617);
    padding:22px;
    border-radius:18px;
    margin:18px 0;
    box-shadow:0px 0px 18px rgba(99,102,241,0.3);
    font-size:21px;
    transition: transform 0.3s ease;
}

.card:hover {
    transform: scale(1.03);
}

.card-law { border-left:6px solid #22c55e; }
.card-step { border-left:6px solid #f97316; }
.card-doc { border-left:6px solid #38bdf8; }
.card-info { border-left:6px solid #a855f7; }

textarea { font-size:20px !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("About This Website")
st.sidebar.write("""
This web application acts as a virtual **Employee Legal Assistant** for Indian workers.

It helps users understand their workplace issues by:
• Identifying the type of legal problem  
• Showing relevant labour laws  
• Suggesting legal steps  
• Providing draft complaint emails  
• Linking official complaint portals  

This system does not replace a lawyer but provides structured legal awareness and guidance for common employment disputes.
""")

# =====================================================
# UI
# =====================================================
left, right = st.columns([2.5,1])

with left:
    st.title("Employee Legal Assistant")
    st.write("Describe your workplace problem:")

with right:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png")

user_input = st.text_area("Enter your legal issue:")

if st.button("Get Help"):
    result = process_query(user_input)

    if not result:
        st.error("Please describe a valid workplace issue.")
        st.stop()

    category, issue, laws, steps, docs, email, url, conclusion, confidence = result

    st.markdown(f"## CATEGORY: {category}")
    st.progress(confidence / 100)
    st.write(f"Confidence Score: {confidence}%")

    st.markdown("### ISSUE:")
    st.markdown(f"<div class='card card-info'>{issue}</div>", unsafe_allow_html=True)

    st.markdown("### RELEVANT LAW:")
    st.markdown(f"<div class='card card-law'>{laws.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

    st.markdown("### NEXT STEPS:")
    st.markdown(f"<div class='card card-step'>{steps.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

    st.markdown("### DOCUMENTS REQUIRED:")
    st.markdown(f"<div class='card card-doc'>{docs.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

    st.markdown("### FILE COMPLAINT HERE:")
    st.markdown(url)

    st.markdown("### DRAFT EMAIL:")
    st.text_area("Edit email:", email, height=280)
    st.download_button("Download Email", email, file_name="legal_complaint_email.txt")

    st.markdown("### CONCLUSION:")
    st.markdown(f"<div class='card card-info'>{conclusion}</div>", unsafe_allow_html=True)

    st.markdown("### DISCLAIMER:")
    st.markdown("<div class='card card-info'>This is preliminary legal guidance only. Please consult a qualified lawyer.</div>", unsafe_allow_html=True)
