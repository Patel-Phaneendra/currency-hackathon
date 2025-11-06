FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt
COPY . .
ENV ALPHAVANTAGE_API_KEY=""
ENTRYPOINT ["python3", "autodocsflow.py"]
