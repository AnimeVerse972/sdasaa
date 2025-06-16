import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive

# .env orqali token olish
API_TOKEN = os.environ.get('BOT_TOKEN')
CHANNELS = ['@AniVerseClip', '@StudioNovaOfficial']

ADMINS = ['6486825926', '7575041003']  # O‘rningizga o‘z Telegram ID'ingizni yozing

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

keep_alive()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    not_subscribed = []

    for channel in CHANNELS:
        try:
            chat_member = await bot.get_chat_member(channel, user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                not_subscribed.append(channel)
        except Exception as e:
            logging.error(f"Error checking subscription for {channel}: {e}")
            not_subscribed.append(channel)

    if not_subscribed:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for ch in not_subscribed:
            keyboard.add(InlineKeyboardButton(f"🔔 {ch}", url=f"https://t.me/{ch.strip('@')}"))
        await message.answer("📛 *Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:*", reply_markup=keyboard)
        return

    buttons = [[KeyboardButton("📢 Reklama"), KeyboardButton("💼 Homiylik")]]
    reply_markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

    await message.answer("✅ Assalomu alaykum!\nAnime kodini yuboring (masalan: 1, 2, 3, ...)", reply_markup=reply_markup)

@dp.message_handler()
async def handle_code(message: types.Message):
    user_id = message.from_user.id

    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                await message.answer(f"⛔ Iltimos, {channel} kanaliga obuna bo‘ling va qaytadan urinib ko‘ring.")
                return
        except Exception as e:
            logging.error(f"Error checking membership for {channel}: {e}")
            await message.answer(f"⚠️ {channel} kanal tekshiruvida xatolik. Iltimos, keyinroq urinib ko‘ring.")
            return

    anime_posts = {
        "1": {"channel": "@AniVerseClip", "message_id": 10},
        "2": {"channel": "@AniVerseClip", "message_id": 23},
        # ... (other codes)
        "44": {"channel": "@AniVerseClip", "message_id": 931},
        # Ensure all codes have message_id
    }

    code = message.text.strip()

    if code in anime_posts:
        channel = anime_posts[code]["channel"]
        message_id = anime_posts[code]["message_id"]
        
        # "TOMOSHA QILISH" tugmasini yaratish
        keyboard = InlineKeyboardMarkup()
        watch_button = InlineKeyboardButton("TOMOSHA QILISH", url=f"https://t.me/{channel.strip('@')}/{message_id}")
        keyboard.add(watch_button)
        
        # Xabarni tugma bilan birga yuborish
        await bot.copy_message(chat_id=user_id, from_chat_id=channel, message_id=message_id, reply_markup=keyboard)
    elif code in ["📢 Reklama", "💼 Homiylik"]:
        if code == "📢 Reklama":
            await message.answer("Reklama uchun @DiyorbekPTMA ga murojat qiling. Faqat reklama boyicha!")
        elif code == "💼 Homiylik":
            await message.answer("Homiylik uchun karta 8800904257677885")
    else:
        await message.answer("❌ Bunday kod topilmadi. Iltimos, to‘g‘ri anime kodini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
