import streamlit as st
from dotenv import load_dotenv

load_dotenv() 
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Youtube video / Meeting Video summarizer for a business firm. 
You will be taking the transcript text/meeting notes or minutes of the meet and summarizing 
the entire video/meeting and providing the important summary in points. 
The points should be exhaustive and should start with date, 
agenda of the video which would be title of the video or the main content of video and 
then things discussed in the video. After that at the end call of action should be mentioned. 
At the end also mention the names of attendes or speakers in the video or characters name mentioned in video. 
Also extract things from web also to simplify the summary and related documents or information available as 
reference material. . Please provide the summary of the text given here:  """


def extract_meeting_details(meeting_url):
    try:
        video_id=meeting_url.split("=")[1]
        
        meeting_text=YouTubeTranscriptApi.get_transcript(video_id)

        notes = ""
        for i in meeting_text:
            notes += " " + i["text"]

        return notes

    except Exception as e:
        raise e
    

def generate_gemini_content(meeting_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+meeting_text)
    return response.text

st.title("Meeting Transcript to Smart Notes 🗒️🔍")
meeting_link = st.text_input("Enter Meeting Video File:")

if meeting_link:
    video_id = meeting_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Smart Notes"):
    print("Button pressed")
    meeting_text=extract_meeting_details(meeting_link)
    print("extracting meeting notes : ",meeting_text)

    if meeting_text:
        summary=generate_gemini_content(meeting_text,prompt)
        st.markdown("Detailed Smart Notes:")
        st.write(summary)




