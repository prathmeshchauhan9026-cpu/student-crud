from app.database import SessionLocal, engine
from app import models, schemas, crud
from datetime import date

models.Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        if db.query(models.Student).count() > 0:
            print("Database already has records. Skipping seed.")
            return
        students = [
            schemas.StudentCreate(
                student_id="STU001",
                name="Aarav Sharma",
                date_of_birth=date(2004, 5, 17),
                email="aarav.sharma@example.com",
                phone="+91-9876543210",
                course="B.Tech CSE",
                address="Pune, Maharashtra",
                enrollment_date=date(2023, 8, 1)
            ),
            schemas.StudentCreate(
                student_id="STU002",
                name="Diya Patel",
                date_of_birth=date(2005, 2, 10),
                email="diya.patel@example.com",
                phone=None,
                course="B.Sc IT",
                address="Ahmedabad, Gujarat",
                enrollment_date=date(2023, 8, 1)
            ),
            schemas.StudentCreate(
                student_id="STU003",
                name="Kabir Singh",
                date_of_birth=date(2003, 11, 23),
                email=None,
                phone="+91-9123456780",
                course="B.Tech ECE",
                address="Delhi",
                enrollment_date=date(2022, 8, 1)
            ),
            schemas.StudentCreate(
                student_id="STU004",
                name="Ananya Rao",
                date_of_birth=date(2006, 7, 5),
                email="ananya.rao@example.com",
                phone="+91-9988776655",
                course="BBA",
                address="Bengaluru, Karnataka",
                enrollment_date=date(2024, 8, 1)
            ),
            schemas.StudentCreate(
                student_id="STU005",
                name="Ishaan Verma",
                date_of_birth=date(2005, 9, 30),
                email="ishaan.verma@example.com",
                phone=None,
                course="B.Tech Mechanical",
                address="Lucknow, Uttar Pradesh",
                enrollment_date=date(2023, 8, 1)
            ),
            schemas.StudentCreate(
                student_id="STU006",
                name="Meera Nair",
                date_of_birth=date(2004, 12, 12),
                email="meera.nair@example.com",
                phone="+91-9871234567",
                course="B.Com",
                address="Kochi, Kerala",
                enrollment_date=date(2022, 8, 1)
            ),
        ]
        for s in students:
            crud.create_student(db, s)
        print(f"Seeded {len(students)} students.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()