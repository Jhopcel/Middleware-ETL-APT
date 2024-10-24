import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from airflow.decorators import dag, task, task_group

from common.utilities.pipelines_tools.data_cleaner import clean_general_data
from modules.extract.store import get_data_store
from modules.load.store import store_data_load

import pandas as pd
from datetime import timedelta
import datetime as dt

@dag(
    "dag_store_etl",
    description= "DAG | This DAG will make a extract to different data sources and finally load these datas in a database",
    start_date= dt.datetime(2021, 1, 1),
    schedule_interval= None,
)

def data_estructure_etl():
    @task
    def get_store_data():
        return get_data_store()
    @task
    def load_store_data(df):
        return store_data_load(df)
    
    df = get_store_data()
    load_store_data(df)
data_estructure_etl()