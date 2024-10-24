import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from airflow.decorators import dag, task, task_group
from airflow.utils.dates import days_ago
from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator,
)

from modules.extract.country import get_data_country
from modules.load.country import country_data_load

import pandas as pd
from datetime import timedelta
import datetime as dt

@dag(
    "dag_country_etl",
    description= "DAG | This DAG will make a extract to different data sources and finally load these datas in a database",
    start_date= dt.datetime(2021, 1, 1),
    schedule_interval= None,
)

def data_estructure_etl():
    @task
    def get_customer():
        return get_data_country()
    
    @task
    def load_data_customer(country_list):
        return country_data_load(country_list)
    
    country_list = get_customer()
    load_data_customer(country_list)
data_estructure_etl()