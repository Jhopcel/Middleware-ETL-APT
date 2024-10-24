from sqlalchemy.orm import sessionmaker
from common.models.model import Employee, engine_db
import pandas as pd

def employee_data_load(df_json):
    
    df = pd.read_json(df_json)
    
    Session = sessionmaker(engine_db)
    
    with Session() as session:
        try:
            data_dict = df.to_dict(orient="records")
            session.bulk_insert_mappings(Employee, data_dict)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Un ERROR ocurrió al hacer querer actualizar o agregar datos {e}")
            raise
        finally:
            session.close()