From python:3.10.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN rm -r data


CMD ["python3", "-m", "main", "-u"]