import speech_recognition as sr 
import pyttsx3 
import openai
import time  #library control the timing of responses.
import elevenlabs


#TTS Elevenlabs 
elevenlabs.set_api_key('Your_api_key')

#api_key form website openAi
openai.api_key = ("Your_api_key")


# empty list to store the conversation  sequence.
conversation = []





#Prompt engineering 
system_msg = "interviewer"                                  
conversation.append({"role": "system", "content": system_msg}) 
print("Noted: This is a simulated interview for practice purposes only. It does not reflect your actual skills or qualifications.")


prompt = '''I want you to act as an interviewer.
your personality type is friendly and warm .
you can ask technical questions and IQ questions.
Only conduct the interview with me. 
Ask the questions one by one and wait for my answers.
Do not write explanations. 
you will ask me the interview questions.
'''
conversation.append({"role": "user", "content": prompt})           




#function Text to speech
def speak(text):
    engine =pyttsx3.init()
    engine .say(text)
    engine.runAndWait()
    # audio_data=elevenlabs.generate(text=text,voice="Rachel")
    # elevenlabs.play(audio_data)
    # time.sleep(1)
    
    
#function speech recgnizer    
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







# set conversation duration to 10 min(600)
max_duration=600
start_time=time.time()




#set maximum number of questions
max_questions=5
question_count=0



# Initial system message asking about name and industry
if question_count == 0:
    
    intro_question = "welcome!Can you please introduce yourself and What industry are you currently working in?"
    conversation.append({"role": "system", "content": intro_question})
    speak(intro_question)
    print("\n" + intro_question + "\n")

    
    user_intro_response = transcribe_input()
    conversation.append({"role": "user", "content": user_intro_response})

    
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=conversation) # uses the OpenAI API to generate a response based on the current conversation context stored in the messages list.
    reply = response["choices"][0]["message"]["content"] #extracts the generated response text from the API response.
    conversation.append({"role": "assistant", "content": reply})
    speak(reply) 
    print("\n" + reply + "\n")
    
    
    
    
    
    #increment the question_count
    question_count+=1
    if question_count < max_questions:
        message = transcribe_input() # To detect and identify the spoken response from the user
        conversation.append({"role": "user", "content": message})#adds the user's input to the conversation history.
       







# while question_count < max_questions:
#     elapsed_time = time.time() - start_time
    
#     if elapsed_time > max_duration - 60:  # Notify the user 1 minute before the timeout
#        print("Attention: The interview will end in 1 minute. Please wrap up your responses.")
#     if elapsed_time > max_duration:
#         print("Interview time exceeded. Thank you for your participation.")
#         break
    
    
