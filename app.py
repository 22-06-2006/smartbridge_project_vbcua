import streamlit as st
import io
import whisper
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.title("🎤 Voice-Based Concept Understanding Analyzer (Whisper AI)")

st.write("Upload your voice (.wav or .mp3)")

audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])

text = ""

# ---------------- LOAD WHISPER MODEL ----------------
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# ---------------- VOICE TO TEXT ----------------
if audio_file is not None:

    file_extension = audio_file.name.split(".")[-1]

    audio_path = f"temp_audio.{file_extension}"

    with open(audio_path, "wb") as f:
        f.write(audio_file.getbuffer())

    result = model.transcribe(audio_path)
    text = result["text"]

    st.success("Transcribed Text:")
    st.write(text)

# ---------------- PDF FUNCTION ----------------
def create_pdf(user_text, result):
    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Whisper Voice Analysis Report")
    c.drawString(100, 700, f"Input: {user_text}")
    c.drawString(100, 650, f"Result: {result}")

    c.save()
    buffer.seek(0)

    return buffer

# ---------------- ANALYSIS ----------------
if st.button("Analyze Understanding"):

    if text:

        text_low = text.lower()

        if "machine learning" in text_low:
            result = "90/100 - Strong Understanding 👍"

        elif "ai" in text_low:
            result = "70/100 - Moderate Understanding 🙂"

        else:
            result = "40/100 - Needs Improvement ⚠️"

        st.success(result)

        pdf_file = create_pdf(text, result)

        st.download_button(
            label="📄 Download PDF",
            data=pdf_file,
            file_name="report.pdf",
            mime="application/pdf"
        )

    else:
        st.error("Please upload audio first")
