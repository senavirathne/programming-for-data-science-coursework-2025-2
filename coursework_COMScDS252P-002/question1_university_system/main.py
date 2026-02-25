"""Demo script for the university management system."""

from course import Course

from department import Department

from faculty import Faculty

from staff import Staff

from student import Student


def print_title(title: str) -> None:
    """Print a formatted section title.

    Args:
        title: Title text to display.

    Returns:
        None
    """
    print(f"\n{'=' * 12} {title} {'=' * 12}")


def demo_class_hierarchy() -> tuple[list[Student], list[Faculty], list[Staff]]:
    """Run the class hierarchy demo.

    Returns:
        Created students, faculty members, and staff members for later demos.
    """
    print_title("A. Class Hierarchy & Inheritance")

    students = [
        Student("Aisha Perera", "P1001", "aisha@uni.edu", "0771111111", "S001", "CS", "2024-01-15"),
        Student("Nimal Silva", "P1002", "nimal@uni.edu", "0772222222", "S002", "Math", "2023-09-01"),
        Student("Kavindi Fernando", "P1003", "kavindi@uni.edu", "0773333333", "S003", "Physics", "2022-09-01"),
    ]

    faculty_members = [
        Faculty("Dr. Jayasinghe", "P2001", "jayasinghe@uni.edu", "0711111111", "F001", "Computer Science", "2019-06-01"),
        Faculty("Dr. Rodrigo", "P2002", "rodrigo@uni.edu", "0712222222", "F002", "Mathematics", "2017-03-10"),
        Faculty("Dr. Nadeesha", "P2003", "nadeesha@uni.edu", "0713333333", "F003", "Physics", "2020-08-20"),
    ]

    staff_members = [
        Staff("Lakmal", "P3001", "lakmal@uni.edu", "0761111111", "ST001", "Registrar Assistant", "Administration"),
        Staff("Chathuri", "P3002", "chathuri@uni.edu", "0762222222", "ST002", "Lab Technician", "Science"),
        Staff("Saman", "P3003", "saman@uni.edu", "0763333333", "ST003", "IT Support Officer", "IT Services"),
    ]

    # Show inherited get_info() from Person.
    for person in [students[0], faculty_members[0], staff_members[0]]:
        print(person.get_info())

    students[0].update_contact(email="aisha.perera@uni.edu")
    print("Updated contact:", students[0].get_info()["email"])

    return students, faculty_members, staff_members


def demo_student_course_management(students: list[Student]) -> None:
    """Run the student enrollment and grading demo.

    Args:
        students: Students available for the demo.

    Returns:
        None
    """
    print_title("B & C. Student Course Management + Validation")

    student = students[0]
    courses = ["CS101", "CS102", "CS103", "CS104", "CS105"]

    for course_code in courses:
        student.enroll_course(course_code)

    grade_map = {
        "CS101": 3.7,
        "CS102": 3.4,
        "CS103": 3.8,
        "CS104": 3.2,
        "CS105": 3.9,
    }

    for course_code, grade in grade_map.items():
        student.add_grade(course_code, grade)

    print(f"Enrolled Courses: {student.enrolled_courses}")
    print(f"Grades: {student.grades}")
    print(f"GPA: {student.gpa}")
    print(f"Academic Status: {student.get_academic_status()}")

    print("\nValidation checks:")
    try:
        student.add_grade("CS101", 4.5)
    except ValueError as err:
        print("Invalid grade error:", err)

    try:
        student.enroll_course("CS106")
        student.enroll_course("CS107")
    except ValueError as err:
        print("Max course error:", err)

    try:
        student.gpa = 3.9  # type: ignore[misc]
    except AttributeError as err:
        print("Read-only GPA error:", err)


def demo_polymorphism(
    students: list[Student], faculty_members: list[Faculty], staff_members: list[Staff]
) -> None:
    """Run the responsibilities demo across person types.

    Args:
        students: Students available for the demo.
        faculty_members: Faculty members available for the demo.
        staff_members: Staff members available for the demo.

    Returns:
        None
    """
    print_title("D. Polymorphism")

    people = [students[1], faculty_members[1], staff_members[1], students[2]]
    for person in people:
        print(f"{person.name} ({person.__class__.__name__}):")
        print(f"  {person.get_responsibilities()}")


def demo_department_and_courses(
    students: list[Student], faculty_members: list[Faculty]
) -> None:
    """Run the department and course management demo.

    Args:
        students: Students available for enrollment examples.
        faculty_members: Faculty members used as instructors and heads.

    Returns:
        None
    """
    print_title("E. Course & Department Classes")

    cs_department = Department("Computer Science", faculty_members[0])
    math_department = Department("Mathematics", faculty_members[1])

    cs_courses = [
        Course("CS101", "Programming Fundamentals", 3, faculty_members[0], 40),
        Course("CS201", "Data Structures", 3, faculty_members[0], 35),
        Course("CS301", "Databases", 3, faculty_members[0], 30),
        Course("CS401", "Software Engineering", 3, faculty_members[0], 30),
    ]

    math_courses = [
        Course("MA101", "Calculus I", 3, faculty_members[1], 45),
        Course("MA201", "Linear Algebra", 3, faculty_members[1], 40),
        Course("MA301", "Probability", 3, faculty_members[1], 35),
    ]

    cs_department.add_faculty(faculty_members[2])
    for course in cs_courses:
        cs_department.add_course(course)

    for course in math_courses:
        math_department.add_course(course)

    # Enroll students in selected courses.
    cs_courses[0].add_student(students[0])
    cs_courses[1].add_student(students[1])
    math_courses[0].add_student(students[2])

    for department in [cs_department, math_department]:
        info = department.get_department_info()
        print(f"Department: {info['dept_name']}")
        print(f"Head: {info['dept_head']}")
        print(f"Faculty Count: {info['faculty_count']}")
        print(f"Course Count: {info['course_count']}")
        print("Courses:")
        for item in info["courses"]:
            print(f"  - {item}")


def main() -> None:
    """Run all demonstration sections in sequence.

    Returns:
        None
    """
    students, faculty_members, staff_members = demo_class_hierarchy()
    demo_student_course_management(students)
    demo_polymorphism(students, faculty_members, staff_members)
    demo_department_and_courses(students, faculty_members)


if __name__ == "__main__":
    main()
