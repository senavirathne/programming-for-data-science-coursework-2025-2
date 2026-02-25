"""In-memory database for the university management system."""

from course import Course
from department import Department
from faculty import Faculty
from staff import Staff
from student import Student


class UniversityDatabase:
    """Holds all data for the university system."""

    def __init__(self) -> None:
        """Initialize the database with demo data."""
        self.students: list[Student] = []
        self.faculty_members: list[Faculty] = []
        self.staff_members: list[Staff] = []
        self.departments: dict[str, Department] = {}
        self.courses: dict[str, Course] = {}

        self._seed_data()

    def _seed_data(self) -> None:
        """Populate the database with initial data."""
        # 1. Create People
        self.students = [
            Student("Aisha Perera", "P1001", "aisha@uni.edu", "0771111111", "S001", "CS", "2024-01-15"),
            Student("Nimal Silva", "P1002", "nimal@uni.edu", "0772222222", "S002", "Math", "2023-09-01"),
            Student("Kavindi Fernando", "P1003", "kavindi@uni.edu", "0773333333", "S003", "Physics", "2022-09-01"),
        ]

        self.faculty_members = [
            Faculty("Dr. Jayasinghe", "P2001", "jayasinghe@uni.edu", "0711111111", "F001", "Computer Science", "2019-06-01"),
            Faculty("Dr. Rodrigo", "P2002", "rodrigo@uni.edu", "0712222222", "F002", "Mathematics", "2017-03-10"),
            Faculty("Dr. Nadeesha", "P2003", "nadeesha@uni.edu", "0713333333", "F003", "Physics", "2020-08-20"),
        ]

        self.staff_members = [
            Staff("Lakmal", "P3001", "lakmal@uni.edu", "0761111111", "ST001", "Registrar Assistant", "Administration"),
            Staff("Chathuri", "P3002", "chathuri@uni.edu", "0762222222", "ST002", "Lab Technician", "Science"),
            Staff("Saman", "P3003", "saman@uni.edu", "0763333333", "ST003", "IT Support Officer", "IT Services"),
        ]

        # 2. Create Departments
        # Note: Department init requires a head (Faculty)
        cs_dept = Department("Computer Science", self.faculty_members[0])
        math_dept = Department("Mathematics", self.faculty_members[1])
        
        # Add extra staff to CS
        cs_dept.add_faculty(self.faculty_members[2])

        self.departments["Computer Science"] = cs_dept
        self.departments["Mathematics"] = math_dept

        # 3. Create Courses
        cs_courses = [
            Course("CS101", "Programming Fundamentals", 3, self.faculty_members[0], 2),
            Course("CS201", "Data Structures", 3, self.faculty_members[0], 2),
            Course("CS301", "Databases", 3, self.faculty_members[0], 2),
            Course("CS401", "Software Engineering", 3, self.faculty_members[0], 2),
        ]

        math_courses = [
            Course("MA101", "Calculus I", 3, self.faculty_members[1], 2),
            Course("MA201", "Linear Algebra", 3, self.faculty_members[1], 2),
            Course("MA301", "Probability", 3, self.faculty_members[1], 2),
        ]

        # Register courses to departments and the global course list
        for c in cs_courses:
            cs_dept.add_course(c)
            self.courses[c.course_code] = c

        for c in math_courses:
            math_dept.add_course(c)
            self.courses[c.course_code] = c

# Create a shared instance
db = UniversityDatabase()
