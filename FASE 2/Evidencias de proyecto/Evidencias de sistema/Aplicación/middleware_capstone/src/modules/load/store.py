from sqlalchemy.orm import sessionmaker
from common.models.model import Store, Base_db, engine_db
import pandas as pd

def store_data_load(df_json):
    
    df = pd.read_json(df_json)
    
    batch_size = 20000 
    
    Session = sessionmaker(engine_db)
    
    with Session() as session:
        try:
            for index, row in df.iterrows():
                existing_store_result = session.query(Store).filter(Store.store_id == row["store_id"]).first()
                if existing_store_result is None:
                    store = Store(
                        store_id=row["store_id"],
                        store_name=row["store_name"],
                    )
                    session.add(store)
                else:
                    existing_store_result.store_name = row["store_name"]
                if (index + 1) % batch_size == 0:
                    session.commit()
                
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Un ERROR ocurrió al hacer querer actualizar o agregar datos {e}")
            raise
        finally:
            session.close()
