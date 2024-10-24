from sqlalchemy.orm import sessionmaker
from common.models.model import Country, Base_db, engine_db
import pandas as pd

def country_data_load(data_json):
    
    data_country = pd.read_json(data_json)
    
    Session = sessionmaker(engine_db)
    
    with Session() as session:
        try:
            for index, row in data_country.iterrows():
                existing_socio = session.query(Country).filter(Country.country_name == row["country_name"]).first()
                if existing_socio is None:
                    customer = Country(
                        id=row["id"],
                        country_name=row["country_name"],
                    )
                    session.add(customer)
                else:
                    existing_socio.country_name = row["country_name"]
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Un ERROR ocurrió al hacer querer actualizar o agregar datos {e}")
            raise
        finally:
            session.close()
