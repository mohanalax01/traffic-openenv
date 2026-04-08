FRFROM python:3.9

WORKDIR /code

# Copy requirements first for faster building
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the files (including the server folder)
COPY . .

# Install the current directory as a package without "editable" mode
RUN pip install .

# Set the command to run your server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
