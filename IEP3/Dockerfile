# Use official Python image
FROM python:3.10.8

# Create working directory
RUN mkdir -p /app/backend
WORKDIR /app/backend

# Copy requirements.txt to leverage Docker cache
COPY FastAPI_Backend/requirements.txt .

# Install dependencies (cached if requirements.txt doesn't change)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Then copy the rest of your app code
COPY FastAPI_Backend/ .
COPY Data /app/Data

# Expose FastAPI port
EXPOSE 8051

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8051", "--reload"]
