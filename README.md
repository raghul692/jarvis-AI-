# 🤖 JARVIS AI Assistant

> **Advanced Voice-Powered AI Assistant with Speech Recognition and Natural Language Processing**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

JARVIS is a sophisticated AI assistant inspired by the Tony Stark AI from Marvel, designed to provide seamless voice-controlled automation and intelligent responses. This project integrates cutting-edge technologies for speech recognition, text-to-speech synthesis, and AI-powered conversation capabilities.

---

## 🌟 Features

### 🎤 Voice Interaction
- **Wake Word Detection**: Responds to "JARVIS" or custom wake words
- **Speech Recognition**: Supports Google, Whisper, and Sphinx engines
- **Text-to-Speech**: Multiple TTS engines (pyttsx3, Google TTS, Microsoft Edge Neural)
- **Natural Voice Output**: High-quality neural voice synthesis

### 🧠 AI Capabilities
- **OpenAI Integration**: GPT-3.5-turbo and GPT-4 support for intelligent conversations
- **Natural Language Processing**: Understands and responds to complex queries
- **Context-Aware Responses**: Maintains conversation context and provides relevant answers

### 📊 System Control
- **System Monitoring**: Real-time CPU, memory, disk, and battery status
- **System Information**: Retrieve detailed system statistics
- **Process Management**: Monitor system performance

### 🌐 Web Integration
- **Weather Information**: Real-time weather data from OpenWeatherMap
- **News Headlines**: Latest news from NewsAPI
- **Web Search**: Comprehensive internet search capability
- **YouTube Integration**: Search and play YouTube videos
- **Definition Lookup**: Word definitions and meanings
- **Wolfram Alpha**: Advanced calculations and factual queries

### 💬 Interaction Modes
- **Voice Mode**: Full voice-controlled interaction
- **Text Mode**: Interactive text-based interface for testing
- **Hybrid Mode**: Seamless switching between voice and text

### ⚙️ Configuration
- **YAML Configuration**: Easy customization via config.yaml
- **Environment Variables**: Secure API key management
- **Multi-Engine Support**: Choose your preferred engines for each component
- **Customizable Wake Words**: Set custom activation phrases

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8 or higher**
- **Microphone** (for voice input)
- **Speaker** (for voice output)
- **Internet Connection** (for web services)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/raghul692/jarvis-AI-.git
   cd jarvis-AI-
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_key_here
   OPENWEATHER_API_KEY=your_openweather_key_here
   NEWS_API_KEY=your_newsapi_key_here
   WOLFRAM_API_KEY=your_wolfram_key_here
   ```

5. **Run JARVIS**
   ```bash
   # Voice Mode (default)
   python main.py
   
   # Text Mode (for testing)
   python main.py --text
   ```

---

## 📋 Commands Reference

### 🎯 Basic Commands

| Category | Commands |
|----------|----------|
| **Activation** | "JARVIS", "hey JARVIS" |
| **Time** | "what time is it?", "current time" |
| **Date** | "what's the date?", "today's date" |
| **Help** | "help", "what can you do?" |

### 📱 System Status

```bash
"System status"        # Full system statistics
"CPU usage"            # CPU percentage
"Memory usage"         # RAM usage
"Battery status"       # Battery level and charging
```

### 🌤️ Weather

```bash
"Weather"              # Default location weather
"Weather in London"    # Weather for specific city
"Weather in New York"  # Any location
```

### 📰 News

```bash
"News"                 # Latest general news
"Tech news"            # Technology headlines
"Business news"        # Business updates
```

### 🔍 Search & Web

```bash
"Search for Python tutorials"
"Search quantum computing"
"Define algorithm"
"Meaning of artificial intelligence"
```

### 📺 YouTube

```bash
"Play Avengers on YouTube"
"Play lo-fi beats on YouTube"
```

### 🧮 Questions & Calculations

```bash
"What is quantum computing?"
"Who is Steve Jobs?"
"Calculate 2+2"
"How many seconds in an hour?"
```

### 💬 AI Conversation (with OpenAI API)

```bash
"Tell me about machine learning"
"Help me debug this code"
"Explain quantum physics"
```

### 🎛️ Control Commands (Text Mode)

```
"exit"     # Exit the program
"voice"    # Switch to voice mode
```

---

## ⚙️ Configuration

### Edit `config.yaml` to customize JARVIS

#### Assistant Settings
```yaml
assistant:
  name: "JARVIS"           # Change assistant name
  wake_word: "jarvis"      # Custom wake word
  voice_rate: 175          # Speech speed (higher = faster)
  voice_volume: 1.0        # Output volume (0.0-1.0)
```

#### Speech Recognition
```yaml
speech:
  recognizer: "google"     # google, whisper, sphinx
  language: "en-US"        # Language code
  ambient_noise_adjustment: true
  timeout: 5               # Listen timeout in seconds
```

#### Text-to-Speech
```yaml
tts:
  engine: "pyttsx3"        # pyttsx3, gtts, edge
  use_edge: true           # Microsoft Edge neural voices
  edge_voice: "en-US-GuyNeural"  # Voice selection
```

#### AI Configuration
```yaml
ai:
  provider: "openai"       # openai, anthropic, local
  model: "gpt-3.5-turbo"   # gpt-3.5-turbo or gpt-4
  max_tokens: 500          # Response length
  temperature: 0.7         # Creativity (0.0-1.0)
```

#### Web Services
```yaml
services:
  weather:
    provider: "openweathermap"
    default_location: "New York"
  news:
    provider: "newsapi"
    country: "us"
  wolfram:
    # Advanced calculations and queries
```

---

## 📦 Dependencies

### Core Libraries

| Package | Purpose | Version |
|---------|---------|---------|
| **speechrecognition** | Speech-to-text | ≥3.10.0 |
| **pyttsx3** | Text-to-speech | ≥2.90 |
| **edge-tts** | Neural voice synthesis | ≥6.1.0 |
| **gTTS** | Google text-to-speech | ≥2.4.0 |
| **openai-whisper** | Advanced speech recognition | ≥20231106 |
| **openai** | GPT API integration | ≥1.0.0 |
| **wolframalpha** | Computational knowledge | ≥5.0.0 |
| **psutil** | System monitoring | ≥5.9.0 |
| **requests** | HTTP requests | ≥2.31.0 |
| **beautifulsoup4** | Web scraping | ≥4.12.0 |
| **PyYAML** | Config file parsing | ≥6.0 |
| **python-dotenv** | Environment variables | ≥1.0.0 |

---

## 🔑 API Keys Setup

### Required for Full Functionality

#### 🔓 OpenAI API
- **Purpose**: AI conversation capabilities
- **Get Key**: https://platform.openai.com/api-keys
- **Cost**: Pay-per-use (starting $0.002 per 1K tokens)

#### 🌡️ OpenWeatherMap API
- **Purpose**: Weather information
- **Get Key**: https://openweathermap.org/api
- **Cost**: Free tier available

#### 📰 NewsAPI
- **Purpose**: News headlines
- **Get Key**: https://newsapi.org
- **Cost**: Free tier available

#### 🧮 Wolfram Alpha API
- **Purpose**: Computations and queries
- **Get Key**: https://www.wolframalpha.com/portal/developer
- **Cost**: Free tier available

---

## 📂 Project Structure

```
jarvis-AI-/
├── main.py                    # Main entry point
├── config.yaml                # Configuration file
├── requirements.txt           # Python dependencies
├── COMMANDS.md                # Commands reference
├── README.md                  # This file
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
│
├── jarvis/                    # Main package directory
│   ├── __init__.py
│   ├── config_loader.py       # Config file loader
│   ├── speech_engine.py       # Speech recognition & TTS
│   ├── conversation.py        # AI conversation module
│   └── services.py            # Web services & system control
│
└── jarvis_core/               # Core modules
    ├── __init__.py
    ├── config_loader.py       # Configuration management
    ├── speech_engine.py       # Speech processing
    ├── conversation.py        # AI responses
    └── services.py            # External services
```

---

## 🎯 Usage Examples

### Example 1: Weather Check
```
User: "JARVIS"
JARVIS: "Yes, sir?"
User: "Weather in Mumbai"
JARVIS: "Weather in Mumbai: Clear sky. Temperature: 32°C. Humidity: 65%."
```

### Example 2: System Status
```
User: "JARVIS"
JARVIS: "Yes, sir?"
User: "System status"
JARVIS: "CPU usage is 45 percent. Memory is at 60 percent. Disk usage is 75 percent."
```

### Example 3: Web Search
```
User: "JARVIS"
JARVIS: "Yes, sir?"
User: "Search for Python best practices"
JARVIS: "Searching the web for 'Python best practices'..."
```

### Example 4: AI Conversation
```
User: "JARVIS"
JARVIS: "Yes, sir?"
User: "Explain machine learning"
JARVIS: "Machine learning is a subset of artificial intelligence that 
enables systems to learn and improve from experience..."
```

---

## 🛠️ Troubleshooting

### Common Issues

#### ❌ Microphone Not Detected
- **Solution**: Check Windows microphone permissions in Settings > Privacy > Microphone
- Ensure microphone is properly connected
- Test microphone in Windows Sound Settings

#### ❌ JARVIS Not Responding to Wake Word
- **Solution**: Speak clearly and reduce background noise
- Check `speech.timeout` in config.yaml
- Ensure microphone volume is adequate

#### ❌ Speech Recognition Errors
- **Solution**: Improve audio quality and reduce background noise
- Try different recognizer in config (google, whisper, sphinx)
- Check internet connection for Google recognizer

#### ❌ API Errors
- **Solution**: Verify all API keys are correct in .env file
- Check API rate limits haven't been exceeded
- Ensure internet connectivity

#### ❌ Text-to-Speech Issues
- **Solution**: Try different TTS engine (pyttsx3, gtts, edge)
- Check audio output device is working
- Reinstall audio dependencies

#### ❌ Import Errors
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.8 or higher
- Check virtual environment is activated

---

## 🚀 Advanced Features

### Custom Wake Words
Edit `config.yaml`:
```yaml
assistant:
  wake_word: "computer"  # Change to your preference
```

### Voice Customization
```yaml
tts:
  edge_voice: "en-US-AriaNeural"  # Different voice
  # Other options: GuyNeural, JennyNeural, etc.
```

### Model Selection
```yaml
ai:
  model: "gpt-4"  # Upgrade to GPT-4 for better responses
```

### Logging
Monitor JARVIS activity in `jarvis.log`:
```bash
# View log file
tail -f jarvis.log
```

---

## 📚 Additional Resources

- **Speech Recognition Docs**: https://github.com/Uberi/speech_recognition
- **OpenAI API**: https://platform.openai.com/docs
- **pyttsx3 Documentation**: https://pyttsx3.readthedocs.io
- **Wolfram Alpha**: https://www.wolframalpha.com/input

---

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## ⭐ Acknowledgments

- Inspired by JARVIS AI from Marvel's Iron Man
- Built with Python and open-source libraries
- Special thanks to the speech recognition and NLP communities

---

## 📞 Support

For issues, questions, or feature requests:
- Open an [Issue](https://github.com/raghul692/jarvis-AI-/issues)
- Start a [Discussion](https://github.com/raghul692/jarvis-AI-/discussions)
- Check existing [Documentation](https://github.com/raghul692/jarvis-AI-/wiki)

---

## 🔗 Links

- **Repository**: https://github.com/raghul692/jarvis-AI-
- **Commands Reference**: [COMMANDS.md](COMMANDS.md)
- **Author**: [@raghul692](https://github.com/raghul692)

---

**Made with ❤️ by Raghul692**

*"Sir, I'm always at your service."* - JARVIS
