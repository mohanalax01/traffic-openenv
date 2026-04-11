FROM python:3.10

# Keep the working directory at /app
WORKDIR /app

# Copy all files from your repo into /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app. Because we are in /app, 'server.app:app' works perfectly.
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
