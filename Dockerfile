FROM python:3.9-slim
WORKDIR /app
COPY ./requirements.txt /app/
COPY ./index.html /app/
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY main.py /app/
CMD  ["fastapi", "run", "main.py", "--port", "8000"]
