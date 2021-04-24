FROM python:3.8.6

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt

CMD gunicorn foodgram.wsgi --bind 0.0.0.0:8000