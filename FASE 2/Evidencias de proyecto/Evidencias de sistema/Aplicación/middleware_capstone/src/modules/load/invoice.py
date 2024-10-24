from sqlalchemy.orm import sessionmaker
from common.models.model import Invoice, engine_db
import pandas as pd

def invoice_data_load(df_json):
    
    df = pd.read_json(df_json)
    
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], dayfirst=True)
    
    print(df["invoice_date"])
    
    Session = sessionmaker(engine_db)
    
    with Session() as session:
        try:
            data_dict = df.to_dict(orient="records")
            session.bulk_insert_mappings(Invoice, data_dict)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Un ERROR ocurrió al hacer querer actualizar o agregar datos {e}")
            raise
        finally:
            session.close()