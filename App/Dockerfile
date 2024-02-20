FROM python:3.6-slim-buster

WORKDIR /app

COPY requeriments.txt ./

RUN pip install -r requeriments.txt

COPY . .

EXPOSE 4000

CMD [ "flask", "run", "--host=0.0.0.0", "port=4000"]