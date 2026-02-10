"""Course class for the university management system."""

from __future__ import annotations

from faculty import Faculty

from student import Student


class Course:
    """Represent a course and manage student enrollment."""

    def __init__(
        self,
        course_code: str,
        course_name: str,
        credits: int,
        instructor: Faculty | None = None,
        max_capacity: int = 30,
    ) -> None:
        """Create a Course object.

        Args:
            course_code: Unique code of the course.
            course_name: Name of the course.
            credits: Number of credits for the course.
            instructor: Faculty member teaching the course.
            max_capacity: Maximum number of students allowed.

        Raises:
            ValueError: If any value is invalid.
        """
        if not course_code.strip():
            raise ValueError("Course code cannot be empty.")

        self._course_code = course_code.strip()
        self.course_name = course_name
        self.credits = credits
        self.instructor = instructor
        self.max_capacity = max_capacity
        self._enrolled_students: list[Student] = []

    @property
    def course_code(self) -> str:
        """Get course code (read-only)."""
        return self._course_code

    @property
    def course_name(self) -> str:
        """Get course name."""
        return self._course_name

    @course_name.setter
    def course_name(self, value: str) -> None:
        """Set course name."""
        if not value.strip():
            raise ValueError("Course name cannot be empty.")
        self._course_name = value.strip()

    @property
    def credits(self) -> int:
        """Get course credits."""
        return self._credits

    @credits.setter
    def credits(self, value: int) -> None:
        """Set course credits."""
        if int(value) <= 0:
            raise ValueError("Credits must be greater than 0.")
        self._credits = int(value)

    @property
    def instructor(self) -> Faculty | None:
        """Get assigned instructor."""
        return self._instructor

    @instructor.setter
    def instructor(self, value: Faculty | None) -> None:
        """Set assigned instructor."""
        self._instructor = value

    @property
    def max_capacity(self) -> int:
        """Get maximum course capacity."""
        return self._max_capacity

    @max_capacity.setter
    def max_capacity(self, value: int) -> None:
        """Set maximum course capacity."""
        capacity = int(value)
        if capacity <= 0:
            raise ValueError("Max capacity must be greater than 0.")

        # If called after students are enrolled, do not allow shrinking below current count.
        if hasattr(self, "_enrolled_students") and capacity < len(self._enrolled_students):
            raise ValueError("Max capacity cannot be less than current enrolled students.")

        self._max_capacity = capacity

    @property
    def enrolled_students(self) -> list[Student]:
        """Return a copy of enrolled students."""
        return list(self._enrolled_students)

    def add_student(self, student: Student) -> None:
        """Add a student if capacity allows.

        Args:
            student: Student to enroll.

        Returns:
            None

        Raises:
            ValueError: If the course is full.
        """
        if student in self._enrolled_students:
            return

        if self.is_full():
            raise ValueError(f"Course {self.course_code} is full.")

        student.enroll_course(self.course_code)
        self._enrolled_students.append(student)

    def remove_student(self, student: Student) -> None:
        """Remove a student from the course.

        Args:
            student: Student to remove.

        Returns:
            None

        Raises:
            ValueError: If the student is not enrolled.
        """
        if student not in self._enrolled_students:
            raise ValueError(
                f"Student {student.student_id} is not enrolled in {self.course_code}."
            )

        self._enrolled_students.remove(student)
        student.drop_course(self.course_code)

    def is_full(self) -> bool:
        """Return True if course reached max capacity.

        Returns:
            True when enrollment count is equal to or greater than capacity.
        """
        return len(self._enrolled_students) >= self.max_capacity
