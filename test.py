import streamlit as st
import time # Importing the time module
import pandas as pd

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
'How would you like to be contacted?',
('Email', 'Home phone', 'Mobile phone')
)
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
'Select a range of values',
0.0, 100.0, (25.0, 75.0)
)

# Menampilkan judul aplikasi
st.title("This is the app title")
# Menampilkan header untuk bagian utama
st.header("This is the header")
# Menampilkan teks dengan format Markdown
st.markdown("This is the markdown")
# Menampilkan subheader untuk sub-bagian
st.subheader("This is the subheader")
# Menampilkan teks kecil sebagai keterangan
st.caption("This is the caption")
# Menampilkan kode dengan format khusus
st.code("x = 2021")
# Menampilkan rumus matematika dengan LaTeX
st.latex(r''' a+a r^1+a r^2+a r^3 ''')

# Menampilkan teks biasa
st.write("Here's our first attempt at using data to create a table:")

# Menampilkan DataFrame sebagai tabel interaktif
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

df = pd.DataFrame({
'first column': [1, 2, 3, 4],
'second column': [10, 20, 30, 40]
})
df


st.subheader("Image:")
st.image("gotei13old.jpg", caption="Old Gotei 13")
st.subheader("Audio:")
st.audio("Arctic Monkeys - No.1 Party Anthem.mp3")
st.subheader("Video:")
st.video("Haikyu.mp4")

# Menampilkan subheader untuk bagian checkbox
st.subheader("Checkbox:")
# Menampilkan checkbox dengan label 'Yes'
st.checkbox('Yes')
# Menampilkan tombol dengan label 'Click Me'
st.button('Click Me')
# Menampilkan pilihan radio untuk memilih gender
st.radio('Pick your gender', ['Male', 'Female'])
# Menampilkan selectbox untuk memilih buah
st.selectbox('Pick a fruit', ['Apple', 'Banana', 'Orange'])
# Menampilkan multiselect untuk memilih planet
st.multiselect('Choose a planet', ['Jupiter', 'Mars', 'Neptune'])
# Menampilkan select slider untuk memilih nilai
st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
# Menampilkan slider untuk memilih angka
st.slider('Pick a number', 0, 50)
# Menampilkan input angka dengan batas 0 hingga 10
st.number_input('Pick a number', 0, 10)
# Menampilkan input teks untuk alamat email
st.text_input('Email address')
# Menampilkan input tanggal untuk memilih tanggal perjalanan
st.date_input('Traveling date')
# Menampilkan input waktu untuk memilih waktu sekolah
st.time_input('School time')
# Menampilkan area teks untuk deskripsi
st.text_area('Description')
# Menampilkan uploader file untuk mengunggah foto
st.file_uploader('Upload a photo')
# Menampilkan pemilih warna untuk memilih warna favorit
st.color_picker('Choose your favorite color')

st.progress(10)  # Progress bar
with st.spinner('Wait for it...'):
    time.sleep(10)  # Simulating a process delay