FROM python:3-slim AS builder

RUN python -m pip install --upgrade pip
RUN apt update
RUN apt install -y build-essential

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

FROM python:3-slim

RUN python -m pip install --upgrade pip
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

WORKDIR app/
COPY app/ .

CMD [ "python", "./main.py" ]
