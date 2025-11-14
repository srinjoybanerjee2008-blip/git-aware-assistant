from typing import List
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        # For code, consider 'microsoft/codebert' or similar models if available locally.
        print(f'Loading embedding model: {model_name}')
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str):
        return self.model.encode(text, show_progress_bar=False)

    def embed_batch(self, texts: List[str]):
        return self.model.encode(texts, show_progress_bar=True)
