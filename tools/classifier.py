"""
classifier.py
-------------
根据笔记内容自动判断主题类别，并返回类别名。
"""

from openai import OpenAI
import re

client = OpenAI()

CATEGORIES = [
    "LLM", "LangChain", "Reinforcement Learning", "Python",
    "Data Science", "Robotics", "AI Agent", "Other"
]

def classify_text(text: str, model="gpt-4o-mini") -> str:
    """
    使用 LLM 根据内容分类。
    返回类别字符串。
    """
    prompt = f"""
你是一个笔记分类助手。
请从以下类别中选择最适合的一个：
{', '.join(CATEGORIES)}。
如果都不符合，请输出 'Other'。

笔记内容如下：
{text[:800]}
请只输出类别名。
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        category = response.choices[0].message.content.strip()
        # 清理可能的多余字符
        category = re.sub(r"[^a-zA-Z0-9_\- ]", "", category)
        return category or "Other"
    except Exception as e:
        print(f"[error] 分类失败: {e}")
        return "Other"
