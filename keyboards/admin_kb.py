from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_panel_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📊 Bot Stats", callback_data="admin_stats"),
        InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
    )
    kb.add(
        InlineKeyboardButton("➕ Add Channel", callback_data="admin_add_ch"),
        InlineKeyboardButton("➖ Remove Channel", callback_data="admin_rem_ch"),
    )
    kb.add(
        InlineKeyboardButton("🎬 Set Video Link", callback_data="admin_set_vid")
    )
    kb.add(
        InlineKeyboardButton("🔙 Close", callback_data="admin_close")
    )
    return kb

def cancel_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("❌ Cancel", callback_data="admin_cancel"))
    return kb
