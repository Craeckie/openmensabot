FROM python:3-alpine

RUN mkdir -p /opt/bot

ENV VIRTUAL_ENV=/opt/bot/env
RUN pip install --upgrade pip && \
    #apk add libxml2-dev libxslt-dev && \
    #apk clean && \
    python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin/:$PATH"

WORKDIR /opt/bot
COPY ./ /opt/bot

RUN apk add --virtual .build build-base && \
    pip install -r requirements.txt && \
    apk del .build && apk clean

CMD ["python3", "wsgi.py"]
