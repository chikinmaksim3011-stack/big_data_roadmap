from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def print_hello():
    print("Hello from Airflow! Analytics roadmap is on track.")

default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'my_first_dag',
    default_args=default_args,
    description='My first DAG for analytics roadmap',
    schedule=timedelta(days=1),
    catchup=False
)

task1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag
)

task2 = PythonOperator(
    task_id='hello_python',
    python_callable=print_hello,
    dag=dag
)

task1 >> task2