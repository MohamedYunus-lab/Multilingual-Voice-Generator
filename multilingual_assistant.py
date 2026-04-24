import pygame
from elevenlabs import generate, set_api_key, voices
from googletrans import Translator
import time
import os

# Initialize translator
translator = Translator()

set_api_key("your_elevenlabs_api_key_here")
pygame.mixer.init()

languages = {
    "english": "en",
    "tamil": "ta",
    "hindi": "hi",
    "spanish": "es",
    "french": "fr",
    "japanese": "ja",
    "arabic": "ar",
    "chinese": "zh-cn",
    "korean": "ko",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "russian": "ru",
    "turkish": "tr"
}

# Language code to full name mapping
lang_names = {
    "en": "English", "ta": "Tamil", "hi": "Hindi", "es": "Spanish",
    "fr": "French", "ja": "Japanese", "ar": "Arabic", "zh-cn": "Chinese",
    "zh-CN": "Chinese", "ko": "Korean", "de": "German", "it": "Italian",
    "pt": "Portuguese", "ru": "Russian", "tr": "Turkish", "sw": "Swahili",
    "tl": "Tagalog", "so": "Somali", "ca": "Catalan", "mixed": "Mixed Languages"
}

def choose_language():
    print("Available languages:")
    for lang in languages.keys():
        print("-", lang.capitalize())
    lang = input("Which language do you want me to speak? ").strip().lower()
    if lang not in languages:
        print("Language not recognized, defaulting to English.")
        lang = "english"
    return lang, languages[lang]

def choose_voice():
    print("\nFetching available ElevenLabs voices...")
    available_voices = voices()
    
    print("\nAvailable voices:")
    for i, v in enumerate(available_voices, 1):
        print(f"{i}. {v.name}")
    
    voice_input = input("\nEnter voice name or number: ").strip()
    
    # Try by number first
    if voice_input.isdigit():
        idx = int(voice_input) - 1
        if 0 <= idx < len(available_voices):
            selected_voice = available_voices[idx]
            print(f"✓ Selected: {selected_voice.name}")
            return selected_voice.voice_id
    
    # Try by name (case-insensitive partial match)
    voice_input_lower = voice_input.lower()
    for v in available_voices:
        if voice_input_lower in v.name.lower():
            print(f"✓ Selected: {v.name}")
            return v.voice_id
    
    print(f"✗ Voice '{voice_input}' not found, defaulting to {available_voices[0].name}")
    return available_voices[0].voice_id

def detect_romanized_language(text):
    """
    Try to detect which language romanized text might be from
    Returns language code or None
    """
    text_lower = text.lower()
    words = text_lower.split()
    
    # Japanese romanization patterns (more specific)
    japanese_patterns = [
        'watashi', 'anata', 'desu', 'masu', 'arigatou', 'gozaimasu',
        'konnichiwa', 'sayonara', 'ohayou', 'sumimasen', 'kudasai',
        'onegai', 'ikimashita', 'shimasu', 'tabemasu', 'nomimasu',
        'ikimasu', 'kimasu', 'imasu', 'arimasu', 'tomodachi', 'sensei'
    ]
    
    # Chinese pinyin patterns (more specific)
    chinese_patterns = [
        'nihao', 'xiexie', 'zaijian', 'duibuqi', 'qing', 'xihuan',
        'xuesheng', 'laoshi', 'pengyou', 'mingtian', 'jintian', 'zuotian',
        'zhongwen', 'yingwen', 'beijing', 'shanghai'
    ]
    
    # Korean romanization patterns
    korean_patterns = [
        'annyeong', 'haseyo', 'kamsahamnida', 'mianhae', 'saranghae',
        'joesonghamnida', 'gamsahamnida', 'yeoboseyo', 'juseyo'
    ]
    
    # Turkish patterns
    turkish_patterns = [
        'merhaba', 'günaydın', 'teşekkür', 'lütfen', 'dünya', 'nasılsın'
    ]
    
    # Arabic romanization patterns
    arabic_patterns = [
        'marhaba', 'shukran', 'afwan', 'sabah', 'masa', 'kayfa', 'halak'
    ]
    
    # Count matches
    jp_count = sum(1 for pattern in japanese_patterns if pattern in text_lower)
    cn_count = sum(1 for pattern in chinese_patterns if pattern in text_lower)
    ko_count = sum(1 for pattern in korean_patterns if pattern in text_lower)
    tr_count = sum(1 for pattern in turkish_patterns if pattern in text_lower)
    ar_count = sum(1 for pattern in arabic_patterns if pattern in text_lower)
    
    # Special check for Japanese: look for common verb endings
    if any(word.endswith(('masu', 'mashita', 'masen', 'desu', 'deshita')) for word in words):
        jp_count += 3  # Strong indicator
    
    # Special check for Chinese: look for pinyin tone markers or common words
    if any(word in ['wo', 'ni', 'ta', 'shi', 'you', 'de'] for word in words):
        cn_count += 1
    
    # Return language with most matches
    counts = {'ja': jp_count, 'zh-cn': cn_count, 'ko': ko_count, 'tr': tr_count, 'ar': ar_count}
    max_lang = max(counts, key=counts.get)
    
    if counts[max_lang] > 0:
        return max_lang
    
    return None

def detect_and_process(user_text, target_lang):
    """
    Detect language and translate using googletrans (handles romanized text better).
    Handles multi-language input and large text by retrying with chunks if needed.
    Now includes smart romanized language detection!
    Returns: (detected_language, original_text, translated_text, is_ascii)
    """
    try:
        # Check if text is romanized (ASCII only)
        is_ascii = all(ord(char) < 128 for char in user_text if char.strip())
        
        # If romanized, try to detect which language it might be
        forced_source = None
        if is_ascii:
            forced_source = detect_romanized_language(user_text)
        
        # Try translation with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Try with forced source language if detected
                if forced_source:
                    result = translator.translate(user_text, src=forced_source, dest=target_lang)
                else:
                    result = translator.translate(user_text, dest=target_lang)
                
                # Check if translation actually happened (not just echoed back)
                if result.text.strip() and result.text != user_text:
                    detected_lang = forced_source if forced_source else result.src
                    
                    # If detected language is unknown/weird, mark as mixed
                    if detected_lang in ['unknown', 'bm', 'so', 'hmn', 'ny']:
                        detected_lang = "mixed"
                    
                    return detected_lang, user_text, result.text, is_ascii
                else:
                    # Translation failed, retry
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(0.5)
                        continue
                    else:
                        # Last attempt failed, return as-is
                        return "unknown", user_text, user_text, is_ascii
                        
            except Exception as e:
                if attempt < max_retries - 1:
                    import time
                    time.sleep(0.5)
                    continue
                else:
                    raise e
        
        return "unknown", user_text, user_text, is_ascii
    
    except Exception as e:
        print(f"⚠️ Translation error: {e}")
        return "unknown", user_text, user_text, False

language, target_lang = choose_language()
VOICE_ID = choose_voice()
last_filename = "output.mp3"

print("\n✨ Assistant ready! Type 'exit' to quit, 'repeat' to replay, 'switch language' or 'switch voice' to change settings.")
print("💡 Tips:")
print("   - For best translation: Use native script (日本語, தமிழ், العربية, 中文)")
print("   - Romanized works well for: Hindi, Tamil, Spanish, French")
print("   - Romanized may fail for: Japanese, Chinese, Korean, Arabic\n")

while True:
    user_text = input("You: ")
    if user_text.lower() == "exit":
        break
    
    if user_text.lower() == "repeat":
        if os.path.exists(last_filename):
            pygame.mixer.music.load(last_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
        else:
            print("No audio to repeat.")
        continue
    
    if user_text.lower() == "switch language":
        language, target_lang = choose_language()
        continue
    
    if user_text.lower() == "switch voice":
        VOICE_ID = choose_voice()
        continue
    
    # Detect and translate
    detected_lang, original_text, translated_text, is_ascii = detect_and_process(user_text, target_lang)
    
    # Get full language names
    detected_lang_name = lang_names.get(detected_lang, detected_lang.upper())
    target_lang_name = lang_names.get(target_lang, language.capitalize())
    
    print(f"🔍 Detected: {detected_lang_name} {'(romanized)' if is_ascii else ''}")
    print(f"🌐 Translated to {target_lang_name}: {translated_text}")
    
    # Clean text for natural speech (remove issues that make it sound robotic)
    speech_text = translated_text
    # Fix common punctuation issues
    speech_text = speech_text.replace('.', '. ')  # Ensure space after period
    speech_text = speech_text.replace('..', '.')  # Remove double periods
    speech_text = speech_text.replace('  ', ' ')  # Remove double spaces
    speech_text = speech_text.replace(' .', '.')  # Remove space before period
    speech_text = speech_text.strip()  # Remove leading/trailing spaces
    
    # Generate audio - completely quit mixer to release file lock
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    time.sleep(0.2)
    
    audio = generate(text=speech_text, voice=VOICE_ID, model="eleven_turbo_v2")
    with open(last_filename, "wb") as f:
        f.write(audio)
    
    # Reinitialize mixer and play
    pygame.mixer.init()
    pygame.mixer.music.load(last_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
