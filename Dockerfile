FROM python:3.7

EXPOSE 5000/tcp

WORKDIR /opt/mtaa-backend/

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
#COPY . ./opt/mtaa-backend/

CMD [ "python", "./server.py" ]
