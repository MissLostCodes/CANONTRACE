from langchain_community.vectorstores import PathwayVectorClient

class PathwayRetriever:
    def __init__(self, url: str):
        self.client = PathwayVectorClient(
            url=url,
           )

    def search(self, query: str, k: int = 10):
        return self.client.similarity_search(query, k=k)
