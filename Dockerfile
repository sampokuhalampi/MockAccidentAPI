FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "-m"]
CMD ["flask", "run"]
EXPOSE 5000
