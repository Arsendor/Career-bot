import telebot
from telebot import types
import json
from db import init_db, save_conversation, save_user_profile
from neural import get_ai_response
from config import TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN)
init_db()

# Загрузка профессий
with open("professions.json", encoding="utf-8") as f:
    professions = json.load(f)

# Словарь для хранения промежуточных данных пользователя
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Ищу свой путь", "Хочу сменить работу")
    bot.send_message(message.chat.id, "Привет! 👋 Я Career-bot. Давай узнаем, что тебе нравится.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id not in user_data:
        user_data[chat_id] = {}

    # Шаги анкеты
    if "Ищу свой путь" in text or "Хочу сменить работу" in text:
        bot.send_message(chat_id, "Сколько тебе лет?")
        user_data[chat_id]["step"] = "age"
        return

    if user_data[chat_id].get("step") == "age":
        user_data[chat_id]["age"] = text
        bot.send_message(chat_id, "Какое у тебя образование?")
        user_data[chat_id]["step"] = "education"
        return

    if user_data[chat_id].get("step") == "education":
        user_data[chat_id]["education"] = text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Общаться и помогать людям", "Работать с данными/кодом/логикой")
        markup.add("Создавать креативно", "Руководить и организовывать")
        bot.send_message(chat_id, "Что тебе нравится делать?", reply_markup=markup)
        user_data[chat_id]["step"] = "interests"
        return

    if user_data[chat_id].get("step") == "interests":
        user_data[chat_id]["interests"] = text
        # Генерация профиля через нейросеть
        prompt = f"Создай короткий профиль пользователя, интересы: {text}"
        profile = get_ai_response(prompt)
        user_data[chat_id]["profile"] = profile

        # Сохраняем профиль в БД
        save_user_profile(
            telegram_id=chat_id,
            age=user_data[chat_id].get("age"),
            education=user_data[chat_id].get("education"),
            interests=text,
            skills="",
            profile=profile
        )

        bot.send_message(chat_id, f"Твой профиль: {profile}\nВот несколько профессий, которые могут тебе подойти:")

        # Показ карточек профессий
        for p in professions:
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("Подробнее", url=p["link"])
            markup.add(btn)
            bot.send_message(chat_id, f"**{p['title']}**\n{p['description']}", parse_mode="Markdown", reply_markup=markup)

        bot.send_message(chat_id, "Хочешь пройти анкету заново? /start")
        user_data[chat_id]["step"] = None
        return

    # Если пользователь пишет свободный текст — через нейросеть
    bot_reply = get_ai_response(text)
    save_conversation(chat_id, text, bot_reply)
    bot.send_message(chat_id, bot_reply)

bot.polling(none_stop=True)
