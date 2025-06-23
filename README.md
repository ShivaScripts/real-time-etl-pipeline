# 🚀 Real‑Time ETL Pipeline  
*A real‑time ETL pipeline leveraging Kafka, Spark, Airflow, and Docker containers.*  

---

## 📋 Summary  
This pipeline automatically generates example log messages, sends them through Kafka, saves the raw logs, cleans and analyzes them with Spark, and is scheduled and monitored by Airflow.
- 🔄 **Streaming Ingestion:** Apache Kafka ingests synthetic logs in real time.  
- 🤖 **Data Generation:** Python `Faker` library creates realistic fake log entries.  
- ⚡ **Stream Processing:** Spark Structured Streaming transforms and aggregates logs.  
- 📆 **Workflow Orchestration:** Airflow schedules & monitors your ETL DAG.  
- 🐳 **Containerized Deployment:** Docker Compose spins up Kafka, Spark, Airflow, etc.

---
## Architecture Diagram

![Architecture](assets/architecture.png)

---

## Demo / Screenshots

Below are key screenshots demonstrating the pipeline in action.

### 1. Airflow DAG Running
![Airflow DAG Working](assets/airflow.png)
*Airflow UI showing the `log_file_processor` DAG with tasks `run_producer`, `run_consumer`, and `process_raw_logs` all succeeding.*

---

### 2. Cleaned Data by Spark
![Spark Cleaned Data](assets/sparkc.png)
*Directory listing of cleaned JSON output under `data/processed_logs/cleaned`, produced by the Spark Structured Streaming job.*

---

### 3. Aggregated Metrics by Spark
![Spark Metrics](assets/sparkm.png)
*Directory listing of Parquet files under `data/processed_logs/metrics`, containing the 1-minute window aggregations.*

---

### 4. Raw Logs Stored
![Raw Logs](assets/raw.png)
*Directory listing of raw JSON log batches under `data/raw_logs`, showing files created by the Kafka consumer.*

---

## ✨ Features  
- **Real-Time Data Ingestion** via Kafka topics  
- **Synthetic Log Generation** with `Faker`  
- **Fault-Tolerant Stream Processing** using Spark (exactly-once semantics)  
- **DAG-Based Scheduling** through Airflow  
- **One‑Click Deployment** with Docker Compose  

---

## 🛠 Tech Stack  
- **Kafka** – Distributed streaming platform  
- **Spark Structured Streaming** – Scalable, fault-tolerant stream processing  
- **Airflow** – Workflow orchestration and scheduling  
- **Docker & Docker Compose** – Containerization and multi-service orchestration  
- **Python** – Core language for scripts  
- **Faker** – Synthetic data generation library  

---

## 🗂️ Folder Structure  
real_time_data_pipeline/
│
├── .gitignore
├── requirements.txt
├── docker-compose.yml         # (optional) for containerized Kafka/Spark/Airflow
├── docker/                    # Dockerfiles, if any
│   └── python-app/
│       └── Dockerfile
│
├── src/                       # Application source code
│   ├── producer/
│   │   └── producer.py        # Kafka producer: generates synthetic logs via Faker
│   ├── consumer/
│   │   └── consumer.py        # Kafka consumer: writes raw JSON to data/raw_logs/
│   └── sparkk/
│       └── spark_streaming_consumer.py  # Spark Structured Streaming job
│
├── airflow/
│   ├── dags/
│   │   └── log_file_processor_dag.py    # Airflow DAG orchestrating tasks
│   ├── webserver_config.py             # (optional) custom Airflow settings
│   └── logs/                           # Airflow runtime logs
│
├── data/                       # Local data storage (or mounted volumes)
│   ├── raw_logs/               # Raw JSON batches created by consumer
│   └── processed_logs/
│       ├── cleaned/            # Cleaned JSON output by Spark
│       └── metrics/            # Parquet metrics by Spark
│
├── assets/                     # Documentation assets
│   ├── architecture.png        # Architecture diagram
│   ├── airflow.png             # Airflow DAG screenshot
│   ├── sparkc.png              # Spark cleaned data screenshot
│   ├── sparkm.png              # Spark metrics screenshot
│   └── raw.png                 # Raw logs screenshot
│
└── README.md                   # This file

