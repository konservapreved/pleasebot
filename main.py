from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import os

# ✅ Вставь сюда свой токен
TOKEN = "7375977414:AAG-oZ8bSpGPN5H5_XqMLc2seVj-Xo4_rYw"

# ✅ Вставь сюда свой Telegram user ID (чтобы получать уведомления)
ADMIN_CHAT_ID = 206005992

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Ссылки, на которые бот будет перенаправлять
LINKS = {
    "to_channel": "https://t.me/metod_agency",
    "to_manager": "https://t.me/hello_metod"
}

# Логирование в консоль (удобно для Railway)
logging.basicConfig(level=logging.INFO)

async def log_click_and_notify(user_id, username, action):
    msg = f"👤 User {user_id} ({username}) clicked: {action}"
    logging.info(msg)
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    args = message.get_args()
    user_id = message.from_user.id
    username = message.from_user.username or "без username"

    if args in LINKS:
        await log_click_and_notify(user_id, username, args)
        await message.answer(f"Перенаправляю... [Нажмите здесь]({LINKS[args]})", parse_mode="Markdown")
    else:
        buttons = [
            types.InlineKeyboardButton("Канал", url=LINKS["to_channel"]),
            types.InlineKeyboardButton("Менеджер", url=LINKS["to_manager"])
        ]
        keyboard = types.InlineKeyboardMarkup().add(*buttons)
        await message.answer("Выберите, куда перейти:", reply_markup=keyboard)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)