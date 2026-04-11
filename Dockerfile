FROM python:3.10

WORKDIR /app

# Copy everything to the root so env.py is easily importable
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Start from root, pointing to the app inside the server folder
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
