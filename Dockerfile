FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露端口（根据你的项目调整）
EXPOSE 8080

# 运行命令（生产环境建议使用gunicorn）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
