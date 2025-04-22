FROM python:3.13

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt
COPY ./asr_api.py /app/

CMD ["fastapi", "run", "asr_api.py", "--port", "8001"]