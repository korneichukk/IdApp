from sqlalchemy.orm import Session

from . import models, schemas


# Category CRUD
# Create
def insert_upwork_category(db: Session, category: schemas.UpworkCategoryCreate):
    db_category = models.UpworkCategory(name=category.name, link=category.link)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# Read
def get_all_upwork_categories(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.UpworkCategory).offset(skip).limit(limit).all()


# Delete
def flush_all_upwork_categories(db: Session):
    db.query(models.UpworkCategory).delete()
    db.commit()


# Job CRUD
# Create
def insert_upwork_job(db: Session, job: schemas.UpworkJobCreate, category_id: int):
    db_job = models.UpworkJob(vars(job), category_id=category_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


# Read
def get_all_upwork_jobs(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.UpworkJob).offset(skip).limit(limit).all()
