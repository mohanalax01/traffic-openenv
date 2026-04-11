FROM python:3.10

WORKDIR /app

# Copy all files into /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Instead of changing WORKDIR again, run the app from /app 
# and point to the file inside the server folder.
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
