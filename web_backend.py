from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from elevenlabs import generate, set_api_key, voices
from googletrans import Translator
import os

translator = Translator()
set_api_key("your_elevenlabs_api_key_here")

app = Flask(__name__)
CORS(app)

# Language code to full name mapping
lang_names = {
    "en": "English", "ta": "Tamil", "hi": "Hindi", "es": "Spanish",
    "fr": "French", "ja": "Japanese", "ar": "Arabic", "zh-cn": "Chinese",
    "zh-CN": "Chinese", "ko": "Korean", "de": "German", "it": "Italian",
    "pt": "Portuguese", "ru": "Russian", "tr": "Turkish", "sw": "Swahili",
    "tl": "Tagalog", "so": "Somali", "ca": "Catalan"
}

def detect_and_process(user_text, target_lang):
    """
    Detect language and translate using googletrans (handles romanized text better).
    Returns: (detected_language, original_text, translated_text, is_ascii)
    """
    try:
        # Check if text is romanized (ASCII only)
        is_ascii = all(ord(char) < 128 for char in user_text if char.strip())
        
        # Translate - googletrans auto-detects source language
        result = translator.translate(user_text, dest=target_lang)
        
        return result.src, user_text, result.text, is_ascii
    
    except Exception as e:
        return "unknown", user_text, user_text, False

@app.route('/voices', methods=['GET'])
def get_voices():
    try:
        available_voices = voices()
        voice_list = [{"name": v.name, "voice_id": v.voice_id} for v in available_voices]
        return jsonify({"voices": voice_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    user_text = data.get('text', '')
    target_lang = data.get('target_lang', 'en')
    voice_id = data.get('voice_id', 'pNInz6obpgDQGcFmaJgB')
    
    if not user_text:
        return jsonify({"error": "No text provided"}), 400
    
    try:
        detected_lang, original_text, translated_text, is_ascii = detect_and_process(user_text, target_lang)
        
        # Get full language names
        detected_lang_name = lang_names.get(detected_lang, detected_lang.upper())
        target_lang_name = lang_names.get(target_lang, target_lang.upper())
        
        audio = generate(text=translated_text, voice=voice_id, model="eleven_turbo_v2")
        
        audio_filename = "output.mp3"
        with open(audio_filename, "wb") as f:
            f.write(audio)
        
        return jsonify({
            "detected_language": detected_lang_name,
            "detected_code": detected_lang,
            "target_language": target_lang_name,
            "is_romanized": is_ascii,
            "original": original_text,
            "translated": translated_text,
            "audio_file": audio_filename
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    if os.path.exists(filename):
        return send_file(filename, mimetype='audio/mpeg')
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
