import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st 
import seaborn as sns

"""
main.py - Step-by-Step: Child Progress Tracker

This Streamlit app allows educators to log and visualize developmental milestones
for children in various categories like Mobility, Language, Social Emotional, and Fine Motor.

Features:
- Log entries manually
- View progress per category
- Classroom-wide comparisons using pie charts

To run:
    streamlit run main.py

Author: Silvia Alberti
Last updated: August 1st, 2025
"""


def load_csv(filepath):
    """
    Loads the CSV and parses dates and flags.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Cleaned DataFrame with 'parsed_date' and 'Flag' columns.
    """
    
    df = pd.read_csv(filepath)

    #Updated this if statement because the streamlit would give me an error with the date column. 
    if 'Date' in df.columns:
        df['parsed_date'] = pd.to_datetime(df['Date'], format='%b %d, %Y', errors='coerce').dt.date
        # GOTCHA: If the date format in the CSV is wrong or inconsistent, parsing may silently fail and return NaT.
        df.drop(columns=['Date'], inplace=True)
    else:
        df['parsed_date'] = pd.to_datetime(df['parsed_date'], errors='coerce').dt.date


    #Added this so if the flags arent in the csv they dont show up as NaN on the table
    if 'Flag' not in df.columns:
        df['Flag'] = ""
    else:
        df['Flag'] = df['Flag'].fillna("")
    return df

    #Now I replace the old CLI input with the Streamlit interface (at the bottom of my code)


def plot_category_progress(df): 
    """
    Display a line chart of milestone progress for a selected category.

    Args:
        df (pd.DataFrame): Filtered DataFrame for the selected child.

    Returns:
        None. Displays the chart using Streamlit.
    """
    categories = list(df['Category'].unique())
    selected_category = st.selectbox("Pick a category to plot progress for:", categories)

    df_cat = df[df['Category'] == selected_category].copy()
    df_cat = df_cat.sort_values('parsed_date')

    if df_cat.empty:
        st.info("No data available for this category.")
        return

    st.write(df_cat[['parsed_date', 'Milestone']])

    #Create the Seaborn-style plot
    plt.figure(figsize=(10, 5))
    sns.set_theme(style="whitegrid")  # sets a clean background
    
    sns.lineplot(data=df_cat, x='parsed_date', y='Milestone', marker='o', linewidth=2.5)

    #Add average line
    average = df_cat['Milestone'].mean()
    plt.axhline(average, color='gray', linestyle='--', linewidth=1)
    plt.text(df_cat['parsed_date'].iloc[-1], average, f' Avg: {average:.1f}', 
             color='gray', fontsize=9, va='bottom')

    #Labels and title
    plt.title(f"{df['Child'].iloc[0]}'s Progress in '{selected_category}' Category", fontsize=14) #Include child name in chart title

    plt.xlabel("Date")
    plt.ylabel("Milestone")
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt.gcf())


def plot_overall_distribution(df):
    """
    Display a pie chart showing the distribution of milestone logs by category
    for a selected child.

    Args:
        df (pd.DataFrame): Filtered DataFrame containing logs for one child.

    Returns:
        None. Displays a pie chart using Streamlit.
    """
    #Since this is for all the categories, first I count how many entries there are for each category
    category_counts = df['Category'].value_counts()

    #Then I plot a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title("Overall Log Distribution by Category")
    plt.tight_layout()
    st.pyplot(plt.gcf()) 

# === Load initial dataset ===
df_full = load_csv("data/test_data.csv")

#Here I initialize session state for selected child 
if 'selected_child' not in st.session_state:
    st.session_state.selected_child = df_full['Child'].iloc[0] if not df_full.empty else ""

child_options = df_full['Child'].unique().tolist()

# === Child selector ===
selected_child = st.selectbox(
    "Select a child", 
    child_options, 
    index=child_options.index(st.session_state.selected_child) if st.session_state.selected_child in child_options else 0
)

df_filtered = df_full[df_full['Child'] == selected_child]

# === Display table ===
st.title("Step by Step: Child Progress Tracker")
st.subheader("Current Data")
st.dataframe(df_filtered)

#Sidebar form for logging new milestone entry
st.sidebar.header("Add New Log Entry")
child_name = st.sidebar.text_input("Child's name", value=selected_child)  #Allow manual input of child name

categories = ['Mobility', 'Social Emotional', 'Cognitive', 'Language', 'Fine Motor'] #Fixed small mistake here, it was not showing the categories correctly
category = st.sidebar.selectbox("Select a Category", categories)
existing_logs = df_full[(df_full['Child'] == child_name) & (df_full['Category'] == category)]
current_max = existing_logs['Milestone'].max() if not existing_logs.empty else -1 # Check existing logs for this child and category to find highest milestone
milestone = st.sidebar.number_input("Enter milestone number", min_value=0, step=1)
flag = ""
if milestone < current_max:
    flag = "regression" # Flag if milestone is lower than previous maximum
    st.sidebar.warning(f"This milestone is lower than the current max ({current_max})")
note = st.sidebar.text_input("Add a note")
if st.sidebar.button("Add Log Entry"):
    new_row = {
        'Child': child_name, 
        'Category': category,
        'Milestone': int(milestone),
        'Note': note,
        'parsed_date': datetime.now().date(),
        'Flag': flag,
    }
    df_full = pd.concat([df_full, pd.DataFrame([new_row])], ignore_index=True)
    df_full.to_csv("data/test_data.csv", index=False)

    #Set selected child so the dropdown updates after saving
    st.session_state.selected_child = child_name
    st.rerun()

# === Plotting section ===
#Section: category progress chart
with st.expander("View Category Graphs", expanded=False):
    plot_category_progress(df_filtered)
#Section: overall category distribution chart
with st.expander("Display Pie Chart for Overall Progress", expanded=False):
    plot_overall_distribution(df_filtered)

#Section: classroom comparison by category
st.sidebar.markdown("---")
st.sidebar.header("View Classroom Development")
show_classroom_dev = st.sidebar.checkbox("Show classroom overview by category")

# === Classroom Overview ===
if show_classroom_dev:
    st.subheader("Classroom Development by Category")
    selected_cat = st.selectbox("Select a category to compare children", categories)

    cat_df = df_full[df_full['Category'] == selected_cat]
    child_counts = cat_df['Child'].value_counts()

    if child_counts.empty:
        st.info("No data available for this category.")
    else:
        #Pie chart of child distribution for selected category
        plt.figure(figsize=(6, 6))
        plt.pie(child_counts, labels=child_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title(f"Distribution of Milestones in '{selected_cat}' Category")
        plt.tight_layout()
        st.pyplot(plt.gcf())