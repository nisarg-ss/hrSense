from app.models.models import Base
import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session

user=os.environ.get('user')
password=os.environ.get('password')
host=os.environ.get('host')
DB=os.environ.get('DB')

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}/{DB}'
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base.metadata.create_all(bind=engine)
conn=engine.connect()
metadata = sqlalchemy.MetaData()
Session = sessionmaker(bind=engine)
sess=Session()