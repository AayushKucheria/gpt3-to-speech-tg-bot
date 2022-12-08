import text2speech
import time

# TELEGRAM THINGY

TELEGRAM_API_KEY = '5754230605:AAErjhrodU9sjLdSXG_9bkh_T395phP5p-M'

# Remove this line
from telegram import Update, Bot
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

from pydub import AudioSegment
debug = False

def get_voice(update: Update, context: CallbackContext) -> None:
    # get basic info about the voice note file and prepare it for downloading
    print("voice detected")
    print(update)
    new_file = context.bot.get_file(update.message.voice.file_id)
    # download the voice note as a file
    new_file.download(f"voice_note.ogg")
    print("download done?")
    # Convert to mp3
    AudioSegment.from_file("voice_note.ogg").export("prompt.mp3", format="mp3")

    # Get text from audio
    prompt = text2speech.get_text("prompt.mp3")
    
    # Get name of user
    name_of_user = "User"
    try:
      name_of_user = update.message.from_user.first_name
    except:
      pass
    prompt = name_of_user + ": " + prompt + "\n" + text2speech.name_of_AI + ": "

    print("prompt: ", prompt)
    # Get response from GPT
    response = text2speech.get_completion(prompt)
    while response == "":
        time.sleep(0.1)
    print("response: ", response)
    # Get audio from response

    text2speech.get_audio(response, "audio.mp3")
    print("audio done")

    # Use the send_message method to send a message to the user
    chat_id = update.message.chat_id
    if debug:
      print(chat_id)
    return bot.send_voice(chat_id=chat_id, voice=open("audio.mp3", "rb"))
    # return bot.send_voice(chat_id=chat_id, "voice_note.ogg")

# Create bot
bot = Bot(token=TELEGRAM_API_KEY)

# Monitor the bot
print("starting")
updater = Updater(TELEGRAM_API_KEY)
forward_message_handler = MessageHandler(Filters.voice, get_voice)
updater.dispatcher.add_handler(forward_message_handler)
updater.start_polling(
)  # This runs in the background, looking for new forwarded messages.
# try if bug: updater.idle()