import pandas as pd

def get_data_employee():
    data = pd.read_excel('src/assets/data_sources/employee.xlsx')
    
    estructure_list = ["employee_id","nombre","apellido", "education","age", "correo", "gender", "Local"]
    name_change = ["employee_id","first_name","last_name", "education","age","email", "gender", "store_id"]
    
    data = data[estructure_list]
    data.columns = name_change
    
    return data.to_json()
