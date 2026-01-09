###############################################
# FTZ Savings – Agentic AI Calculator (MAIN)
###############################################

import streamlit as st
import pandas as pd
import difflib
import os
import pandas as pd
from datetime import datetime


# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="FTZ Savings – Agentic AI Calculator",
    layout="wide",
    page_icon="💼"
)

# -----------------------------
# MONEY FORMATTER
# -----------------------------
def money(x):
    try:
        x = float(x)
    except:
        return x
    return f"(${abs(x):,.0f})" if x < 0 else f"${x:,.0f}"

# -----------------------------
# GLOBAL STYLE (CLEAN & LIGHT)
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#f8fafc,#eef2f7);
}
h1,h2,h3 {
    color:#0f172a;
}
.soft-card {
    background:white;
    border-radius:10px;
    padding:14px;
    box-shadow:0 3px 10px rgba(0,0,0,0.08);
}
.kpi-card {
    background:#0f172a;
    color:white;
    border-radius:10px;
    padding:14px;
    text-align:center;
}
.kpi-value {
    font-size:20px;
    font-weight:700;
}
.glass {
    background:rgba(15,23,42,0.75);
    backdrop-filter:blur(12px);
    padding:24px;
    border-radius:14px;
    color:white;
}

/* COMPLETELY HIDE STREAMLIT SIDEBAR */
[data-testid="stSidebar"] {
    display: none;
}


.chat-user {color:#0f172a;font-weight:600;}
.chat-ai {color:#2563eb;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div style="text-align:center">
<h1>FTZ Savings – Agentic AI Calculator</h1>
<img src="https://media.licdn.com/dms/image/v2/D4E3DAQFJGwigqBHKlA/image-scale_191_1128/B4EZiEeml4GwAc-/0/1754569272021/mas_acme_cover?e=2147483647&v=beta&t=rwzmlYeduqWUeo3PoaYkuiFgagFfpPn9CT8oEEda9V4"
     style="width:160px;border-radius:8px">
<p style="max-width:800px;margin:auto;color:#334155">
We MAS US Holdings have created a best-in-class, transparent, and conversion-focused digital experience,
ready to drive full spectrum of value unlocks through the FTZ apparel offering.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# INPUTS (16 FIELDS)
# -----------------------------
# st.subheader("Customer Data Assumptions")

# c1,c2,c3,c4 = st.columns(4)

# with c1:
#     shipments_per_week = st.number_input("Shipments / Week",1, value=2)
#     export_pct = st.number_input("Export %",0.0,100.0,1.0)

# with c2:
#     avg_import_value = st.number_input("Avg Import Value ($)",1000,value=50000,step=1000)
#     offspec_pct = st.number_input("Off-Spec %",0.0,100.0,0.25)

# with c3:
#     mpf_pct = st.number_input("MPF %",0.0,100.0,0.35)
#     hmf_pct = st.number_input("HMF %",0.0,100.0,0.13)

# with c4:
#     broker_cost = st.number_input("Broker Cost ($/entry)",0.0,value=125.0)
#     duty_pct = st.number_input("Avg Duty %",0.0,100.0,30.0)

# st.markdown("---")

# -----------------------------
# INPUTS (16 FIELDS TOTAL)
# -----------------------------
# =====================================================
# COMPACT 16 INPUT FIELDS — 4 x 4 GRID
# =====================================================

st.subheader("Customer Data Assumptions")

# -------- ROW 1 --------
r1c1, r1c2, r1c3, r1c4 = st.columns(4)

with r1c1:
    shipments_per_week = st.number_input("Shipments / Week", min_value=1, value=2)

with r1c2:
    avg_import_value = st.number_input(
        "Avg Import Value ($)", min_value=1000, value=50000, step=1000
    )

with r1c3:
    mpf_pct = st.number_input("MPF %", 0.0, 100.0, 0.35)

with r1c4:
    broker_cost = st.number_input("Broker Cost ($/entry)", min_value=0.0, value=125.0)


# -------- ROW 2 --------
r2c1, r2c2, r2c3, r2c4 = st.columns(4)

with r2c1:
    export_pct = st.number_input("Export %", 0.0, 100.0, 1.0)

with r2c2:
    offspec_pct = st.number_input("Off-Spec %", 0.0, 100.0, 0.25)

with r2c3:
    hmf_pct = st.number_input("HMF %", 0.0, 100.0, 0.13)

with r2c4:
    duty_pct = st.number_input("Avg Duty %", 0.0, 100.0, 30.0)


# -------- ROW 3 — COSTS WITH FTZ --------
st.markdown("**Costs With FTZ (Annual)**")

r3c1, r3c2, r3c3, r3c4 = st.columns(4)

with r3c1:
    ftz_consult = st.number_input("FTZ Consulting ($)", value=50000)

with r3c2:
    ftz_mgmt = st.number_input("FTZ Management ($)", value=150000)

with r3c3:
    ftz_software = st.number_input("FTZ Software Fee ($)", value=40000)

with r3c4:
    ftz_bond = st.number_input("FTZ Operator Bond ($)", value=1000)


# -------- ROW 4 — COSTS WITHOUT FTZ --------
st.markdown("**Costs Without FTZ (Annual)**")

r4c1, r4c2, r4c3, r4c4 = st.columns(4)

with r4c1:
    noftz_consult = st.number_input("Consulting (No FTZ) ($)", value=0)

with r4c2:
    noftz_mgmt = st.number_input("Management (No FTZ) ($)", value=0)

with r4c3:
    noftz_software = st.number_input("Software (No FTZ) ($)", value=0)

with r4c4:
    noftz_bond = st.number_input("Operator Bond (No FTZ) ($)", value=0)



# =========================================================
# CORE CALCULATIONS — DEFINE ALL VARIABLES ONCE
# =========================================================

# --- Percentage conversions ---
export_sales = export_pct / 100
off_spec = offspec_pct / 100
mpf_rate = mpf_pct / 100
hmf_rate = hmf_pct / 100
avg_duty = duty_pct / 100

# --- Annual import value ---
total_import_value = shipments_per_week * avg_import_value * 52

# --- Duty calculations ---
total_duty = total_import_value * avg_duty
duty_saved_export = total_import_value * export_sales * avg_duty
duty_saved_offspec = total_import_value * off_spec * avg_duty

total_net_duty_no_ftz = total_duty
total_net_duty_with_ftz = total_duty - duty_saved_export - duty_saved_offspec

# --- Entry & MPF calculations ---
entries_per_year = shipments_per_week * 52

per_entry_mpf = min(avg_import_value * mpf_rate, 634.62)
mpf_no_ftz = per_entry_mpf * entries_per_year

weekly_mpf_base = shipments_per_week * avg_import_value * mpf_rate
mpf_with_ftz = min(weekly_mpf_base, 634.62) * 52

# --- Broker & HMF ---
broker_hmf_no_ftz = (
    entries_per_year * broker_cost
    + shipments_per_week * avg_import_value * hmf_rate
)

broker_hmf_with_ftz = (
    52 * broker_cost
    + shipments_per_week * avg_import_value * hmf_rate
)

# --- Operating costs ---
cost_with_ftz = ftz_consult + ftz_mgmt + ftz_software + ftz_bond
cost_without_ftz = noftz_consult + noftz_mgmt + noftz_software + noftz_bond

# --- Total landed cost ---
total_cost_without_ftz = (
    total_net_duty_no_ftz + mpf_no_ftz + broker_hmf_no_ftz + cost_without_ftz
)

total_cost_with_ftz = (
    total_net_duty_with_ftz + mpf_with_ftz + broker_hmf_with_ftz + cost_with_ftz
)

# --- Final savings ---
net_savings_to_brand = total_cost_without_ftz - total_cost_with_ftz




# -----------------------------
# BUTTONS
# -----------------------------
b1,b2,b3 = st.columns(3)

calculate = b1.button("📊 Calculate Savings", use_container_width=True)
#cta = b2.button("📞 Smart CTA", use_container_width=True)
details = b3.button("📄 Show Details", use_container_width=True)

# -----------------------------
# CALCULATIONS (ONLY SHOWN IF CLICKED)
# -----------------------------
# if calculate:
#     entries_year = shipments_per_week * 52
#     import_value = avg_import_value * shipments_per_week * 52
#     total_duty = import_value * (duty_pct/100)

#     savings_ftz = import_value * ((export_pct + offspec_pct)/100) * (duty_pct/100)
#     savings_no_ftz = 0

#     k1,k2,k3,k4 = st.columns(4)
#     with k1:
#         st.markdown(f"<div class='kpi-card'><div>Entries / Year</div><div class='kpi-value'>{entries_year:,}</div></div>",unsafe_allow_html=True)
#     with k2:
#         st.markdown(f"<div class='kpi-card'><div>Total Duty Baseline</div><div class='kpi-value'>{money(total_duty)}</div></div>",unsafe_allow_html=True)
#     with k3:
#         st.markdown(f"<div class='kpi-card'><div>Savings with FTZ</div><div class='kpi-value'>{money(savings_ftz)}</div></div>",unsafe_allow_html=True)
#     with k4:
#         st.markdown(f"<div class='kpi-card'><div>Savings without FTZ</div><div class='kpi-value'>{money(savings_no_ftz)}</div></div>",unsafe_allow_html=True)

# ---------------------------------------------------------
# MONEY FORMATTER (GLOBAL)
# ---------------------------------------------------------
def money_fmt_val(x):
    try:
        x = float(x)
    except:
        return x

    if x < 0:
        return f"(${abs(x):,.0f})"
    return f"${x:,.0f}"


# ---------------------------------------------------------
# UPDATED KPI CARDS — Revised Metrics Set
# ---------------------------------------------------------


if calculate:
    k1, k2, k3, k4 = st.columns(4)

    # -------- KPI 1 — Total Duty Baseline --------
    with k1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>💰 Total Duty Baseline</div>
            <div class='kpi-value'>
                {money_fmt_val(total_duty)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------- KPI 2 — Cost With FTZ --------
    with k2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>📦 Cost With FTZ</div>
            <div class='kpi-value'>
                {money_fmt_val(total_cost_with_ftz)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------- KPI 3 — Cost Without FTZ --------
    with k3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>🏷 Cost Without FTZ</div>
            <div class='kpi-value'>
                {money_fmt_val(total_cost_without_ftz)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------- KPI 4 — Net Savings --------
    with k4:
        savings_color = "#22c55e" if net_savings_to_brand >= 0 else "#ef4444"

        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>📉 Net Savings</div>
            <div class='kpi-value' style='color:{savings_color};'>
                {money_fmt_val(net_savings_to_brand)}
            </div>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------
# SMART CTA MODAL (SIMULATED)
# -----------------------------
# if cta:
#     st.markdown("""
#     <div class="glass">
#     <h3>Request a Consultation</h3>
#     </div>
#     """, unsafe_allow_html=True)

#     name = st.text_input("Name")
#     email = st.text_input("Email")
#     brand = st.text_input("Brand")
#     message = st.text_area("Message")

#     if st.button("Submit Request"):
#         st.success("✅ Request submitted. Our Customer Success Lead will contact you shortly.")
#         st.write({"name":name,"email":email,"brand":brand,"message":message})

# =========================================================
# SMART CTA — SEND REAL EMAIL (OUTLOOK / OFFICE 365)
# =========================================================
# ---------------------------------------------------------
# SMART CTA — STATE-SAFE VERSION
# ---------------------------------------------------------
if "cta_open" not in st.session_state:
    st.session_state.cta_open = False

cta = b2.button("📞 Smart CTA", use_container_width=True)
if cta:
    st.session_state.cta_open = True

if st.session_state.cta_open:

    st.markdown("---")
    st.markdown(
        "<h4 style='color:#0f172a;'>📞 Smart CTA — Request a Consultation</h4>",
        unsafe_allow_html=True
    )

    with st.form("smart_cta_form"):

        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input("Full Name *")
            company = st.text_input("Company *")

        with c2:
            email = st.text_input("Business Email *")
            phone = st.text_input("Phone Number")

        message = st.text_area(
            "Additional Notes (optional)",
            placeholder="Anything specific you'd like us to review before the call?"
        )

        submit = st.form_submit_button("📩 Request a Call")

    if submit:
        if not name or not company or not email:
            st.error("Please fill in all required fields.")
        else:
            st.success(
                "✅ Thank you! Your request has been received.\n\n"
                "Our FTZ advisory team will contact you shortly."
            )




# -----------------------------
# DETAILS PAGE NAV
# -----------------------------
if details:
    #st.switch_page("details.py")
    st.switch_page("pages/1_Show_Details.py")

# -----------------------------
# CHATBOT (UNCHANGED)
# -----------------------------
# st.markdown("---")
# st.subheader("💬 FTZ Chatbot Assistant")

# faq = {
#     "why ftz":"FTZ reduces duty exposure and improves cash flow."
# }

# if "chat" not in st.session_state:
#     st.session_state.chat=[]

# q = st.text_input("Ask a question")

# if st.button("Ask AI"):
#     ans = faq.get(q.lower(),"Thank you for your question, we are directing it to oscarc@masholdings.com")
#     st.session_state.chat.append(("You",q))
#     st.session_state.chat.append(("AI",ans))

# for s,m in st.session_state.chat:
#     st.markdown(f"<div class='chat-user'>{m}</div>" if s=="You" else f"<div class='chat-ai'>{m}</div>", unsafe_allow_html=True)

# =========================================================
# CHATBOT — MOSTLY ASKED QUESTIONS MATCHING
# =========================================================

st.markdown("---")
st.markdown("<h4 style='color:#0f172a;'>FTZ Chatbot Assistant</h4>", unsafe_allow_html=True)

# -------------------------
# FAQ DATASET
# -------------------------
faq_qa = {
    "ftz-enabled single-sku omnichannel advantages apparel 3pl": 
    "Think of one, unified inventory heartbeat serving DTC, marketplaces, and retail. "
    "In our FTZ, that single-SKU pool removes duplicate stock, cuts stockouts, and enables "
    "two-day promises—while the zone’s duty advantages keep more margin in your pocket. "
    "It’s the apparel-native system founders wish they had from day one.",

    "direct cash flow savings immediate not deferral": 
    "You’ll feel savings right away: duties vanish on exports and off-spec goods, MPF fees drop "
    "when we consolidate entries weekly, and you only part with duty when product enters U.S. commerce. "
    "It’s immediate cash you can redirect to growth, not just an accounting fiction.",

    "brands benefit most ftz omnichannel": 
    "Brands that import, move fast, and sell across channels—DTC expanding to wholesale, "
    "marketplace-heavy, international entrants, seasonal or high-SKU lines—see the biggest lift.",

    "how are numbers calculated": 
    "The calculator uses your operational inputs—shipments per week, average import value, "
    "export %, off-spec %, broker fees, and average duty rate. FTZ rules are applied to show "
    "duty saved on exports, off-spec relief, and MPF savings from weekly consolidation.",

    "numbers unusual outside typical ranges": 
    "No problem—outliers are fine. The calculator is directional. For unusual flows, "
    "a consultation unlocks a tuned, custom analysis.",

    "why savings negative": 
    "Negative savings signal volume, cost structure, or assumption issues. "
    "Higher consolidation, better HTS averages, and stronger export/off-spec flows "
    "often flip results positive.",

    "data bring consultation precise analysis": 
    "Bring HTS mix, channel split, return rates, freight modes, and your cost stack. "
    "These inputs unlock precision and actionable ROI insights.",

    "how estimate savings exported off spec inputs": 
    "Using shipments per week, average import value, export %, off-spec %, broker fees, "
    "and duty rate, the calculator converts flows into duty savings and entry reductions.",

    "what are mpf hmf weekly entry consolidation": 
    "MPF is capped per entry; HMF applies to ocean freight. Weekly consolidation "
    "reduces how often fees are paid—so savings compound quickly.",

    "hmf air land freight": 
    "HMF applies only to ocean freight. If your flow is air or land, it is excluded "
    "so results reflect reality.",

    "varying duty rates hts season accuracy": 
    "We start with an average duty rate to show direction. SKU-level precision "
    "comes during a consult.",

    "entries per shipment vs weekly consolidated entries": 
    "Non-FTZ assumes one entry per shipment; FTZ assumes one weekly entry. "
    "Enter shipments per week and the calculator models both automatically.",

    "difference vs global 3pls d2c brokers": 
    "We combine FTZ economics, apparel-native workflows, and omnichannel execution—"
    "speed, compliance, and margin in one system.",

    "support retail edi asn marketplace prep": 
    "Yes. One FTZ inventory pool feeds retail, marketplaces, and DTC—"
    "eliminating duplicate stock.",

    "how fast pilot go live 60 90 days": 
    "Our 60–90 day pilot connects systems, activates FTZ inventory, "
    "and runs live orders quickly.",

    "what not included calculator results": 
    "We focus on immediate savings. Working capital, inventory days, "
    "and deeper ROI come in custom models.",

    "quantify working capital inventory days": 
    "Yes—deferral, inventory pooling, and margin impacts are quantified "
    "during consultation.",

    "compliance guardrails audit ready apparel": 
    "Tight inventory controls, auditable entries, and apparel-specific SOPs "
    "keep operations compliant and scalable.",

    "export off spec ranges validation": 
    "Exports typically 0–30%; off-spec usually under 5%. "
    "Outliers are fine but directional.",

    "export share results pdf excel consult": 
    "Export PDF/Excel directly and use the consult CTA "
    "to turn estimates into execution."
}

faq_keys = list(faq_qa.keys())

# -------------------------
# MATCHING FUNCTION
# -------------------------
import difflib

def match_question(user_question: str):
    cleaned = user_question.lower().strip()

    match = difflib.get_close_matches(
        cleaned,
        faq_keys,
        n=1,
        cutoff=0.55
    )

    if match:
        return faq_qa[match[0]]

    return None

# -------------------------
# SESSION STATE
# -------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_q = st.text_input("Ask a question about FTZ:")

if st.button("Ask AI"):
    if user_q.strip():
        response = match_question(user_q)

        if not response:
            response = (
                "Thank you for your question, for further questions please contact "
                "the Customer Success Lead at MAS US Holdings at oscarc@masholdings.com."
            )

        st.session_state.chat_history.append(("You", user_q))
        st.session_state.chat_history.append(("AI", response))

# -------------------------
# RENDER CHAT HISTORY
# -------------------------
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(
            f"<div class='chat-user'><strong>You:</strong> {msg}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-ai'><strong>AI:</strong> {msg}</div>",
            unsafe_allow_html=True
        )


# -----------------------------
# DISCLAIMER
# -----------------------------
st.markdown("---")
st.markdown("""
**Disclaimer:**  
This calculator provides directional estimates only and does not constitute financial,
legal, or compliance advice.
""")
