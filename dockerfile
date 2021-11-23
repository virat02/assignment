FROM python:latest

# Environment variables

ENV PROXY_ADDRESS ${PROXY_ADDRESS}
ENV MAX_CLIENTS ${MAX_CLIENTS}
ENV MAX_REQUESTS ${MAX_REQUESTS}

WORKDIR /usr/assignment/app/

COPY requirements.txt /usr/assignment/app/requirements.txt
RUN pip3 install -r requirements.txt

# Add remote file to root directory in container
COPY . /usr/assignment

EXPOSE 5000

COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]