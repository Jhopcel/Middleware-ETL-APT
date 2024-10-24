import pandas as pd

def get_data_country():
    data = pd.read_csv('src/assets/data_sources/customer.csv', usecols=["nacionalidad"])
    
    data.drop_duplicates(subset=["nacionalidad"], inplace=True)
    data['id'] = range(1, len(data) + 1)
    
    structure_data = ["id", "nacionalidad"]
    data = data[structure_data]
    change_columns = ["id", "country_name"]
    data.columns = change_columns

    return data.to_json()

