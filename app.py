import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="Mahesh Fitness Dashboard",
    layout="wide"
)

st.title("🏋️ Personal Fitness Tracker")

# ===============================
# LOAD DATA
# ===============================

DATA_FILE = "fitness_data.csv"

try:
    df = pd.read_csv(DATA_FILE)
except:
    df = pd.DataFrame(columns=[
        "Date","Weight","Calories","Protein",
        "Steps","Sleep","Workout","Mood"
    ])

# ===============================
# SIDEBAR ENTRY FORM
# ===============================

st.sidebar.header("➕ Add Daily Entry")

entry_date = st.sidebar.date_input("Date", date.today())
weight = st.sidebar.number_input("Weight (kg)")
calories = st.sidebar.number_input("Calories")
protein = st.sidebar.number_input("Protein (g)")
steps = st.sidebar.number_input("Steps")
sleep = st.sidebar.number_input("Sleep (hrs)")
workout = st.sidebar.selectbox(
    "Workout",
    ["Rest","Gym","Cardio","Sports","Yoga"]
)
mood = st.sidebar.slider("Mood / Energy",1,10)

if st.sidebar.button("Save Entry"):

    new_data = pd.DataFrame([{
        "Date": entry_date,
        "Weight": weight,
        "Calories": calories,
        "Protein": protein,
        "Steps": steps,
        "Sleep": sleep,
        "Workout": workout,
        "Mood": mood
    }])

    df = pd.concat([df,new_data],ignore_index=True)
    df.to_csv(DATA_FILE,index=False)

    st.sidebar.success("Entry Saved ✅")

# ===============================
# DATA PREP
# ===============================

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

# ===============================
# KPI SECTION
# ===============================

if not df.empty:

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Latest Weight",f"{df['Weight'].iloc[-1]} kg")
    col2.metric("Calories Today",df['Calories'].iloc[-1])
    col3.metric("Protein Today",f"{df['Protein'].iloc[-1]} g")
    col4.metric("Steps Today",df['Steps'].iloc[-1])

# ===============================
# CHARTS
# ===============================

if not df.empty:

    st.subheader("📈 Progress Trends")

    tab1,tab2,tab3 = st.tabs(["Weight","Nutrition","Recovery"])

    with tab1:
        fig = px.line(df,x="Date",y="Weight",markers=True)
        st.plotly_chart(fig,use_container_width=True)

    with tab2:
        fig = px.line(
            df,
            x="Date",
            y=["Calories","Protein"]
        )
        st.plotly_chart(fig,use_container_width=True)

    with tab3:
        fig = px.line(
            df,
            x="Date",
            y=["Sleep","Mood"]
        )
        st.plotly_chart(fig,use_container_width=True)

# ===============================
# RAW DATA
# ===============================

st.subheader("📋 Fitness Log")

st.dataframe(df,use_container_width=True)
