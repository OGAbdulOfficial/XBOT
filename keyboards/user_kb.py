from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PRIVATE_CHANNEL

def user_main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎬 𝐆𝐞𝐭 𝐕𝐢𝐝𝐞𝐨", callback_data="get_video"),
        InlineKeyboardButton("🔗 𝐆𝐞𝐭 𝐋𝐢𝐧𝐤", callback_data="get_link"),
    )
    kb.add(
        InlineKeyboardButton("📊 𝐕𝐢𝐞𝐰 𝐒𝐭𝐚𝐭𝐬", callback_data="view_stats")
    )
    return kb

def force_join_kb(channels_list):
    kb = InlineKeyboardMarkup(row_width=1)
    
    # Add Private/Sponsor Channel First (No Check)
    if PRIVATE_CHANNEL and PRIVATE_CHANNEL["url"] != "https://t.me/+AbCdEfGhIjKlMnOp":
         kb.add(InlineKeyboardButton(PRIVATE_CHANNEL["name"], url=PRIVATE_CHANNEL["url"]))

    for ch in channels_list:
        # Handling Invite Links vs Usernames
        if ch.startswith("http") or ch.startswith("t.me"):
            url = ch
        else:
            # Assume username, ensure proper format for url
            clean_ch = ch.replace("@", "")
            url = f"https://t.me/{clean_ch}"
            
        # Viral bots usually just say "JOIN" or "JOIN CHANNEL"
        label = "𝐉𝐎𝐈𝐍"
            
        kb.add(InlineKeyboardButton(label, url=url))
        
    kb.add(InlineKeyboardButton("✅ 𝐉𝐨𝐢𝐧𝐞𝐝", callback_data="check_join"))
    return kb

def get_video_kb(link):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("▶️ Open Video", url=link))
    return kb

def forward_link_kb(link):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔁 Forward My Link", url=f"https://t.me/share/url?url={link}"))
    return kb
