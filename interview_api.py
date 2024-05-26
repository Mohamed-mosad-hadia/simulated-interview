# File: interview_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import speech_recognition as sr 
import pyttsx3 
import openai
import time  
import elevenlabs
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Elevenlabs TTS setup
elevenlabs.set_api_key('Your_api_key')

# OpenAI API key
openai.api_key = "API"

# Initialize conversation list
conversation = []

# Prompt engineering
system_msg = "interviewer"
conversation.append({"role": "system", "content": system_msg})

prompt = '''I want you to act as an interviewer.
your personality type is friendly and warm.
you can ask technical questions and IQ questions.
Only conduct the interview with me.
Ask the questions one by one and wait for my answers.
Do not write explanations.
you will ask me the interview questions.
'''
conversation.append({"role": "user", "content": prompt})

# FastAPI Models
class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    conversation: List[Message]

class Response(BaseModel):
    reply: str

# TTS function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Speech recognizer function
def transcribe_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
    try:
        input_text = r.recognize_google(audio)
        print(f"You said: {input_text}")
        return input_text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Interview API. Use /start_interview to start and /next_question to continue."}

# Initial system message asking about name and industry
@app.post("/start_interview", response_model=Response)
def start_interview():
    global conversation
    conversation = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ]
    
    intro_question = "Welcome! Can you please introduce yourself and what industry are you currently working in?"
    conversation.append({"role": "system", "content": intro_question})
    speak(intro_question)
    print("\n" + intro_question + "\n")

    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=conversation)
    reply = response["choices"][0]["message"]["content"]
    conversation.append({"role": "assistant", "content": reply})
    speak(reply)
    print("\n" + reply + "\n")

    return {"reply": intro_question}

# Process user responses and generate next question
@app.post("/next_question", response_model=Response)
def next_question(message: Message):
    global conversation

    conversation.append(message.dict())

    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=conversation)
    reply = response["choices"][0]["message"]["content"]
    conversation.append({"role": "assistant", "content": reply})
    speak(reply)
    print("\n" + reply + "\n")

    return {"reply": reply}



#uvicorn interview_api:app --reload
