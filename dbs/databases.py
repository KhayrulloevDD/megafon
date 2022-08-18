from dbs.sqlite import SessionLocal, engine
from dbs.postgresql import SessionLocal as pg_SessionLocal, engine as pg_engine
import models


models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=pg_engine)


# sqlite Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PG Dependency
def get_pg_db():
    db = pg_SessionLocal()
    try:
        yield db
    finally:
        db.close()
