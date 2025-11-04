import gradio as gr
from pathlib import Path
from tools.note_manager import add_note

from tools.file_loader import load_files
from tools.embedder import get_embeddings
from tools.retriever import build_vector_store, query
from openai import OpenAI

# === 初始化 ===
client = OpenAI()
DATA_DIR = Path("data/notes")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# === 构建向量数据库（初始化一次） ===
def build_collection():
    docs = load_files([str(DATA_DIR)])
    texts = [d["content"] for d in docs]
    if not texts:
        return None
    embeddings = get_embeddings(texts)
    collection = build_vector_store(texts, embeddings)
    return collection

collection = build_collection()


# === 回调函数 1：新增笔记 ===
def process_note(note_text):
    if not note_text.strip():
        return "⚠️ 请输入内容！"
    try:
        category, note_path = add_note(note_text)
        return f"✅ 分类：**{category}**\n📄 已保存到：`{note_path.resolve()}`"
    except Exception as e:
        return f"❌ 出错啦：{str(e)}"


# === 回调函数 2：查看历史笔记 ===
def show_notes():
    files = sorted(Path(DATA_DIR).rglob("*.md"))
    if not files:
        return "📭 暂无笔记，请先添加内容。"

    md_text = "## 📚 历史笔记列表\n"
    for f in files:
        md_text += f"- `{f}`\n"
    return md_text


# === 回调函数 3：自然语言检索分析 ===
def query_notes(query_text):
    if not query_text.strip():
        return "⚠️ 请输入查询内容！"

    # 确保数据库已加载
    global collection
    if collection is None:
        collection = build_collection()
        if collection is None:
            return "📭 当前还没有可用的笔记。"

    try:
        # 检索最相关的 3 条笔记内容
        results = query(collection, query_text, get_embeddings)
        context = "\n\n".join([doc for doc in results[0]])

        # 调用 LLM 进行总结与回答
        prompt = f"""
你是一个个人知识助手。根据以下资料回答问题。

问题：{query_text}
资料：
{context}

请用简洁的中文总结回答。
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ 检索或分析出错：{str(e)}"


# === 构建 Gradio 界面 ===
with gr.Blocks(title="🧠 Personal Knowledge Agent") as demo:
    gr.Markdown("## 🧠 Personal Knowledge Agent\n输入笔记即可分类保存，也可自然语言检索分析。")

    with gr.Tab("✏️ 添加笔记"):
        note_input = gr.Textbox(
            label="输入笔记内容",
            placeholder="在这里输入你的笔记...",
            lines=8,
        )
        note_output = gr.Markdown(label="输出结果")
        submit_btn = gr.Button("🚀 提交保存")
        submit_btn.click(fn=process_note, inputs=note_input, outputs=note_output)

    with gr.Tab("📚 查看历史笔记"):
        view_output = gr.Markdown()
        view_btn = gr.Button("📖 查看全部笔记")
        view_btn.click(fn=show_notes, outputs=view_output)

    with gr.Tab("🔍 查询笔记知识库"):
        query_input = gr.Textbox(
            label="自然语言查询",
            placeholder="例如：总结我写过的关于 RAG 的笔记",
            lines=3,
        )
        query_output = gr.Markdown(label="LLM 分析结果")
        query_btn = gr.Button("🔍 检索并分析")
        query_btn.click(fn=query_notes, inputs=query_input, outputs=query_output)

# === 启动应用 ===
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
