# Use a slim Python image as the base
FROM python:3.12-slim


# Install system dependencies, including FFmpeg and other necessary libraries
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Whisper dependencies
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy the entire project into the container
COPY . /app

# Set the working directory inside the container
WORKDIR /app/app

# Install Python dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Expose the port that Streamlit runs on (8501 by default)
# EXPOSE 8501

# Run the Streamlit app
ENTRYPOINT [ "streamlit","run","synthex.py"]
