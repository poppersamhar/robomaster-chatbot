import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


class KnowledgeBase:
    def __init__(self, data_path: str = None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'qa_pairs.json')

        self.data_path = data_path
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.qa_pairs = []
        self.index = None
        self.embeddings = None

        self._load_data()
        self._build_index()

    def _load_data(self):
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.qa_pairs = json.load(f)

    def _build_index(self):
        questions = [qa['question'] for qa in self.qa_pairs]
        self.embeddings = self.model.encode(questions, convert_to_numpy=True)

        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)

        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings)

    def search(self, query: str, top_k: int = 3) -> list:
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.qa_pairs):
                results.append({
                    'question': self.qa_pairs[idx]['question'],
                    'answer': self.qa_pairs[idx]['answer'],
                    'score': float(scores[0][i])
                })

        return results


_knowledge_base = None

def get_knowledge_base() -> KnowledgeBase:
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base
