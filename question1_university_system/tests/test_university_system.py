"""Unit tests for Question 1 university management system."""

import unittest

from course import Course

from department import Department

from faculty import Faculty

from staff import Staff

from student import Student


class TestUniversitySystem(unittest.TestCase):
    """Test suite for key business rules."""

    def setUp(self) -> None:
        """Create reusable sample objects for each test case.

        Returns:
            None
        """
        self.student = Student(
            "Test Student",
            "P999",
            "test.student@uni.edu",
            "+94 77 000 0000",
            "S999",
            "CS",
            "2025-01-01",
        )
        self.faculty = Faculty(
            "Dr. Test",
            "P998",
            "dr.test@uni.edu",
            "+94 71 000 0000",
            "F999",
            "Computer Science",
            "2020-01-01",
        )
        self.staff = Staff(
            "Staff Test",
            "P997",
            "staff.test@uni.edu",
            "+94 76 000 0000",
            "ST999",
            "Administrative Assistant",
            "Administration",
        )

    def test_course_enrollment_limit(self) -> None:
        """Student cannot enroll in more than 6 courses."""
        for i in range(1, 7):
            self.student.enroll_course(f"CSE{i:03}")

        with self.assertRaises(ValueError):
            self.student.enroll_course("CSE007")

    def test_grade_validation(self) -> None:
        """Grade must be in the range 0.0 to 4.0."""
        self.student.enroll_course("CS101")
        with self.assertRaises(ValueError):
            self.student.add_grade("CS101", 4.5)

    def test_gpa_read_only_property(self) -> None:
        """GPA property cannot be directly assigned."""
        with self.assertRaises(AttributeError):
            self.student.gpa = 3.0  # type: ignore[misc]

    def test_calculate_gpa_and_status(self) -> None:
        """GPA and status should match grade data."""
        self.student.enroll_course("CS101")
        self.student.enroll_course("CS102")
        self.student.add_grade("CS101", 3.6)
        self.student.add_grade("CS102", 3.8)

        self.assertEqual(self.student.gpa, 3.7)
        self.assertEqual(self.student.get_academic_status(), "Dean's List")

    def test_course_capacity(self) -> None:
        """Course should reject students after reaching capacity."""
        tiny_course = Course("CS999", "Tiny Course", 1, self.faculty, max_capacity=1)
        tiny_course.add_student(self.student)

        other_student = Student(
            "Other Student",
            "P996",
            "other.student@uni.edu",
            "+94 77 999 9999",
            "S998",
            "Math",
            "2025-01-01",
        )

        with self.assertRaises(ValueError):
            tiny_course.add_student(other_student)

    def test_polymorphism_responsibilities(self) -> None:
        """Each person subtype should return customized responsibilities."""
        messages = [
            self.student.get_responsibilities(),
            self.faculty.get_responsibilities(),
            self.staff.get_responsibilities(),
        ]

        self.assertIn("Attend classes", messages[0])
        self.assertIn("Teach courses", messages[1])
        self.assertIn("support university operations", messages[2])

    def test_department_additions(self) -> None:
        """Department should track faculty and courses correctly."""
        department = Department("Computer Science", self.faculty)
        department.add_faculty(
            Faculty(
                "Dr. New",
                "P995",
                "dr.new@uni.edu",
                "+94 71 123 4567",
                "F998",
                "Computer Science",
                "2022-09-01",
            )
        )
        department.add_course(Course("CS201", "Data Structures", 3, self.faculty))

        info = department.get_department_info()
        self.assertEqual(info["faculty_count"], 2)
        self.assertEqual(info["course_count"], 1)


if __name__ == "__main__":
    unittest.main()
