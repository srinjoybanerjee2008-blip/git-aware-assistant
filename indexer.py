import chromadb
from chromadb.config import Settings
import numpy as np

class Indexer:
    def __init__(self, collection_name: str = 'default', persist_directory: str = './chroma_db'):
        client = chromadb.Client(Settings(chroma_db_impl='duckdb+parquet', persist_directory=persist_directory))
        self.client = client
        self.collection = client.get_or_create_collection(name=collection_name)

    def upsert(self, texts, vectors, metadatas):
        ids = [m['chunk_id'] for m in metadatas]
        # chroma accepts list-like embeddings
        vecs = vectors.tolist() if hasattr(vectors, 'tolist') else [list(v) for v in vectors]
        self.collection.add(documents=texts, embeddings=vecs, metadatas=metadatas, ids=ids)
        self.client.persist()

    def query(self, q_vector, n_results=5):
        res = self.collection.query(query_embeddings=[q_vector], n_results=n_results, include=['metadatas','documents','distances'])
        return res

    def retrieve_by_text(self, text: str, embedder, n_results=5):
        v = embedder.embed(text)
        return self.query(v, n_results=n_results)
