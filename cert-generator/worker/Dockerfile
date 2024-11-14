FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wkhtmltopdf && \
    rm -rf /var/lib/apt/lists/*  # Limpar cache de pacotes para reduzir o tamanho da imagem

WORKDIR /worker

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PATH="/usr/local/bin:$PATH"

CMD ["python", "worker.py"]
