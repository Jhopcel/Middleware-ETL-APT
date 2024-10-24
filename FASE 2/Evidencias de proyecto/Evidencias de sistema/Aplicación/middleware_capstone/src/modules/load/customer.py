from sqlalchemy.orm import sessionmaker
from common.models.model import Customer, engine_db
import pandas as pd

def data_load_customer(df_json):
    
    df = pd.read_json(df_json)
    
    Session = sessionmaker(engine_db)
    
    with Session() as session:
        try:
            data_dict = df.to_dict(orient="records")
            session.bulk_insert_mappings(Customer, data_dict)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Un ERROR ocurrió al hacer querer actualizar o agregar datos {e}")
            raise
        finally:
            session.close()
