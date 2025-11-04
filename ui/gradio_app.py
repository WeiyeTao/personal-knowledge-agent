import gradio as gr
from pathlib import Path
from openai import OpenAI
import yaml

from tools.file_loader import load_files
from tools.embedder import get_embeddings
from tools.retriever import build_vector_store, query


# === 初始化 ===
client = OpenAI()
cfg = yaml.safe_load(open("configs/settings.yaml", "r"))
DATA_DIR = Path("data/uploads")
DATA_DIR.mkdir(parents=True, exist_ok=True)


# === 处理文件上传 ===
def process_files(files):
    """保存上传的文件并加载为文本"""
    saved_files = []
    for f in files:
        dest = DATA_DIR / Path(f.name).name
        with open(dest, "wb") as out:
            out.write(f.read())
        saved_files.append(str(dest))

    # 加载文本
    docs = load_files([str(DATA_DIR)])
    texts = [d["content"] for d in docs]
    embeddings = get_embeddings(texts)
    collection = build_vector_store(texts, embeddings)
    return "✅ 已成功加载并嵌入文件", collection


# === 处理自然语言指令 ===
def handle_query(query_text, collection):
    """根据用户自然语言指令检索 + 调用 LLM"""
    if not query_text.strip():
        return "请输入内容。"

    results = query(collection, query_text, get_embeddings)
    context = "\n\n".join([doc for doc in results[0]])

    prompt = f"""
你是一个个人知识助手，请结合以下内容回答问题。
如果文件中包含代码，请解释代码逻辑。
如果是图片，请描述它的内容。

问题：{query_text}
相关资料：
{context}
"""
    response = client.chat.completions.create(
        model=cfg["model"]["llm_model"],
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# === 构建 Gradio 界面 ===
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Personal Knowledge Agent")
    gr.Markdown("上传文档或输入自然语言指令，AI 将帮助你整理、理解与生成内容。")

    with gr.Row():
        upload = gr.Files(label="📂 上传文件（代码 / 图片 / 文本）")
        output_status = gr.Textbox(label="系统状态", interactive=False)

    query_box = gr.Textbox(label="💬 输入你的问题 / 指令", placeholder="例如：请解释我上传的代码逻辑")
    result_box = gr.Textbox(label="🧠 智能回答", lines=8)

    collection_state = gr.State(None)

    upload.upload(process_files, upload, [output_status, collection_state])
    query_box.submit(handle_query, [query_box, collection_state], result_box)

demo.launch(server_name="0.0.0.0", server_port=7860)
