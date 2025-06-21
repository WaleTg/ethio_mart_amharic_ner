
import json
from telethon.sync import TelegramClient
from telethon.tl.types import Message
import os
from datetime import datetime
import base64
import os
from dotenv import load_dotenv
import os
from dotenv import load_dotenv

# Load the .env file from the myEnv folder
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'myEnv', '.env')
load_dotenv(dotenv_path)
# getting hidden variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')


channels = [
    "ZemenExpress",
    "nevacomputer",
    "meneshayeofficial",
    "Leyueqa",
    "Shewabrand",
    "helloomarketethiopia"
]



def serialize_message(message):
    d = message.to_dict()
    
    def convert_value(value):
        if isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, bytes):
            # Encode bytes to base64 string to safely serialize
            return base64.b64encode(value).decode('ascii')
        elif isinstance(value, dict):
            # Recursively convert dictionary values
            return {k: convert_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            # Recursively convert list items
            return [convert_value(v) for v in value]
        else:
            return value

    return {k: convert_value(v) for k, v in d.items()}

with TelegramClient('session', api_id, api_hash) as client:
    for channel in channels:
        try:
            messages = client.iter_messages(channel, limit=500)
            serialized = []
            for msg in messages:
                if isinstance(msg, Message):
                    serialized.append(serialize_message(msg))
            os.makedirs("data/raw", exist_ok=True)
            with open(f"data/raw/{channel}_messages.json", "w", encoding='utf-8') as f:
                json.dump(serialized, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(serialized)} messages from @{channel} to data/raw/{channel}_messages.json")
        except Exception as e:
            print(f"Error scraping @{channel}: {e}")
