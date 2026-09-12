FROM python:3.11-slim
WORKDIR /app

# تثبيت المتطلبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# انسخ التطبيق
COPY . .

# متغيرات بيئية آمنة تفضل وضعها عبر GitHub Secrets أو ENV عند التشغيل
ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]
