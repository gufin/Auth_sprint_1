FROM python:3.10.2-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN  \
    apk update && \
    apk upgrade && \
    pip install --upgrade pip
COPY requirements.txt .
RUN   \
     apk add --no-cache postgresql-libs &&  \
     apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
     python3 -m pip install -r /app/requirements.txt --no-cache-dir &&  \
     apk --purge del .build-deps
COPY src/. .
CMD ["python", "app.py"]