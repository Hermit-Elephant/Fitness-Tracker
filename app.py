import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fitness Energy Dashboard", layout="wide")

st.title("🏋️ Fitness Energy Dashboard")

# ==================================
# BODY DETAILS
# ==================================

st.sidebar.header("⚖️ Body Setup")

current_weight = st.sidebar.number_input("Current Weight (kg)", value=70)
target_weight = st.sidebar.number_input("Target Weight (kg)", value=65)

goal = st.sidebar.selectbox(
    "Goal",
    ["Weight Loss", "Maintain", "Muscle Gain"]
)

# ==================================
# CALORIE REQUIREMENT
# ==================================

maintenance_calories = current_weight * 30

if goal == "Weight Loss":
    target_calories = maintenance_calories - 500
elif goal == "Muscle Gain":
    target_calories = maintenance_calories + 300
else:
    target_calories = maintenance_calories

# ==================================
# FOOD DATABASE (AUTO NUTRIENTS)
# ==================================

food_db = pd.DataFrame({
    "Food":[
        "Whole Egg",
        "Egg White",
        "Rice (1 cup)",
        "Roti",
        "Chicken Curry 100g",
        "Dal (1 bowl)",
        "Banana",
        "Grapes 100g",
        "Whey Protein",
        "Peanut Butter 1 tbsp",
        "Milk 250ml"
    ],
    "Calories":[70,17,200,120,220,180,100,70,120,95,150],
    "Protein":[6,4,4,3,28,9,1,1,24,4,8],
    "Carbs":[1,0,45,20,5,25,27,18,3,3,12],
    "Fat":[5,0,0,2,10,3,0,0,1,8,8]
})

# ==================================
# SESSION STATE STORAGE
# ==================================

if "food_log" not in st.session_state:
    st.session_state.food_log = pd.DataFrame(
        columns=["Food","Qty","Calories","Protein","Carbs","Fat"]
    )

# ==================================
# FOOD ENTRY
# ==================================

st.sidebar.header("🍽 Add Food")

food_selected = st.sidebar.selectbox("Select Food", food_db["Food"])
quantity = st.sidebar.number_input("Quantity", 1)

if st.sidebar.button("Add Food"):

    food_row = food_db[food_db["Food"] == food_selected]

    new_entry = {
        "Food": food_selected,
        "Qty": quantity,
        "Calories": food_row["Calories"].values[0] * quantity,
        "Protein": food_row["Protein"].values[0] * quantity,
        "Carbs": food_row["Carbs"].values[0] * quantity,
        "Fat": food_row["Fat"].values[0] * quantity,
    }

    st.session_state.food_log = pd.concat(
        [st.session_state.food_log, pd.DataFrame([new_entry])],
        ignore_index=True
    )

# ==================================
# TOTAL NUTRIENTS
# ==================================

log = st.session_state.food_log

total_calories = log["Calories"].sum()
total_protein = log["Protein"].sum()
total_carbs = log["Carbs"].sum()
total_fat = log["Fat"].sum()

remaining = target_calories - total_calories

# ==================================
# DASHBOARD METRICS
# ==================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("🔥 Target Calories", int(target_calories))
col2.metric("🍽 Calories Consumed", int(total_calories))
col3.metric("⚖️ Calories Remaining", int(remaining))
col4.metric("💪 Protein Intake", f"{int(total_protein)} g")

# ==================================
# NUTRIENT BREAKDOWN
# ==================================

st.subheader("🥗 Nutrient Breakdown")

c1, c2, c3 = st.columns(3)

c1.metric("Protein", f"{int(total_protein)} g")
c2.metric("Carbs", f"{int(total_carbs)} g")
c3.metric("Fat", f"{int(total_fat)} g")

# ==================================
# FOOD LOG TABLE
# ==================================

st.subheader("📋 Today's Food Log")
st.dataframe(log, use_container_width=True)
