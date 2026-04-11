FROM python:3.10

WORKDIR /app

# Copy all files to the root folder
COPY . .

# Install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Run uvicorn from the root, pointing to the app inside the server folder 
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
