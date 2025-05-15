from flask import Flask, render_template, request

app = Flask(__name__)

# 20 languages (10 Indian + 10 International)
languages = {
    'Hindi': 'hi',
    'Telugu': 'te',
    'Tamil': 'ta',
    'Kannada': 'kn',
    'Malayalam': 'ml',
    'Marathi': 'mr',
    'Gujarati': 'gu',
    'Bengali': 'bn',
    'Punjabi': 'pa',
    'Odia': 'or',
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Japanese': 'ja',
    'Chinese (Simplified)': 'zh',
    'Arabic': 'ar',
    'Russian': 'ru',
    'Portuguese': 'pt',
    'Korean': 'ko'
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        language = request.form.get("language")
        print(f"YouTube URL: {youtube_url}, Language: {language}")
    return render_template("index.html", languages=languages)

if __name__ == "__main__":
    app.run(debug=True)

