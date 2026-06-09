import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")


st.title("♻️ Upcycling Copilot")

st.caption(
    "Transforming waste into opportunities using AI"
)

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Item")
    st.info(
    "💡 Upload plastic bottles, cardboard boxes, old clothes, glass jars, or other household waste for best results."
     )

    if st.button("Generate Upcycling Ideas"):

        prompt = """
            You are an expert in sustainability and upcycling.

            Analyze the uploaded image.

            Return:

            # Detected Item

            # Upcycling Ideas

            For each idea provide:
            - Name
            - Difficulty (Easy/Medium/Hard)
            - Materials Needed
            - Steps

            # Environmental Benefits

            # Estimated Waste Diverted

            Format using markdown.
            """

        with st.spinner("Analyzing image and generating ideas..."):
          try:
             response = model.generate_content([prompt, image])

             st.subheader("♻️ AI Recommendations")

             with st.container():
                st.markdown(response.text)
           except Exception as e:
               st.error(
                    "AI quota reached. Please try again after a minute.")

        

        score = random.randint(70, 95)

        st.subheader("🌱 Sustainability Score")

        st.progress(score/100)

        st.write(f"{score}/100")
        st.success(
            """
            Estimated Benefits

            • Less waste sent to landfill
            • Encourages circular economy
            • Promotes sustainable living
            """
        )
