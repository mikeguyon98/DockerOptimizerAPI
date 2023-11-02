# Use the Docker-in-Docker base image
FROM docker:dind

# Update and install dependencies
RUN apk update && \
    apk add --no-cache \
    bash \
    curl \
    python3 \
    py3-pip \
    tar \
    xz

# Install Dive from the Alpine testing repository
RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    apk add dive@testing

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY . /app
WORKDIR /app

# Copy the start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose the port your application runs on
EXPOSE 5000

# Start the Docker daemon and then run the application
ENTRYPOINT ["/start.sh"]
