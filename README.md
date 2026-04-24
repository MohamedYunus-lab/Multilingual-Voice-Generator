# 🌍 Multilingual AI Voice Generator

An advanced text-to-speech system that converts written text into natural-sounding speech across 14+ languages with automatic translation and romanized text support.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)

## ✨ Features

- 🗣️ **High-Quality AI Voices** - Natural-sounding speech using ElevenLabs
- 🌐 **14+ Languages** - English, Spanish, French, German, Hindi, Tamil, Japanese, Chinese, and more
- 🔤 **Romanized Text Support** - Type "Namaste duniya" and it understands Hindi
- 🔄 **Real-time Translation** - Automatic translation between languages
- 🎯 **Smart Detection** - Auto-detects language (native or romanized)
- 💻 **Dual Interface** - CLI and modern web interface
- 🎤 **50+ Voices** - Choose from multiple AI voices
- 📝 **Large Text Support** - Handles 100+ word inputs

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection (for APIs)
- ElevenLabs API key ([Get it here](https://elevenlabs.io))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/MohamedYunus-lab/Multilingual-Voice-Generator.git
cd Multilingual-Voice-Generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your ElevenLabs API key in `multilingual_assistant.py` (line 13):
```python
set_api_key("your_api_key_here")
```

### Usage

**CLI Version:**
```bash
python multilingual_assistant.py
```

**Web Version:**
```bash
# Start backend server
python web_backend.py

# Open web_app.html in your browser
```

## 📖 How It Works

1. **Input:** Type text in any language (native or romanized)
2. **Detection:** System detects the source language
3. **Translation:** Text translated to your target language
4. **Generation:** ElevenLabs generates high-quality audio
5. **Output:** Audio played and saved as MP3

## 🎯 Supported Languages

| Language | Native Script | Romanized |
|----------|--------------|-----------|
| English | ✅ | ✅ |
| Spanish | ✅ | ✅ |
| French | ✅ | ✅ |
| German | ✅ | ✅ |
| Hindi | ✅ | ✅ |
| Tamil | ✅ | ✅ |
| Japanese | ✅ | ⚠️ Limited |
| Chinese | ✅ | ✅ |
| Korean | ✅ | ⚠️ Limited |
| Arabic | ✅ | ⚠️ Limited |
| Russian | ✅ | ✅ |
| Turkish | ✅ | ✅ |
| Portuguese | ✅ | ✅ |
| Italian | ✅ | ✅ |

## 💡 Examples

**Hindi (Romanized):**
```
Input: "Namaste duniya"
Output: Detects Hindi → Translates to English → "Hello world"
```

**Japanese (Native):**
```
Input: "私は東京に行きました"
Output: Detects Japanese → Translates to English → "I went to Tokyo"
```

**Large Text:**
```
Input: 100+ word paragraph in any language
Output: Full translation with natural speech
```

## 🛠️ Technology Stack

- **Python 3.11** - Core programming language
- **googletrans** - Translation and language detection
- **ElevenLabs API** - AI voice generation
- **pygame** - Audio playback
- **Flask** - Web backend
- **HTML/CSS/JS** - Web frontend

## 📁 Project Structure

```
multilingual-voice-generator/
├── multilingual_assistant.py  # CLI interface
├── web_backend.py             # Flask server
├── web_app.html               # Web interface
├── requirements.txt           # Dependencies
├── README.md                  # This file
└── output.mp3                 # Generated audio (auto-created)
```

## 🎨 Screenshots

### CLI Interface
```
Available languages:
- English
- Tamil
- Hindi
...

You: Namaste duniya
🔍 Detected: Hindi (romanized)
🌐 Translated to English: Hello world
```

### Web Interface
Modern, responsive design with:
- Real-time translation display
- Audio player with controls
- Translation history
- Voice selection dropdown

## 🔧 Configuration

### Change Voice
In CLI: Type `switch voice` and select from available voices

In Web: Use the voice dropdown menu

### Change Target Language
In CLI: Type `switch language` and select your language

In Web: Use the language dropdown menu

## 🐛 Troubleshooting

**Issue: "Translation failed"**
- Check internet connection
- Verify API key is correct

**Issue: "Permission denied: output.mp3"**
- Close any media players using the file
- Restart the program

**Issue: Romanized Japanese not translating well**
- Use native script (ひらがな/漢字) for best results
- Google Translate has limitations with romaji

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ElevenLabs](https://elevenlabs.io) for amazing voice generation API
- [Google Translate](https://translate.google.com) for translation services
- [pygame](https://www.pygame.org) for audio playback

## 📧 Contact

MOHAMED YUNUS ALI F - [yunusalimohamed734@gmail.com]

Project Link: [https://github.com/MohamedYunus-lab/Multilingual-Voice-Generator]
(https://github.com/MohamedYunus-lab/Multilingual-Voice-Generator)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Made with ❤️ using Python and AI**
