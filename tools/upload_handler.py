# tools/upload_handler.py
from pathlib import Path
from tools.classifier import classify_text
from openai import OpenAI
import yaml

# 读取配置
cfg = yaml.safe_load(open("configs/settings.yaml", "r"))
client = OpenAI()

def llm_markdown_refine(raw_text: str, model="gpt-4o-mini"):
    """
    使用 LLM 将用户输入的内容润色成 Markdown 格式
    """
    prompt = f"""
你是一个专业的笔记排版助手。请将以下内容转换为结构化的 Markdown 格式，
保持信息完整，添加合适的标题、段落、列表、代码块（如有），并去掉冗余文字。

原始内容：
{raw_text}
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def save_uploaded_content(content, base_dir="data/notes"):
    """
    输入: 原始知识内容（str）
    功能: 1. 用 LLM 转为 Markdown
          2. 自动分类
          3. 保存为 .md 文件
    """
    # 1️⃣ Markdown 格式化
    refined_md = llm_markdown_refine(content)

    # 2️⃣ 分类
    category = classify_text(content)

    # 3️⃣ 创建分类文件夹
    category_dir = Path(base_dir) / category
    category_dir.mkdir(parents=True, exist_ok=True)

    # 4️⃣ 生成文件名
    files = list(category_dir.glob("note_*.md"))
    file_id = len(files) + 1
    file_path = category_dir / f"note_{file_id}.md"

    # 5️⃣ 保存 Markdown 文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# 分类：{category}\n\n")
        f.write(refined_md)

    print(f"✅ 已保存 Markdown 文件：{file_path}")
    return str(file_path), category
