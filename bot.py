import logging
from telegram import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from dotenv import load_dotenv
import yt_dlp

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Grab API Token from .env file
load_dotenv()
API_Token = os.environ.get('API_Token')


def start(update, context):
    update.message.reply_text('Hi! Send me a youtube (or supported) link for some music 🎵')


def help_me(update, context):
    update.message.reply_text(
        '1. This bot can download the audio from a video (Playlists supported).\n\n' \
        '2. For a list of supported sites visit https://ytdl-org.github.io/youtube-dl/supportedsites.html\n\n' \
        '3. The Telegram API that this bot uses has a 50MB limit for audio files. The bot will not be able to send a file if it is larger than that.\n\n' \
        '4. Youtube does compress their audio so there are compromises to make when it comes to quality. The bot does download the best quality available')


def get_audio(update, context):
    url = update.message.text
    # Get audio from link
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': 'Audio/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Send every song that was downloaded
    for file in os.listdir("Audio"):
        update.message.reply_audio(audio=open("Audio/" + file, 'rb'), timeout=50)

    # Delete everything in the Audio Folder
    for file in os.listdir("Audio"):
        os.remove("Audio/" + file)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text("Hmm, that doesn't look like a link I can process. Please try again with another link")


def main():
    updater = Updater(API_Token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, get_audio))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
