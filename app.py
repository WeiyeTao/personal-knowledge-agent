import yaml
from pathlib import Path
from openai import OpenAI
from tools.classifier import classify_text

# 初始化 OpenAI 客户端
client = OpenAI()

def llm_refine_markdown(note_text: str, model="gpt-4o-mini"):
    """调用 LLM 将笔记内容转为 Markdown 格式"""
    prompt = f"""
你是一个知识笔记助手。
请把下面的内容润色为结构化的 Markdown 格式：
- 添加合理的标题（如 ## 概念、### 步骤等）
- 保持原意，提炼要点，优化格式
- 使用简体中文输出

原始内容：
{note_text}
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


def add_note(note_text: str):
    """输入笔记 → LLM Markdown润色 → 自动分类 → 保存为.md文件"""
    # 1️⃣ 调用 LLM 进行 Markdown 润色
    refined_md = llm_refine_markdown(note_text)
    print("🪄 已通过 LLM 生成 Markdown 格式笔记。")

    # 2️⃣ 调用分类器
    category = classify_text(note_text)
    print(f"[classify] 笔记分类为：{category}")

    # 3️⃣ 创建对应类别目录
    category_dir = Path(f"data/notes/{category}")
    category_dir.mkdir(parents=True, exist_ok=True)

    # 4️⃣ 生成新文件名（避免覆盖）
    files = list(category_dir.glob("note_*.md"))
    note_id = len(files) + 1
    note_path = category_dir / f"note_{note_id}.md"

    # 5️⃣ 写入 Markdown 文件
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(f"# 分类：{category}\n\n")
        f.write(refined_md)

    print(f"[save] ✅ 笔记已保存到：{note_path.resolve()}")
    return category, note_path


if __name__ == "__main__":
    print("=== 🧠 Personal Knowledge Agent Markdown 分类笔记 ===")
    note = input("请输入一段笔记内容（自动分类 + Markdown润色保存）:\n> ")

    if not note.strip():
        print("⚠️ 输入为空，已退出。")
    else:
        add_note(note)
