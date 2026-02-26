"""Executable simulation for Question 1 university management system."""

from course import Course
from department import Department
from faculty import Faculty
from staff import Staff
from student import Student


def print_section(title: str) -> None:
    """Print a clear section heading."""
    print(f"\n{title}\n" + "-" * len(title))


def create_objects() -> tuple[list[Student], list[Faculty], list[Staff], list[Course], Department]:
    """Create core objects used in the simulation."""
    print_section("1. Object Creation")

    students = [
        Student("Aisha Perera", "P1001", "aisha@uni.edu", "0771111111", "S001", "Computer Science", "2024-01-15"),
        Student("Nimal Silva", "P1002", "nimal@uni.edu", "0772222222", "S002", "Data Science", "2023-09-01"),
    ]
    faculty_members = [
        Faculty("Dr. Jayasinghe", "P2001", "jayasinghe@uni.edu", "0711111111", "F001", "Computer Science", "2019-06-01"),
    ]
    staff_members = [
        Staff("Lakmal", "P3001", "lakmal@uni.edu", "0761111111", "ST001", "Registrar Assistant", "Administration"),
    ]

    courses = [
        Course("CS101", "Programming Fundamentals", 3, faculty_members[0], 40),
        Course("CS201", "Data Structures", 3, faculty_members[0], 40),
    ]

    cs_department = Department("Computer Science", faculty_members[0])
    for course in courses:
        cs_department.add_course(course)

    for person in [students[0], faculty_members[0], staff_members[0]]:
        info = person.get_info()
        print(f"{info['person_type']}: {info['name']} ({info['person_id']})")

    return students, faculty_members, staff_members, courses, cs_department


def run_enrollment_and_grading(students: list[Student], courses: list[Course]) -> None:
    """Simulate course enrollment, grading, and validation rules."""
    print_section("2. Enrollment and Grading")

    courses[0].add_student(students[0])
    courses[1].add_student(students[0])
    courses[0].add_student(students[1])

    students[0].add_grade("CS101", 3.8)
    students[0].add_grade("CS201", 3.6)

    print(f"{students[0].name} enrolled courses: {students[0].enrolled_courses}")
    print(f"{students[0].name} grades: {students[0].grades}")
    print(f"{students[0].name} GPA: {students[0].gpa}")
    print(f"{students[0].name} status: {students[0].get_academic_status()}")

    print("\nValidation checks:")
    try:
        students[0].add_grade("CS101", 4.5)
    except ValueError as error:
        print(f"Invalid grade error: {error}")

    for i in range(1, 6):
        students[1].enroll_course(f"EL{i:03}")
    try:
        students[1].enroll_course("EL007")
    except ValueError as error:
        print(f"Course limit error: {error}")


def run_polymorphism(students: list[Student], faculty_members: list[Faculty], staff_members: list[Staff]) -> None:
    """Show polymorphic behavior through role-specific responsibility methods."""
    print_section("3. Polymorphism")

    people = [students[0], faculty_members[0], staff_members[0]]
    for person in people:
        print(f"{person.__class__.__name__} - {person.name}")
        print(f"  {person.get_responsibilities()}")


def show_department_summary(department: Department) -> None:
    """Print a short department summary."""
    print_section("4. Department Summary")
    info = department.get_department_info()
    print(f"Department: {info['dept_name']}")
    print(f"Head: {info['dept_head']}")
    print(f"Faculty Count: {info['faculty_count']}")
    print(f"Course Count: {info['course_count']}")
    print(f"Courses: {', '.join(info['courses'])}")


def main() -> None:
    """Run the full university system simulation."""
    students, faculty_members, staff_members, courses, department = create_objects()
    run_enrollment_and_grading(students, courses)
    run_polymorphism(students, faculty_members, staff_members)
    show_department_summary(department)


if __name__ == "__main__":
    main()
