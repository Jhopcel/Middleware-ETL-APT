import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from airflow.decorators import dag, task, task_group

# from common.utilities.pipelines_tools.data_cleaner import clean_data
from modules.extract.invoice import get_data_invoice
from modules.load.invoice import invoice_data_load

import pandas as pd
from datetime import timedelta
import datetime as dt

@dag(
    "dag_invoice_etl",
    description= "DAG | This DAG will make a extract to different data sources and finally load these datas in a database",
    start_date= dt.datetime(2021, 1, 1),
    schedule_interval= None,
)

def data_estructure_etl():
    @task
    def get_invoice_data():
        return get_data_invoice()
    @task
    def load_invoice_data(df):
        return invoice_data_load(df)
    
    df = get_invoice_data()
    load_invoice_data(df)
data_estructure_etl()