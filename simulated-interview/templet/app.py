import numpy as np
from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
from openai import OpenAI
import time
import elevenlabs
import pickle

flask_app = Flask(__name__)
elevenlabs.set_api_key('074f50e26caa45f26ad028a1371ff6c8')

# Load your machine learning model or chatbot model
with open("main.py", "rb") as file:
    model = pickle.load(file)

@flask_app.route("/")
def home():
    return render_template("index.HTML")

@flask_app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    r = sr.Recognizer()
    with sr.AudioFile(request.files["audio_data"]) as source:
        audio_data = r.record(source)
    try:
        text = r.recognize_google(audio_data)
        return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"})

@flask_app.route("/chat", methods=["POST"])
def chat():
    # Get user's message from the request
    user_message = request.form["message"]
    
    # Send user's message to chatbot model and get response
    response = OpenAI.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{"role": "user", "content": user_message}])
    chatbot_response = response["choices"][0]["message"]["content"]
    
    return jsonify({"response": chatbot_response})

if __name__ == "__main__":
    flask_app.run(debug=True)
