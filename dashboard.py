import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Coba Streamlit",
    # page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("Sidebar Title")
st.sidebar.slider("Pick a number", 0, 100)
st.sidebar.markdown("This is the sidebar content")
st.sidebar.radio("Pick your gender", ["Male", "Female"])

container = st.container()
container.title("Container Title")
container.write("This is the container content")
st.write("This is the outsite container")

st.markdown("This is the markdown") # Allows for some HTML tags and CSS for styling within certain constraints

col1, col2 = st.columns((5.5, 5.5), gap='large')

col1.title("Column 1 Title")
col2.title("Column 2 Title")

with col1:
    st.write("This is column 1")
    rand = np.random.normal(1, 2, size=20)
    fig, ax = plt.subplots()
    ax.hist(rand, bins=15)
    st.pyplot(fig)

with col2:
    st.write("This is column 2")
    df = pd.DataFrame(np.random.randn(10, 2), columns=['x', 'y'])
    st.line_chart(df)

df = pd.DataFrame(
    np.random.randn(500, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon']
)
st.map(df)
