import telebot
from telebot import types
from telegram import ReplyKeyboardMarkup

bot = telebot.TeleBot('6394055251:AAE2TpNPM29tQiK0ARhCrZSN0VsiKT7hJJ8')


@bot.message_handler(commands=['start'])
def start_handler(message):
    show_start_button(message.chat.id)


@bot.message_handler(func=lambda message: message.text != "Почати запис в щоденник")
def handle_message(message):
    bot.send_message(
        message.chat.id, "Почніть нову розмову, якщо хочете поговорити")


@bot.message_handler(func=lambda message: message.text == "Почати запис в щоденник")
def handle_start(message):
    hide_start_button(message.chat.id)
    with open('questions.txt', 'r', encoding='utf-8') as file:
        questions = file.read().splitlines()
    bot.send_message(message.chat.id, f'1/{len(questions)} {questions[0]}')
    bot.register_next_step_handler(message, ask_question, questions, 1)


def hide_start_button(chat_id):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    show_skip(keyboard=keyboard)
    show_stop(keyboard=keyboard)
    bot.send_message(
        chat_id, text="Відповідайте на питання чесно!", reply_markup=keyboard)


def show_skip(keyboard: ReplyKeyboardMarkup):
    skip_button = types.KeyboardButton("Наступне питання")
    keyboard.add(skip_button)


def show_stop(keyboard: ReplyKeyboardMarkup):
    stop_button = types.KeyboardButton("Закінчити")
    keyboard.add(stop_button)


def ask_question(message, questions, index):
    chat_id = message.chat.id
    if (message.text == 'Закінчити'):
        bot.send_message(chat_id, "Зупиняю бесіду")
        show_start_button(chat_id)
        return

    questions_count = len(questions)
    if index < questions_count:
        bot.send_message(chat_id, f'{index + 1}/{questions_count} {questions[index]}')
        bot.register_next_step_handler(
            message, ask_question, questions, index + 1)
    elif index == questions_count:
        bot.send_message(
            chat_id, 'Дякую за розмову, більше запитань немає!')
        show_start_button(chat_id)
        return


def show_start_button(chat_id):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    start_button = types.KeyboardButton("Почати запис в щоденник")
    keyboard.add(start_button)
    bot.send_message(chat_id, 'Виберіть дію:', reply_markup=keyboard)


bot.polling()
