from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.providers.microsoft.azure.secrets.key_vault import AzureKeyVaultBackend
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def creds():
    credential = DefaultAzureCredential()
    x=AzureKeyVaultBackend()
    xv=x.client()
    print(xv)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
        dag_id='test_backend_operators',
        default_args=default_args,
        schedule_interval=None,
        start_date=days_ago(1),
        tags=["tests", "data-lake"]
) as dag:

    start_node: DummyOperator = DummyOperator(task_id="start")

    with TaskGroup("test_layer", tooltip="Test Azure Secrets Layer") as test_layer:
    
        bash_test_node_1 = \
            PythonOperator(task_id='test-task', python_callable=creds, dag=dag) 
        
        bash_test_node_2 = \
            BashOperator(
                task_id="test_secrets_short",
                bash_command="echo {{ var.value.dummy }}")     


    end_node: DummyOperator = DummyOperator(task_id='end')

    start_node >> test_layer >> end_node
