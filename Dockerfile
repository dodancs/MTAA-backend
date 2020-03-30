FROM python:3.7

EXPOSE 5000/tcp

WORKDIR ./

COPY requirements.txt ./opt/mtaa-backend/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./opt/mtaa-backend/requirements.txt
COPY . ./opt/mtaa-backend/

CMD [ "python", "./opt/mtaa-backend/server.py" ]
