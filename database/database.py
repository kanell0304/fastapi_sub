from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel

DABASE_URL="mysql+mysqlconnector://root:1234@localhost:3306/board"

#연결객체 생성
engine=create_engine(DABASE_URL)

# def get_con():
#     db = Session(bind=engine)
#     try:
#         yield db
#     finally:
#         db.close()

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

#sqlalchemy에서 모델 정의할때 상속받는 기본 클래스
Base=declarative_base()