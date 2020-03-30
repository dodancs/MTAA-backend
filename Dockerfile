FROM python:3.7

EXPOSE 5000/tcp

# Install Python requirements

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
RUN rm requirements.txt

# Create data directory for the volume
RUN mkdir /opt/mtaa-backend/
COPY . ./opt/mtaa-backend/
VOLUME /opt/mtaa-backend/

# Set the work directory

WORKDIR /opt/mtaa-backend/

CMD [ "python", "./server.py" ]
