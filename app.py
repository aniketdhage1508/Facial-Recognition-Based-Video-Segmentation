import streamlit as st
from main_video import process_video

st.set_page_config(page_title="Face Recognition Video Processor", layout="wide")

def home():
    st.title("Face Recognition Video Processor")
    st.markdown("""
    This project uses **OpenCV** and **Face_Recognition** to detect known faces in videos.  
    - Upload an **image** of a known person.  
    - Upload a **video** to be processed.  
    - Click the **Process** button to generate the output video.  
    - You can **download** the processed video after completion.
    """)

def video_processor():
    st.title("Upload Image and Video")

    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "avi", "mov"])

    if uploaded_image and uploaded_video:
        if st.button("Process Video"):
            image_path = f"person_image.jpg"
            video_path = f"video_footage.mp4"
            output_path = "segmented_video.mp4"

            with open(image_path, "wb") as f:
                f.write(uploaded_image.read())
            with open(video_path, "wb") as f:
                f.write(uploaded_video.read())

            with st.spinner("Processing..."):
                output = process_video(image_path, video_path, output_path)
                st.success("Processing complete!")

                # Display video
                st.video(output)

                # Provide download link
                with open(output, "rb") as f:
                    st.download_button(
                        label="Download Processed Video",
                        data=f,
                        file_name="processed_video.mp4",
                        mime="video/mp4"
                    )

# Streamlit multipage layout
page = st.sidebar.selectbox("Choose a page", ["Home", "Process Video"])

if page == "Home":
    home()
else:
    video_processor()
