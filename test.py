import streamlit as st
import time # Importing the time module

# st.title('Hello World!')
# st.write('This is a simple Streamlit app.')

st.title("This is the app title")
st.header("This is the header")
st.markdown("This is the markdown")
st.subheader("This is the subheader")
st.caption("This is the caption")
st.code("x = 2021")
st.latex(r''' a+a r^1+a r^2+a r^3 ''')

st.subheader("Image:")
st.image("gotei13old.jpg", caption="Old Gotei 13")
st.subheader("Audio:")
st.audio("Arctic Monkeys - No.1 Party Anthem.mp3")
st.subheader("Video:")
st.video("Haikyu.mp4")

st.subheader("Checkbox:")
st.checkbox('Yes')
st.button('Click Me')
st.radio('Pick your gender', ['Male', 'Female'])
st.selectbox('Pick a fruit', ['Apple', 'Banana', 'Orange'])
st.multiselect('Choose a planet', ['Jupiter', 'Mars', 'Neptune'])
st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
st.slider('Pick a number', 0, 50)

st.number_input('Pick a number', 0, 10)
st.text_input('Email address')
st.date_input('Traveling date')
st.time_input('School time')
st.text_area('Description')
st.file_uploader('Upload a photo')
st.color_picker('Choose your favorite color')

st.progress(10)  # Progress bar
with st.spinner('Wait for it...'):
    time.sleep(10)  # Simulating a process delay