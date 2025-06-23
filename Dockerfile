FROM python:3.10-slim-bullseye
COPY . /app

WORKDIR /app

# Must install R
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update && \
    apt-get install -y ncbi-blast+ && \
    apt-get install -y r-base && \
    R -e "install.packages('protr')" && \
    pip install --upgrade pip &&  \
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.headless=true", "--browser.gatherUsageStats=false"]
