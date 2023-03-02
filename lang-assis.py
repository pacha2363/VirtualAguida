import speech_recognition as sr
import openai
from langdetect import detect
from gtts import gTTS
import os

openai.api_key = "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"

r = sr.Recognizer()
mic = sr.Microphone()

conversation = ""
user_name = "User"
bot_name = "Bot"

while True:
    with mic as source:
        print("\n Listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("no longer listening")

    try:
        user_input = r.recognize_google(audio)
    except:
        continue

    prompt = user_name + ": " + user_input + "\n" + bot_name + ": "
    conversation += prompt

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=conversation,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]

    conversation += response_str + "\n"
    print(response_str)

    # detect the language of the response
    lang_code = detect(response_str)
    print(f"Detected language: {lang_code}")

    # use GTTS to convert OpenAI response to speech
    tts = gTTS(text=response_str, lang=lang_code)
    tts.save("response.mp3")

    # play the speech using the default media player
    os.system("afplay response.mp3")
