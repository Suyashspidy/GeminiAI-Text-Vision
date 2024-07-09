from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Load the models
text_model = genai.GenerativeModel("gemini-1.5-pro-latest")
image_model = genai.GenerativeModel("gemini-1.0-pro-vision-latest")

def get_text_response(question):
    response = text_model.generate_content(question)
    return response.text

def get_image_response(input, image):
    if input != "":
        response = image_model.generate_content([input, image])
    else:
        response = image_model.generate_content(image)
    return response.text

## Initializing Streamlit app
st.set_page_config(page_title="Gemini LLM Application")

st.header("Gemini LLM Application")

# Select Task
task = st.selectbox("Choose the task:", ["Text Generation", "Image Analysis"])

if task == "Text Generation":
    input = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")

    if submit:
        response = get_text_response(input)
        st.subheader("The Response is")
        st.write(response)

elif task == "Image Analysis":
    input = st.text_input("Input Prompt: ", key="input_image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit = st.button("Tell me more about the image")

    if submit:
        response = get_image_response(input, image)
        st.subheader("The Response is")
        st.write(response)
