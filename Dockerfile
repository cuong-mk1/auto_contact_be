FROM python:3.12

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libgbm1 \
    libasound2 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxshmfence1 \
    libglib2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcursor1 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for Playwright
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
COPY .env.dev .env
RUN pip install --no-cache-dir -r requirements.txt

RUN pip uninstall browser_use -y
RUN pip install browser_use==0.1.40
RUN pip install langchain_anthropic==0.3.3

# Install playwright and its browsers
RUN pip install --no-cache-dir playwright && \
    playwright install chromium
# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99


# Install Chrome WebDriver
# RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
#     mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
#     unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     rm /tmp/chromedriver_linux64.zip && \
#     chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
#     ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     default-mysql-client \
#     wget \
#     gnupg \
#     unzip \
#     xvfb && \
#     wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
#     apt-get update && apt-get install -y --no-install-recommends google-chrome-stable && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*


# Install Chrome
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
#     && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install \
#     && rm google-chrome-stable_current_amd64.deb

# # Install ChromeDriver
# RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
#     wget -q "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" && \
#     unzip chromedriver_linux64.zip && \
#     mv chromedriver /usr/local/bin/ && \
#     chmod +x /usr/local/bin/chromedriver && \
#     rm chromedriver_linux64.zip
COPY . .

# RUN python install_chrome.py
# RUN chmod +x /root/.wdm/drivers/chromedriver/linux64/134.0.6998.88/chromedriver-linux64/chromedriver

EXPOSE 5000
# Define environment variable
CMD ["gunicorn", "--workers=1","--bind=0.0.0.0:5000","--timeout=6000","--log-level=debug", "--access-logfile=-", "--error-logfile=-", "app:app","debug=True"]
