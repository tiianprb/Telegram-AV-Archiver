# Telegraudio

Self hosted Telegram bot to download audio and video from [supported sites](https://www.github.com/yt-dlp/yt-dlp/blob/master/supportedsites.html)



Commands:

- /start - Start the bot

- /help - Get help and informations

- /get_audio - Downloads audio from a given site in mp3 format

- /get_video - Downloads video from a given site in mp4 format

- /source - Get the source code for the bot



Limitations: 

- Telegram's Bot API has a [50MB limit](https://core.telegram.org/bots/faq#how-do-i-upload-a-large-file) for audio and video files. So this bot will not work on large video or audio files



Setup

1. Make a new bot with [@botfather](https://www.t.me/botfather) and grab the API Key
2. Rename .env-example to .env and put the API key in the `API_Token` variable
3. Install requirements via `pip install -r requirements.txt`in your virtual environment 
4. Run `bot.py`



Deploy on Heroku:

- Connect repository to account either through Heroku CLI or github

- Add ffmpeg https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git to your buildpacks

- In Config Vars add a new Key (API_Token) and Value (Your API Key)

- Deploy
