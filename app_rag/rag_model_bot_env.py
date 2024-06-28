import os

import time
import jwt
import requests
import time
import jwt
import json

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('/app/.env')

class Config:

    @staticmethod
    def get_telegram_bot_token():
        return os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    @staticmethod
    def get_api_key():
        return os.getenv('API_KEY', '')

    @staticmethod
    def load_token():
        with open('/app/.configs/authorized_key.json', 'r') as f: 
            obj = f.read() 
            obj = json.loads(obj)
            private_key = obj['private_key']
            key_id = obj['id']
            service_account_id = obj['service_account_id']

        now = int(time.time())
        payload = {
                'aud': 'https://iam.{{ api-host }}/iam/v1/tokens',
                'iss': service_account_id,
                'iat': now,
                'exp': now + 3600
            }

        # Формирование JWT.
        encoded_token = jwt.encode(
            payload,
            private_key,
            algorithm='PS256',
            headers={'kid': key_id}
        )
        #Запись ключа в файл
        with open('jwt_token.txt', 'w') as j:
            j.write(encoded_token) 
    
    @staticmethod
    def get_iam_token():
        if os.path.exists('/app/jwt_token.txt'):
            with open('/app/jwt_token.txt', 'r') as j:
                encoded_token = j.read()
            return encoded_token
        else:
            return Config.load_token()
    
    @staticmethod
    def get_hosts():
        return os.getenv('HOSTS', '')

    @staticmethod
    def get_db_pwd():
        return os.getenv('DB_PWD', '')

    @staticmethod
    def get_ca():
        return os.getenv('CA', '')
    
    @staticmethod
    def get_directory_id():
        return os.getenv('FOLDER_ID', '')