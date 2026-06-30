import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import speech_recognition as sr

st.title("🎤 Voice-Based Concept Understanding Analyzer")

st.write("Upload your voice (.wav file) OR type text")

# ---------------- VOICE INPUT ----------------
audio_file = st.file_uploader("🎤 Upload Voice File (.wav)", type=["wav"])

text = ""

if audio_file is not None:
    r = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        st.success("Voice Converted Text: " + text)
    except:
        st.error("Could not understand audio")

# ---------------- TEXT INPUT (OPTIONAL) ----------------
typed_text = st.text_input("Or Type Text Here:")

if typed_text:
    text = typed_text

# ---------------- PDF FUNCTION ----------------
def create_pdf(user_text, result):
    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Voice-Based Concept Understanding Report")
    c.drawString(100, 700, f"Input: {user_text}")
    c.drawString(100, 650, f"Result: {result}")

    c.save()
    buffer.seek(0)

    return buffer

# ---------------- ANALYZE BUTTON ----------------
if st.button("Analyze Understanding"):

    if text:

        text_low = text.lower()

        if "machine learning" in text_low:
            result = "90/100 - Strong Understanding 👍"
            st.success(result)

        elif "ai" in text_low or "artificial intelligence" in text_low:
            result = "70/100 - Moderate Understanding 🙂"
            st.info(result)

        else:
            result = "40/100 - Needs Improvement ⚠️"
            st.warning(result)

        pdf_file = create_pdf(text, result)

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name="report.pdf",
            mime="application/pdf"
        )

    else:
        st.error("Please provide voice or text input")