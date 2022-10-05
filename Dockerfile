FROM python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY ./startmarketplace.sh .
RUN chmod +x startmarketplace.sh

WORKDIR /app
