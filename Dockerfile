FROM python:3.8-slim-buster

WORKDIR /app

COPY ./app/requirements.txt /requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt
# copy script
COPY ./app/main.py /app/main.py

# copy models
COPY ./app/models /app/models

# copy routes
COPY ./app/routes /app/routes

# copy utils
COPY ./app/utils /app/utils

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]
