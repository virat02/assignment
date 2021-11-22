FROM python:latest

# Environment variables

# ENV BACKING_REDIS_ADDRESS=
# ENV CACHE_EXPIRY_TIME=
# ENV CACHE_CAPACITY=
# ENV IP_ADDRESS=
# ENV PORT=

WORKDIR /usr/assignment/app/

COPY requirements.txt /usr/assignment/app/requirements.txt
RUN pip3 install -r requirements.txt

# Add remote file to root directory in container
COPY ./app /usr/assignment/app/

CMD [ "python3", "-u", "routes.py"]

EXPOSE 5000
