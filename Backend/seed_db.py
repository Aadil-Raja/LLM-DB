# seed_db.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Product

load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)

def seed():
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        if s.query(Product).count() == 0:
            s.add_all([
                Product(name="Running Shoes", category="Footwear",  price=79.99, units_sold=320),
                Product(name="Leather Wallet", category="Accessories", price=39.50, units_sold=540),
                Product(name="Wireless Mouse", category="Electronics", price=24.99, units_sold=860),
                Product(name="Headphones",    category="Electronics", price=149.00, units_sold=210),
                Product(name="Sports Bottle", category="Fitness",    price=12.00, units_sold=1200),
                Product(name="Yoga Mat",      category="Fitness",    price=25.00, units_sold=630),
            ])
            s.commit()

if __name__ == "__main__":
    seed()
    print("Seeded ✅")
