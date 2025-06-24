# Install the necessary libraries
# $ pip install google-generativeai
# $ pip install pyttsx3
# $ pip install SpeechRecognition

import pyttsx3
import speech_recognition as sr
import google.generativeai as genai

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Configure the Google Generative AI with the API key
genai.configure(api_key="AIzaSyCV4QPs5zokQXJk9tw4uR9yH28f7acdCfk")

# Define the generation configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Create the GenerativeModel instance
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings can be added here if needed
)

# Start a chat session with an initial message
chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": ["hi"],
    },
  ]
)

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Capture audio input from the microphone
with sr.Microphone() as source:
    print("Speak something...")
    audio_data = recognizer.listen(source)

# Perform speech recognition using Google Web Speech API
try:
    text = recognizer.recognize_google(audio_data)
    print("You said:", text)
    
    # Send the recognized text to the chat session and get a response
    response = chat_session.send_message(f"Limit to 100 words \n{text}")
    print("AI response:", response.text)
    
    # Convert the AI response to speech
    engine.say(response.text)
    print("speaking...")
    engine.runAndWait()
    print("completed...")
except sr.UnknownValueError:
    print("Sorry, could not understand audio.")
except sr.RequestError as e:
    print(f"Error: Could not request results from Google Speech Recognition service; {e}")
