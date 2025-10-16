FROM python:3.12.3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERD=1
WORKDIR /code/
COPY requirements.txt /code/
RUN pip install -r  requirements.txt
# Instalacja zależności systemowych potrzebnych do Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxfixes3 \
    libx11-xcb1 \
    libxcursor1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*


# Instalacja  Firefoxa
RUN playwright install firefox
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY . /code/