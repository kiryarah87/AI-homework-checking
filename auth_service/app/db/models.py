from datetime import datetime
from sqlalchemy import Integer, String, Enum, ForeignKey, Table, text, TIMESTAMP, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .enums import Role


parent_student = Table(
    "parent_student",
    Base.metadata,
    Column("parent_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("student_id", Integer, ForeignKey("users.id"), primary_key=True),
)

teacher_student = Table(
    "teacher_student",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("student_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        server_onupdate=text("now()"),
    )
    # Для родителей: список детей
    children: Mapped[list["User"]] = relationship(
        "User",
        secondary=parent_student,
        primaryjoin=lambda: User.id == parent_student.c.parent_id,
        secondaryjoin=lambda: User.id == parent_student.c.student_id,
        back_populates="parents"
    )

    # Для детей: список родителей
    parents: Mapped[list["User"]] = relationship(
        "User",
        secondary=parent_student,
        primaryjoin=lambda: User.id == parent_student.c.student_id,
        secondaryjoin=lambda: User.id == parent_student.c.parent_id,
        back_populates="children"
    )

    # Для учителей: список учеников
    students: Mapped[list["User"]] = relationship(
        "User",
        secondary=teacher_student,
        primaryjoin=lambda: User.id == teacher_student.c.teacher_id,
        secondaryjoin=lambda: User.id == teacher_student.c.student_id,
        back_populates="teachers"
    )

    # Для учеников: список учителей
    teachers: Mapped[list["User"]] = relationship(
        "User",
        secondary=teacher_student,
        primaryjoin=lambda: User.id == teacher_student.c.student_id,
        secondaryjoin=lambda: User.id == teacher_student.c.teacher_id,
        back_populates="students"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
