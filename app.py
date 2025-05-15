from flask import Flask, render_template, request
import os

app = Flask(__name__)

# ✅ 20 languages list
languages = [
    "Hindi", "Telugu", "Tamil", "Kannada", "Malayalam",
    "Marathi", "Gujarati", "Bengali", "Punjabi", "Odia",
    "English", "Spanish", "French", "German", "Arabic",
    "Japanese", "Korean", "Russian", "Chinese", "Portuguese"
]

@app.route('/')
def index():
    # ✅ Pass languages to HTML
    return render_template('index.html', languages=languages)

@app.route('/process', methods=['POST'])
def process():
    url = request.form['youtube_url']
    language = request.form['language']

    # Log input
    print(f"URL: {url}, Language: {language}")

    try:
        # Download audio using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return f"✅ Audio downloaded for {url} in MP3 format!"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

