"""Student class with enrollment and grading behavior."""


from datetime import datetime
from person import Person


class Student(Person):
    """Represent a student and their academic record."""

    MAX_COURSES_PER_SEMESTER = 6
    MIN_GRADE = 0.0
    MAX_GRADE = 4.0
    MIN_YEAR = 1900
    MAX_YEAR = 2100

    def __init__(
        self,
        name: str,
        person_id: str,
        email: str,
        phone: str,
        student_id: str,
        major: str,
        enrollment_date: str,
    ):
        """Initialize a student record.

        Args:
            name: Student full name.
            person_id: Unique person identifier.
            email: Student email address.
            phone: Student phone number.
            student_id: Unique student identifier.
            major: Student's major subject.
            enrollment_date: Enrollment date.

        Returns:
            None
        
        Raises:
            TypeError: If an argument is of the wrong type.
            ValueError: If an argument is invalid.
        """
        super().__init__(name, person_id, email, phone)

        if not isinstance(student_id, str):
            raise TypeError("Student ID must be a string.")
        if not isinstance(major, str):
            raise TypeError("Major must be a string.")
        if not isinstance(enrollment_date, str):
            raise TypeError("Enrollment date must be a string.")

        if not student_id.strip():
            raise ValueError("Student ID cannot be empty.")

        self._validate_date(enrollment_date)

        self._student_id = student_id
        self.major = major
        self.enrollment_date = enrollment_date
        self._enrolled_courses: list[str] = []
        self._grades: dict[str, float] = {}
        self._gpa: float = 0.0

    @property
    def student_id(self) -> str:
        """Get student ID (read-only).

        Returns:
            The student's unique ID.
        """
        return self._student_id

    @property
    def major(self) -> str:
        """Get student's major."""
        return self._major

    @major.setter
    def major(self, value: str) -> None:
        """Set student's major.
        
        Args:
           value: The new major.

        Raises:
            ValueError: If the major is empty.
            TypeError: If the major is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Major must be a string.")
        if not value.strip():
            raise ValueError("Major cannot be empty.")
        self._major = value.strip()



    @property
    def enrolled_courses(self) -> list[str]:
        """Return a copy of enrolled course codes."""
        return list(self._enrolled_courses)

    @property
    def grades(self) -> dict[str, float]:
        """Return a copy of the grade records."""
        return dict(self._grades)

    @property
    def gpa(self) -> float:
        """Return the current GPA.

        Returns:
            The grade point average for available grades.
        """
        return self._gpa

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
            self.calculate_gpa()

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
        self.calculate_gpa()

    def calculate_gpa(self) -> None:
        """Calculate cumulative GPA and set gpa.

        Returns:
            None
        """
        if not self._grades:
            self._gpa = 0.0
        else:
            self._gpa = round(sum(self._grades.values()) / len(self._grades), 2)

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
        """Validate that a grade is within the allowed range.

        Args:
            grade: Grade value to validate.

        Returns:
            None

        Raises:
            ValueError: If the grade is outside the valid range.
        """
        if not (Student.MIN_GRADE <= float(grade) <= Student.MAX_GRADE):
            raise ValueError(
                f"Grade must be between {Student.MIN_GRADE} and {Student.MAX_GRADE}."
            )

    @staticmethod
    def _validate_date(date_str: str) -> None:
        """Validate date format and range.

        Args:
            date_str: Date string in YYYY-MM-DD format.

        Returns:
            None

        Raises:
            ValueError: If format is invalid or year is out of range.
        """
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format '{date_str}'. Expected YYYY-MM-DD.")

        if not (Student.MIN_YEAR <= dt.year <= Student.MAX_YEAR):
            raise ValueError(
                f"Year must be between {Student.MIN_YEAR} and {Student.MAX_YEAR}."
            )
