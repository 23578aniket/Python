import speech_recognition as sr
import pyttsx3 as tts
import pywhatkit as wk
import datetime as dt
import wikipedia
import schedule
import time
import pyautogui as py
import webbrowser
import os
import cv2
import sys
import random
import requests
from gtts import gTTS
import playsound
import openai
import calendar


engine = tts.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate', 150)

print("Try saying Assistant or Six to activate")

def talk(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = 300
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"Master said: {query}")
        
    except Exception as e:
        print("Sorry, I didn't get that.")
        return "None"
    return query.lower()

def respond(text):
    print(text)
    tts = gTTS(text=text, lang='en')
    audio = "Audio.mp3"
    tts.save(audio)
    playsound.playsound(audio)
    os.remove("Audio.mp3")

def today_date():
    now = dt.datetime.now()
    date_now = dt.datetime.today()
    week_now = calendar.day_name[date_now.weekday()]
    month_now = now.month
    day_now = now.day
    
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    ordinals = ["1st", "2nd", "3rd"] + ["{}th".format(i) for i in range(4, 31)]
    if 11 <= day_now <= 13:
        ordinals.append("{}th".format(day_now))
    else:
        ordinals.append("{}{}".format(day_now, {1: 'st', 2: 'nd', 3: 'rd'}.get(day_now % 10, 'th')))
    
    return f'Today is {week_now}, {months[month_now - 1]} the {ordinals[day_now - 1]}'

def say_hello(query):
    greet = ["hi", "hey", "hola", "greetings", "wassup", "hello", "hey there", "howdy"]
    response = ["hi", "hey", "hola", "greetings", "wassup", "hello", "hey there", "howdy"]
    for word in query.split():
        if word.lower() in greet:
            return random.choice(response)
    return ""


def wishMe():
    hour = int(dt.datetime.now().hour)
    if hour>=0 and hour<12:
        talk("Good Morning!")
    
    elif hour>=12 and hour<18:
        talk("Good Afternoon!")
    
    elif hour>=18 and hour<24:
        talk("Good Evening!")
        
    talk("How may I assist you?")
    
is_camera_open = False
def open_camera():
    global is_camera_open
    is_camera_open = True
    cap = cv2.VideoCapture(0)
    while is_camera_open:
        ret, img = cap.read()
        cv2.imshow("webcam", img)
        k = cv2.waitkey(50)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    is_camera_open = False
    
def wake_assistant(query):
    wake_words = ["assistant", "six", "6"]
    for word in wake_words:
        if word in query:
            return True
    return False

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(url)
    
if __name__== "__main__":
    
    is_awake = False
    while True:
        try:   
            if not is_awake:  # If the assistant is not awake, listen for wake words
                query = takeCommand().lower()
                if wake_assistant(query):
                    print("Assistant is awake!")
                    talk("Yes Sire!!!")
                    is_awake = True
                    wishMe()
            
            else:
                query = takeCommand().lower()
                print("Assistant is awake and Listening")
                
                if "go to sleep" in query:
                    print("Alright then, Saayonara...")
                    talk("Alright then, saayonara...")
                    is_awake = False
                    continue
                
                greeting_response = say_hello(query)
                if greeting_response:
                        talk(greeting_response)
                
                elif 'play' in query: #2
                    query = query.replace("play", " ")
                    query = query.replace("assistant", " ")
                    print("Playing...")
                    talk("Playing..." + query)
                    wk.playonyt(query)
                    time.sleep(5)
                    py.press('enter')
                    

                elif 'time' in query: #3
                    time = dt.datetime.now().strftime("%I:%M %p")
                    print("The time is: " f"{time}")
                    talk("The time is " + time)

                elif 'date' in query:#4
                    today = today_date()
                    print(today)
                    talk(today)

                elif "how are you" in query:#5
                    print("I am fine, Thank you")
                    talk("I am fine, thank you")

                elif "what are you" in query:#6
                    print("Greetings, I am 6, I am an AI assistant, what can I do for you?")
                    talk("Greetings, I am 6, I am an AI assistant, what can I do for you?")
                    
                elif "what can you do" in query:#7
                    print("I can do Everything that my creator programmed me to do.")
                    talk("I can do Everything that my creator programmed me to do.")
                    print("How may I help you?")
                    talk("how may I help you?")

                elif "who created you" in query:#8
                    print("I was created by Aniket, ")
                    talk("I was created by Aniket") 
                    print("I was created in VS Code using Python.") 
                    talk("I was created in VS Code using Python.") 
                
                elif "aniket" in query:
                    print("My creator is a B Tech CSE student and he is studing in HNB Garhwal University.")
                    talk("My creator is a B Tech CSE student and he is studing in HNB Garhwal University.")
                    
                elif "what" in query or "when" in query or "who" in query or "why" in query or "how" in query:
                    talk("Searching on Google...")
                    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
                    
                    # Fetching summary from Wikipedia
                    try:
                        summary = wikipedia.summary(query, sentences=1)
                        print(summary)
                        talk(summary)
                    except wikipedia.exceptions.DisambiguationError as e:
                        print("Ambiguous search query. Please refine your search.")
                        talk("Ambiguous search query. Please refine your search.")
                    except wikipedia.exceptions.PageError as e:
                        print("No information found. Please try again.")
                        talk("No information found. Please try again.")
                    
                elif "search" in query:
                    if "YouTube" in query or "video" in query or "youtube"  in query:
                        query = query.replace("search", "").replace("assistant", "")
                        talk("Searching on YouTube...")
                        wk.playonyt(query)
                        
                    else:
                        query = query.replace("search", "").replace("assistant", "")
                        talk("Searching on Google...")
                        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")

#############################################################################################################################
                elif "open camera" in query:
                    talk("Opening Camera...")
                    open_camera()
                    
                elif "open chrome" in query:
                    talk("Opening Chrome...")
                    py.hotkey("alt", "space")
                    py.typewrite("chrome", 0.1)
                    py.press("enter")
                    
                elif "close chrome" in query:#18
                    talk("Closing Chrome...")
                    os.system("taskkill /f /im chrome.exe")
                    
                elif "open opera" in query:
                    talk("Opening opera...")
                    py.hotkey("alt", "space")
                    py.typewrite("opera", 0.1)
                    py.press("enter")
                
                elif "close opera" in query:#19
                    talk("Closing opera...")
                    os.system("taskkill /f /im opera.exe")
                    
                elif "open edge" in query:
                    talk("Opening edge...")
                    py.hotkey("alt", "space")
                    py.typewrite("edge", 0.1)
                    py.press("enter")
                
                elif "open settings" in query:
                    talk("Opening settings...")
                    py.hotkey("alt", "space")
                    py.typewrite("settings", 0.1)
                    py.press("enter")
                    
                elif "open cmd" in query:#20
                    talk("opening cmd...")
                    py.hotkey("alt", "space")
                    py.typewrite("cmd", 0.1)
                    py.press("enter")
                    
                elif "close edge" in query:#20
                    talk("Closing Edge...")
                    os.system("taskkill /f /im msedge.exe")
                    
                    
###########################################################################################################################

                elif "shut down the system" in query:#35
                    talk("Shutting down the system...")
                    os.system("shutdown /s /t 1")
                    
                elif "restart the system" in query:#36
                    talk("Restarting the system...")
                    os.system("shutdown /r /t 1")
                
                elif "sleep the system" in query:#37
                    talk("Sleeping the system...")
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    
                elif "hibernate the system" in query:#38
                    talk("Hibernating the system...")
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,1")
                    
                elif "lock the system" in query:#39
                    talk("Locking the system...")
                    os.system("rundll32.exe user32.dll,LockWorkStation")
                    
#############################################################################################################################

                    
                elif "take screenshot" in query:#42
                    talk("Tell me the name for the file")
                    name = takeCommand().lower()
                    time.sleep(3)
                    img = py.screenshot()
                    img.save(f"{name}.png")
                    talk(f"Screenshot saved as {name}.png")
                    
                elif "stop music" in query:#44
                    talk("Stopping music...")
                    os.system("taskkill /f /im wmplayer.exe")
                    
                elif "what is my ip address" in query:#45
                    talk("checking...")
                    try:
                        ip = requests.get('https://api.ipify.org').text
                        print(ip)
                        talk(f"Your IP address is {ip}")
                    except Exception as e:
                        talk("Network is not available. Please try again later.")
                        
                elif "volume up" in query or "increase volume" in query:#46
                    py.press('volumeup')
                    py.press('volumeup')
                    py.press('volumeup')
                    py.press('volumeup')
                    py.press('volumeup')
                
                elif "volume down" in query or "decrease volume" in query:#47
                    py.press('volumedown')
                    py.press('volumedown')
                    py.press('volumedown')
                    py.press('volumedown')
                    py.press('volumedown')
                    
                elif "open spotlight" in query:#49
                    talk("opening spotlight")
                    py.hotkey("alt", "space")
                    time.sleep(3)
                    py.press('backspace')
                    time.sleep(0.5)
                    talk("What should I search for?")
                    search_query = takeCommand().lower()
                    py.typewrite(search_query, interval=0.1)
                    talk("Searching..." f"{search_query}")
                    py.press("enter")
                
                elif "open text extractor" in query:#50
                    talk("opening text extractor")
                    py.hotkey("win", "shift", "t")
                    
                elif "open fancy zone" in query:#51
                    talk("opening fancyzones")
                    py.hotkey("win", "shift", "`")              
                    
                elif "open new window" in query:#52
                    py.hotkey('ctrl', 'n')
                    
                elif "start again" in query:#53
                    py.press('space')
                
                elif "stop it" in query:#54
                    py.press('space')
                
                elif "open new tab" in query:#55
                    py.hotkey('ctrl', 't')
                    
                elif "go to next tab" in query:#56
                    py.hotkey('ctrl', 'tab')
                    
                elif "go to previous tab" in query:#57
                    py.hotkey('ctrl','shift', 'tab')
                    
                elif "open home page" in query:#58
                    py.hotkey('alt', 'home')
                
                elif "close this tab" in query:
                    py.hotkey('ctrl', 'w')
                    
                elif "close this window" in query:
                    py.hotkey('ctrl', 'shift' 'w')
                    
                elif "open download page" in query:
                    py.hotkey('ctrl', 'j')
                
                elif "login to different user" in query:
                    py.hotkey('ctrl', 'shift', 'm')
                
                elif "open address bar" in query:
                    py.hotkey('ctrl', 'l')
                
                elif "always on top" in query:
                    py.hotkey('win', 'ctrl', 't')

                pass     
        except Exception as e:
            print("Apologies, I can't assist you with that, but I am still learning.", e)
            talk("Apologies, I can't assist you with that, but I am still learning.")            
            



