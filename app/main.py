from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import date

from . import crud, models, schemas
from .database import engine, get_db
from .ai import ask_ollama

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students Database CRUD API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Students CRUD API is running"}

@app.post("/students", response_model=schemas.StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing = crud.get_student(db, student.student_id)
    if existing:
        raise HTTPException(status_code=409, detail="student_id already exists")
    if student.email:
        existing_email = db.query(models.Student).filter(models.Student.email == student.email).first()
        if existing_email:
            raise HTTPException(status_code=409, detail="email already exists")
    try:
        return crud.create_student(db, student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Duplicate student_id or email")

@app.get("/students", response_model=List[schemas.StudentOut])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    name: Optional[str] = None,
    course: Optional[str] = None,
    born_after: Optional[date] = None,
    born_before: Optional[date] = None,
    db: Session = Depends(get_db)
):
    return crud.get_students(db, skip=skip, limit=limit, name=name, course=course, born_after=born_after, born_before=born_before)

@app.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: str, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.patch("/students/{student_id}", response_model=schemas.StudentOut)
def patch_student(student_id: str, student_update: schemas.StudentUpdate, db: Session = Depends(get_db)):
    try:
        updated = crud.update_student(db, student_id, student_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated

@app.put("/students/{student_id}", response_model=schemas.StudentOut)
def put_student(student_id: str, student: schemas.StudentReplace, db: Session = Depends(get_db)):
    updated = crud.replace_student(db, student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return None

@app.post("/ask", response_model=schemas.AskResponse)
def ask_question(request: schemas.AskRequest, db: Session = Depends(get_db)):
    students = crud.get_students(db, limit=500)
    return ask_ollama(request.question, students)