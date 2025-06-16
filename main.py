import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import os

API_TOKEN = os.getenv('7731135599:AAGHCmXngriv1XO5WeRjN2XhMB6_qeKQTHU')  # API tokenni muhit o'zgaruvchisi orqali oling
CHANNEL_ID = '@AniVerseClip'  # Obuna bo'lishi kerak bo'lgan kanal
ANIME_DATA = {
    '1': {"channel": "@AniVerseClip", "message_id": 10},
    # Qo'shimcha kodlar va ularning ma'lumotlari
}

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Start komandasi
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)

    if chat_member.status not in ['member', 'administrator']:
        await message.answer("Obuna bo'ling: " + CHANNEL_ID)
    else:
        await message.answer("Obuna bo'lganingiz uchun rahmat! Anime kodini yuboring.")

# Anime kodini qabul qilish
@dp.message_handler(lambda message: message.text in ANIME_DATA.keys())
async def send_anime_info(message: types.Message):
    anime_code = message.text
    info = ANIME_DATA[anime_code]
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Yuklab olish", url="https://example.com/download"))
    markup.add(types.InlineKeyboardButton("Tomosha qilish", url="https://example.com/watch"))

    await message.answer(info, reply_markup=markup)

# Botni ishga tushirish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
