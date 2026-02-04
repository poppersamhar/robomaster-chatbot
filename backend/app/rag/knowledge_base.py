import json
import os
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class KnowledgeBase:
    def __init__(self, data_path: str = None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'qa_pairs.json')

        self.data_path = data_path
        self.qa_pairs = []
        self.vectorizer = None
        self.tfidf_matrix = None

        self._load_data()
        self._build_index()

    def _load_data(self):
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.qa_pairs = json.load(f)

    def _tokenize(self, text: str) -> str:
        """中文分词"""
        return ' '.join(jieba.cut(text))

    def _build_index(self):
        """使用TF-IDF构建索引"""
        questions = [self._tokenize(qa['question']) for qa in self.qa_pairs]
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(questions)

    def search(self, query: str, top_k: int = 3) -> list:
        """搜索最相似的问答对"""
        query_tokenized = self._tokenize(query)
        query_vec = self.vectorizer.transform([query_tokenized])

        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = similarities.argsort()[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append({
                'question': self.qa_pairs[idx]['question'],
                'answer': self.qa_pairs[idx]['answer'],
                'score': float(similarities[idx])
            })

        return results


_knowledge_base = None

def get_knowledge_base() -> KnowledgeBase:
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base
