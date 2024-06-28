import telebot
from telebot import types

from app_rag.rag_view_message_handler import MessageHandler

class BotView:

    def __init__(self, bot, message_handler : MessageHandler):
        self.message_handler = message_handler
        self.bot = bot
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            self.message_handler.handle_start(message)

        @self.bot.message_handler(commands=['help'])
        def help_command(message):
            self.message_handler.handle_help(message)

        @self.bot.message_handler(func=lambda message: True)
        def all_messages(message):
            self.message_handler.handle_message(message)

    def run(self):
        self.bot.polling(non_stop=True)
