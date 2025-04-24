FROM python:3.13-alpine@sha256:18159b2be11db91f84b8f8f655cd860f805dbd9e49a583ddaac8ab39bf4fe1a7

WORKDIR /app

COPY ./requirements.txt ./
COPY ./data.json ./

COPY ./tests ./tests
COPY ./prints ./prints
COPY ./reports ./reports

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /app/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  chown -R duser:duser /venv

ENV PATH="/venv/bin:$PATH"

USER duser

CMD ["sh"]