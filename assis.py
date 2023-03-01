import speech_recognition as sr
from gtts import gTTS
import os
import openai

openai.api_key = "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"

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = ""
user_name = "Pacha"
bot_name = "Aguida"

while True:
    with mic as source:
        print("\n Listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("no longer listening")

    try:
        user_input = r.recognize_google(audio, language='fr-FR')
    except:
        continue

    prompt = user_name+":"+user_input + "\n"+bot_name+":"
    conversation += prompt

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=conversation,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(
        user_name + ":" ,1)[0].split(bot_name+ ":",1)[0]

    conversation+= response_str +"\n"
    print(response_str)

    # use gTTS to convert OpenAI response to speech
    tts = gTTS(text=response_str, lang='fr')
    tts.save("response.mp3")

    # play the speech using the default media player
    os.system("afplay response.mp3")
