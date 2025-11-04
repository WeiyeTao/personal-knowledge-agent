from openai import OpenAI
client = OpenAI()

def get_embeddings(texts, model="text-embedding-3-small"):
    response = client.embeddings.create(input=texts, model=model)
    return [d.embedding for d in response.data]
