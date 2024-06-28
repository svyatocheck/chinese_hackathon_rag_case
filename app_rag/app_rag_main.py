import os
import sys
import jwt
import telebot
from telebot import types

from opensearchpy import OpenSearch

# set src directory as default
sys.path.append(os.path.abspath('.'))

from app_rag.rag_view_message_handler import MessageHandler

from app_rag.rag_model_bot_env import Config
from app_rag.rag_view_app_bot import BotView
from app_rag.rag_model_gpt import YandexLLM
from app_rag.rag_model_opensearch import OpenSearchDB
from app_rag.rag_model_translate import YandexTranslator
from app_rag.rag_presenter_app_bot import BotPresenter

def init_yandex_llm():
    api_key = Config.get_api_key()
    directory = Config.get_directory_id()
    yandex_llm = YandexLLM(api_key = api_key, folder_id=directory)
    return yandex_llm

def init_opensearch_database():
    ca = Config.get_ca()
    db_pwd = Config.get_db_pwd()
    hosts = Config.get_hosts()
    opensearch = OpenSearchDB(ca, db_pwd, hosts) #TODO fix
    return opensearch

def init_translator():
    api_key = Config.get_api_key()
    print(api_key)
    translator = YandexTranslator(api_key)
    return translator

def init_bot_presenter(llm, database, translator):
    bot_presenter = BotPresenter(translator, llm, database)
    return bot_presenter


def init_tele_bot(presenter):
    bot_token = Config.get_telegram_bot_token()
    bot = telebot.TeleBot(bot_token)
    message_handler = MessageHandler(bot, presenter)
    bot_view_rag = BotView(bot, message_handler=message_handler)
    return bot_view_rag


def init_app_components():
    yandex_llm = init_yandex_llm()
    database = init_opensearch_database()
    translator = init_translator()

    presenter = init_bot_presenter(yandex_llm, database, translator)
    bot_view_rag = init_tele_bot(presenter)

    return bot_view_rag


if __name__ == '__main__':
    bot = init_app_components()
    bot.run()
