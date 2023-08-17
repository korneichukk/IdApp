from pydantic import BaseModel
from typing import List


# Upwork Job schema
class UpworkJobBase(BaseModel):
    title: str
    link: str
    description: str
    time_posted: str


class UpworkJobCreate(UpworkJobBase):
    pass


class UpworkJob(UpworkJobBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True


# Upwork Category schema
class UpworkCategoryBase(BaseModel):
    name: str
    link: str


class UpworkCategoryCreate(UpworkCategoryBase):
    pass


class UpworkCategory(UpworkCategoryBase):
    id: int
    jobs: List[UpworkJob] = []

    class Config:
        orm_mode = True
