FROM python:3.13-alpine3

WORKDIR /app

COPY ./requirements.txt ./
COPY ./data.json ./

COPY ./tests ./tests
COPY ./prints ./prints
COPY ./reports ./reports

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "bash"]