import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

# Konfigurasi kredensial Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'streamlitdata-81152a1bca18.json'  # Path ke file JSON Anda

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

gc = gspread.authorize(credentials)

# ID spreadsheet dan nama sheet
SPREADSHEET_ID = '1_pX58cuF4c82WEvnNEOpuudSskZ53kcJRuLf7BLxfQk'
SHEET_NAME = 'Sheet3'

# Membaca data dari Google Sheets
worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
data = worksheet.get_all_records()  # Mengembalikan list of dictionaries

# Konversi ke DataFrame
data = pd.DataFrame(data)

# Debug: Show column names
st.write(data.columns.tolist())  # Debugging: Check all columns in the DataFrame

# Rename 'New Perusahaan Regional / Asal Wilayah TREG' to 'TREG'
data.rename(columns={'New Perusahaan Regional / Asal Wilayah TREG': 'TREG'}, inplace=True)

# Ensure 'Time in' is converted to datetime
if 'Time in' in data.columns:
    data['Time in'] = pd.to_datetime(data['Time in'], errors='coerce')
    # Create 'Month-Year' from 'Time in'
    data['Month-Year'] = data['Time in'].dt.to_period('M')
else:
    st.error("The 'Time in' column is missing, and we cannot create 'Month-Year'.")

# Check for missing columns
required_columns = ['TREG', 'Month-Year', 'Kategori Feedback', 'Sentimen Feedback v2', 'Product', 'Sub-Product', 'Topik', 'Type']
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"Missing columns: {missing_columns}")
else:
    # Proceed with the operations
    columns_needed = [
        'TREG', 
        'Month-Year', 
        'Kategori Feedback', 
        'Sentimen Feedback v2', 
        'Product', 
        'Sub-Product', 
        'Topik', 
        'Type'
    ]
    dashboard_data = data[columns_needed].copy()

    # Drop rows with missing values in the relevant columns
    dashboard_data = dashboard_data.dropna(subset=columns_needed)

    # Normalize the sentiment feedback column
    dashboard_data['Sentimen Feedback v2'] = dashboard_data['Sentimen Feedback v2'].str.strip().str.capitalize()

    # Aggregations
    stacked_data = (
        dashboard_data.groupby(['TREG', 'Month-Year', 'Sentimen Feedback v2'])
        .size()
        .reset_index(name='Count')
    )
    category_data = (
        dashboard_data.groupby(['TREG', 'Kategori Feedback', 'Sentimen Feedback v2'])
        .size()
        .reset_index(name='Count')
    )

    # Convert Month-Year to string for JSON serialization
    stacked_data['Month-Year'] = stacked_data['Month-Year'].apply(lambda x: x.strftime('%b %Y'))

    # Streamlit app layout
    st.set_page_config(layout="wide", page_title="Feedback Dashboard")
    st.title("Feedback Dashboard by TREG")

    # Sidebar filters
    st.sidebar.header("Filters")

    # Filter 1: Select Date Range
    start_date = st.sidebar.date_input("Start Date", value=data['Time in'].min())
    end_date = st.sidebar.date_input("End Date", value=data['Time in'].max())

    # Filter 2: Sentimen
    sentimen_filter = st.sidebar.multiselect(
        "Select Sentimen", 
        options=dashboard_data['Sentimen Feedback v2'].unique(),
        default=dashboard_data['Sentimen Feedback v2'].unique()
    )

    # Filter 3: Product
    product_filter = st.sidebar.multiselect(
        "Select Product", 
        options=dashboard_data['Product'].unique(),
        default=dashboard_data['Product'].unique()
    )

    # Filter 4: Sub Product
    sub_product_filter = st.sidebar.multiselect(
        "Select Sub Product", 
        options=dashboard_data['Sub-Product'].unique(),
        default=dashboard_data['Sub-Product'].unique()
    )

    # Filter 5: Kategori Feedback
    kategori_filter = st.sidebar.multiselect(
        "Select Kategori Feedback", 
        options=dashboard_data['Kategori Feedback'].unique(),
        default=dashboard_data['Kategori Feedback'].unique()
    )

    # Filter 6: TREG
    treg_filter = st.sidebar.multiselect(
        "Select TREG", 
        options=dashboard_data['TREG'].unique(),
        default=dashboard_data['TREG'].unique()
    )

    # Filter 7: Topik
    topik_filter = st.sidebar.multiselect(
        "Select Topik", 
        options=dashboard_data['Topik'].unique(),
        default=dashboard_data['Topik'].unique()
    )

    # Filter 8: Type
    type_filter = st.sidebar.multiselect(
        "Select Type", 
        options=dashboard_data['Type'].unique(),
        default=dashboard_data['Type'].unique()
    )

    # Apply filters
    filtered_data = dashboard_data[
        (dashboard_data['Time in'] >= pd.Timestamp(start_date)) &
        (dashboard_data['Time in'] <= pd.Timestamp(end_date)) &
        (dashboard_data['Sentimen Feedback v2'].isin(sentimen_filter)) &
        (dashboard_data['Product'].isin(product_filter)) &
        (dashboard_data['Sub-Product'].isin(sub_product_filter)) &
        (dashboard_data['Kategori Feedback'].isin(kategori_filter)) &
        (dashboard_data['TREG'].isin(treg_filter)) &
        (dashboard_data['Topik'].isin(topik_filter)) &
        (dashboard_data['Type'].isin(type_filter))
    ]

    # Aggregations
    stacked_data = (
        dashboard_data.groupby(['TREG', 'Month-Year', 'Sentimen Feedback v2'])
        .size()
        .reset_index(name='Count')
    )
    category_data = (
        dashboard_data.groupby(['TREG', 'Kategori Feedback', 'Sentimen Feedback v2'])
        .size()
        .reset_index(name='Count')
    )

    # Convert Month-Year to string for JSON serialization
    stacked_data['Month-Year'] = stacked_data['Month-Year'].apply(lambda x: x.strftime('%b %Y'))

    # Visualization and layout
    st.subheader("Sentiment Trends by Month and Year")
    tregs = dashboard_data['TREG'].unique()  # Dynamically generate TREG list
    stacked_columns = st.columns(len(tregs))

    for i, treg in enumerate(tregs):
        filtered_stacked = stacked_data[stacked_data['TREG'] == treg]
        with stacked_columns[i]:
            fig = px.bar(
                filtered_stacked,
                x="Month-Year",
                y="Count",
                color="Sentimen Feedback v2",
                labels={"Month-Year": "Month-Year", "Count": "Feedback Count"},
                barmode="stack",
            )
            st.plotly_chart(fig, use_container_width=True)
