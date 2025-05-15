from flask import Flask, render_template, request
import whisper
import os

app = Flask(__name__)

# Load tiny model to reduce memory usage
model = whisper.load_model("tiny")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dub', methods=["POST"])
def dub():
    if 'file' not in request.files:
        return "No file uploaded", 400

    audio = request.files['file']
    if audio.filename == '':
        return "No file selected", 400

    # Save the uploaded audio file
    filename = os.path.join("static", audio.filename)
    audio.save(filename)

    # Transcribe the audio using Whisper
    result = model.transcribe(filename)
    text = result["text"]

    return render_template("result.html", transcript=text)

if __name__ == '__main__':
    app.run(debug=True)

