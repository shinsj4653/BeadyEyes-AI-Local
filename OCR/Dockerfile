From ubuntu:latest

# Path: dockerfile
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip
    libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV IMAGE_URI ""
ENV GOOGLE_APPLICATION_CREDENTIALS="ocrAccountKey.json"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

