# Use official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency requirements file first (to leverage Docker layer caching)
COPY requirements.txt .

# Install dependencies without caching the index files locally (keeps image size small)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the working directory
COPY . .

# Run the FastAPI server using Uvicorn, binding to 0.0.0.0 on port 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]