import re
from .knowledge_base import get_knowledge_base


class Retriever:
    def __init__(self, use_llm: bool = True):
        self.kb = get_knowledge_base()
        self.similarity_threshold = 0.5
        self.use_llm = use_llm
        self.llm_client = None

        # 尝试初始化 DeepSeek
        if self.use_llm:
            try:
                from ..llm import get_deepseek_client
                self.llm_client = get_deepseek_client()
            except Exception as e:
                print(f"DeepSeek initialization failed: {e}")
                self.use_llm = False

        # 敏感词列表
        self.sensitive_keywords = [
            '政治', '政府', '领导人', '国家政策',
            '赌博', '博彩', '色情', '暴力', '毒品',
            '内幕', '泄露', '机密', '作弊', '黑幕',
            '骂人', '侮辱', '歧视',
        ]

        # 热门问题推荐
        self.popular_questions = [
            "RoboMaster是什么比赛？",
            "如何报名参加RoboMaster？",
            "RoboMaster有哪些机器人类型？",
            "参加RoboMaster需要什么技能？",
            "RoboMaster比赛规则是什么？",
        ]

    def get_answer(self, query: str) -> str:
        # 1. 敏感词检测 - 直接拒绝，不走LLM
        if self._is_sensitive(query):
            return self._get_sensitive_response()

        # 2. RAG检索
        results = self.kb.search(query, top_k=3)
        best_score = results[0]['score'] if results else 0

        # 3. 使用LLM生成回答
        if self.use_llm and self.llm_client:
            return self._get_llm_answer(query, results, best_score)

        # 4. 降级到纯RAG模式
        return self._get_rag_answer(query, results, best_score)

    def _get_llm_answer(self, query: str, results: list, best_score: float) -> str:
        """使用Claude生成回答"""
        context = None

        # 如果RAG有匹配结果，构建上下文
        if best_score > 0.3:
            context_parts = []
            for r in results[:3]:
                if r['score'] > 0.3:
                    context_parts.append(f"问：{r['question']}\n答：{r['answer']}")
            if context_parts:
                context = "\n\n---\n\n".join(context_parts)

        # 调用Claude
        llm_response = self.llm_client.chat(query, context)

        if llm_response:
            return llm_response

        # LLM失败，降级到RAG
        return self._get_rag_answer(query, results, best_score)

    def _get_rag_answer(self, query: str, results: list, best_score: float) -> str:
        """纯RAG模式回答"""
        # 高置信度匹配
        if best_score > 0.85:
            return results[0]['answer']

        # 中等置信度
        if best_score > self.similarity_threshold:
            response = results[0]['answer']
            if len(results) > 1 and results[1]['score'] > 0.6:
                response += f"\n\n您可能还想了解：{results[1]['question']}"
            return response

        # 无匹配
        return self._get_no_match_response(results)

    def _is_sensitive(self, query: str) -> bool:
        """检测敏感内容"""
        query_lower = query.lower()
        for keyword in self.sensitive_keywords:
            if keyword in query_lower:
                return True
        return False

    def _get_sensitive_response(self) -> str:
        """敏感内容回复"""
        return (
            "抱歉，这个问题我无法回答。如有其他疑问，请通过官方渠道咨询：\n\n"
            "• 官网：www.robomaster.com\n"
            "• 官方邮箱：robomaster@dji.com\n"
            "• 官方微信公众号：RoboMaster机甲大师\n\n"
            "我可以回答RoboMaster赛事相关的问题，比如比赛规则、报名方式等~"
        )

    def _get_no_match_response(self, results: list) -> str:
        """无匹配时返回推荐问题"""
        response = "抱歉，我没有找到完全匹配的答案。\n\n"

        if results and results[0]['score'] > 0.3:
            response += "您是否想问以下问题：\n"
            for i, r in enumerate(results[:3]):
                response += f"{i+1}. {r['question']}\n"
        else:
            response += "您可以试试问我这些问题：\n"
            for i, q in enumerate(self.popular_questions[:3]):
                response += f"{i+1}. {q}\n"

        response += "\n或者换一种方式描述您的问题~"
        return response


_retriever = None

def get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever
