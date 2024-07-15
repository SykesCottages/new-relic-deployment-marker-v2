FROM python:3.11-slim

WORKDIR /usr/src/app

COPY pipe/pipe.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "pipe.py"]