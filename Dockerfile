# 使用官方 Python 运行时作为父镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /workspace

# 设置环境变量，确保 Python 输出直接打印到控制台，不进行缓冲
ENV PYTHONUNBUFFERED=1

# 安装 uv 以加快依赖安装速度，使用阿里云镜像加速
RUN pip install --no-cache-dir uv -i https://mirrors.aliyun.com/pypi/simple/

# 首先只复制 requirements.txt 以利用 Docker 缓存
COPY backend/requirements.txt ./backend/

# 使用 uv 安装 Python 依赖，配置阿里云镜像
# --system 标志告诉 uv 将包安装到系统 Python 环境中
RUN uv pip install --system --no-cache -r backend/requirements.txt --index-url https://mirrors.aliyun.com/pypi/simple/

# 复制项目的所有文件
COPY . .

# 暴露后端运行的端口
EXPOSE 8000

# 设置默认环境变量（可以在运行时通过 docker run -e 覆盖）
ENV HOST=0.0.0.0
ENV PORT=8000
ENV UVICORN_RELOAD=false

# 启动应用程序
# 使用 python -m uvicorn 直接启动，以便更好地处理信号
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]