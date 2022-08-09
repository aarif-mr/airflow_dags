from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.hooks.base_hook import BaseHook
from airflow.providers.microsoft.azure.secrets.key_vault import AzureKeyVaultBackend
from airflow import DAG


def get_secrets(**kwargs):
    variable = AzureKeyVaultBackend().get_variable(key='var_name')
    print(variable)

dag = DAG('azure_key_vault_example_dag', start_date=datetime(2022, 1, 1), schedule_interval=None)

test_task = PythonOperator(task_id='test-task', python_callable=get_secrets, op_kwargs={'var_name': 'BDSQLXXXX'}, dag=dag)

test_task