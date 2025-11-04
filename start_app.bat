@echo off
echo 🚀 启动 Personal Knowledge Agent ...
cd /d D:\personal-knowledge-agent
call conda activate pk-agent
python -m ui.gradio_app
pause
