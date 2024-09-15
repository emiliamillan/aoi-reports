# Step 1: Use a Python base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy your application code into the container
COPY . /app

# Step 4: Install the necessary dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Step 5: Install PyInstaller to build the executable
RUN pip install pyinstaller

# Step 6: Build the executable using PyInstaller
RUN pyinstaller --onefile --windowed run.py

# Step 7: Define the entry point when the container is run
CMD ["python", "run.py"]
