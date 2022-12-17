FROM python:3.11.1-slim-buster
WORKDIR /app
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY . .
ENV GCP_KEY_PATH=/app/gcp_service_key.json
ENV PERFORMANCE_GRAPH_OUTPUT_PATH=/
ENV TRANSACTIONS_OUTPUT_PATH=/
ENTRYPOINT [ "python3" ]
CMD ["./src/main.py", "gcp"]
