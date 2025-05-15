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
    url = request.form['url']
    target_lang = request.form['language']
    return f"You entered URL: {url} and selected language: {target_lang}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host='0.0.0.0', port=port)

