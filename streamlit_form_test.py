#!pip install streamlit
import streamlit as st
import pandas as pd
import sqlite3
from streamlit import *

def create_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS entries (ID INTEGER PRIMARY KEY, Timestamp TEXT, Email TEXT, FirstName TEXT, LastName TEXT, LinkedInProfile TEXT, PortfolioLink TEXT, ExperienceLevel TEXT, Skills TEXT, ResumeLink TEXT, OpenToJobs INTEGER)')
    conn.commit()
    conn.close()

def save_data():
    timestamp = st.text_input('Timestamp')
    email = st.text_input('Email')
    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    linkedin_profile = st.text_input('LinkedIn Profile')
    portfolio_link = st.text_input('Portfolio Link')
    experience_level = st.text_input('Experience Level')
    skills = st.text_input('Skills (Top 3, Comma Separated)')
    resume_link = st.text_input('Link to Resume')
    open_to_jobs = st.checkbox('Open To Receiving Jobs?')

    if st.button('Save'):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO entries (Timestamp, Email, FirstName, LastName, LinkedInProfile, PortfolioLink, ExperienceLevel, Skills, ResumeLink, OpenToJobs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (timestamp, email, first_name, last_name, linkedin_profile, portfolio_link, experience_level, skills, resume_link, open_to_jobs))
        conn.commit()
        conn.close()
        st.success('Data saved successfully!')

def view_data():
    conn = sqlite3.connect('data.db')
    data = pd.read_sql_query('SELECT * FROM entries', conn)
    conn.close()
    st.dataframe(data)

st.title('Data Entry and Display App')

create_table()
save_data()
view_data()
