import speech_recognition as sr # convert spoken audio into text 
import pyttsx3 #convert written text to spoken audio using 
import openai
import time #library control the timing of responses.
import elevenlabs


#TTS Elevenlabs 
elevenlabs.set_api_key('Your_API')
#api_key form website openAi
openai.api_key = ("Your_API")


# empty list to store the conversation  sequence.
messages = []





#sys_msg
system_msg = '''interviewer.act as an interviewer.
your personality type is friendly and warm .
you can ask technical questions and IQ questions.
Only conduct the interview with me. 
Ask the questions one by one and wait for my answers.
Do not write explanations.
At the end of the conversation, give me a stay. '''

#chatbot will act as an interviewer in the conversation
messages.append({"role": "system", "content": system_msg})  # system --> chat-gpt act as interviewer
print("Noted: This is a simulated interview for practice purposes only. It does not reflect your actual skills or qualifications.")


message = '''I want you to act as an interviewer.
your personality type is friendly and warm .
you can ask technical questions and IQ questions.
Only conduct the interview with me. 
Ask the questions one by one and wait for my answers.
Do not write explanations. 
you will ask me the interview questions.
'''
messages.append({"role": "user", "content": message}) 





def speak(text):
    #engine =pyttsx3.init()
    #engine .say(text)
    #engine.runAndWait()
    audio_data=elevenlabs.generate(text=text,voice="Rachel")
    elevenlabs.play(audio_data)
    time.sleep(1)
    
    

def transcribe_input():
    r = sr.Recognizer()
    with sr.Microphone() as source: #Accesses the Microphone:
        print("Speak now...")
        audio = r.listen(source) # audio= input from the microphone 
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







# set conversation duration to 15 min(900sec)
max_duration=600
start_time=time.time()


#set maximum number of questions
max_questions=10
question_count=0

while question_count < max_questions:
    elapsed_time = time.time() - start_time
    
    if elapsed_time > max_duration - 60:  # Notify the user 1 minute before the timeout
       print("Attention: The interview will end in 1 minute. Please wrap up your responses.")
    if elapsed_time > max_duration:
        print("Interview time exceeded. Thank you for your participation.")
        break
    
    
    if question_count == 0:
        # Initial system message asking about name and industry
        intro_question = "welcome!Can you please introduce yourself and ur industry?"
        messages.append({"role": "system", "content": intro_question})
        speak(intro_question)
        print("\n" + intro_question + "\n")
        user_intro_response = transcribe_input()
        messages.append({"role": "user", "content": user_intro_response})
    
    
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages) # uses the OpenAI API to generate a response based on the current conversation context stored in the messages list.
    reply = response["choices"][0]["message"]["content"] #extracts the generated response text from the API response.
    messages.append({"role": "assistant", "content": reply})
    speak(reply)
    print("\n" + reply + "\n")
    
    
    
    
    
    #increment the question_count
    question_count+=1
    if question_count < max_questions:
        follow_up_question = "Please provide more details."
        messages.append({"role": "system", "content": follow_up_question})
        speak(follow_up_question)
        message = transcribe_input()#transcribe_input function to listen for and recognize the user's spoken response.  or To detect and identify the spoken response from the user
      
        messages.append({"role": "user", "content": message})
       
        if message.lower() == "quit()":
           
         break




# Interview button
#if st.button("Start Interview"):
   # conduct_interview()


# Quit button
#if st.button("Quit"):
    #st.stop()
