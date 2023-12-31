FROM python:latest

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "advert.py"]