FROM python:3.10.5 as base

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
COPY scripts/ /scripts
RUN apt-get update \
    && apt-get install unixodbc -y \
    && apt-get install unixodbc-dev -y \ 
    && python -m pip install --upgrade pip && pip install -r /tmp/requirements.txt \
    && chmod -R +x /scripts

COPY . /app
EXPOSE 5000

ENV PATH="/scripts:usr/local/bin:$PATH"
ENTRYPOINT [ "automation.sh" ]