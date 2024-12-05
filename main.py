import os
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey, Date,MetaData
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session
from datetime import date

UniverBase =declarative_base()


class Faculty(UniverBase):
    __tablename__ = "faculty"
    id = Column(Integer,primary_key=True)
    name = Column(String, nullable = False)
    year_founded = Column(Integer,nullable=False)
    students = relationship('Students', back_populates = 'faculty')
    directions = relationship('Direction', back_populates='faculty')

class Direction(UniverBase):
    __tablename__ = "direction"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    key = Column(Integer, nullable = False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship('Faculty',back_populates='directions')
    students = relationship('Students', back_populates='direction')


class Students(UniverBase):
    __tablename__ = "student"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    Dr = Column(Date)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    direction_id = Column(Integer, ForeignKey('direction.id'))
    faculty = relationship('Faculty', back_populates='students')
    direction = relationship('Direction', back_populates='students')

    # очистка базы
    db_path = 'Vsu.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    #работа с базой
engine = create_engine('sqlite:///Vsu.db', echo=False)
UniverBase.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

faculty1 = Faculty(name="ФКН", year_founded = 1980)
faculty2 = Faculty(name="ПММ", year_founded = 1920)

session.add(faculty1)
session.add(faculty2)
session.commit()

direction1 = Direction(name="Программная инженерия", key = 183, faculty=faculty1)
direction2 = Direction(name="Информационная безопасность", key = 286, faculty=faculty1)
direction3 = Direction(name="Математика и прочее", key = 334, faculty=faculty2)

session.add(direction1)
session.add(direction2)
session.add(direction3)
session.commit()

student1 = Students(name="Антон", Dr=date (2004,1,12), faculty=faculty1, direction=direction1)
student2 = Students(name="Жора", Dr=date (2010,3,14), faculty=faculty1, direction=direction2)
student3 = Students(name="Мотя", faculty=faculty2, direction=direction3)

session.add(student1)
session.add(student2)
session.add(student3)
session.commit()

faculties = session.query(Faculty).all()

#вывод данных
for faculty in faculties:
    print(f"Факультет: {faculty.name}, Год основания: {faculty.year_founded}")
    for student in faculty.students:
        print(f"  Студент: {student.name}, День рождения: {student.Dr}, Направление: {student.direction.name}, Код направления: {student.direction.key}")


# Закрываем сессию
session.close()
