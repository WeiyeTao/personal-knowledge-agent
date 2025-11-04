"""
file_loader.py
--------------
负责加载本地文件（文本、代码、图片等），
并将其内容整理为可嵌入的文本格式。

返回数据格式：
[
    {"path": "data/notes/example.md", "content": "...文件文本内容..."},
    {"path": "data/code/demo.py", "content": "...代码内容..."}
]
"""

from pathlib import Path
import mimetypes

def load_files(folder_paths):
    """
    遍历指定文件夹，读取其中的文本或代码文件内容。
    返回 [{'path': str, 'content': str}, ...]
    """
    docs = []

    for folder in folder_paths:
        folder = Path(folder)
        if not folder.exists():
            print(f"[warn] 文件夹不存在: {folder}")
            continue

        for file in folder.rglob("*"):
            if not file.is_file():
                continue

            mime, _ = mimetypes.guess_type(file)
            suffix = file.suffix.lower()

            try:
                # 处理文本文件
                if suffix in [".txt", ".md", ".py", ".json", ".csv"]:
                    text = file.read_text(encoding="utf-8", errors="ignore")
                    docs.append({"path": str(file), "content": text})

                # 处理图片文件（这里只记录文件名）
                elif suffix in [".png", ".jpg", ".jpeg"]:
                    docs.append({"path": str(file), "content": f"[图片文件] {file.name}"})

                # 其他文件类型可扩展
                else:
                    print(f"[skip] 不支持的文件类型: {file.name}")

            except Exception as e:
                print(f"[error] 无法读取文件 {file}: {e}")

    print(f"[load_files] 已加载 {len(docs)} 个文件")
    return docs
