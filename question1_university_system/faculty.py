"""Faculty class for the university management system."""

from __future__ import annotations

from datetime import datetime

from person import Person


class Faculty(Person):
    """Represent a faculty member and their employment details."""

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
            hire_date: Hiring date in YYYY-MM-DD format.

        Returns:
            None
        """
        super().__init__(name, person_id, email, phone)

        if not employee_id.strip():
            raise ValueError("Employee ID cannot be empty.")

        self._employee_id = employee_id
        self.department = department
        self.hire_date = hire_date

    @property
    def employee_id(self) -> str:
        """Get employee ID (read-only)."""
        return self._employee_id

    @property
    def department(self) -> str:
        """Get department name."""
        return self._department

    @department.setter
    def department(self, value: str) -> None:
        """Set department name."""
        if not value.strip():
            raise ValueError("Department cannot be empty.")
        self._department = value.strip()

    @property
    def hire_date(self) -> str:
        """Get hire date."""
        return self._hire_date

    @hire_date.setter
    def hire_date(self, value: str) -> None:
        """Set hire date in YYYY-MM-DD format."""
        if not self._is_valid_date(value):
            raise ValueError("Hire date must be in YYYY-MM-DD format.")
        self._hire_date = value

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
