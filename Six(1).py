import speech_recognition as sr
import pyttsx3 as tts
import pywhatkit as wk
import datetime as dt
import wikipedia
import webbrowser
import os
import pyautogui as py
import cv2
import sys
import random
import requests
from gtts import gTTS
import playsound
import calendar
import time

print("Try saying Assistant or Six")

# Initialization and Configuration
def initialize_engine():
    engine = tts.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    return engine

def talk(audio):
    engine.say(audio)
    engine.runAndWait()
def get_wake_words():
    return ["assistant", "six", "6"]

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

def respond_to_wake_words(wake_words):
    query = takeCommand()
    for word in wake_words:
        if word in query:
            print("Assistant is awake!")
            talk("Yes Sire!!!")
            return True
    return False

def greet():
    hour = dt.datetime.now().hour
    if 0 <= hour < 12:
        talk("Good Morning!")
    elif 12 <= hour < 18:
        talk("Good Afternoon!")
    else:
        talk("Good Evening!")
    talk("How may I assist you?")

# Actions
def play_on_youtube(query):
    query = query.replace("play", "").replace("assistant", "")
    print("Playing...")
    talk("Playing..." + query)
    wk.playonyt(query)
    time.sleep(5)
    py.press('enter')
    
def search_on_youtube(query):
    query = query.replace("search", "").replace("assistant", "")
    print("Searching...")
    talk("Searching..." + query)
    wk.search(query)
    time.sleep(5)
    py.press('enter')

def get_time():
    time = dt.datetime.now().strftime("%I:%M %p")
    print("The time is: " f"{time}")
    talk("The time is " + time)

def get_today_date():
    now = dt.datetime.now()
    date_now = dt.datetime.today()
    week_now = calendar.day_name[date_now.weekday()]
    month_now = now.month
    day_now = now.day
    year_now = now.year
    
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    ordinals = ["1st", "2nd", "3rd"] + ["{}th".format(i) for i in range(4, 31)]
    if 11 <= day_now <= 13:
        ordinals.append("{}th".format(day_now))
    else:
        ordinals.append("{}{}".format(day_now, {1: 'st', 2: 'nd', 3: 'rd'}.get(day_now % 10, 'th')))
    
    today = f'Today is {week_now}, {months[month_now - 1]} the {ordinals[day_now - 1]}, {year_now}'
    print(today)
    talk(today)

def search_on_google(query):
    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
    
def respond_to_greetings(query):
    greet = ["hi", "hey", "hola", "greetings", "wassup", "hello", "hey there", "howdy"]
    response = ["hi", "hey", "hola", "greetings", "wassup", "hello", "hey there", "howdy"]
    for word in query.split():
        if word.lower() in greet:
            return random.choice(response)
    return ""

def what_can_you_do():
    print("I can do everything that my creator programmed me to do.")
    talk("I can do everything that my creator programmed me to do.")
    print("How may I help you?")
    talk("How may I help you?")
def respond_to_how_are_you():
    print("I am fine, Thank you")
    talk("I am fine, thank you")

def introduce_assistant():
    print("Greetings, I am 6, I am an AI assistant, what can I do for you?")
    talk("Greetings, I am 6, I am an AI assistant, what can I do for you?")

def who_created_assistant():
    print("I was created by Aniket.")
    talk("I was created by Aniket.") 
    print("I was created in VS Code using Python.") 
    talk("I was created in VS Code using Python.")
    
def about_the_creator():
    print("My creator name is Aniket and he is a B Tech CSE student and he is studing in HNB Garhwal University. His roll number is 21134501015.")
    talk("My creator name is Aniket and he is a B Tech CSE student and he is studing in HNB Garhwal University. His roll number is 21134501015.")

def questions():
    talk("Searching on Google...")
    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
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

def take_screenshot():
    talk("Tell me the name for the file")
    name = takeCommand().lower()
    time.sleep(3)
    img = py.screenshot()
    img.save(f"{name}.png")
    talk(f"Screenshot saved as {name}.png")

def adjust_volume(direction):
    if direction == "up":
        for _ in range(5):
            py.press('volumeup')
    elif direction == "down":
        for _ in range(5):
            py.press('volumedown')

def open_system_feature(feature_name):
    talk(f"Opening {feature_name}...")
    if feature_name == "spotlight":
        py.hotkey("alt", "space")
        time.sleep(3)
        py.press('backspace')
        time.sleep(0.5)
        talk("What should I search for?")
        search_query = takeCommand().lower()
        py.typewrite(search_query, interval=0.1)
        talk("Searching..." f"{search_query}")
        py.press("enter")
    elif feature_name == "text extractor":
        py.hotkey("win", "shift", "t")
    elif feature_name == "fancy zone":
        py.hotkey("win", "shift", "`")
    elif feature_name == "always on top":
        py.hotkey('win', 'ctrl', 't')

# Actions (continued)
def stop_music():
    talk("Stopping music...")
    os.system("taskkill /f /im wmplayer.exe")

def get_ip_address():
    talk("Checking your IP address...")
    try:
        ip = requests.get('https://api.ipify.org').text
        print(ip)
        talk(f"Your IP address is {ip}")
    except Exception as e:
        talk("Network is not available. Please try again later.")

def control_browser_tab(action):
    if action == "new":
        py.hotkey('ctrl', 't')
    elif action == "next":
        py.hotkey('ctrl', 'tab')
    elif action == "previous":
        py.hotkey('ctrl','shift', 'tab')
    elif action == "home":
        py.hotkey('alt', 'home')
    elif action == "close":
        py.hotkey('ctrl', 'w')
    elif action == "close_window":
        py.hotkey('ctrl', 'shift' 'w')
    elif action == "download_page":
        py.hotkey('ctrl', 'j')
    elif action == "address_bar":
        py.hotkey('ctrl', 'l')
    elif action == "login_to_different_user":
        py.hotkey('ctrl', 'shift', 'm')

# Actions (continued)
def start_again():
    py.press('space')
    
def stop_the_video():
    py.press('space')

def open_task_manager():
    talk("Opening Task Manager...")
    os.system("taskmgr")

def minimize_all_windows():
    talk("Minimizing all windows...")
    py.hotkey('win', 'd')

def maximize_window():
    talk("Maximizing the window...")
    py.hotkey('win', 'up')

def minimize_window():
    talk("Minimizing the window...")
    py.hotkey('win', 'down')

def open_calendar():
    talk("Opening Calendar...")
    os.system("start outlookcal:")

def open_file_explorer():
    talk("Opening File Explorer...")
    os.system("explorer")

def open_notepad():
    talk("Opening Notepad...")
    os.system("start notepad")

def open_control_panel():
    talk("Opening Control Panel...")
    os.system("control")

def open_command_prompt():
    talk("Opening Command Prompt...")
    os.system("start cmd")

def open_power_settings():
    talk("Opening Power Settings...")
    os.system("powercfg.cpl")

def open_device_manager():
    talk("Opening Device Manager...")
    os.system("devmgmt.msc")

def open_system_properties():
    talk("Opening System Properties...")
    os.system("sysdm.cpl")

def open_network_connections():
    talk("Opening Network Connections...")
    os.system("ncpa.cpl")

# Actions (continued)
def open_browser(browser_name):
    talk(f"Opening {browser_name}...")
    if browser_name.lower() == "chrome":
        os.system("start chrome")
    elif browser_name.lower() == "firefox":
        os.system("start firefox")
    elif browser_name.lower() == "edge":
        os.system("start msedge")
    elif browser_name.lower() == "opera":
        os.system("start opera")

def close_browser(browser_name):
    talk(f"Closing {browser_name}...")
    if browser_name.lower() == "chrome":
        os.system("taskkill /f /im chrome.exe")
    elif browser_name.lower() == "firefox":
        os.system("taskkill /f /im firefox.exe")
    elif browser_name.lower() == "edge":
        os.system("taskkill /f /im msedge.exe")
    elif browser_name.lower() == "opera":
        os.system("taskkill /f /im opera.exe")

def open_media_player():
    talk("Opening Windows Media Player...")
    os.system("wmplayer")

def close_media_player():
    talk("Closing Windows Media Player...")
    os.system("taskkill /f /im wmplayer.exe")

def open_text_editor():
    talk("Opening Text Editor...")
    os.system("notepad")

def close_text_editor():
    talk("Closing Text Editor...")
    os.system("taskkill /f /im notepad.exe")

# Main function
if __name__ == "__main__":
    engine = initialize_engine()
    wake_words = get_wake_words()
    is_awake = False
    
    while True:
        if not is_awake:
            is_awake = respond_to_wake_words(wake_words)
            if is_awake:
                greet()
        else:
            query = takeCommand().lower()
            print("Assistant is awake and Listening")
            
            if "go to sleep" in query:
                print("Alright then, Saayonara...")
                talk("Alright then, saayonara...")
                is_awake = False
                continue
            
            greeting_response = respond_to_greetings(query)
            if greeting_response:
                talk(greeting_response)
            
            if "play" in query:
                play_on_youtube(query)
            
            elif "time" in query:
                get_time()
                
            elif "date" in query:
                get_today_date()
                
            elif "search" in query:
                if "YouTube" in query or "youtube" in query or "video" in query:
                    search_on_youtube(query)
                else:
                    search_on_google(query)
            
            elif "what" in query or "when" in query or "who" in query or "why" in query or "how" in query:
                if "how are you" in query:
                    respond_to_how_are_you()
                elif "what are you" in query:
                    introduce_assistant()
                elif "who created you" in query:
                    who_created_assistant()
                elif "who is Aniket" in query or "creator" in query:
                    about_the_creator()
                elif "what can you do" in query:
                    what_can_you_do()
                else:
                    questions()
            
            elif "take screenshot" in query:
                take_screenshot()
            
            elif "volume" in query:
                if "up" in query or "increase" in query:
                    adjust_volume("up")
                elif "down" in query or "decrease" in query:
                    adjust_volume("down")
            
            elif "open spotlight" in query:
                open_system_feature("spotlight")
            
            elif "open text extractor" in query:
                open_system_feature("text extractor")
            
            elif "open fancy zone" in query:
                open_system_feature("fancy zone")
            
            elif "always on top" in query:
                open_system_feature("always on top")
                
            elif "shut down the system" in query:
                talk("Shutting down the system...")
                os.system("shutdown /s /t 1")
                
            elif "restart the system" in query:
                talk("Restarting the system...")
                os.system("shutdown /r /t 1")
                
            elif "sleep the system" in query:
                talk("Sleeping the system...")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                
            elif "hibernate the system" in query:
                talk("Hibernating the system...")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,1")
                
            elif "lock the system" in query:
                talk("Locking the system...")
                os.system("rundll32.exe user32.dll,LockWorkStation")
                
            elif "check my ip address" in query:
                get_ip_address()
            
            elif "open new tab" in query:
                control_browser_tab("new")
                
            elif "go to next tab" in query:
                control_browser_tab("next")
                
            elif "go to previous tab" in query:
                control_browser_tab("previous")
                
            elif "open home page" in query:
                control_browser_tab("home")
                
            elif "close this tab" in query:
                control_browser_tab("close")
                
            elif "close this window" in query:
                control_browser_tab("close_window")
                
            elif "open download page" in query:
                control_browser_tab("download_page")
                
            elif "open address bar" in query:
                control_browser_tab("address_bar")
            
            elif "open task manager" in query:
                open_task_manager()
            
            elif "minimise all windows" in query:
                minimize_all_windows()
            
            elif "maximize window" in query:
                maximize_window()
            
            elif "minimise window" in query:
                minimize_window()
            
            elif "open calender" in query:
                open_calendar()
            
            elif "open file explorer" in query:
                open_file_explorer()
            
            elif "open notepad" in query:
                open_notepad()
            
            elif "open control panel" in query:
                open_control_panel()
            
            elif "open command prompt" in query:
                open_command_prompt()
            
            elif "open power settings" in query:
                open_power_settings()
            
            elif "open device manager" in query:
                open_device_manager()
            
            elif  "open system properties" in query:
                open_system_properties()
            
            elif "open network connections" in query:
                open_network_connections()
            
            elif "open chrome" in query:
                open_browser("chrome")
            
            elif "open firefox" in query:
                open_browser("firefox")
            
            elif "open edge" in query:
                open_browser("edge")
            
            elif "open opera" in query:
                open_browser("opera")
            
            elif "close chrome" in query:
                close_browser("chrome")
            
            elif "close firefox" in query:
                close_browser("firefox")
            
            elif "close opera" in query:
                close_browser("opera")
            
            elif "close edge" in query:
                close_browser("edge")
            
            elif "open media player" in query:
                open_media_player()
            
            elif "close media player" in query:
                close_media_player()
            
            elif "open text editor" in query:
                open_text_editor()
            
            elif "close text editor" in query:
                close_text_editor()
            
            





