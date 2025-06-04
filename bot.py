import json
import logging
from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '8192820654:AAGkHpm9bd5UtQgRFo7llt_Ysvz-JYnK28g'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def get_user_data(user_id):
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = {"hearts": 0, "kisses": 0}
        save_data(data)
    return data[str(user_id)]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user = get_user_data(message.from_user.id)
    await message.answer(
        f"Привет, мой любимый 💖\n\n"
        f"Ты накопил:\n"
        f"💛 Нежности: {user['hearts']}\n"
        f"💋 Поцелуев: {user['kisses']}\n\n"
        "Что хочешь сегодня? 😊",
        reply_markup=main_menu()
    )

def main_menu():
    buttons = [
        [types.KeyboardButton('🍳 Завтрак в постель')],
        [types.KeyboardButton('💆 Массаж')],
        [types.KeyboardButton('📺 Посмотреть сериал')],
        [types.KeyboardButton('💛 Баланс')],
        [types.KeyboardButton('💰 Получить 💛')],
    ]
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(*sum(buttons, []))

@dp.message_handler(lambda m: m.text == '💛 Баланс')
async def show_balance(message: types.Message):
    user = get_user_data(message.from_user.id)
    await message.answer(f"У тебя:\n💛 {user['hearts']} нежности\n💋 {user['kisses']} поцелуев")

@dp.message_handler(lambda m: m.text == '💰 Получить 💛')
async def add_hearts(message: types.Message):
    data = load_data()
    uid = str(message.from_user.id)
    if uid not in data:
        data[uid] = {"hearts": 0, "kisses": 0}
    data[uid]['hearts'] += 1
    save_data(data)
    await message.answer("Ты получил 💛! Спасибо, что ты такой заботливый 🥰")

@dp.message_handler(lambda m: m.text in ['🍳 Завтрак в постель', '💆 Массаж', '📺 Посмотреть сериал'])
async def spend(message: types.Message):
    uid = str(message.from_user.id)
    data = load_data()
    cost = {
        '🍳 Завтрак в постель': 2,
        '💆 Массаж': 2,
        '📺 Посмотреть сериал': 1
    }
    need = cost[message.text]
    if data[uid]['hearts'] >= need:
        data[uid]['hearts'] -= need
        save_data(data)
        await message.answer(f"Готовлю {message.text} с любовью 💖 Осталось 💛: {data[uid]['hearts']}")
    else:
        await message.answer("Не хватает 💛. Сделай что-нибудь хорошее, и я подарю их 😘")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
