import streamlit as st
import streamlit_option_menu as option_menu
import speech_recognition as sr
from gpt4all import GPT4All
import sys
import whisper
import warnings
import time
import datetime
import pyautogui
import webbrowser
import os
import pyttsx3


# Initialize GPT4All model
model = GPT4All("C:\\Users\\Harnil\\AppData\\Local\\nomic.ai\\GPT4All\\gpt4all-falcon-newbpe-q4_0.gguf", allow_download=False)

# Initialize speech recognizer
source = sr.Microphone()
recognizer = sr.Recognizer()

# Initialize Whisper tiny model
tiny_model_path = os.path.expanduser('~/.cache/whisper/tiny.pt')
tiny_model = whisper.load_model('tiny')


with st.sidebar:
    
    st.subheader('Presented By : ')
    st.markdown('1.Bhandari Jenil')
    st.markdown('2.Chodvadiya Harnil')
    st.markdown('3.Halpati Kush')
    st.markdown('4.Prajapati Isha')
    
    st.subheader('Guided By : ')
    st.markdown('Abdul Aziz Md, Master Trainer, Edunet Foundation.')

st.markdown("<h1 style='text-align: center;; color: #4783c4;font-size:50px;'>Voice Assistant</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
container1 = col1.container(border=True, height=650)
container2 = col2.container(border=True, height=650)

def update_container1(content):
    container1.write(content)

def update_container2(content):
    container2.write(content)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
tasks = []
listening_for_trigger_word = True
should_run = True
listeningToTask = False
askingAQuestion = False

# Function to respond to user
def respond(text):
    update_container2(text)
    engine.say(text)
    engine.runAndWait()

def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		respond("Good Morning Sir! I am your Assistant, Edith. How can i Help you, Sir?")

	elif hour>= 12 and hour<18:
		respond("Good Afternoon Sir! I am your Assistant, Edith. How can i Help you, Sir?") 

	else:
		respond("Good Evening Sir! I am your Assistant, Edith. How can i Help you, Sir?")

# Function to listen for command
def listen_for_command():
    with source as s:
        update_container2("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        #command = command.lower()
        return command
    except sr.UnknownValueError:
        update_container2("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        update_container2("Unable to access the Google Speech Recognition API.")
        return None

# Function to perform command
def perform_command(command):
    global tasks
    global listeningToTask
    global askingAQuestion
    global should_run
    global listening_for_trigger_word
    if command:
        update_container1(command)
        if "take a screenshot" in command:
            pyautogui.screenshot("screenshot.png")
            respond("I took a screenshot for you.")
        elif 'open youtube' in command:
                # webbrowser.open("https://www.youtube.com/")
                # speak('Opening YouTube...')
                if 'search' in command:
                    search_query = command.split('open youtube and search')[-1].strip()
                    search_url = f"https://www.youtube.com/results?search_query={search_query}"
                    webbrowser.open(search_url)
                    respond(f"Searching on youtube for {search_query}")
                else:
                    webbrowser.open("https://www.youtube.com/")
                    respond('Opening youtube...')
        elif 'open google' in command:
                 if 'search' in command:
                    search_query = command.split('open google and search')[-1].strip()
                    search_url = f"https://www.google.com/search?q={search_query}"
                    webbrowser.open(search_url)
                    respond(f"Searching Google for {search_query}")
                 else:
                    webbrowser.open("https://www.google.com/")
                    respond('Opening Google...')
        elif 'the time' in command or 'time please' in command or 'current time' in command:
            strTime = datetime.datetime.now().strftime("% H:% M:% S") 
            respond(f"Sir, the time is {strTime}")
        elif "question" in command:
            askingAQuestion=True
            respond("What's your question?")
            return
        elif askingAQuestion:
            askingAQuestion = False
            respond("Thinking...")
            update_container2("Please wait a while...")
            output = model.generate(command, max_tokens=200)
            respond(output)
        elif "exit" in command:
            should_run = False
        else:
            respond("Sorry, I'm not sure how to handle that command.")
    listening_for_trigger_word = True

# Main function
def main():
    global listening_for_trigger_word
    while should_run:
        command = listen_for_command()
        if listening_for_trigger_word:
            listening_for_trigger_word = False
        else:
            perform_command(command)
        time.sleep(1)
    respond("Goodbye.")
    print("Goodbye.")

# Run the app
if __name__ == "__main__":
    wishMe()
    main()
