FROM python:3.10-slim-bullseye
COPY . /app

WORKDIR /app

# Must install R
RUN apt-get update && \
    apt-get install -y r-base && \
    pip install --upgrade pip &&  \
    pip install -r requirements.txt && \
    apt-get install -y ncbi-blast+ && \
    rm -rf /var/lib/apt/lists/*

RUN R -e "install.packages('protr')"

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
