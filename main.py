# jarvis
import speech_recognition as sr 
import webbrowser     #This is used to open browser 
import pyttsx3   #It is used to convert text to speech
import musicLibrary
from openai import OpenAI 
from gtts import gTTS  #google text to speech
import pygame
import os
import requests
# pip install pocketsphinx 

recognizer = sr.Recognizer()   #It is a class which is used to recognize speech
engine = pyttsx3.init()  #It is used to initilize 
newsapi = "1ff6860287e7b217a623dfaac520e64b"


def speak_old(text):
    engine.say(text) #This is come from pyttsx3 website to say text
    engine.runAndWait()

#google text to speech    
def speak(text):
    
    tts = gTTS(text)
    tts.save('temp.mp3')
    

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")  # Replace with your actual file name

    # Play the mp3
    pygame.mixer.music.play()

    # Keep the script running while the music plays
    while pygame.mixer.music.get_busy():
        clock = pygame.time.Clock()  

        
        clock.tick(10)  # This limits the loop to 10 frames per second

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(api_key = "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",)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )
    return (completion.choices[0].message.content)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apikey={newsapi}")
        if r.status ==200:
            # JSON response
            data = r.json()

            # Extract the headlines
            articles = data.get('articles',[])

            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # let openai handle the request by openai api
        output = aiProcess(c)
        speak(output)


if __name__ =="__main__":
    speak("Initializing Jarvis....")
    while True:
        #listen for the wake word "jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
      
        print("recgonizing...")
        # recognize speech using google cloud
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        
        except Exception as e:
            print("Error; {0}".format(e))


