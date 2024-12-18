import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data_path = 'Raw Data Sheet 3.xlsx'  # Ganti dengan path file Excel Anda
data = pd.read_excel(data_path, sheet_name='Sheet3')

# Preprocess data
data['Time in'] = pd.to_datetime(data['Time in'], errors='coerce')
data['Month-Year'] = data['Time in'].dt.to_period('M')
columns_needed = ['New Perusahaan Regional / Asal Wilayah TREG', 'Month-Year', 'Kategori Feedback', 'Sentimen Feedback v2']
dashboard_data = data[columns_needed].copy()
dashboard_data.rename(columns={'New Perusahaan Regional / Asal Wilayah TREG': 'TREG'}, inplace=True)
dashboard_data = dashboard_data.dropna(subset=['TREG', 'Month-Year', 'Kategori Feedback', 'Sentimen Feedback v2'])
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
stacked_data['Month-Year'] = stacked_data['Month-Year'].astype(str)

# Streamlit app layout
st.set_page_config(layout="wide", page_title="Feedback Dashboard")
st.title("Feedback Dashboard")

# Sidebar filter
treg_filter = st.sidebar.selectbox("Select TREG", options=dashboard_data['TREG'].unique())

# Filter data
filtered_stacked = stacked_data[stacked_data['TREG'] == treg_filter]
filtered_category = category_data[category_data['TREG'] == treg_filter]

# Split data by Sentiment Feedback and keep top 10 categories
neg_data = (
    filtered_category[filtered_category['Sentimen Feedback v2'] == 'Negatif']
    .nlargest(10, 'Count')
    # .sort_values(by='Count', ascending=False)
)
# neg_data['Kategori Feedback'] = pd.Categorical(
#     neg_data['Kategori Feedback'], 
#     categories=neg_data['Kategori Feedback'], 
#     ordered=True
# )

pos_data = (
    filtered_category[filtered_category['Sentimen Feedback v2'] == 'Positif']
    .nlargest(10, 'Count')
    # .sort_values(by='Count', ascending=False)
)
# pos_data['Kategori Feedback'] = pd.Categorical(
#     pos_data['Kategori Feedback'], 
#     categories=pos_data['Kategori Feedback'], 
#     ordered=True
# )

neu_data = (
    filtered_category[filtered_category['Sentimen Feedback v2'] == 'Netral']
    .nlargest(10, 'Count')
    # .sort_values(by='Count', ascending=False)
)
# neu_data['Kategori Feedback'] = pd.Categorical(
#     neu_data['Kategori Feedback'], 
#     categories=neu_data['Kategori Feedback'], 
#     ordered=True
# )


# Stacked bar chart
st.header("Sentiment Trends by Month and Year")
fig_stacked = px.bar(
    filtered_stacked,
    x="Month-Year",
    y="Count",
    color="Sentimen Feedback v2",
    title=f"Sentiment Trends for {treg_filter}",
    labels={"Month-Year": "Month-Year", "Count": "Feedback Count"},
    barmode="stack",
)
st.plotly_chart(fig_stacked, use_container_width=True)

# Feedback category chart: Negative Sentiment
st.header("Feedback Categories - Negative Sentiment")
fig_neg = px.bar(
    neg_data,
    x="Count",
    y="Kategori Feedback",
    orientation="h",
    title=f"Top 10 Feedback Categories (Negative Sentiment) for {treg_filter}",
    labels={"Count": "Feedback Count", "Kategori Feedback": "Feedback Category"},
    category_orders={"Kategori Feedback": neg_data['Kategori Feedback'].tolist()},  # Force descending order
    color_discrete_sequence=["#FF5733"]  # Oranye

)
st.plotly_chart(fig_neg, use_container_width=True)

# Feedback category chart: Positive Sentiment
st.header("Feedback Categories - Positive Sentiment")
fig_pos = px.bar(
    pos_data,
    x="Count",
    y="Kategori Feedback",
    orientation="h",
    title=f"Top 10 Feedback Categories (Positive Sentiment) for {treg_filter}",
    labels={"Count": "Feedback Count", "Kategori Feedback": "Feedback Category"},
    category_orders={"Kategori Feedback": pos_data['Kategori Feedback'].tolist()},  # Force descending order
    color_discrete_sequence=["#2ECC71"]  # Hijau


)
st.plotly_chart(fig_pos, use_container_width=True)

# Feedback category chart: Neutral Sentiment
st.header("Feedback Categories - Neutral Sentiment")
fig_neu = px.bar(
    neu_data,
    x="Count",
    y="Kategori Feedback",
    orientation="h",
    title=f"Top 10 Feedback Categories (Neutral Sentiment) for {treg_filter}",
    labels={"Count": "Feedback Count", "Kategori Feedback": "Feedback Category"},
    category_orders={"Kategori Feedback": neu_data['Kategori Feedback'].tolist()},  # Force descending order
    color_discrete_sequence=["#33A1FF"]  # Biru

)
st.plotly_chart(fig_neu, use_container_width=True)