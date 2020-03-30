FROM python:3.7

WORKDIR ./

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "./server.py" ]
