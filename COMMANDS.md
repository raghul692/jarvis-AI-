

# JARVIS AI Assistant - Commands Reference

## Voice Commands

### Wake Word
- **"JARVIS"** or **"hey JARVIS"** - Activates JARVIS listening mode

### Time & Date
- **"What time is it?"** - Tells current time
- **"What's the date?"** - Tells today's date

### System Information
- **"System status"** - Reports CPU, memory, disk, battery usage
- **"CPU usage"** - Shows CPU percentage
- **"Memory usage"** - Shows RAM usage
- **"Battery status"** - Shows battery level and charging status

### Weather
- **"Weather"** - Shows weather for default location
- **"Weather in [city]"** - Shows weather for specified city

### News
- **"News"** - Gets latest general news headlines
- **"Tech news"** - Gets latest technology news

### Web Search
- **"Search for [query]"** - Performs web search
- **"Search [query]"** - Alternative search command

### YouTube
- **"Play [video] on YouTube"** - Searches and plays video on YouTube
- **"Play [song] on YouTube"** - Plays music video

### Definitions
- **"Define [word]"** - Gets definition of a word
- **"Meaning of [word]"** - Alternative definition command

### Wolfram Alpha / Questions
- **"What is [something]?"** - Answers factual questions
- **"Who is [person]?"** - Gets information about a person
- **"How many [something]?"** - Answers quantitative questions
- **"Calculate [math problem]"** - Solves math problems

### AI Conversation
When OpenAI API is configured, JARVIS can:
- Answer general questions
- Have natural conversations
- Help with coding
- Provide explanations
- Discuss topics
- Give recommendations

---

## Text Mode Commands

Run JARVIS with `--text` flag for interactive text mode:

```bash
python main.py --text
```

### Text Commands
- Type any command naturally
- **"exit"** - Quit the program
- **"voice"** - Switch to voice mode
- Any voice command also works in text mode

---

## Example Conversations

### Basic Interaction
```
User: "JARVIS"
JARVIS: "Yes, sir?"
User: "What time is it?"
JARVIS: "The current time is 03:45 PM."

User: "JARVIS"
JARVIS: "Yes, sir?"
User: "System status"
JARVIS: "CPU usage is 45 percent. Memory is at 60 percent. Disk usage is 75 percent."
```

### Web Queries
```
User: "JARVIS"
JARVIS: "Yes, sir?"
User: "Search for Python tutorials"
JARVIS: "Searching the web for 'Python tutorials'"

User: "JARVIS"
JARVIS: "Yes, sir?"
User: "Weather in London"
JARVIS: "Weather in London: clear sky. Temperature: 15°C. Humidity: 65%."
```

### AI Conversation (with OpenAI API)
```
User: "JARVIS"
JARVIS: "Yes, sir?"
User: "Tell me about machine learning"
JARVIS: "Machine learning is a subset of artificial intelligence..."
```

---

## Configuration Commands

### Edit `config.yaml` to customize:

```yaml
assistant:
  name: "JARVIS"              # Change assistant name
  wake_word: "jarvis"         # Change wake word

tts:
  use_edge: true              # Enable neural voices
  edge_voice: "en-US-GuyNeural"  # Change voice

ai:
  model: "gpt-4"              # Use GPT-4 if available
```

---

## API Keys Required

For full functionality, add these to your `.env` file:

| Service | Purpose | Get Key At |
|---------|---------|------------|
| OPENAI_API_KEY | AI Conversation | platform.openai.com |
| OPENWEATHER_API_KEY | Weather | openweathermap.org |
| NEWS_API_KEY | News Headlines | newsapi.org |
| WOLFRAM_API_KEY | Computations | wolframalpha.com |

---

## Quick Command Reference Card

| Category | Commands |
|----------|----------|
| **Activation** | "JARVIS", "hey JARVIS" |
| **Time** | "what time", "time now" |
| **Date** | "what date", "today's date" |
| **System** | "system status", "cpu", "memory", "battery" |
| **Weather** | "weather", "weather in [city]" |
| **News** | "news", "tech news" |
| **Search** | "search for [query]" |
| **YouTube** | "play [video] on YouTube" |
| **Define** | "define [word]", "meaning of [word]" |
| **Questions** | "what is", "who is", "calculate" |
| **Help** | "help", "what can you do" |

---

## Troubleshooting

- **No microphone detected**: Check Windows microphone permissions
- **JARVIS not responding**: Say "JARVIS" clearly, reduce background noise
- **Speech not recognized**: Check microphone placement and volume
- **API errors**: Verify API keys in `.env` file
- **Text-to-speech issues**: Try different TTS engine in config
