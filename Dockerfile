FROM python:3.10

WORKDIR /app

# Copy all files to /app root
COPY . .

# Install all necessary dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Run uvicorn from the root directory
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
