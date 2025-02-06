from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.two_sum_result import Base  # Import Base model

# Database Configuration
DATABASE_URL = "postgresql://username:password@localhost/twosumdb"

# Create engine & session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Create tables
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✅ Database setup completed.")
