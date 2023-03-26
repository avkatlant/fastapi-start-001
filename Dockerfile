FROM python:3.10-slim

# set work directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# Flag to optimize container size a bit by removing runtime python cache
ENV PYTHONDONTWRITEBYTECODE 1
# This flag is important to output python logs correctly in docker!
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy and run entrypoint.sh
COPY ./entrypoint_db.sh /usr/src/app/entrypoint_db.sh
RUN ["chmod", "a+x", "/usr/src/app/entrypoint_db.sh"]
ENTRYPOINT ["sh", "/usr/src/app/entrypoint_db.sh"]
