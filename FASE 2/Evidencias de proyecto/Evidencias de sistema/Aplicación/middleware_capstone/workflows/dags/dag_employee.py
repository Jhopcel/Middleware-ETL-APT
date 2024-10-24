import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from airflow.decorators import dag, task, task_group

# from common.utilities.pipelines_tools.data_cleaner import clean_data
from modules.extract.employee import get_data_employee
from modules.load.employee import employee_data_load

from common.utilities.pipelines_tools.data_cleaner import clean_general_data

from common.models.model import Employee

import pandas as pd
from datetime import timedelta
import datetime as dt

@dag(
    "dag_employee_etl",
    description= "DAG | This DAG will make a extract to different data sources and finally load these datas in a database",
    start_date= dt.datetime(2021, 1, 1),
    schedule_interval= None,
)

def data_estructure_etl():
    @task
    def get_employee_data():
        return get_data_employee()
    @task
    def clean_employee_data(df_json, affected_column):
        return clean_general_data(df_json, affected_column)
    @task
    def load_employee_data(df):
        return employee_data_load(df)
    
    df = get_employee_data()
    data_clean_js = clean_employee_data(df, Employee)
    load_employee_data(data_clean_js)
data_estructure_etl()