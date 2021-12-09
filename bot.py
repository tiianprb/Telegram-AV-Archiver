import logging
import telegram
from telegram import update, ParseMode
from telegram.chataction import ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from dotenv import load_dotenv
import yt_dlp
import time

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Grab API Token from .env file
load_dotenv()
API_Token = os.environ.get("API_Token")


def start(update, context):
    logger.info(f"User {update.message.chat.first_name} started a chat")
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text("Hi! I can download audio and video from supported links. /help for more info")


def help_me(update, context):
    logger.info(f"User {update.message.chat.first_name} requested help")
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text(
        "1. This bot can download the audio from a video (Playlists supported).\n\n" \
        "2. To download audio use the /get_audio command. <em>Example: /get_audio https://www.mylink.com </em> .\n\n" \
        "3. To download a video use the /get_video command. <em> Example: /get_video https://www.mylink.com </em>.\n\n" \
        "4. For a list of supported sites visit https://ytdl-org.github.io/youtube-dl/supportedsites.html\n\n" \
        "5. The Telegram API that this bot uses has a 50MB limit for audio files. The bot will not be able to send a file if it is larger than that.\n\n" \
        "6. Youtube does compress their audio so there are compromises to make when it comes to quality. The bot does download the best quality available\n\n"
        "7. For help or issues please open a new ticket at https://github.com/mascode/Telegram-AV-Archiver/issues ", parse_mode=ParseMode.HTML)


def get_audio(update, context):
    url = context.args[0]
    logger.info(f"User {update.message.chat.first_name} requested audio from {url}")
    # Get audio from link
    logger.info(f"Setting downloading options for audio")
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
        "outtmpl": "Audio/%(title)s.%(ext)s"
    }
    logger.info(f"Bot requested audio from {url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    time.sleep(3)
    # Check file size
    for file in os.listdir("Audio"):
        if os.path.getsize("Audio/" + file) > 50000000:
            context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
            update.message.reply_text("Sorry the file is too large to send :(, but I did save it in the folder")
            logger.info(f"File {file} is too large to send")
            # Move file to "Large" folder
            os.rename("Audio/" + file, "Large/Audio/" + file)
            logger.info(f"Moved file {file} to Large folder")
            break

    # Send every song that was downloaded
    for file in os.listdir("Audio"):
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_AUDIO)
        update.message.reply_audio(audio=open("Audio/" + file, "rb"), timeout=50)
        logger.info(f"Sent audio file {file}")
    # Delete everything in the Audio Folder
    for file in os.listdir("Audio"):
        os.remove("Audio/" + file)
        logger.info(f"Deleted audio file {file}")

def get_video(update, context):
    url = context.args[0]
    logger.info(f"User {update.message.chat.first_name} requested video from {url}")
    # Get video from link
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": "Video/%(title)s.%(ext)s"
    }
    logger.info(f"Bot requested video from {url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Check file size
    for file in os.listdir("Video"):
        if os.path.getsize("Video/" + file) > 50000000:
            context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
            update.message.reply_text("Sorry the file is too large to send :(, but I did save it in the folder")
            logger.info(f"File {file} is too large to send")
            # Move file to "Large" folder
            os.rename("Video/" + file, "Large/Video/" + file)
            logger.info(f"Moved file {file} to Large folder")
            break
    
    time.sleep(3)
    # Send every video that was downloaded
    for file in os.listdir("Video"):
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_VIDEO)
        update.message.reply_video(video=open("Video/" + file, "rb"), timeout=50)
        logger.info(f"Sent video file {file}")

    # Delete everything in the Video Folder
    for file in os.listdir("Video"):
        os.remove("Video/" + file)
        logger.info(f"Deleted video file {file}")

def error(update, context):
    logger.warning(f"{update} caused error {context.error}") 
    logger.info(f"User {update.message.chat.first_name} caused error. Error = {context.error} Type = {type(context.error)}")
    if type(context.error) == IndexError:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        update.message.reply_text("Please send a link with your command. <strong>See /help for more information</strong>", parse_mode=ParseMode.HTML)

    elif type(context.error) == yt_dlp.utils.DownloadError:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        update.message.reply_text("Sorry, the link you sent is not supported.")

    elif type(context.error) == telegram.error.NetworkError:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        update.message.reply_text("Sorry the file is too large to send :(")

    else:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        update.message.reply_text("Something went wrong. Please try again.")
    
def echo(update, context):
    logger.info(f"User {update.message.chat.first_name} sent a message")
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text("Sorry I'm really dumb. I can only understand commands and can't actually have any kind of meaningful conversation with you. /help for more info")
    
def source(update, context):
    logger.info(f"User {update.message.chat.first_name} requested source code")
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text("Check every now and then for updates: https://github.com/mascode/Telegram-AV-Archiver")

def main():
    # Updater and dispatcher.
    updater = Updater(API_Token, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_me))
    dispatcher.add_handler(CommandHandler("get_audio", get_audio, pass_args=True))
    dispatcher.add_handler(CommandHandler("get_video", get_video, pass_args=True))
    dispatcher.add_handler(CommandHandler("source", source))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_error_handler(error)
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    logger.info("Starting bot")
    main()
