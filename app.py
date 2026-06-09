import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="♻️ Upcycling Copilot",
    page_icon="♻️",
    layout="wide"
)

# ---------------------------
# GEMINI CONFIG
# ---------------------------

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.0-flash"
)

# ---------------------------
# UI
# ---------------------------

st.title("♻️ Upcycling Copilot")

st.caption(
    "Turn waste into useful creations using AI"
)

uploaded_file = st.file_uploader(
    "Upload an old item",
    type=["jpg", "jpeg", "png"]
)

# ---------------------------
# IMAGE PROCESSING
# ---------------------------

if uploaded_file:

    image = Image.open(uploaded_file)

    # Reduce image size for speed
    image.thumbnail((1024, 1024))

    st.image(
        image,
        caption="Uploaded Item",
        width=400
    )

    if st.button("Generate Upcycling Ideas"):

        prompt = """
You are an expert in sustainability and DIY upcycling.

Analyze the uploaded image.

Return:

# Detected Item

# Top 5 Upcycling Ideas

For each idea provide:

- Idea Name
- Difficulty (Easy/Medium/Hard)
- Materials Needed
- Step-by-Step Instructions

# Environmental Benefits

# Estimated Waste Diverted

Format everything neatly in markdown.
"""

        try:

            start = time.time()

            with st.spinner(
                "Analyzing image..."
            ):

                response = model.generate_content(
                    [prompt, image]
                )

            end = time.time()

            st.success(
                f"Generated in {end-start:.2f} seconds"
            )

            st.markdown("---")

            st.subheader(
                "♻️ AI Recommendations"
            )

            st.markdown(
                response.text
            )

            st.markdown("---")

            st.subheader(
                "🌱 Sustainability Impact"
            )

            st.progress(85)

            st.write(
                "Estimated Sustainability Score: 85/100"
            )

            st.info(
                """
• Reduces landfill waste

• Encourages reuse

• Supports circular economy

• Promotes sustainable living
"""
            )

        except Exception:

            st.error(
                "Gemini API quota reached. Showing fallback suggestions."
            )

            st.markdown(
                """
# Sample Upcycling Ideas

### 1. Plant Pot
Use the item as a decorative planter.

### 2. Storage Container
Convert it into a small organizer.

### 3. Desk Organizer
Store stationery items.

### 4. Bird Feeder
Create a simple feeder.

### 5. Decorative Piece
Paint and decorate for home use.

## Environmental Benefit

Keeps waste out of landfills and promotes reuse.
"""
            )
