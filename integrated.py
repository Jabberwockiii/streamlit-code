import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px

# Configuration
GITHUB_DATA_DIR = "/home/ubuntu/streamlit-code/static/githubstatic"  # Directory for GitHub data
FEDERAL_DATA_DIR = "./federal1"    # Directory for Federal data
HUGGINGFACE_DATA_DIR = "/home/ubuntu/streamlit-code/static/huggingfacestatic"  # Directory for Hugging Face data

# Function to read and aggregate GitHub data with granularity
def read_aggregate_github_files(start_date, end_date, data_dir, granularity):
    delta = timedelta(days=1)
    current_date = start_date
    all_data = []

    while current_date <= end_date:
        filename = os.path.join(data_dir, f"github_data_{current_date.strftime('%Y-%m-%d')}.json")
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                df = pd.read_json(file, lines=True)
            df['date'] = current_date
            all_data.append(df)
        current_date += delta

    full_df = pd.concat(all_data) if all_data else pd.DataFrame()
    if not full_df.empty:
        full_df = full_df.set_index('date')
        if granularity == 'Weekly':
            return full_df.resample('W').sum()
        elif granularity == 'Monthly':
            return full_df.resample('M').sum()
        elif granularity == 'Yearly':
            return full_df.resample('Y').sum()
    return full_df

# Function to plot GitHub data using Plotly
def plot_github_data(df, selected_models, selected_field):
    fig = px.line(df, x=df.index, y=selected_field, color='Repository', markers=True)
    fig.update_layout(title=f'GitHub {selected_field} Over Time', xaxis_title='Date', yaxis_title=selected_field)
    st.plotly_chart(fig, use_container_width=True)

# Function to read JSON data (Award Amount Visualization)
def read_federal_file(file_name, data_dir):
    with open(os.path.join(data_dir, file_name), 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

# Function to check if JSON file is empty
def is_json_file_empty(file_name, data_dir):
    file_path = os.path.join(data_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return len(data) == 0
    return True  # Treat non-existent files as empty

# Function to read Hugging Face GitHub data
def read_huggingface(start_date, end_date, data_dir):
    delta = timedelta(days=1)
    current_date = start_date
    all_data = []

    while current_date <= end_date:
        filename = os.path.join(data_dir, f"huggingface_models_{current_date.strftime('%Y-%m-%d')}.json")
        if os.path.exists(filename):
            df = pd.read_json(filename, lines=True)
            df['date'] = current_date
            all_data.append(df)
        current_date += delta

    return pd.concat(all_data) if all_data else pd.DataFrame()

# Function to plot Hugging Face data using Plotly
def plot_hugging_face_data(df):
    fig = px.line(df, x='date', y='downloads', color='modelId', markers=True, 
                  title='Hugging Face Model Downloads Over Time', labels={'date': 'Date', 'downloads': 'Downloads'})
    fig.update_layout(xaxis_title='Date', yaxis_title='Downloads', legend_title='Model ID')
    st.plotly_chart(fig, use_container_width=True)

# Streamlit UI
st.set_page_config(layout="wide")
mode = st.sidebar.selectbox("Select Mode", ["GitHub Data", "Award Amount Visualization", "Hugging Face Model Downloads"])

if mode == "GitHub Data":
    # GitHub Data UI and Logic
    st.sidebar.title("GitHub Data Settings")
    start_date = st.sidebar.date_input("Start date", datetime(2023, 10, 1))
    end_date = st.sidebar.date_input("End date", datetime.now())
    granularity = st.sidebar.selectbox("Select Granularity", ["Daily", "Weekly", "Monthly", "Yearly"])
    selected_field = st.sidebar.selectbox("Select Field to Plot", ['Stars', 'Watches', 'Forks'])

    if start_date <= end_date:
        df = read_aggregate_github_files(start_date, end_date, GITHUB_DATA_DIR, granularity)
        if not df.empty:
            model_ids = df['Repository'].unique()
            selected_models = st.sidebar.multiselect("Select Model IDs", model_ids, default=model_ids[:5])

            st.title("GitHub Statistics Over Time")
            if selected_models:
                filtered_df = df[df['Repository'].isin(selected_models)]
                plot_github_data(filtered_df, selected_models, selected_field)
                st.dataframe(filtered_df)  # Display data as a spreadsheet
            else:
                st.error("Please select at least one model.")
        else:
            st.error("No data available for the selected date range.")
    else:
        st.error("End date must fall after start date.")

elif mode == "Award Amount Visualization":
    # Award Amount Visualization UI and Logic
    st.title('Award Amount Visualization')

    # List available JSON files in the directory and filter out empty files
    json_files = [f for f in os.listdir(FEDERAL_DATA_DIR) if f.endswith('.json') and not is_json_file_empty(f, FEDERAL_DATA_DIR)]

    if json_files:
        selected_file = st.sidebar.selectbox('Select a JSON file', json_files)

        # Granularity selection
        granularity = st.sidebar.selectbox('Select granularity', ['Monthly', 'Quarterly', 'Yearly'])

        # Date column selection
        date_column = st.sidebar.selectbox('Select date column', ['Start Date', 'End Date'])

        # Read the selected JSON file
        df = read_federal_file(selected_file, FEDERAL_DATA_DIR)

        if not df.empty:
            if date_column in df.columns:
                df[date_column] = pd.to_datetime(df[date_column])
                df = df.sort_values(by=date_column)

                if granularity == 'Monthly':
                    df_resampled = df.resample('M', on=date_column).sum()
                elif granularity == 'Quarterly':
                    df_resampled = df.resample('Q', on=date_column).sum()
                else:  # Yearly
                    df_resampled = df.resample('Y', on=date_column).sum()

                fig = px.line(df_resampled, x=df_resampled.index, y='Award Amount', markers=True,
                              title=f'Award Amount Over Time ({granularity}, {date_column})')
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(df_resampled)  # Display resampled data as a spreadsheet
            else:
                st.error(f"The selected JSON file does not contain a '{date_column}' column.")
        else:
            st.error("The selected JSON file is empty.")
    else:
        st.error("No non-empty JSON files available in the directory.")

elif mode == "Hugging Face Model Downloads":
    # Hugging Face Model Downloads UI and Logic
    st.sidebar.title("Hugging Face Downloads Settings")
    start_date = st.sidebar.date_input("Start date", datetime(2023, 1, 1))
    end_date = st.sidebar.date_input("End date", datetime.now())

    if start_date <= end_date:
        df = read_huggingface(start_date, end_date, HUGGINGFACE_DATA_DIR)
        if not df.empty:
            model_ids = df['modelId'].unique()
            selected_models = st.sidebar.multiselect("Select Model IDs", model_ids, default=model_ids[:5])

            st.title("Hugging Face Model Downloads Over Time")
            if selected_models:
                filtered_df = df[df['modelId'].isin(selected_models)]
                plot_hugging_face_data(filtered_df)
                st.dataframe(filtered_df)  # Display data as a spreadsheet
            else:
                st.error("Please select at least one model.")
        else:
            st.error("No data available for the selected date range.")
    else:
        st.error("End date must fall after start date.")
