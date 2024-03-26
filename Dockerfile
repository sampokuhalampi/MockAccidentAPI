FROM python:3.12

RUN useradd -m appuser

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt && chown -R appuser /app
USER appuser

ENTRYPOINT ["python3", "-m"]
CMD ["flask", "run"]
EXPOSE 5000
