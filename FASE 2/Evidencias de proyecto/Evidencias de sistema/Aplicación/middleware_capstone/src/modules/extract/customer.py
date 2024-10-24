import pandas as pd

def get_data_customer():
    data = pd.read_csv('src/assets/data_sources/customer.csv')
    
    new_headers = ['id', 'gender', 'age', 'name', 'last_name', 'email', 'nationality']
    
    data.columns = new_headers
    
    data["id"] = data["id"].astype(str)
    data["gender"] = data["gender"].astype(str)
    data["age"] = data["age"].astype(int)
    data["name"] = data["name"].astype(str)
    data["last_name"] = data["last_name"].astype(str)
    data["email"] = data["email"].astype(str)
    data["nationality"] = data["nationality"].astype(str)
    
    return data.to_json()