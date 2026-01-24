import streamlit as st
import requests
import os
import json
import pandas as pd
from dotenv import load_dotenv
import time

load_dotenv()

# App Configuration
st.set_page_config(
    page_title="AI CAR LEASE / LOAN INTELLIGENCE",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "http://localhost:8000"

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .contract-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #007bff;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .fairness-fair { color: #28a745; font-weight: bold; }
    .fairness-average { color: #ffc107; font-weight: bold; }
    .fairness-unfair { color: #dc3545; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

# Sidebar Authentication
with st.sidebar:
    st.title("📱 AI Car Intelligence")
    
    if st.session_state.user_id is None:
        auth_mode = st.radio("Account", ["Login", "Register"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if auth_mode == "Login":
            if st.button("Sign In"):
                try:
                    resp = requests.post(f"{API_BASE}/login", json={"username": username, "password": password})
                    data = resp.json()
                    if "user_id" in data:
                        st.session_state.user_id = data["user_id"]
                        st.session_state.username = data["username"]
                        st.rerun()
                    else: st.error(data.get("error", "Login failed"))
                except: st.error("Backend connection error")
        else:
            email = st.text_input("Email (Optional)")
            if st.button("Create Account"):
                try:
                    resp = requests.post(f"{API_BASE}/register", json={"username": username, "password": password, "email": email})
                    data = resp.json()
                    if "message" in data:
                        st.success("Account created! Please login.")
                    else: st.error(data.get("error", "Registration failed"))
                except: st.error("Backend connection error")
    else:
        st.success(f"Logged in as: **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Features")
    st.markdown("- SLA/Clause Extraction\n- Fairness Scoring\n- VIN Intelligence\n- Negotiation Scripts")

# Main Content
if st.session_state.user_id is None:
    st.title("Welcome to Car Lease Intelligence")
    st.info("Please login or register to analyze your contracts and save reports.")
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Contracts Analyzed", "1,200+")
    with col2: st.metric("Users Protected", "850+")
    with col3: st.metric("Dealer Transparency", "92%")
else:
    tab_dash, tab_analyze, tab_compare, tab_chat, tab_vin = st.tabs(["📊 Dashboard", "📄 New Analysis", "⚖️ Compare", "💬 Chat", "🔍 VIN Lookup"])

    # DASHBOARD TAB
    with tab_dash:
        st.header(f"Welcome back, {st.session_state.username}!")
        
        try:
            history_resp = requests.get(f"{API_BASE}/history/{st.session_state.user_id}")
            history = history_resp.json()
            
            if not history:
                st.info("You haven't analyzed any contracts yet. Head to 'New Analysis' to start!")
            else:
                st.subheader("Recent Contracts")
                for c in history[:5]:
                    sla = c.get("sla", {})
                    fairness = sla.get("fairness", {}) if sla else {}
                    score = fairness.get("fairness_score", "N/A")
                    verdict = fairness.get("verdict", "N/A")
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="contract-card">
                            <h4>{c['file_name']}</h4>
                            <p>Analyzed on: {c['created_at']}</p>
                            <p>Fairness Score: <b>{score}/100</b> | Verdict: <span class="fairness-{verdict.lower()}">{verdict}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"View Full Report: {c['id']}", key=f"btn_{c['id']}"):
                            st.session_state.selected_contract = c
                        
                if "selected_contract" in st.session_state:
                    sc = st.session_state.selected_contract
                    st.markdown("---")
                    st.subheader(f"Detail Analysis: {sc['file_name']}")
                    st.json(sc.get("sla", {}))
                    if st.button("Close Details"):
                        del st.session_state.selected_contract
                        st.rerun()
        except:
            st.error("Failed to load history")

    # ANALYZE TAB
    with tab_analyze:
        st.header("Analyze New Contract")
        uploaded_file = st.file_uploader("Upload car lease/loan PDF", type="pdf")
        
        if uploaded_file and st.button("Start AI Analysis"):
            with st.spinner("Processing document... (OCR + LLM Extraction)"):
                files = {"file": uploaded_file.getvalue()}
                params = {"user_id": st.session_state.user_id}
                resp = requests.post(f"{API_BASE}/analyze", files=files, params=params)
                
                if resp.status_code == 200:
                    data = resp.json()
                    st.success("Analysis Complete!")
                    
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.subheader("Fairness Level")
                        f = data.get("fairness", {})
                        st.metric("Fairness Score", f"{f.get('fairness_score')}/100", f.get("verdict"))
                        st.progress(f.get("fairness_score", 0) / 100)
                        
                        if f.get("reasons"):
                            st.markdown("**Core Findings:**")
                            for r in f["reasons"]: st.error(r)
                            
                    with c2:
                        st.subheader("SLA Summary")
                        sla = data.get("sla", {})
                        terms = {
                            "Monthly Payment": sla.get("monthly_payment"),
                            "APR": f"{sla.get('apr_percent')}%",
                            "Term": f"{sla.get('term_months')} months",
                            "Down Payment": sla.get("down_payment")
                        }
                        st.json(terms)

                    st.markdown("---")
                    st.subheader("🤝 Negotiation Strategy")
                    points = data.get("negotiation_points", [])
                    for p in points: st.markdown(f"✅ {p}")
                    
                    with st.expander("📧 Generated Negotiation Email"):
                        st.code(data.get("negotiation_email", "Email loading..."), language="markdown")
                    
                    st.markdown("---")
                    st.subheader("📊 Buy vs Lease Comparison")
                    if sla.get("loan_type") == "Vehicle Lease":
                        st.write("Since this is a lease, here is the estimated cost of ownership vs buying:")
                        monthly = sla.get("monthly_payment", 0)
                        term = sla.get("term_months", 36)
                        total_lease = monthly * term + sla.get("down_payment", 0)
                        st.write(f"Total Lease Cost over {term} months: **${total_lease:,}**")
                        st.write("Estimated Buy Cost for same car: **$35,000** (Example)")
                        if total_lease > 20000:
                            st.warning("Strategy: This lease cost is high relative to vehicle value. Negotiate residual value!")
                    
                    if st.button("Download Full Analysis PDF"):
                        st.info("Generating report... (Feature in Progress - Backend Integration Required)")
                else:
                    st.error("Analysis failed. Please try a different PDF.")

    # COMPARE TAB
    with tab_compare:
        st.header("Side-by-Side Comparison")
        c1, c2 = st.columns(2)
        with c1: f1 = st.file_uploader("Contract A", type="pdf")
        with c2: f2 = st.file_uploader("Contract B", type="pdf")
        
        if f1 and f2 and st.button("Compare Contracts"):
            with st.spinner("Comparing..."):
                files = {"file1": f1.getvalue(), "file2": f2.getvalue()}
                resp = requests.post(f"{API_BASE}/compare", files=files)
                if resp.status_code == 200:
                    res = resp.json()
                    col1, col2 = st.columns(2)
                    for i, (col, key) in enumerate(zip([col1, col2], ["contract1", "contract2"])):
                        with col:
                            st.subheader(res[key]["filename"])
                            st.metric("Fairness", f"{res[key]['fairness']['fairness_score']}/100")
                            st.write(res[key]["sla"])
                    
                    st.success(f"Winner: {res.get('better_deal')} is the more favorable deal.")

    # CHAT TAB
    with tab_chat:
        st.header("💬 Chat with your Contract")
        
        # 1. Select Contract
        if "history_list" not in st.session_state:
            try:
                hist = requests.get(f"{API_BASE}/history/{st.session_state.user_id}").json()
                st.session_state.history_list = hist
            except:
                st.session_state.history_list = []
        
        contracts = {f"{c['file_name']} (ID: {c['id']})": c['id'] for c in st.session_state.history_list}
        selected_name = st.selectbox("Select a contract to discuss:", options=list(contracts.keys()))
        
        if selected_name:
            selected_id = contracts[selected_name]
            
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            # Display chat
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            # Chat Input
            if prompt := st.chat_input("Ask about mileage, penalties, or clauses..."):
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.spinner("AI is reading the contract..."):
                    try:
                        resp = requests.post(f"{API_BASE}/chat", json={
                            "contract_id": selected_id,
                            "message": prompt,
                            "history": st.session_state.messages[:-1]
                        })
                        bot_reply = resp.json().get("response", "Error connecting to AI.")
                    except:
                        bot_reply = "Connection Error."
                
                with st.chat_message("assistant"):
                    st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # VIN TAB
    with tab_vin:
        st.header("Vehicle Identification & Price Check")
        vin = st.text_input("Enter 17-digit VIN")
        if vin and st.button("Decode VIN"):
            with st.spinner("Fetching global vehicle data..."):
                resp = requests.get(f"{API_BASE}/vin/{vin}")
                if resp.status_code == 200:
                    v = resp.json()
                    st.success("Vehicle Found")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Make:** {v.get('make')}")
                        st.write(f"**Model:** {v.get('model')}")
                        st.write(f"**Year:** {v.get('year')}")
                    with col2:
                        st.metric("Est. Market Value", v.get("estimated_market_price"))
                        st.info(v.get("recalls_note"))
                else:
                    st.error("Invalid VIN or connection error")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 AI CAR LEASE INTELLIGENCE - Enterprise Grade")