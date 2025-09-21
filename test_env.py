from dotenv import load_dotenv
import os
from pathlib import Path

# Automatically find the .env file in the script's directory
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("OPENROUTER_API_KEY")

print("Current directory:", Path().resolve())  # shows where Python is running from

if api_key:
    print("✅ Key loaded:", api_key[:15] + "...")
else:
    print("❌ Key not found. Make sure .env exists and has OPENROUTER_API_KEY")
