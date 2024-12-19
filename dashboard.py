import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


st.set_page_config(
    page_title="Coba Streamlit",
    page_icon="🐹",
    layout="centered",
    initial_sidebar_state="expanded",
)


# Menampilkan judul di sidebar
st.sidebar.title("Sidebar Title")
# Menampilkan slider di sidebar untuk memilih angka
st.sidebar.slider("Pick a number", 0, 100)
# Menampilkan konten markdown di sidebar
st.sidebar.markdown("This is the sidebar content")
# Menampilkan pilihan radio di sidebar untuk memilih gender
st.sidebar.radio("Pick your gender", ["Male", "Female"])
# Membuat container untuk konten
container = st.container()
# Menampilkan judul di dalam container
container.title("Container Title")
# Menampilkan konten teks di dalam container
container.write("This is the container content")
# Menampilkan teks di luar container
st.write("This is the outsite container")
# Menampilkan teks dengan format Markdown
st.markdown("This is the markdown")  
# Membagi halaman menjadi dua kolom dengan ukuran yang sama
col1, col2 = st.columns((5.5, 5.5), gap='large')
# Menampilkan judul di kolom 1
col1.title("Column 1 Title")
# Menampilkan judul di kolom 2
col2.title("Column 2 Title")

# Mengisi kolom 1 dengan konten
with col1:
    # Menampilkan teks di kolom 1
    st.write("This is column 1")
    # Membuat data acak dan histogram
    rand = np.random.normal(1, 2, size=20)
    fig, ax = plt.subplots()
    ax.hist(rand, bins=15)
    # Menampilkan histogram di kolom 1
    st.pyplot(fig)

# Mengisi kolom 2 dengan konten
with col2:
    # Menampilkan teks di kolom 2
    st.write("This is column 2")
    # Membuat data acak dan menampilkannya sebagai line chart
    df = pd.DataFrame(np.random.randn(10, 2), columns=['x', 'y'])
    st.line_chart(df)

# Membuat data acak untuk peta
df = pd.DataFrame(
    np.random.randn(500, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon']
)
# Menampilkan peta berdasarkan data latitude dan longitude
st.map(df)

