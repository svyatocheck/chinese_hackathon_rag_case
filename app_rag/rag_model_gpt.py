import langchain
from langchain.chains import LLMChain
from langchain_community.llms import YandexGPT
from langchain_core.documents.base import Document
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

stuff_prompt_override = """
Ты - ассистент востоковеда. Ты умеешь читать новости на китайском языке, анализировать их, находить нужную информацию и переводить ее на русский. Ты отвечаешь на вопросы о Китае. Ответы ты находишь в тексте новостей. 

Для имен собственных ты дополнительно приводишь оригинальное написание на китайском (приводишь цитату из источника). Для объектов в новости ты приводишь обобщающую характеристику. Например, если в ответе перечисляются автомобильные компании, то помимо их названия указывается юридическая принадлежность, время создания, специализация (авто для широкого покупателя, авто премиум класса, электромобили, строительные машины и т.п.), оценка размера (считается крупной, ведущей, прошлогодний стартап и т.п.), отношение к другим компаниям (подразделение, дочерняя компания, подрядчик крупного концерна и т.п.). Если по одному и тому же запросу ты находишь разные сведения, прикрепляй каждую точку зрения и указывай ссылку на источник.

Ответы должны быть четко структурированы и включать следующие элементы:
1. Описание события или факта.
2. Подробная информация об участвующих лицах или объектах.
3. Оригинальные имена собственных на китайском языке с цитатой из источника (по возможности).
4. К каждому тезису приводи URL ссылку на статью источник.
---
Текст:
-----
{context}
-----
Вопрос:
{query}
"""

class YandexLLM:

    def __init__(self, api_key, folder_id, iam_token = '') -> None:
        self.llm = YandexGPT(
            api_key=api_key,
            folder_id=folder_id)
        self._init_chain()

    def _init_chain(self):

        # Промпт для обработки документов
        document_prompt = PromptTemplate(
            input_variables=["page_content"], template="{page_content}"
        )

        # Промпт для языковой модели
        document_variable_name = "context"
        prompt = PromptTemplate(
            template=stuff_prompt_override, input_variables=["context", "query"]
        )

        # Создаём цепочку
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        self.chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=document_prompt,
            document_variable_name=document_variable_name,
        )

    def invoke_chain(self, input_context : list[Document], query : str):
        if input_context:
            # Adjust your code to include an 'input' dictionary
            input_data = {
                'input_documents': input_context,
                'query': query,  # Используем оригинальный русский запрос
            }
            # Now, pass the 'input_data' dictionary to the 'invoke' method
            response = self.chain.invoke(input=input_data)
            return response['output_text']
        else:
            print("No relevant documents found.")