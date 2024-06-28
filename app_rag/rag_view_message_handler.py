import telebot
import re
from telebot import types

from app_rag.rag_presenter_app_bot import BotPresenter

message_error = "Что-то пошло не так...\n\nПопробуйте перезапустить бота /start. Если проблема повторится, свяжитесь с автором\n @sams3pi01"
class MessageHandler:

    def __init__(self, bot, presenter: BotPresenter):
        self.bot = bot
        self.presenter = presenter
        self.gif_message_id = None

    def handle_start(self, message):
        keyboard = types.ReplyKeyboardMarkup()
        button2 = types.KeyboardButton("Настроить актуальность 📅")
        keyboard.add(button2)
        self.bot.reply_to(
            message,
            "👋 Привет! 你好！\n\nЯ твой ассистент по китайским СМИ. \n\nЯ умею читать новости на китайском и извлекать из них нужную информацию.\n\nГотов попытаться ответить на интересующие тебя вопросы по китайским СМИ!",
            reply_markup=keyboard,
        )

    def handle_message(self, message):
        if "Настроить актуальность" in message.text:
            self.choose_period(message)
        else:
            try:
                self.bot.reply_to(message, "Дайте подумать...\n\n" + message.text)
                self.send_waiting_gif(message)
                gpt_response = self.presenter.send_query(message.text)
                # escaped_response = self.escape_markdown_v2(gpt_response)
                self.delete_gif_message(message)
                self.bot.reply_to(message, gpt_response)
            except Exception as ex:
                print(ex)
                self.bot.reply_to(message, message_error)

    def escape_markdown_v2(self, text):
        escape_chars = r'\_*[]()~`>#+-=|{}.!'
        return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)
    
    def start_discussion(self, message):
        # Placeholder for starting a new dialog with context saving
        self.bot.reply_to(
            message, "Начато новое обсуждение 📝. (Контекст будет сохранен.)"
        )

    def choose_period(self, message):
        # Placeholder for handling period selection
        self.bot.reply_to(message, "Введите год из диапазона 2016-2023:")
        self.bot.register_next_step_handler(message, self.get_year)

    def get_year(self, message):
        try:
            period = int(message.text)
            self.presenter.period = period
            self.bot.reply_to(message, f"Год: {period} установлен! Весь контекст будет не позже {period} года.")
        except Exception as ex:
            print(ex)
            self.bot.reply_to(message, f"Хм...\n\nЭто не похоже на число.")

    def handle_help(self, message):
        self.bot.send_message(
            message.chat.id, "Доступные команды: /start, /help", parse_mode="html"
        )

    def send_waiting_gif(self, message):
        # Sending a GIF file to the user while waiting for GPT response
        gif_path = "/app/app_rag/sources/tom-ching-cheng-hanji.gif"  # Update with the actual path to your GIF file
        with open(gif_path, "rb") as gif:
            sent_message = self.bot.send_animation(message.chat.id, gif)
            self.gif_message_id = (
                sent_message.message_id
            )  # Store the message ID of the sent GIF

    def delete_gif_message(self, message):
        if self.gif_message_id:
            self.bot.delete_message(
                chat_id=message.chat.id, message_id=self.gif_message_id
            )
            self.gif_message_id = None
