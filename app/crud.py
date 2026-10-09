from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

def get_student(db: Session, student_id: str):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()

def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str | None = None,
    course: str | None = None,
    born_after: date | None = None,
    born_before: date | None = None
):
    query = db.query(models.Student)
    if name:
        query = query.filter(models.Student.name.ilike(f"%{name}%"))
    if course:
        query = query.filter(models.Student.course.ilike(f"%{course}%"))
    if born_after:
        query = query.filter(models.Student.date_of_birth > born_after)
    if born_before:
        query = query.filter(models.Student.date_of_birth < born_before)
    return query.offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: str, student_update: schemas.StudentUpdate):
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    if not db_student.email and not db_student.phone:
        raise ValueError("At least one of email or phone must be provided")

    db.commit()
    db.refresh(db_student)
    return db_student

def replace_student(db: Session, student_id: str, student: schemas.StudentReplace):
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    update_data = student.model_dump()
    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: str):
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    db.delete(db_student)
    db.commit()
    return db_student