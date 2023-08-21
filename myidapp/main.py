from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import models, schemas, crud
from .database.database import SessionLocal, engine
from .upwork_parser.upwork_category_parser import UpworkCategoryParser

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "message"}


@app.get("/collect_categories", response_model=list[schemas.UpworkCategory])
async def collect_categories(db: Session = Depends(get_db)):
    parser = UpworkCategoryParser()
    parser.run(db=db)


@app.get("/categories", response_model=list[schemas.UpworkCategory])
async def get_categories(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    categories = crud.get_all_upwork_categories(db, skip=skip, limit=limit)
    return categories
