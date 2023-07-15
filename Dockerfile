FROM python:latest
WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    tesseract-ocr libtesseract-dev \
    sane sane-utils xsane libsane-dev \
    curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    apt-get install -y npm && \
    node -v && npm -v

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

RUN mkdir -p scannedImages && touch image_database.db

COPY . .
WORKDIR /app/front-end

RUN npm install
WORKDIR /app

CMD [ "python", "run.py" ]
