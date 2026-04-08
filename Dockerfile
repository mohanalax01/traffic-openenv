FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
# Copy everything from your repo to the container
COPY . .

# Ensure the server folder is explicitly recognized
RUN pip install -e .
