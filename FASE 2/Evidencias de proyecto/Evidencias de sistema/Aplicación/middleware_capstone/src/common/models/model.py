from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Float, Date
from decouple import config

engine_db = create_engine(config('CONNECTION_TO_DB'))
Base_db = declarative_base()

class Country(Base_db):
    __tablename__= 'country'

    id = Column(Integer(), primary_key=True)
    country_name = Column(String(30), nullable=False)
    
    def __str__(self):
        return self.id

class Customer(Base_db):
    __tablename__= 'customer'

    id = Column(String(30), primary_key=True)
    gender = Column(String(20), nullable=False)
    age = Column(Integer(), nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(30), nullable=True)
    email = Column(String(50), nullable=True)
    nationality = Column(String(30), nullable=True)

    invoices = relationship("Invoice", back_populates="customer")
    def __str__(self):
        return self.id

class Store(Base_db):
    __tablename__= 'store'

    store_id = Column(Integer(), primary_key=True)
    store_name = Column(String(20), nullable=False)

    invoices_relational = relationship("Invoice", back_populates="store")
    employee_relational = relationship("Employee", back_populates="store_emp")
    def __str__(self):
        return self.store_id

class Invoice(Base_db):
    __tablename__= "invoice"

    invoice_no = Column(String(25), primary_key=True)
    category = Column(String(25), nullable=False)
    quantity = Column(Integer(), nullable=True)
    product_name = Column(String(100), nullable=True)
    price = Column(Float(), nullable=True)
    payment_method = Column(String(20), nullable=True)
    invoice_date = Column(Date(), nullable=True)
    store_id = Column(Integer(), ForeignKey('store.store_id'), nullable=True)
    customer_id = Column(String(20), ForeignKey('customer.id'), nullable=False)

    customer = relationship("Customer", back_populates="invoices")
    store = relationship("Store", back_populates="invoices_relational")
    
    def __str__(self):
        return self.invoice_no


class Employee(Base_db):
    __tablename__= "employee"

    employee_id = Column(Integer(), primary_key=True)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    education = Column(String(50), nullable=True)
    age = Column(Float(), nullable=True)
    email = Column(String(50), nullable=True)
    gender = Column(String(20), nullable=True)
    store_id = Column(Integer(), ForeignKey('store.store_id'), nullable=False)
    
    store_emp = relationship("Store", back_populates="employee_relational")
    report_emp = relationship("Hr_report", back_populates="employee", uselist=False)
    
    def __str__(self):
        return self.employee_id

class Hr_report(Base_db):
    __tablename__= "hr_report"

    employee_id = Column(Integer(), ForeignKey('employee.employee_id'),primary_key=True)
    department = Column(String(50), nullable=False)
    recruitment_channel = Column(String(15), nullable=True)
    no_of_trainings = Column(Integer(), nullable=True)
    previous_year_rating = Column(Integer(), nullable=True)
    length_of_service = Column(Integer(), nullable=True)
    kpis_met = Column(Integer(), nullable=True)
    awards_won = Column(Integer(), nullable=True)
    avg_training_score = Column(Integer(), nullable=True)
    
    employee = relationship("Employee", back_populates="report_emp")
    
    def __str__(self):
        return self.employee_id

if __name__ == '__main__':
    pass