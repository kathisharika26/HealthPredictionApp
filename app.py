import re
import sqlite3
from datetime import date

import streamlit as st
import pandas as pd

# --- Database setup ---
conn = sqlite3.connect("health.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT,
    email TEXT,
    glucose REAL,
    haemoglobin REAL,
    cholesterol REAL,
    remarks TEXT
)
""")
conn.commit()


def add_patient(name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    c.execute(
        "INSERT INTO patients(name,dob,email,glucose,haemoglobin,cholesterol,remarks) VALUES(?,?,?,?,?,?,?)",
        (name, dob, email, glucose, haemoglobin, cholesterol, remarks)
    )
    conn.commit()


def view_patients():
    c.execute("SELECT * FROM patients")
    return c.fetchall()


def delete_patient(patient_id):
    c.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()


# --- UI ---
st.title("Health Prediction Application")

st.subheader("Patient Information")

name = st.text_input("Full Name")
dob = st.date_input("Date of Birth")
email = st.text_input("Email Address")

glucose = st.number_input("Glucose", min_value=0.0)
haemoglobin = st.number_input("Haemoglobin", min_value=0.0)
cholesterol = st.number_input("Cholesterol", min_value=0.0)

remarks = ""

if st.button("Submit"):

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("Please enter a valid email address")
        st.stop()

    if dob and dob > date.today():
        st.error("Date of Birth cannot be a future date")
        st.stop()

    if glucose > 140 and cholesterol > 200:
        remarks = "High Risk of Diabetes and Heart Disease"
    elif glucose > 140:
        remarks = "Possible Diabetes Risk"
    elif cholesterol > 200:
        remarks = "High Cholesterol Risk"
    elif haemoglobin < 12:
        remarks = "Possible Anemia"
    else:
        remarks = "Healthy"

    add_patient(name, str(dob), email, glucose, haemoglobin, cholesterol, remarks)
    st.success("Patient Record Saved Successfully")

st.write("### AI Prediction")
if remarks:
    st.info(remarks)

st.subheader("Patient Records")

records = view_patients()

if records:
    df = pd.DataFrame(
        records,
        columns=["ID", "Name", "DOB", "Email", "Glucose", "Haemoglobin", "Cholesterol", "Remarks"]
    )
    st.dataframe(df)

st.subheader("Delete Patient Record")

delete_id = st.number_input("Enter Patient ID to Delete", min_value=1, step=1)

if st.button("Delete Record"):
    delete_patient(delete_id)
    st.success("Record Deleted Successfully")
