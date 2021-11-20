FROM python:latest

# Environment variables

# ENV BACKING_REDIS_ADDRESS=
# ENV CACHE_EXPIRY_TIME=
# ENV CACHE_CAPACITY=
# ENV IP_ADDRESS=
# ENV PORT=
ENV FLASK_APP=routes.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /usr/app/src/assignment

COPY ./requirements.txt /usr/app/src/assignment/requirements.txt
RUN pip install -r requirements.txt

# Add remote file to root directory in container
COPY . /usr/app/src/assignment

CMD [ "python3", "-m", "flask", "run"]

EXPOSE 5000
