# Synthex

**Synthex** is an AI-powered document and meeting analysis tool designed to extract key insights from PDFs, audio files, and video meetings. Using **Generative AI** and **speech-to-text models** like **Whisper**, Synthex processes both documents and meeting content to generate summaries and provide intelligent responses to queries.

## Features

- Summarizes PDF documents and audio from meetings.
- Uses Whisper for high-quality speech recognition.
- Processes audio and video files using **FFmpeg**.
- Provides intelligent answers to queries on internal documents and meeting discussions.
- Designed for ease of deployment with **Docker**.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
   - [Clone the Repository](#clone-the-repository)
   - [Using Docker](#using-docker)
3. [Building the Docker Image](#building-the-docker-image)
4. [Running the Docker Container](#running-the-docker-container)
5. [Accessing the Application](#accessing-the-application)
6. [License](#license)

---

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Git**: [Download and install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose (optional)**: Recommended for multi-container applications.

---

## Installation

### Clone the Repository

To get started, clone the **Synthex** repository:

```bash
git clone https://github.com/RounakRaman/SyntheX.git
cd SyntheX
```
## Using Docker

Since **Synthex** relies on heavy dependencies like **Whisper** and **FFmpeg**, Docker is recommended for a smooth, isolated setup.

### Dockerfile

Ensure you have a `Dockerfile` that contains all the necessary instructions. Here’s a basic example:

```Dockerfile
# Use official Python base image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy contents to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Expose port for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "synthex.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
## Building the Docker Image

To build the Docker image for **Synthex**, follow these steps:

```bash
docker build -t synthex-app .
```
## Running the Docker Container

Once the Docker image is built, you can run the container using:

```bash

docker run -d -p 8501:8501 synthex-app
```

- -d: Runs the container in detached mode.
- -p 8501:8501: Maps the container’s port 8501 to the host’s port 8501.
- synthex-app: The Docker image name.-  
## Running in Interactive Mode

If you need to access the container for debugging, you can run:

```bash

docker run -it synthex-app /bin/bash
```
## Accessing the Application
Once the container is running, you can access the Synthex application in your browser:

```bash
Copy code
http://localhost:8501
```

## For access over a local network (other devices connected to the same network), use:

```bash

http://<your_local_ip>:8501
```
To find your local IP address:

On Linux/macOS, run: ifconfig
On Windows, run: ipconfig


## Build the Docker image:

```bash

docker build -t synthex-app .
```
## Run the container:

```bash

docker run -d -p 8501:8501 synthex-app
```
## Stop the container:

```bash

docker stop <container_id>
```
## View running containers:
```bash

docker ps
```


## License
Distributed under the MIT License. See LICENSE for more information.



You can copy and paste this content directly into your `README.md` file for GitHub or any markdown-supported platform.





 


