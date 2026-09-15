FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install nginx -y
COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 80


CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]