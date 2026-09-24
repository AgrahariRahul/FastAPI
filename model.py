from sqlalchemy.orm import sessionmaker,declarative_base,Session
from sqlalchemy import Column,String,Boolean,Integer,create_engine

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
        DATABASE_URL, connect_args= {
            "check_same_thread":False
        }
    )
sessionLocal = sessionmaker(bind=engine)

BASE = declarative_base()    

class ToDo(BASE):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True,index=True)
    title = Column(String)
    status = Column(Boolean)
    
BASE.metadata.create_all(engine)
      
      
        
        




    


def get_db():
    
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()        
     