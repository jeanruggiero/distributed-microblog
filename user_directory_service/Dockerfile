FROM python:3.9.6-alpine3.14

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR code/
COPY src ./src
COPY main.py .

EXPOSE 8080

CMD ["python3", "main.py"]
