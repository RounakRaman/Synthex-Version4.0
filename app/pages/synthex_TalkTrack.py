import whisper
import streamlit as st
import os
import warnings
from pydub import AudioSegment
import numpy as np
warnings.filterwarnings("ignore", category=FutureWarning)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
import google.generativeai as genai

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for summarizing audio content
prompt = """You are a YouTube video/Meeting Video/audio summarizer for a business firm. 
You will be taking the transcript text/meeting notes/audio or minutes of the meet/call recordings and summarizing 
the entire video/meeting/audio file and providing the important summary in points. 
The points should be exhaustive and should start with the date, 
agenda of the video or mentioned in the audio which would be the title of the video/main point of audio or the main content of video/audio and 
then things discussed in the video/audio. After that at the end call of action should be mentioned. 
At the end also mention the names of attendees or speakers in the video/audio or characters name mentioned in video/audio. 
Also extract things from the web also to simplify the summary and related documents or information available as 
reference material. Please provide the summary of the text given here:  """

def extract_transcript_from_audio(audio_data):
    audio_text=audio_data
    try:
        model = whisper.load_model("turbo")
        print("Hello")
        result = model.transcribe(audio_text)
        notes = result["text"]
        return notes
    except Exception as e:
        raise e
    
def load_and_process_audio(uploaded_file):
    
    try:
        # Load the audio file using pydub
        audio = AudioSegment.from_file(uploaded_file)  # Directly load the uploaded file
        audio_data = np.array(audio.get_array_of_samples())  # Convert to NumPy array
        
        # Normalize audio data to range [-1, 1]
        audio_data = audio_data.astype(np.float32) / np.max(np.abs(audio_data))
        notes=extract_transcript_from_audio(audio_data)
        return notes
    except Exception as e:
        st.error(f"Error processing audio file: {e}")
        return None  # Return None if an error occurs    

def generate_gemini_content(audio_text, prompt):
   
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + audio_text)
    return response.text    


st.title("From Meeting Call to Smart Notes: Capture, Analyze, and Summarize 🗒️🔍")


audio_file = st.file_uploader("Upload Audio (MP3)", type=["mp3","m4a"])

if audio_file is not None:
    st.write(f"Audio filename: {audio_file.name}")

    if audio_file.name.endswith('.mp3') or audio_file.name.endswith('.m4a'):
        st.success("Valid audio file uploaded.")
        
    else:
        st.error("Please upload a valid audio file.")


if st.button("Get Smart Notes from Call Recording"):
    if audio_file:
        call_text = load_and_process_audio(audio_file)
       
        print("Extracting call notes...")
        summary = generate_gemini_content(call_text, prompt)
        st.markdown("Your Detailed Smart Notes:")
        st.write(summary)

      