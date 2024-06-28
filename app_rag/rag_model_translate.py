import requests

from langchain_core.documents.base import Document

class YandexTranslator:

    def __init__(self, service_account_api_key) -> None:
        self.service_api_key = service_account_api_key

    def translate_similar_docs_to_russian(self, docs):
        translated_docs = []
        for doc in docs:
            print(doc.page_content)
            translated_content = self._translate_text(doc.page_content, 'ru', 'zh')
            translated_content += f"\n\nСсылка на источник: {doc.metadata['url']}" # need to extract to dif func
            translated_docs.append(Document(page_content=translated_content, metadata=doc.metadata))
        return translated_docs

    def translate_query_to_chinese(self, query):
        try:
            translated_query = self._translate_text(query, "zh", "ru")
            print("chinese: {translated_query}")
            return translated_query
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def _translate_text(self, text, target_language, source_language) -> str:
        url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
        headers = {
            "Authorization": f"Api-Key {self.service_api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "sourceLanguageCode": source_language,
            "targetLanguageCode": target_language,
            "texts": [text],
        }
        response = requests.post(url, headers=headers, json=body, timeout=300)
        result = response.json()
        print(result)

        if "translations" in result:
            return result["translations"][0]["text"]
        else:
            raise Exception(f"Error in translation: {result}")