
FROM python:3.10-slim
WORKDIR /app

# 👇 Instala ping (iputils-ping)
RUN apt-get update && apt-get install -y iputils-ping && apt-get clean

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
