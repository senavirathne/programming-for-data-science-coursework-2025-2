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
        self.department_name = dept_name
        self.department_head = dept_head
        self._faculty_members: list[Faculty] = [dept_head]
        self._courses: list[Course] = []

    @property
    def department_name(self) -> str:
        """Return the department name.

        Returns:
            The department name.
        """
        return self._department_name

    @property
    def dept_name(self) -> str:
        """Return the department name.

        Returns:
            The department name.
        """
        return self.department_name

    @dept_name.setter
    def dept_name(self, value: str) -> None:
        """Set the department name.

        Args:
            value: New department name.

        Returns:
            None

        Raises:
            ValueError: If the provided name is empty.
        """
        self.department_name = value

    @department_name.setter
    def department_name(self, value: str) -> None:
        """Set the department name.

        Args:
            value: New department name.

        Returns:
            None

        Raises:
            ValueError: If the provided name is empty.
        """
        if not value or not value.strip():
            raise ValueError("Department name cannot be empty.")
        self._department_name = value.strip()

    @property
    def department_head(self) -> Faculty:
        """Return the faculty member leading this department.

        Returns:
            The faculty member assigned as department head.
        """
        return self._department_head

    @property
    def dept_head(self) -> Faculty:
        """Return the faculty member leading this department.

        Returns:
            The faculty member assigned as department head.
        """
        return self.department_head

    @dept_head.setter
    def dept_head(self, value: Faculty) -> None:
        """Set the faculty member who leads the department.

        Args:
            value: Faculty member to set as department head.

        Returns:
            None

        Raises:
            ValueError: If the value is None.
        """
        self.department_head = value

    @department_head.setter
    def department_head(self, value: Faculty) -> None:
        """Set the faculty member who leads the department.

        Args:
            value: Faculty member to set as department head.

        Returns:
            None

        Raises:
            ValueError: If the value is None.
        """
        if value is None:
            raise ValueError("Department head cannot be None.")
        self._department_head = value

    @property
    def faculty_members(self) -> list[Faculty]:
        """Return faculty members in this department.

        Returns:
            A new list containing the department faculty members.
        """
        return list(self._faculty_members)

    @property
    def faculty_list(self) -> list[Faculty]:
        """Return faculty members in this department.

        Returns:
            A new list containing the department faculty members.
        """
        return self.faculty_members

    @property
    def courses(self) -> list[Course]:
        """Return courses offered by this department.

        Returns:
            A new list containing the department courses.
        """
        return list(self._courses)

    @property
    def course_list(self) -> list[Course]:
        """Return courses offered by this department.

        Returns:
            A new list containing the department courses.
        """
        return self.courses

    def add_faculty(self, faculty: Faculty) -> None:
        """Add a faculty member to this department.

        Args:
            faculty: Faculty member to add to the department.

        Returns:
            None
        """
        if faculty not in self._faculty_members:
            self._faculty_members.append(faculty)

    def add_course(self, course: Course) -> None:
        """Add a course offering to this department.

        Args:
            course: Course to add to the department.

        Returns:
            None
        """
        if course not in self._courses:
            self._courses.append(course)

    def get_department_info(self) -> dict[str, object]:
        """Return a simple summary of this department.

        Returns:
            A dictionary with department details, counts, and course labels.
        """
        return {
            "department_name": self.department_name,
            "department_head": self.department_head.name,
            "dept_name": self.department_name,
            "dept_head": self.department_head.name,
            "faculty_count": len(self._faculty_members),
            "course_count": len(self._courses),
            "courses": [
                f"{course.course_code} - {course.course_name}"
                for course in self._courses
            ],
        }
