# import necessary libraries
from dotenv import load_dotenv
import openai
from gtts import gTTS
from playsound import playsound
import os
import winsound
import time
from pydub import AudioSegment
import speech_recognition as sr


# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.environ.get('sk-EwZeGboRfAkEMbIzxN0VT3BlbkFJFWbLMSvedcO83hJok20y')
openai.api_key = "sk-EwZeGboRfAkEMbIzxN0VT3BlbkFJFWbLMSvedcO83hJok20y"

# Initialize speech recognizer
r = sr.Recognizer()

# Initialize conversation variables
conversation = ""
user_name = input("Enter your name: ")
bot_name = "Aguida"

# Prompt for user's preferred input mode
input_mode = input(f"{user_name}, would you like to use text input or voice input? (Enter 'text' or 'voice'): ")

if input_mode.lower() == "voice":
    mic = sr.Microphone()
else:
    mic = None


def generate_response(conversation, model_engine="text-davinci-002", temperature=0.5, max_tokens=1024):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=conversation,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )

    message = completions.choices[0].text.strip()
    return message


def text_to_audio(text, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("response.mp3")
    time.sleep(0.5)  # add a delay to ensure the file has been completely written and closed
    #playsound("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    with open("response.wav", "rb") as f:
        winsound.PlaySound(f.read(), winsound.SND_MEMORY)


while True:
    if mic:
        with mic as source:
            print("\nListening...")
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
        print("No longer listening")
        prompt = r.recognize_google(audio)
    else:
        prompt = input(f"{user_name}, please enter a prompt: ")

    if prompt.lower() == "exit":
        break

    conversation += f"\n{user_name}: {prompt}"
    response_str = generate_response(conversation)

    # Detecting the language of the response
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Detect the language of the following text:\n{response_str}\n---\n",
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.0,
    )
    lang_code = response.choices[0].text.strip()

    if lang_code == "fr":
        lang = "fr-FR"
    elif lang_code == "ja":
        lang = "ja"
    else:
        lang = "en"

    print(f"{bot_name}: {response_str}")
    text_to_audio(response_str, lang)