# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Create virtual environment
RUN python -m venv /app/venv

# Ensure venv is used
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements first (better caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy rest of the project
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
