from flask import Flask, render_template, request
import os
import yt_dlp
import uuid
import whisper
import edge_tts
import asyncio

app = Flask(__name__)

whisper_model = whisper.load_model("base")

LANGUAGE_CODES = {
    "Hindi": "hi", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Malayalam": "ml",
    "Gujarati": "gu", "Bengali": "bn", "Marathi": "mr", "Punjabi": "pa", "Urdu": "ur",
    "English": "en", "Spanish": "es", "French": "fr", "German": "de", "Chinese": "zh",
    "Japanese": "ja", "Korean": "ko", "Russian": "ru", "Portuguese": "pt", "Arabic": "ar"
}

# Gender detection: simple pronoun heuristic
def detect_gender(text):
    text = text.lower()
    male = text.count(" he ") + text.count(" his ") + text.count(" him ")
    female = text.count(" she ") + text.count(" her ") + text.count(" hers ")
    return "male" if male >= female else "female"

async def generate_edge_tts(text, lang_code, gender, output_path):
    if gender == "male":
        voice = f"{lang_code}-IN-MohanNeural"
    else:
        voice = f"{lang_code}-IN-SwaraNeural"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

@app.route('/')
def home():
    return render_template('index.html', languages=LANGUAGE_CODES)

@app.route('/translate', methods=['POST'])
def translate():
    youtube_url = request.form['youtube_url']
    lang_name = request.form['language']
    lang_code = LANGUAGE_CODES.get(lang_name)
    if not lang_code:
        return "Invalid language."

    uid = str(uuid.uuid4())
    audio_path = f"static/audio_{uid}"
    dubbed_path = f"static/dubbed_{uid}.mp3"

    try:
        # Download YouTube audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': audio_path,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        full_audio_path = audio_path + ".mp3"
        if not os.path.exists(full_audio_path):
            raise Exception("Audio download failed.")

        # Transcribe
        result = whisper_model.transcribe(full_audio_path, fp16=False, condition_on_previous_text=False, verbose=True)
        full_text = result['text']
        gender = detect_gender(full_text)

        # Generate dubbed audio
        asyncio.run(generate_edge_tts(full_text, lang_code, gender, dubbed_path))

        return render_template("result.html",
                               audio_file=dubbed_path,
                               youtube_url=youtube_url,
                               languages=LANGUAGE_CODES)

    except Exception as e:
        return f"Error: {e}"

