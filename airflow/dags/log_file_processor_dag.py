from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# -------------------------------------
# CONFIGURATION
# -------------------------------------
default_args = {
    'owner': 'shivam',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

PRODUCER_SCRIPT_PATH = '/Users/Shivam/Documents/real_time_data_pipeline/src/producer/producer.py'
CONSUMER_SCRIPT_PATH = '/Users/Shivam/Documents/real_time_data_pipeline/src/consumer/consumer.py'
SPARK_PROCESSOR_PATH = '/Users/Shivam/Documents/real_time_data_pipeline/src/sparkk/spark_streaming_consumer.py'
SPARK_SUBMIT = '/Users/Shivam/spark/bin/spark-submit'  # absolute path to spark-submit

# -------------------------------------
# DAG DEFINITION
# -------------------------------------
with DAG(
    dag_id='log_file_processor',
    default_args=default_args,
    description='Process raw log files from Kafka sink',
    schedule_interval="*/10 * * * * *",  # every 10 seconds
    start_date=days_ago(0),
    catchup=False,
    tags=['real-time'],
) as dag:

    # Step 1: Produce logs
    producer_task = BashOperator(
        task_id='run_producer',
        bash_command=(
            f'python3 "{PRODUCER_SCRIPT_PATH}"'
            ' & sleep 5; pkill -f producer.py'
        ),
    )

    # Step 2: Consume logs
    consumer_task = BashOperator(
        task_id='run_consumer',
        bash_command=(
            f'python3 "{CONSUMER_SCRIPT_PATH}"'
            ' & sleep 5; pkill -f consumer.py'
        ),
    )

    # Step 3: Process logs with Spark (include Kafka connector)
    task_process_logs = BashOperator(
        task_id='process_raw_logs',
        bash_command=(
            f'{SPARK_SUBMIT} '
            '--master "local[*]" '
            '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 '
            f'"{SPARK_PROCESSOR_PATH}"'
        ),
    )

    # Task order
    producer_task >> consumer_task >> task_process_logs
