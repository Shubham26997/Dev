FROM python:3.12

WORKDIR /app

RUN pip install Django==6.0

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]