# pull official base image
FROM python:3.10-slim-bullseye

# create directory for the app user
RUN mkdir -p /home/wasp

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/home/wasp/.local/bin:${PATH}"

# # create the app user
# RUN addgroup -S wasp && adduser -S wasp -G wasp

# create the appropriate directories
ENV HOME=/home/wasp
ENV APP_HOME=/home/wasp/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

# chown all the files to the app user
# RUN chown -R wasp:wasp $HOME
# RUN chown -R wasp:wasp $APP_HOME

# install dependencies
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install build-essential libssl-dev libffi-dev libblas3 libc6 libpq-dev gcc python3-dev python3-pip cython3
RUN apt-get -y install python3-numpy python3-scipy 
RUN apt install -y netcat

# # change to the app user
# USER wasp

RUN pip install --upgrade pip setuptools wheel

COPY ./project/requirements.txt $APP_HOME
RUN pip --default-timeout=1000 install -r requirements.txt --user

COPY ./entrypoint.prod.sh $APP_HOME
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
RUN chmod +x  $APP_HOME/entrypoint.prod.sh

# copy project
COPY ./project $APP_HOME

# run entrypoint.prod.sh
ENTRYPOINT ["/home/wasp/app/entrypoint.prod.sh"]

# chown all the files to the app user
# RUN chown -R wasp:wasp $HOME
# RUN chown -R wasp:wasp $APP_HOME
