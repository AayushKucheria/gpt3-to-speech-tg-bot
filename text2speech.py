# Text2Speech
# Src: https://www.geeksforgeeks.org/convert-text-speech-python/
from gtts import gTTS
import os
from io import BytesIO
from pygame import mixer
import time
from secrets import openai_key

## Speech2Text pip install git+https://github.com/openai/whisper.git
import openai
import whisper

import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

name_of_AI = "AI"

def get_completion(prompt, user="User"):
  response = openai.Completion.create(
          model="text-davinci-003", #TODO which one is best?
          prompt=prompt,
          max_tokens=100,
          temperature=0.6, #TODO which one is best?
          stop=user+":"
      )
  if debug:
    print("whole big GPT response: ", response)
  response = response.choices[0].text
  return response


def get_audio(text, filename, toPlay=False):

    # Generate
    # print("Text = ", text)
    tts = gTTS(text=text, lang='en', slow=False)
    # Save
    tts.save(filename)

    # Use pygame to play the audio
    if toPlay:
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
    

def get_text(filename):
    audio_result = audio_model.transcribe(filename)
    prompt = audio_result["text"]
    # print(prompt)
    return prompt


audio_model = whisper.load_model("base", device="cpu")
# pygame.init()
# GPT Generates Response
openai.api_key = openai_key
debug = False
prompt = "Hello my name is Rianna. I just woke up! What should I do today?"
filename = "audio.mp3"

c = 0
# while True:
#     # Get text from audio
#     print(c, ": ", prompt)
#     # Get audio from response
#     get_audio(prompt + " yo ", filename)
    
#     # Get response from GPT
#     response = get_completion(prompt)
#     while response == "":
#         time.sleep(5)
    
#     prompt = response

#     c += 1



