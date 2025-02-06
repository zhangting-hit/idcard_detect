# 使用官方的 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件到工作目录
COPY requirements.txt .

# 安装 Python 依赖
RUN ["pip", "install", "-r", "requirements.txt"]

# 复制当前目录所有内容到工作目录
COPY . .

# 暴露端口
EXPOSE 4998

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 运行 Flask 应用
CMD ["python", "app.py"]
