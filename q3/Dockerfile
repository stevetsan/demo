FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000
RUN chmod +x ./script.sh
CMD ["./script.sh"]
#CMD ["python3", "database/db_init.py"] && ["python3", "app.py"]
