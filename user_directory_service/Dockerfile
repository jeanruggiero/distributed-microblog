FROM python:3.9.6-alpine3.14

WORKDIR /code

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "main.py"]
