"""
Smart WhatsApp Auto-Reply Bot with Gemini AI
Automatically detects and replies to any type of message with intelligent, contextual responses
"""

import os
import time
import hashlib
import pyautogui
import pygetwindow as gw
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image, ImageOps
from datetime import datetime
import json

load_dotenv()

# WhatsApp Window Settings
WHATSAPP_WINDOW_TITLE = "WhatsApp"
print("[✓] Bot will capture the entire WhatsApp window for better message detection")

# Gemini AI Settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in .env file")

# Bot Behavior Settings
REPLY_COOLDOWN = 300  # 5 minutes between replies to similar messages
SCAN_INTERVAL = 20    # Check every 20 seconds
MAX_REPLIES_PER_HOUR = 10  # Prevent spam
DEBUG_MODE = True     # Save screenshots for debugging

# Response Personality (customize this!)
BOT_PERSONALITY = """
You are a friendly, witty friend who gives clever automated replies.
Keep responses SHORT (1-2 sentences max), casual, and sometimes sarcastic.
Use emojis occasionally but don't overdo it.
"""

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
vision_model = genai.GenerativeModel("models/gemini-2.5-flash")

# Message tracking
message_history = {}
reply_counter = {"count": 0, "reset_time": time.time()}


def focus_whatsapp():
    """Brings WhatsApp window to focus"""
    try:
        wins = gw.getWindowsWithTitle(WHATSAPP_WINDOW_TITLE)
        if not wins:
            print("[!] WhatsApp window not found")
            return False
        
        win = wins[0]
        if win.isMinimized:
            win.restore()
        win.activate()
        time.sleep(1)
        return True
    except Exception as e:
        print(f"[!] Window focus error: {e}")
        return False


def get_chat_image():
    """Captures the full WhatsApp window screenshot"""
    try:
        # Get WhatsApp window
        wins = gw.getWindowsWithTitle(WHATSAPP_WINDOW_TITLE)
        if not wins:
            print("[!] WhatsApp window not found")
            return None
        
        win = wins[0]
        # Capture the entire WhatsApp window
        img = pyautogui.screenshot(region=(win.left, win.top, win.width, win.height))
        img = ImageOps.exif_transpose(img)
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        # Save debug screenshot
        if DEBUG_MODE:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            debug_path = f"debug/chat_{timestamp}.png"
            os.makedirs("debug", exist_ok=True)
            img.save(debug_path)
        
        return img
    except Exception as e:
        print(f"[!] Screenshot error: {e}")
        return None


def generate_image_hash(img):
    """Generates hash to detect duplicate messages"""
    return hashlib.md5(img.tobytes()).hexdigest()


def analyze_message_and_generate_reply(img):
    """
    Uses Gemini Vision to:
    1. Detect if there's a new message
    2. Extract the message content
    3. Generate an appropriate reply
    """
    try:
        prompt = f"""{BOT_PERSONALITY}

Analyze this WhatsApp chat screenshot. 

Task:
1. Check if there's a recent message that needs a reply (look at the LAST message in the chat)
2. If yes, read the message content
3. Generate a SHORT, witty, contextual reply

Response format (JSON):
{{
    "should_reply": true/false,
    "message_detected": "the actual message you see",
    "reply": "your witty response here"
}}

Important rules:
- Only reply to the MOST RECENT message
- If it's just a casual "hi/hello", make it funny
- If it's "good morning", be creative (not boring)
- If it's a question, give a clever answer
- If it's spam/repeated, acknowledge it sarcastically
- Keep replies under 20 words
- Return ONLY valid JSON, no other text
"""
        
        response = vision_model.generate_content(
            [prompt, img],
            generation_config={"temperature": 0.7}
        )
        
        result = response.text.strip()
        
        # Try to extract JSON even if there's extra text
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        elif "```" in result:
            result = result.split("```")[1].split("```")[0].strip()
        
        data = json.loads(result)
        
        print(f"[AI] Detected: {data.get('message_detected', 'N/A')}")
        print(f"[AI] Should reply: {data.get('should_reply', False)}")
        
        return data
        
    except json.JSONDecodeError as e:
        print(f"[!] JSON parsing error: {e}")
        print(f"[!] Raw response: {result}")
        return {"should_reply": False, "message_detected": "", "reply": ""}
    except Exception as e:
        print(f"[!] Gemini error: {e}")
        return {"should_reply": False, "message_detected": "", "reply": ""}


def click_on_chat_area_and_input():
    """Clicks on the message area and navigates to input box - simpler, more reliable approach"""
    try:
        wins = gw.getWindowsWithTitle(WHATSAPP_WINDOW_TITLE)
        if not wins:
            return False
        
        win = wins[0]
        
        # Click on the right side of WhatsApp (where messages are displayed)
        # This ensures we're focused on the active chat
        chat_area_x = win.left + int(win.width * 0.65)  # Right side, middle
        chat_area_y = win.top + int(win.height * 0.5)   # Vertical center
        
        pyautogui.click(chat_area_x, chat_area_y)
        time.sleep(0.3)
        print(f"[👆] Clicked on chat area at ({chat_area_x}, {chat_area_y})")
        
        # Now click on the message input box at bottom
        input_x = win.left + int(win.width * 0.65)
        input_y = win.top + win.height - 80  # 80px from bottom
        
        pyautogui.click(input_x, input_y)
        time.sleep(0.3)
        print(f"[👆] Clicked on message input at ({input_x}, {input_y})")
        
        return True
    except Exception as e:
        print(f"[!] Click error: {e}")
        return False


def send_reply(message):
    """Sends the reply with human-like typing"""
    try:
        # Click on chat area and message input (combined, simpler approach)
        if not click_on_chat_area_and_input():
            print("[!] Failed to focus on chat input")
            return False
        
        # Type the message
        print(f"[⌨️] Typing reply...")
        pyautogui.write(message, interval=0.05)  # Type with realistic speed
        time.sleep(0.5)
        
        # Send the message
        pyautogui.press("enter")
        time.sleep(0.3)
        
        print(f"[✓] Sent: {message}")
        return True
    except Exception as e:
        print(f"[!] Reply failed: {e}")
        return False


def check_rate_limit():
    """Prevents spam by limiting replies per hour"""
    current_time = time.time()
    
    # Reset counter every hour
    if current_time - reply_counter["reset_time"] > 3600:
        reply_counter["count"] = 0
        reply_counter["reset_time"] = current_time
    
    if reply_counter["count"] >= MAX_REPLIES_PER_HOUR:
        print("[!] Rate limit reached. Cooling down...")
        return False
    
    return True


def main():
    """Main bot loop"""
    print("=" * 50)
    print("🤖 Smart WhatsApp Auto-Reply Bot")
    print("=" * 50)
    print(f"Configuration:")
    print(f"  • Scan Interval: {SCAN_INTERVAL}s")
    print(f"  • Reply Cooldown: {REPLY_COOLDOWN}s")
    print(f"  • Max Replies/Hour: {MAX_REPLIES_PER_HOUR}")
    print(f"  • Capture Mode: Full WhatsApp Window")
    print(f"  • Debug Mode: {DEBUG_MODE}")
    print("=" * 50)
    print("\n[🚀] Bot started! Monitoring WhatsApp...\n")
    
    while True:
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"\n[{timestamp}] 🔍 Checking for new messages...")
            
            # Focus WhatsApp
            if not focus_whatsapp():
                time.sleep(SCAN_INTERVAL)
                continue
            
            # Capture chat
            chat_img = get_chat_image()
            if not chat_img:
                time.sleep(SCAN_INTERVAL)
                continue
            
            # Generate image hash to detect duplicates
            img_hash = generate_image_hash(chat_img)
            
            # Check if we've already replied to this message
            last_reply_time = message_history.get(img_hash, 0)
            if time.time() - last_reply_time < REPLY_COOLDOWN:
                print("[→] Already replied to this message recently (cooldown active)")
                time.sleep(SCAN_INTERVAL)
                continue
            
            # Check rate limit
            if not check_rate_limit():
                time.sleep(SCAN_INTERVAL)
                continue
            
            # Analyze message and generate reply
            result = analyze_message_and_generate_reply(chat_img)
            
            if result.get("should_reply") and result.get("reply"):
                print(f"[💬] Preparing to reply to: \"{result['message_detected']}\"")
                
                # Send the reply
                if send_reply(result["reply"]):
                    # Update tracking
                    message_history[img_hash] = time.time()
                    reply_counter["count"] += 1
                    
                    # Cleanup old history (keep last 24 hours)
                    current_time = time.time()
                    message_history.clear()
                    for h, t in list(message_history.items()):
                        if current_time - t > 86400:
                            del message_history[h]
            else:
                print("[→] No new message requiring a reply")
            
            time.sleep(SCAN_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n[!] Bot stopped by user")
            break
        except Exception as e:
            print(f"[💥] Error: {e}")
            time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
