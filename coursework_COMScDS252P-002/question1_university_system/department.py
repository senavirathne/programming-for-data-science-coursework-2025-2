"""Department class for the university management system."""

from __future__ import annotations

from faculty import Faculty


class Department:
    """Represent an academic department with people and course offerings."""

    def __init__(self, dept_name: str, dept_head: Faculty) -> None:
        """Create a department record.

        Args:
            dept_name: Human-readable department name.
            dept_head: Faculty member who leads the department.

        Raises:
            ValueError: If the department name is empty or the head is missing.
        """
        self.dept_name = dept_name
        self.dept_head = dept_head
        self._faculty_list: list[Faculty] = [dept_head]
        self._course_list: list['Course'] = []

    @property
    def dept_name(self) -> str:
        """Return the department name."""
        return self._dept_name

    @dept_name.setter
    def dept_name(self, value: str) -> None:
        """Set the department name.

        Args:
            value: New department name.

        Raises:
            ValueError: If the provided name is empty.
        """
        if not value or not value.strip():
            raise ValueError("Department name cannot be empty.")
        self._dept_name = value.strip()

    @property
    def dept_head(self) -> Faculty:
        """Return the faculty member leading this department."""
        return self._dept_head

    @dept_head.setter
    def dept_head(self, value: Faculty) -> None:
        """Set the faculty member who leads the department.

        Args:
            value: Faculty member to set as department head.

        Raises:
            ValueError: If the value is None.
        """
        if value is None:
            raise ValueError("Department head cannot be None.")
        self._dept_head = value


    def add_faculty(self, faculty: Faculty) -> None:
        """Add a faculty member to this department."""
        if faculty not in self._faculty_list:
            self._faculty_list.append(faculty)

    def add_course(self, course: 'Course') -> None:
        """Add a course offering to this department."""
        if course not in self._course_list:
            self._course_list.append(course)

    def get_department_info(self) -> dict[str, object]:
        """Return a simple summary of this department.

        Returns:
            A dictionary with department details, counts, and course labels.
        """
        return {
            "dept_name": self.dept_name,
            "dept_head": self.dept_head.name,
            "faculty_count": len(self._faculty_list),
            "course_count": len(self._course_list),
            "courses": [
                f"{course.course_code} - {course.course_name}"
                for course in self._course_list
            ],
        }
