import pandas as pd
import json
from sqlalchemy import inspect


def clean_general_data(json_load, affected_column):
    
    df = pd.read_json(json_load)
    
    inspector = inspect(affected_column)
    
    atributos_con_largo = [
    attr for attr in inspector.c if hasattr(attr.type, 'length') and attr.type.length is not None
    ]
    
    print(atributos_con_largo)
    
    for columns_collab in atributos_con_largo:
        df[columns_collab.name] = df[columns_collab.name].replace("", "No_Registrado").fillna("No_Registrado")
        column = affected_column.__table__.columns[columns_collab.name]
        length_column = column.type.length
        print(f"La columna {columns_collab.name} tiene una longitud de {length_column}")
        df[columns_collab.name] = df[columns_collab.name].apply(lambda x: x[:length_column] if len(x) > length_column else x)
    
    return df.to_json()