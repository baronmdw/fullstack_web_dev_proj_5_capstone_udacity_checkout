FROM python:3.11.1-slim

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
