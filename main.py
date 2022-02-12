from gtts import gTTS
import os
import speech_recognition as sr
import playsound
import datetime
from time import localtime,strftime
import re
import requests
import webbrowser
import bs4
import smtplib

def listen():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        audio = r.listen(source,phrase_time_limit=5)
    data=""

    try:
        data = r.recognize_google(audio,language='en-US')
        print ("You said: "+data)
    except sr.UnknownValueError:
        print("I could't hear you.")
    except sr.RequestError as e:
        print("Request Failed")
    return data


def respond(String):
    print(String)
    tts=gTTS(text=String,lang='en')
    tts.save('speech.mp3')
    playsound.playsound('speech.mp3')
    os.remove('speech.mp3')


def voice_assistant(data):
    if "how are you" in data:
        listening = True
        respond("I am good my creater.")

    if "time" in data:
        listening = True
        respond("it's "+ strftime('%H hour and %M minutes',localtime()))

    if "date" in data:
        listening = True
        respond("today is "+ str(datetime.date.today()) )

    if "open google" in data.casefold():
        listening = True
        reg_ex = re.search('open google(.*)',data)
        url = 'https://www.google.com/'
        if reg_ex:
            sub = reg_ex.group(1)
            url = url+'r/'
        webbrowser.open(url)
        respond('Done')

    if "email" in data:
        listening = True
        respond("whom should i send email to?")
        to = listen()
        emaildict = {'first' : 'ayush1@tempmail.com', 'second':'ayush2@tempmail.com'}
        toaddr = emaildict[to]
        respond("what is the subject?")
        subject = listen()
        respond("what should i write in email?")
        message = listen()
        content = 'Subject: {}\n\n'.format(subject,message)

        #init gmail setting
        mail = smtplib.SMTP('smtp.gmail.com',587)
        #identify server
        mail.ehlo()
        mail.starttls()
        #login id
        mail.login('yourloginemail@gmail.com','password')
        mail.sendmail('yourloginemail@gmail.com',toaddr,content)
        mail.close()
        respond('Email Sent')



    if "wiki" in data.casefold():
        listening = True
        respond("what do you want to know about")
        query = listen()
        response = requests.get('https://en.wikipedia.org/wiki/'+query)
        if response is not None :
            html = bs4.BeautifulSoup(response.text,'html.parser')
            paragraphs = html.select('p')
            intro = [i.text for i in paragraphs]
            halo = ''.join(intro)
        respond(halo[:200])

    if "exit" in data:
        listening = False
        print("Listening Stopped")
        respond("See you Ayush")


    try:
        return listening
    except UnboundLocalError:
        respond("Sorry.... Please try again!!")
        data = listen()
        listening = voice_assistant(data)




respond("Hi, I am Ullu, Your Personal Voice assistant. How can i help you?")
listening = True

while listening == True:
    data = listen()
    listening = voice_assistant(data)