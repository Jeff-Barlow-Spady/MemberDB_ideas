import streamlit as st
import validators
import sqlite3

# Create connection to database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        email TEXT,
        first_name TEXT,
        last_name TEXT,
        linkedin_profile TEXT,
        portfolio_link TEXT,
        experience_level TEXT,
        skills TEXT
    )
''')

# Input form
with st.form("entry_form"):

    st.header("Please enter your details")

    # Input fields
    timestamp = st.text_input('Timestamp')
    email = st.text_input('Email')  
    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    linkedin = st.text_input('LinkedIn Profile')
    portfolio = st.text_input('Portfolio Link')
    experience = st.selectbox('Experience Level', ['Beginner', 'Intermediate', 'Advanced'])
    skills = st.multiselect('Skills', ['Python', 'R', 'SQL', 'Tableau'])

    submit = st.form_submit_button("Submit")

    # Input validation
    if submit:
        if not validators.email(email):
            st.error("Invalid email")
            st.stop()
        
        if linkedin and not validators.url(linkedin):
            st.error("Invalid LinkedIn URL")
            st.stop()

        if portfolio and not validators.url(portfolio):
            st.error("Invalid Portfolio URL")
            st.stop()

# Save data to database
if submit:
    cursor.execute('''
        INSERT INTO entries (timestamp, email, first_name, last_name, 
        linkedin_profile, portfolio_link, experience_level, skills)
        VALUES (?,?,?,?,?,?,?,?)
    ''', (timestamp, email, first_name, last_name, linkedin, portfolio, experience, ",".join(skills)))

    conn.commit()

    st.success("Saved to database!")

# View data
entries = cursor.execute("SELECT * FROM entries").fetchall()
st.header("Submitted Entries")
st.dataframe(entries)

# Styling
st.markdown("<style>...</style>", unsafe_allow_html=True) 

# Close connection
conn.close()
