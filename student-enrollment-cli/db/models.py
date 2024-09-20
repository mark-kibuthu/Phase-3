from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# Many-to-Many relationship between Students and Courses via Enrollments
enrollments_table = Table('enrollments', Base.metadata,
                          Column('student_id', Integer, ForeignKey('students.id')),
                          Column('course_id', Integer, ForeignKey('courses.id'))
                          )

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    major = Column(String)
    year = Column(Integer)

    courses = relationship("Course", secondary=enrollments_table, back_populates="students")

    def __repr__(self):
        return f"<Student(name={self.name}, major={self.major}, year={self.year})>"

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department = Column(String)

    courses = relationship("Course", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher(name={self.name}, department={self.department})>"

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    credits = Column(Integer)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    teacher = relationship("Teacher", back_populates="courses")
    students = relationship("Student", secondary=enrollments_table, back_populates="courses")

    def __repr__(self):
        return f"<Course(name={self.name}, credits={self.credits})>"

# Create Database and session
def create_database(engine):
    Base.metadata.create_all(engine)

# Create session
def get_session(database_url="sqlite:///student_enrollment.db"):
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()
