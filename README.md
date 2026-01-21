# WhatsApp Auto-Reply Bot

An intelligent Python bot that monitors WhatsApp Desktop and automatically sends contextual replies to any message using Google's Gemini AI.

## 🚀 Features

* **Smart Detection**: Uses Gemini Vision AI to understand any message type
* **Contextual Replies**: Generates intelligent, relevant responses
* **Spam Prevention**: Built-in rate limiting and cooldown system
* **Customizable Personality**: Make the bot witty, helpful, sarcastic, or professional
* **Full Window Capture**: Automatically detects messages from entire WhatsApp window

## Setup

1. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Get a Google Gemini API key:
   * Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   * Create an API key

3. Create a `.env` file in the project root:

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and add your API key:

   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

4. Run the bot:

   ```bash
   python smart_bot.py
   ```

### ✅ Verify Setup

Run the setup checker to ensure everything is configured:

```bash
python check_setup.py
```

This will verify:
* All dependencies are installed
* `.env` file has valid API key
* WhatsApp Desktop is running
* Gemini API connection works

## 🎯 Quick Start

```bash
python smart_bot.py
```

The bot will automatically:
* Capture the full WhatsApp window
* Detect new messages using AI
* Generate and send intelligent replies
* Track message history to avoid spam

## 🎨 Customization

### Change Bot Personality

Edit `smart_bot.py` to customize response style:

```python
BOT_PERSONALITY = """
You are a witty, sarcastic friend.
Keep responses under 15 words.
"""
```

### Adjust Behavior

```python
REPLY_COOLDOWN = 300      # Wait 5 min before replying to same message
SCAN_INTERVAL = 20        # Check every 20 seconds
MAX_REPLIES_PER_HOUR = 10 # Prevent spam
```

For more customization options, edit the `BOT_PERSONALITY`, `REPLY_COOLDOWN`, `SCAN_INTERVAL`, and other settings in [smart_bot.py](smart_bot.py).

## ⚠️ Important Notes

* Works only on WhatsApp Desktop (Windows)
* Requires active WhatsApp window
* Uses Google Gemini API (free tier available)
* Be mindful of rate limits to avoid spam detection
* Test in private chats first before using in groups

## 🛡️ Best Practices

1. Keep `DEBUG_MODE = True` initially to verify bot behavior (screenshots saved in `debug/` folder)
2. Start with conservative rate limits (default: 10 replies/hour)
3. Test in private chats before using in groups
4. Monitor API quota usage (free tier: ~20 requests/day for gemini-2.5-flash)
5. Adjust `SCAN_INTERVAL` based on your needs (default: 20 seconds)

---
