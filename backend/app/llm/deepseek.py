import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class DeepSeekClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")

        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

        self.system_prompt = """你是"小粉助手"，RoboMaster机甲大师赛的官方AI问答机器人。

## 你的职责
1. 回答用户关于RoboMaster赛事的问题
2. 友好地处理用户的闲聊，但要引导回赛事主题
3. 拒绝回答敏感、违规或与赛事无关的专业问题

## 回答规则
1. 回答要简洁友好，控制在200字以内
2. 如果提供了参考资料，优先基于参考资料回答
3. 如果参考资料不足以回答，可以基于你对RoboMaster的了解补充
4. 对于敏感问题，礼貌拒绝并引导到官方渠道：
   - 官网：www.robomaster.com
   - 邮箱：robomaster@dji.com
5. 对于完全无关的问题，友好地说明你的职责范围

## 语气风格
- 活泼友好，可以适当使用表情
- 专业但不生硬
- 像一个热情的赛事志愿者"""

    def chat(self, user_message: str, context: str = None) -> str:
        """与DeepSeek对话"""
        system_content = self.system_prompt
        if context:
            system_content += f"\n\n## 参考资料\n{context}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"DeepSeek API error: {e}")
            return None


_deepseek_client = None

def get_deepseek_client() -> DeepSeekClient:
    global _deepseek_client
    if _deepseek_client is None:
        _deepseek_client = DeepSeekClient()
    return _deepseek_client
