FROM python:3.9.6

WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y tzdata
 
# timezone env with default
ENV TZ=Europe/Moscow
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]