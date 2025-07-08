FROM python:3.11

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && \
    apt-get install -y wget gnupg curl ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 \
        libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils libgbm1 \
        libgtk-3-0 libxshmfence1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright and its browsers
RUN pip install playwright && playwright install --with-deps

# Copy app source
COPY . .

# Expose Flask port
EXPOSE 8000

CMD ["python3", "main.py"]
