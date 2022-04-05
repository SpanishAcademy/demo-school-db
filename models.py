import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import MetaData

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.zzzcomputing.com/en/latest/naming.html
NAMING_CONVENTION = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)

# Create Base sqlalchemy model class that all others derive from
Base = declarative_base(metadata=metadata)

class State(Base):
    __tablename__ = 'state'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    code = sa.Column(sa.String, nullable=False, unique=True)
    name = sa.Column(sa.String, nullable=False)

class City(Base):
    __tablename__ = 'city'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.String, unique=True, nullable=False)
    state_id = sa.Column(sa.Integer, sa.ForeignKey('state.id'))
    state = relationship(State)

class Student(Base):
    __tablename__ = 'student'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    last_name = sa.Column(sa.String)
    first_name = sa.Column(sa.String, nullable=False)
    birthday = sa.Column(sa.Date)
    password = sa.Column(sa.String)
    city_id = sa.Column(sa.Integer, sa.ForeignKey('city.id'))
    city = relationship(City)

class Teacher(Base):
    __tablename__ = 'teacher'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    last_name = sa.Column(sa.String)
    first_name = sa.Column(sa.String, nullable=False)
    birthday = sa.Column(sa.Date)
    password = sa.Column(sa.String)

class Classroom(Base):
    __tablename__ = 'classroom'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    teacher_id = sa.Column(sa.Integer, sa.ForeignKey('teacher.id'), nullable=False)
    teacher = relationship(Teacher)
    first_day = sa.Column(sa.Date)
    last_day = sa.Column(sa.Date)

class StudentInClassroom(Base):
    __tablename__ = 'student_in_classroom'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))
    classroom_id = sa.Column(sa.Integer, sa.ForeignKey('classroom.id'))
    student = relationship(Student)
    classroom = relationship(Classroom)

    __table_args__ = (
        sa.UniqueConstraint('student_id', 'classroom_id'),
    )

class Homework(Base):
    __tablename__ = 'homework'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    classroom_id = sa.Column(sa.Integer, sa.ForeignKey('classroom.id'))
    assigned_on = sa.Column(sa.Date, nullable=False)
    due_by = sa.Column(sa.Date, nullable=False)
    total_points = sa.Column(sa.Integer, nullable=False)
    classroom = relationship(Classroom)

class HomeworkGrade(Base):
    __tablename__ = 'homework_grade'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    homework_id = sa.Column(sa.Integer, sa.ForeignKey('homework.id'), nullable=False)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'), nullable=False)
    completed_on = sa.Column(sa.Date)
    points_earned = sa.Column(sa.Integer, nullable=False)
    homework = relationship(Homework)
    student = relationship(Student)

    __table_args__ = (
        sa.UniqueConstraint('homework_id', 'student_id'),
    )
