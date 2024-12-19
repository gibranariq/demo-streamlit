import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

st.set_page_config(layout="wide", page_title="Feedback Dashboard")

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

# Preprocess data
data['Time in'] = pd.to_datetime(data['Time in'], errors='coerce')
data['Month-Year'] = data['Time in'].dt.to_period('M')
columns_needed = [
    'New Perusahaan Regional / Asal Wilayah TREG', 
    'Month-Year', 
    'Kategori Feedback', 
    'Sentimen Feedback v2', 
    'Product', 
    'Sub-Product', 
    'Topik', 
    'Type'
]
dashboard_data = data[columns_needed].copy()
dashboard_data.rename(columns={'New Perusahaan Regional / Asal Wilayah TREG': 'TREG'}, inplace=True)
dashboard_data = dashboard_data.dropna(subset=[
    'TREG', 
    'Month-Year', 
    'Kategori Feedback', 
    'Sentimen Feedback v2', 
    'Product', 
    'Sub-Product', 
    'Topik', 
    'Type'
])
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
st.title("Feedback Dashboard by TREG")

# Sidebar filters
st.sidebar.header("Filters")

# Filter 1: Select Date Range
start_date = st.sidebar.date_input("Start Date", value=data['Time in'].min())
end_date = st.sidebar.date_input("End Date", value=data['Time in'].max())

# Filter 2: Sentimen
sentimen_filter = st.sidebar.radio(
    "Select Sentiment",
    ["All", "Positif", "Negatif", "Netral"]
)

# Filter 3: Product
product_filter = st.sidebar.selectbox(
    "Select Product", 
    options=dashboard_data['Product'].unique(),
)

# Filter 4: Sub Product
sub_product_filter = st.sidebar.selectbox(
    "Select Sub Product", 
    options=dashboard_data['Sub-Product'].unique(),
)

# Filter 5: Kategori Feedback
kategori_filter = st.sidebar.selectbox(
    "Select Kategori Feedback", 
    options=dashboard_data['Kategori Feedback'].unique(),
)

# Filter 6: TREG
treg_filter = st.sidebar.selectbox(
    "Select TREG", 
    options=dashboard_data['TREG'].unique(),
)

# Filter 7: Topik
topik_filter = st.sidebar.selectbox(
    "Select Topik", 
    options=dashboard_data['Topik'].unique(),
)

# Filter 8: Type
type_filter = st.sidebar.selectbox(
    "Select Type", 
    options=dashboard_data['Type'].unique(),
)

# Apply filters
if sentimen_filter == "All":
    filtered_data = dashboard_data[
        (dashboard_data['Month-Year'].dt.to_timestamp() >= pd.Timestamp(start_date)) &
        (dashboard_data['Month-Year'].dt.to_timestamp() <= pd.Timestamp(end_date)) &
        (dashboard_data['Product'] == product_filter) &
        (dashboard_data['Sub-Product'] == sub_product_filter) &
        (dashboard_data['Kategori Feedback'] == kategori_filter) &
        (dashboard_data['TREG'] == treg_filter) &
        (dashboard_data['Topik'] == topik_filter) &
        (dashboard_data['Type'] == type_filter)
    ]
else:
    filtered_data = dashboard_data[
        (dashboard_data['Month-Year'].dt.to_timestamp() >= pd.Timestamp(start_date)) &
        (dashboard_data['Month-Year'].dt.to_timestamp() <= pd.Timestamp(end_date)) &
        (dashboard_data['Sentimen Feedback v2'] == sentimen_filter) &
        (dashboard_data['Product'] == product_filter) &
        (dashboard_data['Sub-Product'] == sub_product_filter) &
        (dashboard_data['Kategori Feedback'] == kategori_filter) &
        (dashboard_data['TREG'] == treg_filter) &
        (dashboard_data['Topik'] == topik_filter) &
        (dashboard_data['Type'] == type_filter)
    ]

# Aggregations
# stacked_data = (
#     dashboard_data.groupby(['TREG', 'Month-Year', 'Sentimen Feedback v2'])
#     .size()
#     .reset_index(name='Count')
# )
if sentimen_filter == "All":
    stacked_data = dashboard_data.groupby(['Month-Year', 'TREG', 'Sentimen Feedback v2']).size().reset_index(name='Count')
else:
    # Filter data berdasarkan sentimen yang dipilih
    stacked_data = dashboard_data[dashboard_data['Sentimen Feedback v2'] == sentimen_filter].groupby(['Month-Year', 'TREG', 'Sentimen Feedback v2']).size().reset_index(name='Count')

category_data = (
    dashboard_data.groupby(['TREG', 'Kategori Feedback', 'Sentimen Feedback v2'])
    .size()
    .reset_index(name='Count')
)

# Convert Month-Year to string for JSON serialization
stacked_data['Month-Year'] = stacked_data['Month-Year'].apply(lambda x: x.strftime('%b %Y'))


# Daftar TREG yang akan divisualisasikan
tregs = ['TREG-1', 'TREG-2', 'TREG-3', 'TREG-4', 'TREG-5']

# Baris 1: Stacked bar chart untuk setiap TREG
st.subheader("Sentiment Trends by Month and Year")
stacked_columns = st.columns(len(tregs))  # Kolom horizontal

for i, treg in enumerate(tregs):
    filtered_stacked = stacked_data[stacked_data['TREG'] == treg]
    with stacked_columns[i]:  # Tempatkan chart di kolom masing-masing
        st.write(f"*{treg}*")
        fig_stacked = px.bar(
            filtered_stacked,
            x="Month-Year",
            y="Count",
            color="Sentimen Feedback v2",
            # title=f"Sentiment Trends ({treg})",
            labels={"Month-Year": "Month-Year", "Count": "Feedback Count"},
            barmode="stack",
            color_discrete_map={
                "Negatif": "#FF5733",  # Merah/Oranye
                "Positif": "#2ECC71",  # Hijau
                "Netral": "#33A1FF",  # Biru
            },
            category_orders={
                "Sentimen Feedback v2": ["Negatif", "Positif", "Netral"]  # Urutan Legend
            }            
        )
        fig_stacked.update_layout(
            legend=dict(
                orientation="h",  # Horizontal legend
                y=1.15,  # Letakkan di bawah grafik
                x=0.5,   # Pusatkan di tengah
                xanchor="center",
                yanchor="top"
            )
        )
        st.plotly_chart(fig_stacked, use_container_width=True)

# Baris 2: Feedback category chart (Negative Sentiment) untuk setiap TREG
st.subheader("Feedback Categories - Negative Sentiment")
neg_columns = st.columns(len(tregs))  # Kolom horizontal untuk sentimen negatif

for i, treg in enumerate(tregs):
    filtered_category = category_data[category_data['TREG'] == treg]
    neg_data = (
        filtered_category[filtered_category['Sentimen Feedback v2'] == 'Negatif']
        .nlargest(10, 'Count')
    )
    with neg_columns[i]:  # Tempatkan chart di kolom masing-masing
        st.write(f"*{treg} - Negative*")
        fig_neg = px.bar(
            neg_data,
            x="Count",
            y="Kategori Feedback",
            orientation="h",
            title=f"Top 10 Negative Feedback ({treg})",
            labels={"Count": "Feedback Count", "Kategori Feedback": "Feedback Category"},
            category_orders={"Kategori Feedback": neg_data['Kategori Feedback'].tolist()},
            color_discrete_sequence=["#FF5733"],  # Oranye
        )
        st.plotly_chart(fig_neg, use_container_width=True)

# Baris 3: Feedback category chart (Positive Sentiment) untuk setiap TREG
st.subheader("Feedback Categories - Positive Sentiment")
pos_columns = st.columns(len(tregs))  # Kolom horizontal untuk sentimen positif

for i, treg in enumerate(tregs):
    filtered_category = category_data[category_data['TREG'] == treg]
    pos_data = (
        filtered_category[filtered_category['Sentimen Feedback v2'] == 'Positif']
        .nlargest(10, 'Count')
    )
    with pos_columns[i]:  # Tempatkan chart di kolom masing-masing
        st.write(f"*{treg} - Positive*")
        fig_pos = px.bar(
            pos_data,
            x="Count",
            y="Kategori Feedback",
            orientation="h",
            title=f"Top 10 Positive Feedback ({treg})",
            labels={"Count": "Feedback Count", "Kategori Feedback": "Feedback Category"},
            category_orders={"Kategori Feedback": pos_data['Kategori Feedback'].tolist()},
            color_discrete_sequence=["#2ECC71"],  # Hijau
        )
        st.plotly_chart(fig_pos, use_container_width=True)

# Baris 4: Feedback category chart (Neutral Sentiment) untuk setiap TREG
st.subheader("Feedback Categories - Neutral Sentiment")
neu_columns = st.columns(len(tregs))  # Kolom horizontal untuk sentimen netral

for i, treg in enumerate(tregs):
    filtered_category = category_data[category_data['TREG'] == treg]
    neu_data = (
        filtered_category[filtered_category['Sentimen Feedback v2'] == 'Netral']
        .nlargest(10, 'Count')
    )
    with neu_columns[i]:  # Tempatkan chart di kolom masing-masing
        st.write(f"*{treg} - Neutral*")
        fig_neu = px.bar(
            neu_data,
            x="Count",
            y="Kategori Feedback",
            orientation="h",
            title=f"Top 10 Neutral Feedback ({treg})",
            labels={"Count": "Feedback Count", "Kategori Feedback": "Feedback Category"},
            category_orders={"Kategori Feedback": neu_data['Kategori Feedback'].tolist()},
            color_discrete_sequence=["#33A1FF"],  # Biru
        )
        st.plotly_chart(fig_neu, use_container_width=True)