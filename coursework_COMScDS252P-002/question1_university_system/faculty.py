"""Faculty class for the university management system."""


from datetime import datetime
from person import Person


class Faculty(Person):
    """Represent a faculty member and their employment details."""

    MIN_YEAR = 1900
    MAX_YEAR = 2100

    def __init__(
        self,
        name: str,
        person_id: str,
        email: str,
        phone: str,
        employee_id: str,
        department: str,
        hire_date: str,
    ) -> None:
        """Initialize a faculty member record.

        Args:
            name: Faculty member full name.
            person_id: Unique person identifier.
            email: Faculty email address.
            phone: Faculty phone number.
            employee_id: Unique employee identifier.
            department: Department name.
            hire_date: Hiring date.

        Returns:
            None

        Raises:
            TypeError: If an argument is of the wrong type.
            ValueError: If an argument is invalid.
        """
        super().__init__(name, person_id, email, phone)

        if not isinstance(employee_id, str):
            raise TypeError("Employee ID must be a string.")
        if not isinstance(department, str):
            raise TypeError("Department must be a string.")
        if not isinstance(hire_date, str):
            raise TypeError("Hire date must be a string.")

        if not employee_id.strip():
            raise ValueError("Employee ID cannot be empty.")

        self._validate_date(hire_date)

        self._employee_id = employee_id
        self.department = department
        self.hire_date = hire_date

    @property
    def employee_id(self) -> str:
        """Get employee ID (read-only).

        Returns:
            The unique employee ID.
        """
        return self._employee_id

    @property
    def department(self) -> str:
        """Get department name."""
        return self._department

    @department.setter
    def department(self, value: str) -> None:
        """Set department name.

        Args:
            value: The new department name.

        Raises:
            ValueError: If the department name is empty.
            TypeError: If the department name is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Department must be a string.")
        if not value.strip():
            raise ValueError("Department cannot be empty.")
        self._department = value.strip()



    def get_info(self) -> dict[str, str]:
        """Return faculty details as a dictionary.

        Returns:
            Faculty profile data including base person fields.
        """
        info = super().get_info()
        info.update(
            {
                "employee_id": self.employee_id,
                "department": self.department,
                "hire_date": self.hire_date,
            }
        )
        return info

    def get_responsibilities(self) -> str:
        """Return faculty responsibilities.

        Returns:
            A short description of faculty responsibilities.
        """
        return (
            "Teach courses, conduct research, mentor students, and participate "
            "in departmental service."
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

        if not (Faculty.MIN_YEAR <= dt.year <= Faculty.MAX_YEAR):
            raise ValueError(
                f"Year must be between {Faculty.MIN_YEAR} and {Faculty.MAX_YEAR}."
            )
