"""Student class with enrollment and grading behavior."""

from __future__ import annotations

from datetime import datetime

from person import Person


class Student(Person):
    """Represent a student and their academic record."""

    MAX_COURSES_PER_SEMESTER = 6

    def __init__(
        self,
        name: str,
        person_id: str,
        email: str,
        phone: str,
        student_id: str,
        major: str,
        enrollment_date: str,
    ) -> None:
        """Initialize a student record.

        Args:
            name: Student full name.
            person_id: Unique person identifier.
            email: Student email address.
            phone: Student phone number.
            student_id: Unique student identifier.
            major: Student's major subject.
            enrollment_date: Enrollment date in YYYY-MM-DD format.

        Returns:
            None
        """
        super().__init__(name, person_id, email, phone)

        if not student_id.strip():
            raise ValueError("Student ID cannot be empty.")

        self._student_id = student_id
        self.major = major
        self.enrollment_date = enrollment_date
        self._enrolled_courses: list[str] = []
        self._grades: dict[str, float] = {}

    @property
    def student_id(self) -> str:
        """Get student ID (read-only)."""
        return self._student_id

    @property
    def major(self) -> str:
        """Get student's major."""
        return self._major

    @major.setter
    def major(self, value: str) -> None:
        """Set student's major."""
        if not value.strip():
            raise ValueError("Major cannot be empty.")
        self._major = value.strip()

    @property
    def enrollment_date(self) -> str:
        """Get enrollment date."""
        return self._enrollment_date

    @enrollment_date.setter
    def enrollment_date(self, value: str) -> None:
        """Set enrollment date in YYYY-MM-DD format."""
        if not self._is_valid_date(value):
            raise ValueError("Enrollment date must be in YYYY-MM-DD format.")
        self._enrollment_date = value

    @staticmethod
    def _is_valid_date(value: str) -> bool:
        """Check whether a date uses the YYYY-MM-DD format.

        Args:
            value: Date string to validate.

        Returns:
            True if the date format is valid, otherwise False.
        """
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @property
    def enrolled_courses(self) -> list[str]:
        """Return a copy of enrolled course codes."""
        return list(self._enrolled_courses)

    @enrolled_courses.setter
    def enrolled_courses(self, courses: list[str]) -> None:
        """Replace enrolled courses after checking the course limit.

        Args:
            courses: Course codes to assign to the student.

        Returns:
            None

        Raises:
            ValueError: If the number of unique courses exceeds the limit.
        """
        unique_courses = list(dict.fromkeys(courses))
        if len(unique_courses) > self.MAX_COURSES_PER_SEMESTER:
            raise ValueError(
                f"Course limit exceeded. Maximum allowed is "
                f"{self.MAX_COURSES_PER_SEMESTER} courses."
            )
        self._enrolled_courses = unique_courses

    @property
    def grades(self) -> dict[str, float]:
        """Return a copy of the grade records."""
        return dict(self._grades)

    @grades.setter
    def grades(self, grade_map: dict[str, float]) -> None:
        """Replace all grade records after validating each grade.

        Args:
            grade_map: Mapping from course code to grade value.

        Returns:
            None

        Raises:
            ValueError: If any grade is outside the 0.0 to 4.0 range.
        """
        validated: dict[str, float] = {}
        for course_code, grade in grade_map.items():
            self._validate_grade(grade)
            validated[course_code] = float(grade)
        self._grades = validated

    @property
    def gpa(self) -> float:
        """Return the current GPA.

        Returns:
            The grade point average for available grades.
        """
        return self.calculate_gpa()

    def enroll_course(self, course_code: str) -> None:
        """Enroll the student in a course.

        Args:
            course_code: Code of the course to add.

        Returns:
            None
        """
        if course_code in self._enrolled_courses:
            return

        if len(self._enrolled_courses) >= self.MAX_COURSES_PER_SEMESTER:
            raise ValueError(
                f"Cannot enroll in more than {self.MAX_COURSES_PER_SEMESTER} courses."
            )

        self._enrolled_courses.append(course_code)

    def drop_course(self, course_code: str) -> None:
        """Remove a course and its grade if present.

        Args:
            course_code: Code of the course to remove.

        Returns:
            None
        """
        if course_code in self._enrolled_courses:
            self._enrolled_courses.remove(course_code)
            self._grades.pop(course_code, None)

    def add_grade(self, course_code: str, grade: float) -> None:
        """Add or update a grade for an enrolled course.

        Args:
            course_code: Course code that receives the grade.
            grade: Grade value on a 0.0 to 4.0 scale.

        Returns:
            None
        """
        if course_code not in self._enrolled_courses:
            raise ValueError(
                f"Cannot add grade. Student is not enrolled in course '{course_code}'."
            )
        self._validate_grade(grade)
        self._grades[course_code] = float(grade)

    def calculate_gpa(self) -> float:
        """Calculate GPA on a 0.0 to 4.0 scale.

        Returns:
            The average grade rounded to two decimal places.
        """
        if not self._grades:
            return 0.0
        return round(sum(self._grades.values()) / len(self._grades), 2)

    def get_academic_status(self) -> str:
        """Return academic status from GPA.

        Returns:
            A status label based on the current GPA.
        """
        if self.gpa >= 3.5:
            return "Dean's List"
        if self.gpa >= 2.0:
            return "Good Standing"
        return "Probation"

    def get_info(self) -> dict[str, str]:
        """Return student details as a dictionary.

        Returns:
            Student profile data including base person fields.
        """
        info = super().get_info()
        info.update(
            {
                "student_id": self.student_id,
                "major": self.major,
                "enrollment_date": self.enrollment_date,
            }
        )
        return info

    def get_responsibilities(self) -> str:
        """Return student responsibilities.

        Returns:
            A short description of student responsibilities.
        """
        return (
            "Attend classes, submit assignments on time, maintain academic integrity, "
            "and meet degree requirements."
        )

    @staticmethod
    def _validate_grade(grade: float) -> None:
        """Validate that a grade is between 0.0 and 4.0.

        Args:
            grade: Grade value to validate.

        Returns:
            None

        Raises:
            ValueError: If the grade is outside the valid range.
        """
        if not (0.0 <= float(grade) <= 4.0):
            raise ValueError("Grade must be between 0.0 and 4.0.")
