FROM python:3.9

EXPOSE 80
EXPOSE 443

WORKDIR /app

COPY ./crontab /etc/cron.d/crontab
ADD . /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt

RUN apt update && apt install cron -y
# run the crontab file
RUN crontab /etc/cron.d/crontab

# Executing crontab command
CMD ["cron", "-f"]