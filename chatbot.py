import streamlit as st
import speech_recognition as sr
import pyttsx3
import openai
import time
import elevenlabs

# Initialize APIs and variables
elevenlabs.set_api_key('074f50e26caa45f26ad028a1371ff6c8')
openai.api_key = ("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")
messages = []

# Function to speak text
def speak(text):
    audio_data = elevenlabs.generate(text=text, voice="Rachel")
    elevenlabs.play(audio_data)
    time.sleep(1)

# Function to transcribe user input
def transcribe_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak now...")
        audio = r.listen(source)
    try:
        input_text = r.recognize_google(audio)
        st.write(f"You said: {input_text}")
        return input_text
    except sr.UnknownValueError:
        st.write("Sorry, I could not understand your speech.")
        return None
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Main function to conduct interview
def conduct_interview():
    # Set conversation duration to 15 min (900 sec)
    max_duration = 900
    start_time = time.time()
    # Set maximum number of questions
    max_questions = 10
    question_count = 0

    while question_count < max_questions:
        elapsed_time = time.time() - start_time

        if elapsed_time > max_duration - 60:  # Notify the user 1 minute before the timeout
            st.write("Attention: The interview will end in 1 minute. Please wrap up your responses.")
        if elapsed_time > max_duration:
            st.write("Interview time exceeded. Thank you for your participation.")
            break

        if question_count == 0:
            # Initial system message asking about name and industry
            intro_question = "Welcome! Can you please introduce yourself and your industry?"
            messages.append({"role": "system", "content": intro_question})
            speak(intro_question)
            st.write("\n" + intro_question + "\n")
            user_intro_response = transcribe_input()
            messages.append({"role": "user", "content": user_intro_response})

        response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        speak(reply)
        st.write("\n" + reply + "\n")

        # Increment the question_count
        question_count += 1
        if question_count < max_questions:
            follow_up_question = "Please provide more details."
            messages.append({"role": "system", "content": follow_up_question})
            speak(follow_up_question)
            message = transcribe_input()
            messages.append({"role": "user", "content": message})

            if message.lower() == "quit()":
                break

# Streamlit app layout
st.title("Simulated Interview Chatbot")
st.write("Noted: This is a simulated interview for practice purposes only. It does not reflect your actual skills or qualifications.")

message = '''I want you to act as an interviewer.
your personality type is friendly and warm .
you can ask technical questions and IQ questions.
Only conduct the interview with me. 
Ask the questions one by one and wait for my answers.
Do not write explanations. 
you will ask me the interview questions.
'''
st.write(message)

# Interview button
if st.button("Start Interview"):
    conduct_interview()

# Quit button
if st.button("Quit"):
    st.stop()
