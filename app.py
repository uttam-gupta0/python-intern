import streamlit as st
from parser import parse_resume
import pandas as pd
import json

st.set_page_config(page_title="Smart Resume Parser", page_icon="🧠")

st.title("🧠 Smart Resume Parser")
st.write("Upload a PDF or DOCX resume and extract structured information automatically.")

uploaded = st.file_uploader("📂 Upload Resume", type=["pdf", "docx", "txt"])

if uploaded:
    with open("temp_resume", "wb") as f:
        f.write(uploaded.getbuffer())

    st.info("🔍 Parsing resume... please wait")
    result = parse_resume("temp_resume")

    st.subheader("📋 Extracted Information")
    st.json(result)

    # Skills Table
    if result["skills"]:
        st.subheader("🧩 Detected Skills")
        st.table(pd.DataFrame({"Skill": result["skills"]}))
    else:
        st.warning("No skills detected — try updating your skills list!")

    # Download JSON
    json_bytes = json.dumps(result, indent=2).encode("utf-8")
    st.download_button("⬇️ Download as JSON", data=json_bytes,
                       file_name="resume_data.json", mime="application/json")

    # Download CSV
    df = pd.DataFrame([{
        "Name": result['name'],
        "Email": result['email'],
        "Phone": result['phone'],
        "Skills": ", ".join(result['skills']),
        "Education": " | ".join(result['education']) if result['education'] else "",
        "Experience": result['experience']
    }])
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download as CSV", data=csv,
                       file_name="resume_summary.csv", mime="text/csv")
