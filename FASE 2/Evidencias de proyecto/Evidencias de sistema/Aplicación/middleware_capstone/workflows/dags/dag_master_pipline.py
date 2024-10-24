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

from modules.extract.store import get_data_store
from modules.load.store import store_data_load

from modules.extract.customer import get_data_customer
from modules.load.customer import data_load_customer

from modules.extract.invoice import get_data_invoice
from modules.load.invoice import invoice_data_load

from modules.extract.employee import get_data_employee
from modules.load.employee import employee_data_load

from modules.extract.hr_report import get_data_hr_report
from modules.load.hr_report import hr_report_data_load

from common.utilities.pipelines_tools.data_cleaner import clean_general_data

from common.models.model import Store, Customer, Employee, Invoice, Hr_report, Country

from datetime import timedelta

@dag(
    "dag_master_pipeline",
    description= "DAG | This DAG is a simple pipeline, only for demonstration purposes",
    start_date= days_ago(1),
    schedule_interval= timedelta(hours=24),
)

def central_pipeline():
    @task_group(group_id="references_tables_first_execution")
    def references_tables_fk():
        @task_group(group_id="country")
        def country():
            @task
            def extract_country():
                return get_data_country()
            
            @task
            def clean_data_country(df_json, affected_column):
                return clean_general_data(df_json, affected_column)
            
            @task
            def load_country(data_clean_js):
                return country_data_load(data_clean_js)
            
            df_json = extract_country()
            data_clean_js = clean_data_country(df_json, Country)
            load_country(data_clean_js)
        
        @task_group(group_id="store")
        def store():
            @task
            def extract_tore():
                return get_data_store()
            
            @task
            def clean_data_store(df_json, affected_column):
                return clean_general_data(df_json, affected_column)

            @task
            def load_store(data_clean_js):
                return store_data_load(data_clean_js)
            
            df_json = extract_tore()
            data_clean_js = clean_data_store(df_json, Store)
            load_store(data_clean_js)
        
        @task_group(group_id="customer")
        def customer():
            @task
            def extract_customer():
                return get_data_customer()
            
            @task
            def clean_data_customer(df_json, affected_column):
                return clean_general_data(df_json, affected_column)
            
            @task
            def load_customer(data_clean_js):
                return data_load_customer(data_clean_js)
            
            df_json = extract_customer()
            data_clean_js = clean_data_customer(df_json, Customer)
            load_customer(data_clean_js)
        
        country()
        store()
        customer()
    
    @task_group(group_id="invoice_table_second_parallel_execution")
    def invoice_table():
        @task
        def extract_invoice():
            return get_data_invoice()
        
        @task
        def clean_data_invoice(df_json, affected_column):
            return clean_general_data(df_json, affected_column)
        @task
        def load_invoice(data_clean_js):
            return invoice_data_load(data_clean_js)
        
        df_json = extract_invoice()
        data_clean_js = clean_data_invoice(df_json, Invoice)
        load_invoice(data_clean_js)    
    
    @task_group(group_id="employee_hr_report_tables_third_parallel_execution")
    def employee_hr_report_tables():
        @task_group(group_id="employee_table")
        def employee():
            @task
            def extract_employee():
                return get_data_employee()
            
            @task
            def clean_data_employee(df_json, affected_column):
                return clean_general_data(df_json, affected_column)
            
            @task
            def load_employee(data_clean_js):
                return employee_data_load(data_clean_js)
            
            df_json = extract_employee()
            data_clean_js = clean_data_employee(df_json, Employee)
            load_employee(data_clean_js)
            
        @task_group(group_id="hr_report_table")
        def hr_report():
            @task
            def extract_hr_report():
                return get_data_hr_report()
            
            @task
            def clean_data_hr_report(df_json, affected_column):
                return clean_general_data(df_json, affected_column)
            
            @task
            def load_hr_report(data_clean_js):
                return hr_report_data_load(data_clean_js)
            
            df_json = extract_hr_report()
            data_clean_js = clean_data_hr_report(df_json, Hr_report)
            load_hr_report(data_clean_js)   
        employee() >> hr_report()
    
    references_tables_fk() >> [invoice_table(), employee_hr_report_tables()]
central_pipeline()