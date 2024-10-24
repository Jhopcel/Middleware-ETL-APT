import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from airflow.decorators import dag, task, task_group
from airflow.utils.dates import days_ago
from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator,
)

from common.utilities.pipelines_tools.data_cleaner import clean_general_data
from modules.extract.customer import get_data_customer
from modules.load.customer import data_load_customer

from common.models.model import Customer

import pandas as pd
from datetime import timedelta
import datetime as dt

@dag(
    "dag_customer_etl",
    description= "DAG | This DAG will make a extract to different data sources and finally load these datas in a database",
    start_date= dt.datetime(2021, 1, 1),
    schedule_interval= None,
)

def data_estructure_etl():
    @task
    def get_customer():
        return get_data_customer()

    @task
    def clean_data_customer(df, affected_column):
        return clean_general_data(df, affected_column)
    
    @task
    def load_data_customer(df):
        return data_load_customer(df)
    
    df = get_customer()
    df_clean = clean_data_customer(df, Customer)
    load_data_customer(df_clean)
data_estructure_etl()