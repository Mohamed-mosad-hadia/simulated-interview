import speech_recognition as sr
import pyttsx3
import openai
import random
import time
import os

openai.api_key = ("your_api_key")

messages = []
system_msg = "interviewer"
messages.append({"role": "system", "content": system_msg})
print("Mediator Is Ready For Asking You ")

message = "I want you to act as an interviewer. I will be the candidate, and you will ask me the interview questions for the position of a job. Only conduct the interview with me. Ask the questions one by one and wait for my answers. Do not write explanations."
messages.append({"role": "user", "content": message})

engine = pyttsx3.init()
engine.setProperty('rate', 100)

def speak(text):
    engine.say(text)
    engine.runAndWait()

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

max_duration = 900
start_time = time.time()

max_questions = 10
question_count = 0

technical_prompt = "Ask a technical question related to [user's expertise or field]."
iq_prompt = "Pose an IQ challenge or puzzle for the candidate to solve."
job_related_prompt = "Generate a job-related question based on the user's profession."

while question_count < max_questions:
    elapsed_time = time.time() - start_time
    
    if elapsed_time > max_duration - 60:
        print("Attention: The interview will end in 1 minute. Please wrap up your responses.")
    if elapsed_time > max_duration:
        print("Interview time exceeded. Thank you for your participation.")
        break

    question_category = random.choice(["technical", "iq", "job_related"])

    if question_category == "technical":
        technical_question = openai.Completion.create(
            engine="text-davinci-edit-001",
            prompt=technical_prompt,
            temperature=0.7,
            max_tokens=100,
        )["choices"][0]["text"].strip()
        question = f"Technical Question: {technical_question}"
    elif question_category == "iq":
        iq_question = openai.Completion.create(
            engine="text-davinci-edit-001",
            prompt=iq_prompt,
            temperature=0.7,
            max_tokens=100,
        )["choices"][0]["text"].strip()
        question = f"IQ Question: {iq_question}"
    else:
        job_related_question = openai.Completion.create(
            engine="text-davinci-edit-001",
            prompt=job_related_prompt,
            temperature=0.7,
            max_tokens=100,
        )["choices"][0]["text"].strip()
        question = f"Job-related Question: {job_related_question}"

    messages.append({"role": "assistant", "content": question})
    speak(question)

    question_count += 1
    if question_count < max_questions:
        user_response = transcribe_input()
        messages.append({"role": "user", "content": user_response})
        if user_response.lower() == "quit()":
            break

print("Interview concluded. Providing feedback...")

positive_keywords = ["good", "impressed", "excellent", "well done"]
negative_keywords = ["improve", "weak", "unsatisfactory", "not clear"]

positive_feedback_count = sum(message["content"].lower() in positive_keywords for message in messages if message["role"] == "user")
negative_feedback_count = sum(message["content"].lower() in negative_keywords for message in messages if message["role"] == "user")

if positive_feedback_count > negative_feedback_count:
    print("Overall, your responses were positive. Well done!")
elif negative_feedback_count > positive_feedback_count:
    print("There were areas that could be improved in your responses. Consider refining your answers.")
else:
    print("Your responses were balanced. Good effort!")
