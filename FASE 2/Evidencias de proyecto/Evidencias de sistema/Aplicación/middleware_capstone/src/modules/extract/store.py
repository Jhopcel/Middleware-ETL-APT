import pandas as pd

def get_data_store():
    data = pd.read_csv('src/assets/data_sources/local_name.csv')
    
    new_headers = ['store_id', 'store_name']
    
    data.columns = new_headers
    
    return data.to_json()