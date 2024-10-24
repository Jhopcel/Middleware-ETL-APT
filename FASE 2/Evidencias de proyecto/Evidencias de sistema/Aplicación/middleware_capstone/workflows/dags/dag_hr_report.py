import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from airflow.decorators import dag, task, task_group

from common.utilities.pipelines_tools.data_cleaner import clean_general_data
from modules.extract.hr_report import get_data_hr_report
from modules.load.hr_report import hr_report_data_load

from common.models.model import Hr_report

import pandas as pd
from datetime import timedelta
import datetime as dt

@dag(
    "dag_hr_report_etl",
    description= "DAG | This DAG will make a extract to different data sources and finally load these datas in a database",
    start_date= dt.datetime(2021, 1, 1),
    schedule_interval= None,
)

def data_estructure_etl():
    @task
    def get_employee_data():
        return get_data_hr_report()
    @task
    def clean_data_hr_report(df, affected_column):
        return clean_general_data(df, affected_column)
    @task
    def load_employee_data(df):
        return hr_report_data_load(df)
    
    df = get_employee_data()
    clean_hr_report = clean_data_hr_report(df, Hr_report)
    load_employee_data(clean_hr_report)
data_estructure_etl()