from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List

from .database import Base


class UpworkCategory(Base):
    __tablename__ = "upwork_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    link: Mapped[str] = mapped_column(String(255))

    jobs: Mapped[List["UpworkJob"]] = relationship(
        "UpworkJob", back_populates="category", cascade="all, delete"
    )

    def __repr__(self):
        return f"<UpworkCategory(id={self.id}, name={self.name}, link={self.link})>"


class UpworkJob(Base):
    __tablename__ = "upwork_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    link: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    time_posted: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey("upwork_categories.id"))

    category: Mapped["UpworkCategory"] = relationship(
        "UpworkCategory", back_populates="jobs"
    )

    def __repr__(self):
        return f"<UpworkJob(id={self.id}, title={self.title}, link={self.link}, description={self.description}, time_posted={self.time_posted}, category_id={self.category.name})>"
