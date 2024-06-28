from opensearchpy import OpenSearch

from langchain.vectorstores import OpenSearchVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model_name = "DMetaSoul/sbert-chinese-general-v2"

embeddings_model = HuggingFaceEmbeddings(
    model_name=embedding_model_name, model_kwargs={"device": "cpu"}
)

class OpenSearchDB:

    def __init__(self, ca: str, pwd: str, hosts: str) -> None:
        self._init_connection(ca=ca, pwd=pwd, hosts=hosts)

    def _init_connection(self, ca, pwd, hosts):
        print(hosts, pwd)
        self.docsearch : OpenSearchVectorSearch = OpenSearchVectorSearch(
            embedding_function=embeddings_model,
            index_name="china-embeddings",
            opensearch_url=hosts,
            http_auth=("admin", pwd),
            use_ssl=True,
            verify_certs=True,
            ca_certs=ca,
            timeout=300
        )

    def find_similar(self, translated_query, year=2023):
        pre_filter_dict = {"range": {"metadata.year": {"lte": year}}}
        documents = self.docsearch.max_marginal_relevance_search(translated_query)
        return documents
