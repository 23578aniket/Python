import requests
import os
import speech_recognition as sr
import pywhatkit as wk
import datetime as dt
import wikipedia
import webbrowser
import pyautogui as py
import sys
import random
import calendar
import time
from playsound import playsound

def talk(text):
    voices = ["alloy", "echo", "fable", "oynx", "nova", "shimmer"]

    # Define the URL and payload data
    url = "https://ttsmp3.com/makemp3_ai.php"

    payload = {
        "msg": text,
        "lang": voices[0],
        "speed": "1.00",
        "source": "ttsmp3"
    }

    # Send the POST request
    response = requests.post(url, data=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        
        # Parse JSON response
        data = response.json()

        # Extract URL
        mp3_url = data["URL"]

        # Download file
        response = requests.get(mp3_url)

        # Get file name from URL
        file_name = os.path.basename(mp3_url)

        # Save file to current folder
        with open(file_name, "wb") as file:
            file.write(response.content)

        # Play the audio
        playsound(file_name)

        # Remove the temporary audio file
        os.remove(file_name)

    else:
        # Print an error message if the request was not successful
        print("Error:", response.status_code)

# Listening and Responding
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = 500
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"Master said: {query}")
        return query.lower()
    except Exception as e:
        print("Sorry, I didn't get that.")
        return "None"

# Actions (continued)
def greet():
    hour = dt.datetime.now().hour
    if 0 <= hour < 12:
        return "Good Morning!"
    elif 12 <= hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

# Main function
if __name__ == "__main__":
    greeting = greet()  # Get greeting message
    print(greeting)
    talk(greeting)  # Speak the greeting

    while True:
        query = takeCommand().lower()
        print("Assistant is awake and Listening")
            
        if "go to sleep" in query:
            print("Alright then, Saayonara...")
            talk("Alright then, saayonara...")
            break

        # Respond based on the query
        if "time" in query:
            current_time = dt.datetime.now().strftime("%I:%M %p")
            print("The time is:", current_time)
            talk("The time is " + current_time)
        elif "date" in query:
            today_date = dt.datetime.today().strftime("%A, %B %d, %Y")
            print("Today's date is:", today_date)
            talk("Today's date is " + today_date)
        # Add more responses for different queries here...

