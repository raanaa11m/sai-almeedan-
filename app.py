from flask import Flask, render_template, request, session, redirect, url_for
from deep_translator import GoogleTranslator

app = Flask(__name__)
app.secret_key = 'any-secret-key'  

# قائمة اللغات المدعومة
supported_languages = {
    "en": "English",
    "ar": "العربية",
    "fr": "Français",
    "es": "Español",
    "de": "Deutsch",
    "zh": "中文"
}


base_text = {
    "greeting": "Welcome!",
    "instruction": "Please select your language:",
    "button": "Submit"
}

def translate_texts(lang_code):
    if lang_code == "en":
        return base_text
    try:
        return {
            key: GoogleTranslator(source='en', target=lang_code).translate(text)
            for key, text in base_text.items()
        }
    except:
        return base_text 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_lang = request.form.get('language', 'en')
        session['lang'] = selected_lang
        return redirect(url_for('index'))

    lang = session.get('lang', 'en')
    translated_text = translate_texts(lang)

    return render_template('index.html',
                           text=translated_text,
                           lang=lang,
                           supported_languages=supported_languages)

if __name__ == '__main__':
    app.run(debug=True)
