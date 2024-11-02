# Start with a base Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Update and install basic system dependencies
RUN apt-get update
RUN apt-get install -y gcc build-essential libffi-dev libssl-dev wget

# Download TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz

# Extract TA-Lib
RUN tar -xzf ta-lib-0.4.0-src.tar.gz

# Build and install TA-Lib
RUN cd ta-lib && ./configure --prefix=/usr && make && make install

# Clean up TA-Lib source files and package manager cache
RUN rm -rf ta-lib ta-lib-0.4.0-src.tar.gz
RUN apt-get clean

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 5000 if you are using a web interface
EXPOSE 5000

# Run Auto-GPT Advanced as the entrypoint
CMD ["python", "autogpt.py"]

