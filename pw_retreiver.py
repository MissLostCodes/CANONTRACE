from langchain_community.vectorstores import PathwayVectorClient
client = PathwayVectorClient(url = "http://127.0.0.1:8080")
query = "who is Marseilles ?"
# x= client.similarity_search(query , k=3)
# print(x)

y = client.similarity_search(query ,k=3 ,  metadata_filter="novel_id == `the_count_of_monte_cristo` && contains(characters_mentioned, 'Marseilles') ")
print(y)

