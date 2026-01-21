"""
Quick Setup and Test Script
Run this to verify your setup before starting the bot
"""

import os
import sys

def check_requirements():
    """Check if all required packages are installed"""
    print("=" * 50)
    print("📦 Checking Dependencies...")
    print("=" * 50)
    
    required = {
        'pyautogui': 'pyautogui',
        'PIL': 'Pillow',
        'google.generativeai': 'google-generativeai',
        'dotenv': 'python-dotenv',
        'pygetwindow': 'pygetwindow',
    }
    
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing packages! Install with:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!\n")
    return True


def check_env():
    """Check if .env file exists and has API key"""
    print("=" * 50)
    print("🔑 Checking Environment Variables...")
    print("=" * 50)
    
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        print("\n📝 Create .env file with:")
        print("GOOGLE_API_KEY=your_api_key_here")
        print("\nGet API key from: https://makersuite.google.com/app/apikey")
        return False
    
    print("✓ .env file exists")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        print("✗ GOOGLE_API_KEY not set properly in .env")
        return False
    
    print("✓ GOOGLE_API_KEY is set")
    print(f"  Key: {api_key[:10]}...{api_key[-4:]}")
    print("\n✅ Environment configured!\n")
    return True


def check_whatsapp():
    """Check if WhatsApp is running"""
    print("=" * 50)
    print("💬 Checking WhatsApp Desktop...")
    print("=" * 50)
    
    try:
        import pygetwindow as gw
        wins = gw.getWindowsWithTitle("WhatsApp")
        
        if not wins:
            print("✗ WhatsApp window not found")
            print("\n⚠️  Please open WhatsApp Desktop and try again")
            return False
        
        print(f"✓ WhatsApp found: {wins[0].title}")
        print(f"  Size: {wins[0].width}x{wins[0].height}")
        print("\n✅ WhatsApp is running!\n")
        return True
        
    except Exception as e:
        print(f"✗ Error checking WhatsApp: {e}")
        return False


def check_config():
    """Check if config.json exists (optional, for legacy compatibility)"""
    print("=" * 50)
    print("⚙️  Checking Configuration...")
    print("=" * 50)
    
    if os.path.exists('config.json'):
        try:
            import json
            with open('config.json') as f:
                config = json.load(f)
                chat_area = config.get('chat_area')
                
            print(f"✓ config.json exists (legacy)")
            print(f"  Chat area: {chat_area}")
        except Exception as e:
            print(f"✗ Error reading config.json: {e}")
    else:
        print("ℹ config.json not found (optional - bot captures full window)")
    
    print("\n✅ Configuration OK! Bot will capture full WhatsApp window.\n")
    return True


def test_gemini_api():
    """Test Gemini API connection"""
    print("=" * 50)
    print("🤖 Testing Gemini API...")
    print("=" * 50)
    
    try:
        from dotenv import load_dotenv
        import google.generativeai as genai
        
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        
        print("Sending test request...")
        response = model.generate_content("Say 'API works!' in 2 words")
        print(f"✓ Response: {response.text.strip()}")
        print("\n✅ Gemini API working!\n")
        return True
        
    except Exception as e:
        print(f"✗ Gemini API error: {e}")
        print("\n⚠️  Check your API key and internet connection")
        return False


def main():
    """Run all checks"""
    print("\n" + "=" * 50)
    print("🚀 WhatsApp Bot Setup Checker")
    print("=" * 50 + "\n")
    
    checks = {
        "Dependencies": check_requirements(),
        "Environment": check_env(),
        "WhatsApp": check_whatsapp(),
        "Configuration": check_config(),
    }
    
    # Only test API if other checks pass
    if all(checks.values()):
        checks["Gemini API"] = test_gemini_api()
    
    # Summary
    print("=" * 50)
    print("📊 Setup Summary")
    print("=" * 50)
    
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
    
    if all(checks.values()):
        print("\n" + "=" * 50)
        print("🎉 ALL CHECKS PASSED!")
        print("=" * 50)
        print("\n✨ You're ready to run the bot!")
        print("\nRun one of these:")
        print("  python smart_bot.py    (recommended)")
        print("  python bot.py          (GM only)")
        print("\n💡 Tip: Check GUIDE.md for customization options")
    else:
        print("\n" + "=" * 50)
        print("⚠️  SETUP INCOMPLETE")
        print("=" * 50)
        print("\nFix the issues above and run this script again.")
    
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Setup check cancelled")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
