FROM python:3.9.18-slim-bullseye

EXPOSE 8000

WORKDIR /app

RUN apt update && apt install -y netcat

COPY --chmod=755 ./entrypoint.sh .

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN python -m pytest

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
