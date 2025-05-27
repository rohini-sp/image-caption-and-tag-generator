import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI setup
st.set_page_config(page_title="Smart Image Caption Generator", layout="centered")
st.title("📸 Smart Image Caption Generator + Auto Tags")

# Style selector
style = st.selectbox("Choose a caption style:", ["Simple", "Humorous", "Technical", "Poetic"])

# File uploader
uploaded_images = st.file_uploader("Upload one or more images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

# Caption generation
def generate_caption_and_tags(image_bytes, style):
    image = Image.open(io.BytesIO(image_bytes))  # Convert bytes to PIL.Image

    caption_prompt = f"Describe this image in a {style} tone. Just return the caption."
    tag_prompt = "Suggest 5 relevant tags for this image. Return them as comma-separated keywords."

    caption_response = model.generate_content([caption_prompt, image])
    tags_response = model.generate_content([tag_prompt, image])

    caption = caption_response.text.strip()
    tags = tags_response.text.strip()

    return caption, tags

# Main image processing loop
if uploaded_images:
    for img in uploaded_images:
        st.image(img, use_container_width=True)
        with st.spinner("Generating caption and tags..."):
            img_bytes = img.read()
            caption, tags = generate_caption_and_tags(img_bytes, style)

            st.success("📝 Caption:")
            st.write(caption)

            st.markdown("🏷️ **Auto-suggested Tags:**")
            st.write(" ".join(tags))

            st.session_state.history.append((img.name, caption, tags))

# Sidebar history
if st.session_state.history:
    st.sidebar.header("🕘 Caption History")
    for name, caption, tags in st.session_state.history:
        st.sidebar.markdown(f"**{name}**\n> {caption}\nTags: {' '.join(tags)}")
