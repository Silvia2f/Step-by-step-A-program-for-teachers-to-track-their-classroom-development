import pandas as pd
from datetime import datetime
from tabulate import tabulate
import matplotlib.pyplot as plt
import streamlit as st 
import seaborn as sns



def load_csv(filepath): #here I load the csv file and parse the dates
    df = pd.read_csv(filepath)

    #Updated this if statement because the streamlit would give me an error with the date column. 
    if 'Date' in df.columns:
        df['parsed_date'] = pd.to_datetime(df['Date'], format='%b %d, %Y', errors='coerce').dt.date
        df.drop(columns=['Date'], inplace=True)
    else:
        df['parsed_date'] = pd.to_datetime(df['parsed_date'], errors='coerce').dt.date


    # Added this so if the flags arent in the csv they dont show up as NaN on the table
    if 'Flag' not in df.columns:
        df['Flag'] = ""
    else:
        df['Flag'] = df['Flag'].fillna("")

    print(df.head()) #here I check if it loaded correclty
    return df

    #Now I replace the old CLI input with the Streamlit interface (at the bottom of my code)

#Updated this once again to start using Seaborn
def plot_category_progress(df): 
    categories = list(df['Category'].unique())
    selected_category = st.selectbox("Pick a category to plot progress for:", categories)

    df_cat = df[df['Category'] == selected_category].copy()
    df_cat = df_cat.sort_values('parsed_date')

    if df_cat.empty:
        st.info("No data available for this category.")
        return

    st.write(df_cat[['parsed_date', 'Milestone']])

    # Create the Seaborn-style plot
    plt.figure(figsize=(10, 5))
    sns.set_theme(style="whitegrid")  # sets a clean background
    
    sns.lineplot(data=df_cat, x='parsed_date', y='Milestone', marker='o', linewidth=2.5)

    # Add average line
    average = df_cat['Milestone'].mean()
    plt.axhline(average, color='gray', linestyle='--', linewidth=1)
    plt.text(df_cat['parsed_date'].iloc[-1], average, f' Avg: {average:.1f}', 
             color='gray', fontsize=9, va='bottom')

    # Labels and title
    plt.title(f"{df['Child'].iloc[0]}'s Progress in '{selected_category}' Category", fontsize=14) #Tweaked the title to include the child's name v2-B
    plt.xlabel("Date")
    plt.ylabel("Milestone")
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt.gcf())


def plot_overall_distribution(df):
    #Since this is for all the categories, first I count how many entries there are for each category
    category_counts = df['Category'].value_counts()

    #then I plot a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title("Overall Log Distribution by Category")
    plt.tight_layout()
    st.pyplot(plt.gcf()) #replaced this too with the st.pyplot so it appears in streamlit and not in the CLI window

#replaced older code with streamlit code 
df = load_csv("data/test_data.csv")

#Added this section for child selection filter V2-B
child_options = df['Child'].unique().tolist()
selected_child = st.selectbox("Select a child", child_options)
df = df[df['Child'] == selected_child]

st.title("Step by Step: Child Progress Tracker")
st.subheader("Current Data")
st.dataframe(df)

#I chnaged the following lines of code (until the if statement) so I moved the entry log to the sidebar.
st.sidebar.header("Add New Log Entry")
child_name = st.sidebar.text_input("Child's name", value=selected_child)  #updated this as well so user can input the child name


categories = df['Category'].unique().tolist()
category = st.sidebar.selectbox("Select a Category", categories)
existing = df[df['Category'] == category]
current_max = existing['Milestone'].max() if not existing.empty else -1
st.sidebar.text(f"Previous milestone: {current_max}")
milestone = st.sidebar.number_input("Enter milestone number", min_value=0, step=1)
flag = ""
if milestone < current_max:
    flag = "regression"
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
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("data/test_data.csv", index=False) #I have added this line so entries start getting saves and appear on the graph

    st.success("New log entry added!")
    st.dataframe(df.tail(1))


#Now I add another button with a dropdown to actually view the graphs for each category
with st.expander("View Category Graphs", expanded=False):
    plot_category_progress(df)
#Lastly I add the pie chart button
with st.expander("Display Pie Chart for Overall Progress", expanded=False):
    plot_overall_distribution(df)