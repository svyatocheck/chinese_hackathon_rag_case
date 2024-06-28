
from app_rag.rag_model_translate import YandexTranslator
from app_rag.rag_model_gpt import YandexLLM
from app_rag.rag_model_opensearch import OpenSearchDB

class BotPresenter:

    def __init__(self, translator : YandexTranslator, llm : YandexLLM, database : OpenSearchDB) -> None:
        self.translator = translator
        self.period = 2023
        self.llm = llm
        self.database = database
    
    def send_query(self, query):
        zh_version = self.translator.translate_query_to_chinese(query)
        print(zh_version)
        similar_documents = self.database.find_similar(zh_version, self.period) 
        print(similar_documents)
        ru_docs_versions = self.translator.translate_similar_docs_to_russian(similar_documents)
        response = self.llm.invoke_chain(similar_documents, ru_docs_versions)
        return response
