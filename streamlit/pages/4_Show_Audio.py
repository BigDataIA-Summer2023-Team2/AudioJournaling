import streamlit as st
import pandas as pd
import os
from utils import backend

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

def get_journal_history():
    response = backend.fetch_journal_history(st.session_state.auth_token)
    if response[0]:
        journal_history = response[1]
        audio_files = [{'id': journal['id'], 'file_url': journal['file_url']} for journal in journal_history]
    else:
        audio_files = []
    return audio_files

def get_audio_data(file_url):
    response = backend.fetch_audio_file(st.session_state.auth_token, file_url)
    return response

def get_transcript_and_emotion(audio_id):
    response = backend.fetch_transcript_and_emotion(st.session_state.auth_token, audio_id)
    return response

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

if auth_user[0]:
    st.title("List of Audio Files")
    audio_files = get_journal_history()
    
    if audio_files:
        audio_df = pd.DataFrame(audio_files)
        audio_df['transcript'] = ""
        audio_df['emotion'] = ""
        
        st.write("Audio Journal History")
        st.write(audio_df)

        # Allow user to select an audio file to play
        selected_idx = st.selectbox("Select an audio file to play:", audio_df['id'])
        selected_row = audio_df[audio_df['id'] == selected_idx].iloc[0]

        st.write(f"Selected audio file: {selected_row['id']} - {selected_row['file_url']}")

        # Get transcript and emotion for the selected audio file
        transcript, emotion = get_transcript_and_emotion(selected_row['id'])
        
        if transcript and emotion:
            audio_df.loc[audio_df['id'] == selected_idx, 'transcript'] = transcript
            audio_df.loc[audio_df['id'] == selected_idx, 'emotion'] = emotion

            st.write("Transcript:", transcript)
            st.write("Emotion:", emotion)
        else:
            st.warning("Transcript and emotion data not available.")

        # Play the selected audio file
        with st.spinner("Downloading audio..."):
            response = get_audio_data(selected_row['file_url'])
            if response[0]:
                st.success('Here is your audio clip')
                st.audio(response[1], format='audio/wav')
            else:
                st.error(f"Error downloading audio journal. Details: {response[1]}", icon="🚨")
    else:
        st.write("No audio files found.")
else:
    st.warning('Access Denied! Please authenticate yourself on User Authentication.', icon="⚠️")
