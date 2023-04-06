#FROM python:3.9.13
FROM python:3.9.13-slim

#WORKDIR /app

# dont write pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# dont buffer to stdout/stderr
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
RUN mkdir /app/config
RUN mkdir /app/logs

# dependencies
#RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# RUN apk add python3
# RUN apk add py3-pip
# RUN apk update
RUN apt-get update
# use the -y yes option to run it
RUN apt-get install -y build-essential
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

WORKDIR /app
EXPOSE 8020
#ENTRYPOINT [ "python3" ]
#CMD ["uvicorn", "src.main:app"]
#CMD ["python3", "main.py"]
# If running behind a proxy like Nginx or Traefik add --proxy-headers
# For the container to accept any ingress IP, we need to add 0.0.0.0 (which is correct for the fa-signal-receiver, which needs to expose it's api to the outside.)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8020", "--root-path", "/signal-ingress"]
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8020"]
