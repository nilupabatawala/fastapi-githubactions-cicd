FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt, index.html /app/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY main.py /app/
CMD  ["fastapi", "run", "main.py", "--port", "8000"]