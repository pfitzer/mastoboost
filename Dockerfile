FROM python:3.11

RUN apt update && apt upgrade -y

EXPOSE 80
EXPOSE 443

WORKDIR /app

ADD . /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Executing crontab command
CMD ["tail", "-f", "/dev/null"]