FROM python:3.10-alpine

# Actualiza el índice de paquetes e instala apk-tools
RUN apk update && apk add --no-cache apk-tools

RUN apk add --no-cache git postgresql-dev gcc libc-dev nano
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

RUN git clone https://github.com/HouseRent16/PGPI-G2.11.git PGPI-G2.11
WORKDIR /app/PGPI-G2.11
RUN pip install -r requirements.txt

COPY settings.py /app/src/houseRent/houseRent/settings.py

WORKDIR /app/PGPI-G2.11
RUN chmod +x ./init.sh
CMD ["sh", "init.sh"]