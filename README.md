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

## 🎥 Demo  
![Pipeline Demo](demo.gif)  
*Placeholder GIF showing logs flowing through Kafka → Spark → Airflow.*

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
