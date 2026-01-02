import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# Replace with actual admin user IDs (integers)
ADMIN_IDS = [8267676849, 5913618698, 1352222165] 

# Start Image (URL or File ID)
START_PIC = "https://ibb.co/k2jMZfvd" 

# Private/Sponsor Channel (Display only, no check)
PRIVATE_CHANNEL = {
    "name": "🔥 PRIVATE CHANNEL",
    "url": "https://t.me/+ChVlNCpLOc9kMTk9" 
}
